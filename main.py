import telebot
import yaml
import argparse
import src.handlers as handlers
import src.callbacks as callbacks
import sqlite3


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

    # State can be 'CREATING_GROUP', or 'JOINING_GROUP', or 'GENERATING_DESRIPTION', None
    state = {} # Dict with {user_id: {state: ... , ...}, database: sqlite3.Connection}, if user is not present, then state is None

    with open(args.config_path) as config:
        config = yaml.safe_load(config)

    # Bot handlers
    bot = telebot.TeleBot(
        token=args.api_key
    )

    # Registering handlers for the bot
    bot.register_message_handler(handlers.oneshot.send_hello(bot=bot, state=state), commands=['start'])
    bot.register_message_handler(handlers.oneshot.cancel_action(bot=bot, state=state), commands=['cancel'])
    bot.register_message_handler(
        handlers.menu.main_menu(bot=bot, state=state), commands=['menu'],
        func=lambda message: state.get(message.from_user.id, None) is None
    )
    bot.register_message_handler(
        handlers.oneshot.extract_group_name(bot=bool, state=state), 
        func=lambda message: state.get(message.from_user.id, None) is not None and state.get(message.from_user.id, None)['state'] == 'CREATING_GROUP'
    )

    # Registering Callbacks for the bot
    bot.register_callback_query_handler(
        callbacks.menu.main_menu(bot=bot, state=state),
        func=lambda call: True
    )

    # Running in a loop
    bot.infinity_polling(skip_pending=True)
