import telebot
import yaml
import argparse
import src.handlers as handlers
import src.callbacks as callbacks
from src.utils import dbutils
import sqlite3
from cryptography.fernet import Fernet
import openai
import os

sqlite3.threadsafety = 3


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--config-path', type=str, default='./config.yaml',
                        help='Path to the file, where base configuration is being stored.')
    parser.add_argument('--telegram-api-key', type=str, default=os.getenv('KEY_TELEGRAM'),
                        help='API-key of your bot.')
    parser.add_argument('--openai-api-key', type=str, default=os.getenv('KEY_OPENAI'),
                        help='key of the openai API.')
    parser.add_argument('-c', '--create-database', action='store_true',
                        help='Path to the sqlite3 database. If not specified, default.db is created.')
    parser.add_argument('--database', type=str, default='default.db',
                        help='Path to the database to which you want to connect.')
    
    return parser.parse_args()


if __name__ == '__main__':
    # Processing arguments
    args = parse_arguments()

    # Creating database
    if args.create_database:
        try:
            database = dbutils.create_database(args.database)

            key = Fernet.generate_key()
            with open('.key', 'xb') as key_file:
                key_file.write(key)

        except Exception as e:
            print('Database or key exists! connecting to that database.')

            database = sqlite3.connect(args.database, check_same_thread=False)
            with open('.key', 'rb') as key_file:
                key = key_file.read()
    else:
        database = sqlite3.connect(args.database, check_same_thread=False)
        with open('.key', 'rb') as key_file:
            key = key_file.read()
    

    # State can be 'CREATING_GROUP', or 'JOINING_GROUP', or 'GENERATING_DESRIPTION', None
    state = {'database': database, 'shiphrator': Fernet(key)} # Dict with {user_id: {state: ... , ...}, database: sqlite3.Connection}, if user is not present, then state is None

    with open(args.config_path) as config:
        config = yaml.safe_load(config)

    # Bot handlers
    bot = telebot.TeleBot(
        token=args.telegram_api_key
    )

    openai.api_key = args.openai_api_key
    print(openai.api_key)

    # Registering handlers for the bot
    bot.register_message_handler(handlers.oneshot.send_hello(bot=bot, state=state), commands=['start'])
    bot.register_message_handler(handlers.oneshot.cancel_action(bot=bot, state=state), commands=['cancel'])
    bot.register_message_handler(
        handlers.menu.main_menu(bot=bot, state=state), commands=['menu'],
        func=lambda message: state.get(message.from_user.id, None) is None
    )
    bot.register_message_handler(
        callback=lambda message: bot.reply_to(message=message, text='🎅 Sorry, command is not recognized! Please, use /menu!'),
        func=lambda message: state.get(message.from_user.id, None) is None
    )
    bot.register_message_handler(
        handlers.oneshot.extract_group_name(bot=bot, state=state), 
        func=lambda message: state.get(message.from_user.id, None) is not None 
            and state.get(message.from_user.id, None)['state'] == 'CREATING_GROUP'
    )
    bot.register_message_handler(
        handlers.oneshot.extract_about_yourself(bot=bot, state=state),
        func=lambda message: state.get(message.from_user.id, None) is not None 
            and state.get(message.from_user.id, None)['state'] == 'WRITING_INFO_ABOUT'
    )
    bot.register_message_handler(
        handlers.oneshot.extract_desire(bot=bot, state=state),
        func=lambda message: state.get(message.from_user.id, None) is not None 
            and state.get(message.from_user.id, None)['state'] == 'WRITING_INFO_DESIRES'
    )
    bot.register_message_handler(
        handlers.oneshot.extract_group_hash(bot=bot, state=state),
        func=lambda message: state.get(message.from_user.id, None) is not None 
            and state.get(message.from_user.id, None)['state'] == 'JOINING_GROUP'
    )

    # Registering Callbacks for the bot

    bot.register_callback_query_handler(
        callback=callbacks.menu.gpt_suggestion(bot=bot, state=state),
        func=lambda call: print(call.data) is None and call.data.split('_')[0] == 'openai'
    )

    bot.register_callback_query_handler(
        callbacks.menu.main_menu(bot=bot, state=state),
        func=lambda call: state.get(call.from_user.id, None) is None
    )

    bot.register_callback_query_handler(
        callback=callbacks.menu.randomize_group(bot=bot, state=state),
        func=lambda call: state.get(call.from_user.id, None) is not None 
            and state.get(call.from_user.id, None)['state'] == 'RANDOMIZING_GROUP'
    )

    # Running in a loop
    bot.infinity_polling(skip_pending=True)
