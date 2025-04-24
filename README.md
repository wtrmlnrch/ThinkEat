The main branch is our most updated branch.

What you need to run ThinkEat on your local machine:
  - Ollama
  - llama3.2 model

Before running ThinkEat:
  - Run: "python manage.py loaddata users.json"

If you are made a new account and would like to keep it between pushes:
  - Run: “python manage.py dumpdata home.CustomUser --indent 2 > users.json”
