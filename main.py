import telebot
from telebot import types
import yaml
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--config-path', type=str, default='./config.yaml',
                        help='Path to the file, where base configuration is being stored.')
    parser.add_argument('--api-key', type=str, required=True,
                        help='API-key of your bot.')
    
    return parser.parse_args()


# Processing arguments
args = parse_arguments()

# Bot handlers
bot = telebot.TeleBot(
    token=args.api_key
)

@bot.message_handler(commands=['start'])
def send_hello(message: types.Message):
    chat_id = message.chat.id
    start_image = open('./misc/start_message_photo.jpg', 'rb').read()
    caption_text = '''
        Hello!
    '''
    print('New chat_id! Chat ID: ', chat_id)
    bot.send_photo(chat_id=chat_id,
                   photo=start_image,
                   caption=caption_text)





if __name__ == '__main__':
    with open(args.config_path) as config:
        config = yaml.safe_load(config)

    bot.infinity_polling()