import os
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def github_webhook(request):
    absolute_path = os.path.abspath(__file__)
    parent = os.path.dirname(absolute_path)
    parent_parent = os.path.dirname(parent)
    # Выполнение git pull
    subprocess.call(["git", '-C', f'{parent_parent}', "pull"])
    # Выполнение makemigrations
    subprocess.call(["python", f'{parent_parent}/manage.py', "makemigrations"])
    # Выполнение migrate
    subprocess.call(["python", f'{parent_parent}/manage.py', "migrate"])
    return JsonResponse({'status': 'success', "code": 200})