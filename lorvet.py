from bot import Bot
from classifier import basic
from handlers import handler_factory
from response import wh_response


class LorvetBot(Bot):
    def __init__(self, token, id):
        self.botid = id
        self.token = token
        Bot.__init__(self)

    def _on_direct_message(self, request_data):
        message = request_data.get('message')
        category = basic.classify(message)

        handler = handler_factory.get_handler(category)
        main_response, certainity = handler.generate_response(message)

        phase_response = wh_response.response(message, certainity) or ''

        return {
            'requestid': request_data.get('id'),
            'response': ' '.join([phase_response, main_response])
        }
