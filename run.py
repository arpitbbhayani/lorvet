import sys
import logging
from ConfigParser import ConfigParser
from optparse import OptionParser
from lorvet import LorvetBot


if __name__ == '__main__':
    parser = OptionParser("usage='usage: %prog [options] arguments'")
    parser.add_option("--config", dest="config_file",
                      help="Config File")

    (options, args) = parser.parse_args()

    if not options.config_file:
        print 'You forgot to mention the config file path'
        exit()

    config = ConfigParser()
    config.read(options.config_file)

    # Log configuration
    log_filepath = config.get('log', 'log_file')

    logging.basicConfig(filename=log_filepath,
                        level=logging.INFO,
                        format='%(asctime)s %(message)s')

    # Bot configuration
    bot_id = config.get('bot', 'bot_id')
    bot_token = config.get('bot', 'bot_token')

    l_bot = LorvetBot(bot_token, bot_id)

    try:
        l_bot.start()
    except KeyboardInterrupt:
        sys.exit(0)
