from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, StickerMessage

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, StickerMessage):
                    messages = []
                    package_id = event.message.package_id
                    sticker_id = event.message.sticker_id
                    sticker = StickerMessage(package_id=package_id, sticker_id=sticker_id)
                    messages.append(sticker)
                    text = TextMessage(text='Hi我是詹姆士')
                    messages.append(text)
                    try:
                        line_bot_api.reply_message(
                            event.reply_token,
                            messages
                        )
                    except:
                        print('fail to reply')

        return HttpResponse(status=200)
    else:
        return HttpResponseBadRequest()
