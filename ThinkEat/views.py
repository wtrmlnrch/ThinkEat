import re
from django.http import JsonResponse, HttpResponse
from .ollama_service import generate_text
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from datetime import datetime
from django.contrib import messages
from .models import SavedRecipe
from io import BytesIO
from xhtml2pdf import pisa

INSTRUCTION = (
    "Here are a couple of different ingredients. I would like you to analyze them and give me name of 5 different recipes that anybody would be able to cook, "
    "expect that I have the basic cooking utensils and ingredients like salt and pepper. Don't give comments besides a numbered list which only contains the title. "
    "Only tell the directions of a recipe in the following request where they specify the number/title. As well, also give and prompt telling the user to press the \"More\" button "
    "for more ingredients, then repeat all the same. If you are unable to come up with any or are unable to make one with certain ingredients, please print the following message, "
    "\"The given ingredients are unable to create and reasonable recipe for you. Please add more ingredients, or remove any illegal ingredients\" AFTER the available recipes, "
    "given that they exist. You don't need to use all the given ingredients as well. Remember, the next response is going to be either a number, a title of a recipe, or by pressing the \"More\" button. "
    "Give the instructions with the title or number associated with the listed recipe. The ingredients are as listed in a comma separated line: "
)

def format_recipe_list(response_text):
    failure_msg = "The given ingredients are unable to create and reasonable recipe"
    if failure_msg.lower() in response_text.lower():
        response_text += "\n\nPlease press the Reset button and try again with different ingredients."
        return response_text, {}

    recipe_lines = re.findall(r"^\s*(\d+)\.\s*(.+)", response_text, re.MULTILINE)
    if recipe_lines:
        formatted = "Here are a couple of recipe ideas:\n"
        for num, title in recipe_lines:
            formatted += f"    {num}. {title}\n"
        formatted += "\nPress the number or enter the title of the recipe you'd like instructions for.\nPress the \"More\" button to get more recipe suggestions."
        return formatted, {num: title for num, title in recipe_lines}

    return response_text, {}

def generate_pdf(recipe_title, recipe_content):
    processed_content = recipe_content.replace('\n', '<br>')
    html = f"""
    <html>
        <head>
            <meta charset=\"utf-8\">
            <title>{recipe_title}</title>
            <style>
                @page {{ size: A4; margin: 1in; }}
                body {{ font-family: Helvetica, Arial, sans-serif; font-size: 12pt; }}
                h1 {{ text-align: center; margin-bottom: 20px; }}
                .content {{ width: 90%; margin: 0 auto; white-space: pre-wrap; word-wrap: break-word; overflow-wrap: break-word; }}
            </style>
        </head>
        <body>
            <h1>{recipe_title}</h1>
            <div class=\"content\">{processed_content}</div>
        </body>
    </html>
    """
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{recipe_title}.pdf"'
        return response
    return HttpResponse("PDF generation failed", status=500)

@csrf_exempt
def chat_view(request):
    if request.method == "POST":
        mode = request.POST.get('mode', request.session.get('mode', 'ingredients'))
        request.session['mode'] = mode

        if 'favorite' in request.POST:
            recipe_title = request.session.get("last_recipe_title", "My_Recipe")
            recipe_content = request.session.get("last_response", "No recipe content found.")
            return generate_pdf(recipe_title, recipe_content)

        if 'reset' in request.POST:
            request.session.flush()
            return render(request, 'thinkeat.html', {
                'chat_history': [],
                'response': "ThinkEat has been reset. Please enter new ingredients to begin.",
                'mode': 'ingredients'
            })

        if 'more' in request.POST:
            last_ingredients = request.session.get("last_ingredients", "")
            if last_ingredients:
                prompt_to_send = INSTRUCTION + last_ingredients
                raw_response = generate_text(prompt_to_send)
                formatted_response, recipe_map = format_recipe_list(raw_response)
                request.session["recipe_map"] = recipe_map
                return render(request, 'thinkeat.html', {
                    'chat_history': [
                        {'role': 'user', 'content': '[Pressed More]', 'timestamp': datetime.now().strftime("%I:%M %p")},
                        {'role': 'ai', 'content': formatted_response, 'timestamp': datetime.now().strftime("%I:%M %p")}
                    ],
                    'response': formatted_response,
                    'mode': mode
                })
            else:
                return render(request, 'thinkeat.html', {
                    'chat_history': [],
                    'response': "No previous ingredients found. Please enter ingredients before using the More button.",
                    'mode': mode
                })

        user_input = request.POST.get('prompt', '').strip()
        lower_input = user_input.lower()
        session = request.session
        last_ingredients = session.get("last_ingredients", "")
        recipe_map = session.get("recipe_map", {})
        chat_history = []

        if mode == 'ingredients':
            if ',' in user_input and lower_input != "more" and not lower_input.isdigit():
                session["last_ingredients"] = user_input
                session["has_submitted_ingredients"] = True
                prompt_to_send = INSTRUCTION + user_input
                raw_response = generate_text(prompt_to_send)
                formatted_response, recipe_map = format_recipe_list(raw_response)
                session["recipe_map"] = recipe_map

            elif ',' not in user_input and len(user_input.split()) <= 5 and not session.get("has_submitted_ingredients", False):
                formatted_response = (
                    "It looks like you entered a dish name.\n\n"
                    "Try switching to Dish Name Mode using the dropdown above."
                )

            elif user_input in recipe_map:
                title = recipe_map[user_input]
                prompt_to_send = f"Make me a simple recipe for {title}"
                formatted_response = generate_text(prompt_to_send)
                session["last_response"] = formatted_response
                session["last_recipe_title"] = title if user_input in recipe_map else user_input


            else:
                prompt_to_send = f"Make me a simple recipe for {user_input}"
                formatted_response = generate_text(prompt_to_send)
                session["last_response"] = formatted_response
                session["last_recipe_title"] = title if user_input in recipe_map else user_input


        elif mode == 'dish':
            if ',' in user_input:
                formatted_response = (
                    "It looks like you entered a list of ingredients.\n\n"
                    "Try switching to Ingredients Mode using the dropdown above."
                )
            else:
                prompt_to_send = f"Make me a simple recipe for {user_input}"
                formatted_response = generate_text(prompt_to_send)
                session["last_response"] = formatted_response
                session["last_recipe_title"] = title if user_input in recipe_map else user_input


        chat_history.append({
            'role': 'user',
            'content': user_input,
            'timestamp': datetime.now().strftime("%I:%M %p")
        })
        chat_history.append({
            'role': 'ai',
            'content': formatted_response,
            'timestamp': datetime.now().strftime("%I:%M %p")
        })

        return render(request, 'thinkeat.html', {
            'chat_history': chat_history,
            'response': formatted_response,
            'mode': mode
        })

    return render(request, 'thinkeat.html', {
        'chat_history': [],
        'response': '',
        'mode': 'ingredients',
        'error': 'POST request required'
    })
