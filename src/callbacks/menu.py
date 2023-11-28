import telebot
from telebot import types


def main_menu(bot: telebot.TeleBot):
    '''
        This enclosure function generates callback for the main_manu handler.

        Callback desription: 
            Answers on corresponding main_menu handler.
    '''

    def callback(query: types.CallbackQuery):
        query_id = query.id
        
        if query.data == 'create_group':
            bot.answer_callback_query(query_id, text='You are trying to create a group!')
        elif query.data == 'join_group':
            bot.answer_callback_query(query_id, text='You are trying to join group!')
        elif query.data == 'list_groups':
            bot.answer_callback_query(query_id, text='You are trying to list all groups!')
        elif query.data == 'list_presentee':
            bot.answer_callback_query(query_id, text='You are trying to list all !')

    return callback