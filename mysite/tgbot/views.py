import json
from django import http
from .commands_service import tgbot_service

# Create your views here.
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        try:
            request_body = json.loads(request.body)
            tgbot_service.execute_command(request_body)
        except Exception as e:
            print(str(e))

        return http.HttpResponse('', status=200)
    else:
        return http.Http404
