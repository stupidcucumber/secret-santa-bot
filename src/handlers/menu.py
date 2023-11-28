from telebot import types
import telebot


def main_menu(bot: telebot.TeleBot, state: dict=None):
    '''
        This is the enclosure function that generates handler for 'main_menu'.

        Handler description:
            This menu contains main functionality of the bot, such as:
            1. Register new group.
            2. Join group.
            3. List all groups.
            4. List all users to whome you will give presents.
    '''
    def generate_inline_markup():
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton(
                'Create group',
                callback_data='create_group'
            ),
            types.InlineKeyboardButton(
                'Join group',
                callback_data='join_group'
            )
        )

        markup.add(
            types.InlineKeyboardButton(
                'List joined groups',
                callback_data='list_groups'
            ),
            types.InlineKeyboardButton(
                'List to whom give presents',
                callback_data='list_presentee'
            ),
            row_width=1
        )

        return markup

    def handler(message: types.Message):
        chat_id = message.chat.id

        bot.send_message(
            chat_id=chat_id,
            text='Please choose from the options below:',
            reply_markup=generate_inline_markup()
        )

    return handler