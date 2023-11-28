import telebot
from telebot import types
from ..utils import dbutils


def main_menu(bot: telebot.TeleBot, state: dict):
    '''
        This enclosure function generates callback for the main_manu handler.

        Callback desription: 
            Answers on corresponding main_menu handler.
    '''

    def callback(query: types.CallbackQuery):
        query_id = query.id
        user_id = query.from_user.id

        postambule = 'If you want to cancel the action use /cancel option.' 

        answer_create_group = '''
        Please specify the name of the group with the following requirements:
        \r- must contain at least one symbol, which is not a space character.
        ''' + postambule
        if state.get(user_id, None) is not None:
            bot.answer_callback_query(query_id, 'You are currently perform another action!')
            return
        
        if query.data == 'create_group':
            bot.answer_callback_query(query_id, text='You are trying to create a group!')

            bot.send_message(query.message.chat.id, answer_create_group)
            state[user_id] = {}
            state[user_id]['state'] = 'CREATING_GROUP'
            print(state)

        elif query.data == 'join_group':
            bot.answer_callback_query(query_id, text='You are trying to join group!')

            bot.send_message(query.message.chat.id, 'Please, write down your invitation hash:')
            state[user_id] = {}
            state[user_id]['state'] = 'JOINING_GROUP'
            print(state)
            
        elif query.data == 'list_groups':
            bot.answer_callback_query(query_id, text='You are trying to list all groups!')
            groups = dbutils.get_all_created_groups(state['database'], user_id)

            answer = 'You are part of the following groups:'
            for group in groups:
                answer += '\n - ' + group

            bot.send_message(chat_id=query.message.chat.id,
                             text=answer)
        elif query.data == 'list_presentee':
            bot.answer_callback_query(query_id, text='You are trying to list all !')

    return callback