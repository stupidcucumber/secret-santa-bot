import telebot
import yaml
import argparse
import src.handlers as handlers


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--config-path', type=str, default='./config.yaml',
                        help='Path to the file, where base configuration is being stored.')
    parser.add_argument('--api-key', type=str, required=True,
                        help='API-key of your bot.')
    
    return parser.parse_args()


# Processing arguments
args = parse_arguments()


if __name__ == '__main__':
    with open(args.config_path) as config:
        config = yaml.safe_load(config)

    # Bot handlers
    bot = telebot.TeleBot(
        token=args.api_key
    )

    # Registering handlers for bot
    bot.register_message_handler(handlers.oneshot.send_hello(bot=bot), commands=['start'])

    # Running in a loop
    bot.infinity_polling(skip_pending=True)