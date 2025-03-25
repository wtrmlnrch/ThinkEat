from django.http import JsonResponse
from .ollama_service import generate_text
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

@csrf_exempt
def chat_view(request):
    if request.method == "POST":
        user_input = request.POST.get('prompt', '')
        ollama_response = generate_text(user_input)
        return render(request, 'thinkeat.html', {'response': ollama_response})
    return render(request, 'thinkeat.html', {'error': 'POST request required'})