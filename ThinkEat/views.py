import re
from django.http import JsonResponse
from .ollama_service import generate_text
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from datetime import datetime

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
        formatted = "Here are 5 recipe ideas:\n"
        for num, title in recipe_lines:
            formatted += f"    {num}. {title}\n"
        formatted += "\nPress the number or enter the title of the recipe you'd like instructions for.\nPress the \"More\" button to get more recipe suggestions."
        return formatted, {num: title for num, title in recipe_lines}

    return response_text, {}

@csrf_exempt
def chat_view(request):
    if request.method == "POST":
        # Mode handling
        mode = request.POST.get('mode', request.session.get('mode', 'ingredients'))
        request.session['mode'] = mode

        # Reset button
        if 'reset' in request.POST:
            request.session.flush()
            return render(request, 'thinkeat.html', {
                'chat_history': [],
                'response': "ThinkEat has been reset. Please enter new ingredients to begin.",
                'mode': 'ingredients'
            })

        # More button
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

        # Main prompt input
        user_input = request.POST.get('prompt', '').strip()
        lower_input = user_input.lower()
        session = request.session
        last_ingredients = session.get("last_ingredients", "")
        recipe_map = session.get("recipe_map", {})
        chat_history = []

        # Handle mode
        if mode == 'ingredients':
            if ',' in user_input and lower_input != "more" and not lower_input.isdigit():
                # Valid ingredient input
                session["last_ingredients"] = user_input
                prompt_to_send = INSTRUCTION + user_input
                raw_response = generate_text(prompt_to_send)
                formatted_response, recipe_map = format_recipe_list(raw_response)
                session["recipe_map"] = recipe_map

            elif ',' not in user_input and len(user_input.split()) <= 5:
                # Looks like a dish name — recommend switching
                formatted_response = (
                    "Looks like you entered a dish name.\n\n"
                    "               Try switching to Dish Name Mode using the dropdown above."
                )


            elif user_input in recipe_map:
                # User entered number from prior list
                title = recipe_map[user_input]
                prompt_to_send = f"Make me a simple recipe for {title}"
                formatted_response = generate_text(prompt_to_send)

            else:
                # Treat as fallback dish name
                prompt_to_send = f"Make me a simple recipe for {user_input}"
                formatted_response = generate_text(prompt_to_send)

        elif mode == 'dish':
            if ',' in user_input:
                # Looks like ingredient input — suggest switching
                formatted_response = (
                    "Looks like you entered a list of ingredients.\n\n"
                    "               Try switching to Ingredients Mode using the dropdown above."
                )

            else:
                # Normal dish request
                prompt_to_send = f"Make me a simple recipe for {user_input}"
                formatted_response = generate_text(prompt_to_send)


        # Add to chat history
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
