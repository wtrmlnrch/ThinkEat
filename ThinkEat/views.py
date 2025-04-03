import re
from django.http import JsonResponse
from .ollama_service import generate_text
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

INSTRUCTION = (
    "Here are a couple of different ingredients. I would like you to analyze them and give me name of 5 different recipes that anybody would be able to cook, "
    "expect that I have the basic cooking utensils and ingredients like salt and pepper. Don't give comments besides a numbered list which only contains the title. "
    "Only tell the directions of a recipe in the following request where they specify the number/title. As well, also give and prompt telling the user to type more "
    "for more ingredients, then repeat all the same. If you are unable to come up with any or are unable to make one with certain ingredients, please print the following message, "
    "\"The given ingredients are unable to create and reasonable recipe for you. Please add more ingredients, or remove any illegal ingredients\" AFTER the available recipes, "
    "given that they exist. You don't need to use all the given ingredients as well. Remember, the next response is going to be either a number, a title of a recipe, or \"more\". "
    "Give the instructions with the title or number associated with the listed recipe. The ingredients are as listed in a comma separated line: "
)

@csrf_exempt
def chat_view(request):
    if request.method == "POST":
        user_input = request.POST.get('prompt', '').strip()
        lower_input = user_input.lower()

        session = request.session
        last_ingredients = session.get("last_ingredients", "")
        recipe_map = session.get("recipe_map", {})

        # INGREDIENT INPUT
        if ',' in user_input and lower_input != "more" and not lower_input.isdigit():
            session["last_ingredients"] = user_input
            prompt_to_send = INSTRUCTION + user_input

            # Get AI response (list of recipes)
            ollama_response = generate_text(prompt_to_send)

            # Extract recipes from response (expects 1. Title \n 2. Title ...)
            recipe_lines = re.findall(r"^\s*(\d+)\.\s*(.+)", ollama_response, re.MULTILINE)
            recipe_map = {num: title for num, title in recipe_lines}
            session["recipe_map"] = recipe_map

        # "MORE" – Use last ingredients
        elif lower_input == "more" and last_ingredients:
            prompt_to_send = INSTRUCTION + last_ingredients
            ollama_response = generate_text(prompt_to_send)

            # Extract recipes again and update map
            recipe_lines = re.findall(r"^\s*(\d+)\.\s*(.+)", ollama_response, re.MULTILINE)
            recipe_map = {num: title for num, title in recipe_lines}
            session["recipe_map"] = recipe_map

        # NUMBER – Map to recipe
        elif user_input in recipe_map:
            title = recipe_map[user_input]
            prompt_to_send = f"Make me a simple recipe for {title}"
            ollama_response = generate_text(prompt_to_send)

        # TITLE or unknown input
        else:
            prompt_to_send = f"Make me a simple recipe for {user_input}"
            ollama_response = generate_text(prompt_to_send)

        return render(request, 'thinkeat.html', {
            'response': ollama_response,
            'chat_history': [
                {'role': 'user', 'content': user_input},
                {'role': 'ai', 'content': ollama_response}
            ]
        })

    return render(request, 'thinkeat.html', {'error': 'POST request required'})
