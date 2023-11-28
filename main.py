import telebot
import yaml
import argparse
import src.handlers as handlers
import src.callbacks as callbacks


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--config-path', type=str, default='./config.yaml',
                        help='Path to the file, where base configuration is being stored.')
    parser.add_argument('--api-key', type=str, required=True,
                        help='API-key of your bot.')
    
    return parser.parse_args()


if __name__ == '__main__':
    # Processing arguments
    args = parse_arguments()


    with open(args.config_path) as config:
        config = yaml.safe_load(config)

    # Bot handlers
    bot = telebot.TeleBot(
        token=args.api_key
    )

    # Registering handlers for the bot
    bot.register_message_handler(handlers.oneshot.send_hello(bot=bot), commands=['start'])
    bot.register_message_handler(handlers.menu.main_menu(bot=bot), commands=['menu'])

    # Registering Callbacks for the bot
    bot.register_callback_query_handler(callbacks.menu.main_menu(bot=bot), func=lambda x: True)

    # Running in a loop
    bot.infinity_polling(skip_pending=True)
