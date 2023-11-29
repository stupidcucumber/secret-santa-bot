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

        answer_create_group = '''🎅 Ho Ho Ho! Santa Needs Your Help! 🌟

Santa is on a quest to give this Secret Santa group a merry and magical name, and he needs your festive creativity! 🎁✨

What enchanting name shall we bestow upon this jolly gathering of Secret Santas? The more creative, the merrier! 🎄✨

Write down suggested name of the group (/cancel to cancel action):'''
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
            groups = dbutils.get_group_names(state['database'], user_id=user_id)
            print(groups)
            created_groups = dbutils.get_all_created_groups(state['database'], user_id)

            answer = 'Behold, dear one! 🌟 Here is the enchanting and festive list of all the groups you are a cherished member of:'
            for group in groups:
                answer += '\n - ' + group + (' (you are admin here)' if group in created_groups else '')

            bot.send_message(chat_id=query.message.chat.id,
                             text=answer)
        elif query.data == 'list_presentee':
            bot.answer_callback_query(query_id, text='🌟 Searching for recipients!..')
            entries = dbutils.get_all_recipients(state['database'], user_id=user_id)
            template = '''🎅 <b>Santa's Present Recipient:</b>  @{recipient_name}

🎄 <b>Group Name:</b> {group_name}

📝 <b>About:</b>
{about}

🎁 <b>Desired Presents:</b>
{desired_presents}

🔔 <b>Important Notes:</b>
[Include any specific instructions or details that Santa and the elves need to know for a successful delivery.]
'''
            bot.send_message(chat_id=query.message.chat.id,
                             text='🌟 Here your recipients:')
            for entry in entries:
                message_text = template.format(group_name=entry[0],
                                               recipient_name=entry[1],
                                               about=entry[2],
                                               desired_presents=entry[3])
                bot.send_message(chat_id=query.message.chat.id,
                                 text=message_text,
                                 parse_mode='HTML')

    return callback