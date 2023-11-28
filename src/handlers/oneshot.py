from telebot import types
import telebot


def send_hello(bot: telebot.TeleBot):
    '''
        This is the enclosure function that generates handler for 'send_hello'.

        Handler description:
            Greets user and registers chat id into the database.
    '''

    def handler(message: types.Message):
        chat_id = message.chat.id
        start_image = open('./misc/start_message_photo.jpg', 'rb').read()
        caption_text = '''
            Hello!
            To start using bot choose /menu option!
        '''
        print('New chat_id! Chat ID: ', chat_id)
        bot.send_photo(chat_id=chat_id,
                    photo=start_image,
                    caption=caption_text)
        
    return handler