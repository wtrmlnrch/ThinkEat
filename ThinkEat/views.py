import re
from django.http import JsonResponse
from .ollama_service import generate_text
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from datetime import datetime

INSTRUCTION = (
    "Here are a couple of different ingredients. I would like you to analyze them and give me name of 5 different recipes that anybody would be able to cook, "
    "expect that I have the basic cooking utensils and ingredients like salt and pepper. Don't give comments besides a numbered list which only contains the title. "
    "Only tell the directions of a recipe in the following request where they specify the number/title. As well, also give and prompt telling the user to type more "
    "for more ingredients, then repeat all the same. If you are unable to come up with any or are unable to make one with certain ingredients, please print the following message, "
    "\"The given ingredients are unable to create and reasonable recipe for you. Please add more ingredients, or remove any illegal ingredients\" AFTER the available recipes, "
    "given that they exist. You don't need to use all the given ingredients as well. Remember, the next response is going to be either a number, a title of a recipe, or \"more\". "
    "Give the instructions with the title or number associated with the listed recipe. The ingredients are as listed in a comma separated line: "
)

def format_recipe_list(response_text):
    # Detect lines like "1. Recipe Name"
    recipe_lines = re.findall(r"^\s*(\d+)\.\s*(.+)", response_text, re.MULTILINE)
    if recipe_lines:
        formatted = "Here are 5 recipe ideas:\n"
        for num, title in recipe_lines:
            formatted += f"    {num}. {title}\n"
        formatted += "\nType the number or title of the recipe you'd like instructions for.\nType \"more\" to get more recipe suggestions."
        return formatted, {num: title for num, title in recipe_lines}
    return response_text, {}

@csrf_exempt
def chat_view(request):
    if request.method == "POST":
        user_input = request.POST.get('prompt', '').strip()
        lower_input = user_input.lower()

        session = request.session
        last_ingredients = session.get("last_ingredients", "")
        recipe_map = session.get("recipe_map", {})

        # Track conversation
        chat_history = []

        if ',' in user_input and lower_input != "more" and not lower_input.isdigit():
            # Ingredient list
            session["last_ingredients"] = user_input
            prompt_to_send = INSTRUCTION + user_input
            raw_response = generate_text(prompt_to_send)
            formatted_response, recipe_map = format_recipe_list(raw_response)
            session["recipe_map"] = recipe_map

        elif lower_input == "more" and last_ingredients:
            # Reuse previous ingredients
            prompt_to_send = INSTRUCTION + last_ingredients
            raw_response = generate_text(prompt_to_send)
            formatted_response, recipe_map = format_recipe_list(raw_response)
            session["recipe_map"] = recipe_map

        elif user_input in recipe_map:
            # User typed "1", "2", etc.
            title = recipe_map[user_input]
            prompt_to_send = f"Make me a simple recipe for {title}"
            formatted_response = generate_text(prompt_to_send)

        else:
            # Treat as title or fallback
            prompt_to_send = f"Make me a simple recipe for {user_input}"
            formatted_response = generate_text(prompt_to_send)

        # Add messages to history
        chat_history.append({'role': 'user', 'content': user_input, 'timestamp': datetime.now().strftime("%I:%M %p")})
        chat_history.append({'role': 'ai', 'content': formatted_response, 'timestamp': datetime.now().strftime("%I:%M %p")})

        return render(request, 'thinkeat.html', {
            'chat_history': chat_history,
            'response': formatted_response
        })

    return render(request, 'thinkeat.html', {'error': 'POST request required'})
