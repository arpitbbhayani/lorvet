import re
import time
import json
from slackclient import SlackClient

import logger
from uuid import uuid4


class Bot:
    def __init__(self):
        self.last_ping = 0
        self.slack_client = None

    def connect(self):
        self.slack_client = SlackClient(self.token)
        self.slack_client.rtm_connect()

    def ping(self):
        now = int(time.time())
        if now > self.last_ping + 4:
            self.slack_client.server.ping()
            self.last_ping = now

    def fetch(self):
        for data in self.slack_client.rtm_read():
            if data.get('type') == 'message':
                if self.botid == data.get('user'):
                    # Do not reply on answers by the Bot
                    continue

                if not self._is_direct(data.get('text')):
                    # Skip the message if bot is not mentioned
                    continue

                request_data = {
                    'id': str(uuid4()),
                    'message': data.get('text')
                }
                logger.log_it(json.dumps(request_data))

                response_data = self._on_direct_message(request_data)

                logger.log_it(response_data)

                if response_data is not None:
                    message = response_data['response'].encode('ascii',
                                                               'ignore')
                    message = "{}".format(message)
                    self.slack_client.api_call('chat.postMessage',
                                               text=message,
                                               as_user="true",
                                               token=self.token,
                                               channel=data.get('channel'))

    def _is_direct(self, msg):
        if not msg:
            return False
        mentions = re.findall('<@' + self.botid + '>', msg)
        return len(mentions) != 0

    def start(self):
        self.connect()
        while True:

            try:
                self.fetch()
            except:
                logger.log_it('OOPS', log_type='exception')

            self.ping()
            time.sleep(.1)
