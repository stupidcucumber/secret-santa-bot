from telebot import types
from ..utils import validators, dbutils
import telebot


def send_hello(bot: telebot.TeleBot, state: dict=None):
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


def cancel_action(bot: telebot.TeleBot, state: dict=None):
    '''
        This is the enclosure function to cancel actions of user.

        Handler desription:
            If user is present in the state dict, then user is being deleted. Therefore there won't be any action.
    '''

    def handler(message: types.Message):
        chat_id = message.chat.id
        user_id = message.from_user.id

        if state.get(user_id, None) is None:
            bot.send_message(chat_id=chat_id, text='Nothing to cancel! :)')
        else:
            state.pop(user_id)
            bot.send_message(chat_id=chat_id, text='Current action has been canceled!')

    return handler


def extract_group_name(bot: telebot.TeleBot, state: dict=None):
    '''
        Handler desciption:
            If user currently in a state of 'CREATING_GROUP', then it checks the name for the
        eligibility and adds it to the database. 
    '''
    def handler(message: types.Message):
        chat_id = message.chat.id
        user_id = message.from_user.id

        group_name = message.text

        if validators.validate_group_name(group_name):
            if dbutils.insert_group_name(state['database'], group_name):
                bot.send_message(chat_id=chat_id, text='Group has been registered! Now others can also join by specifying: %s :)' % group_name)
            else:
                bot.send_message(chat_id=chat_id, text='Sorry, something wrong happened! Try again... :(')

            state.pop(user_id)
        else:
            bot.send_message(chat_id=chat_id, text='Name is bad, please enter another one!')

    return handler