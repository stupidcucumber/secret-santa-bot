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
            group_id = dbutils.insert_group_name(state['database'], group_name, user_id)
            if group_id != -1:
                bot.send_message(chat_id=chat_id, text='Group has been registered! Now others can also join by specifying id: "%s" :)' % group_id)
                bot.send_message(chat_id=chat_id, text='Please tell about yourself: hobbies, films, books etc.')

                state[user_id]['state'] = 'WRITING_INFO_ABOUT'
                state[user_id]['group_id'] = group_id
            else:
                bot.send_message(chat_id=chat_id, text='Sorry, something wrong happened! Try again... :(')
                state.pop(user_id)
        else:
            bot.send_message(chat_id=chat_id, text='Name is bad, please enter another one!')

    return handler


def extract_about_yourself(bot: telebot.TeleBot, state: dict=None):
    '''
        Handler description:
            If user currently in a state of 'WRITING_INFO_ABOUT', then this handler adds to the state of user
        field 'about'.
    '''

    def handler(message: types.Message):
        chat_id = message.chat.id
        user_id = message.from_user.id

        if validators.validate_about(message.text):
            bot.send_message(chat_id=chat_id, 
                             text='Very interesting! Maybe you want something specific or have thoughts on what do you want?)')
            state[user_id]['about'] = message.text
            state[user_id]['state'] = 'WRITING_INFO_DESIRES'
        else:
            bot.send_message(chat_id=chat_id,
                             text='Sorry, you must write about something!')
        
    return handler


def extract_desire(bot: telebot.TeleBot, state: dict=None):
    '''
        Handler description:
            If user currently in a state of 'WRITING_INFO_ABOUT', then this handler adds to the state of user
        field 'desire'.
    '''

    def handler(message: types.Message):
        chat_id = message.chat.id
        user_id = message.from_user.id

        entry_id = dbutils.insert_into_groups_users(
            database=state['database'],
            group_id=state[user_id]['group_id'],
            user_id=user_id,
            about=state[user_id]['about'],
            desired=message.text
        )
        if entry_id == -1:
            bot.send_message(chat_id=chat_id,
                             text='Sorry, but something went wrong... Try again!(')
            state.pop(user_id)
            return

        bot.send_message(chat_id=chat_id, 
                             text='All good! Now you are the member of a group!')
        state.pop(user_id)
        

    return handler