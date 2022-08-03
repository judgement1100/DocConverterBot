import json
from django import http
from .bot_service import common_service
from start import bot


# Create your views here.
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        try:
            request_body = json.loads(request.body)
            common_service.execute_command(request_body)
        except Exception as e:
            print(str(e))

        return http.HttpResponse('', status=200)

    else:
        return http.Http404
