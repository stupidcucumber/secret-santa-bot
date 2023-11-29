from telebot import types
from ..utils import validators, dbutils
import telebot
from cryptography.fernet import Fernet


def send_hello(bot: telebot.TeleBot, state: dict=None):
    '''
        This is the enclosure function that generates handler for 'send_hello'.

        Handler description:
            Greets user and registers chat id into the database.
    '''

    def handler(message: types.Message):
        chat_id = message.chat.id
        start_image = open('./misc/start_message_photo.jpg', 'rb').read()
        caption_text = '''🎅 Welcome to Secret Santa Bot! 🎁

Ho Ho Ho! It's that magical time of the year, and you've just stepped into the Secret Santa world! 🌟 Get ready for some festive fun as we spread joy and surprises.

🎉 Here's how it works:

1. Sign up by clicking /menu and then choosing "Join group", if you were given a special key to join, or create your own group! On this step you also must tell a little about yourself, and optionally provide some thoughts on what do you want to get)\n
2. Next, after admin of the group clicks "Start randomization!" you'll be assigned a Secret Santa recipient anonymously.\n
3. Select a thoughtful gift for them (keep it a secret! 🤫).\n
4. Share the joy when everyone reveals their Secret Santa gifts!\n

Ready to embark on this jolly adventure? Click /menu and let the Secret Santa magic begin! 🎄✨

Happy holidays! 🎅🎄
        '''
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
                bot.send_message(chat_id=chat_id, text='''🎉 Ho Ho Ho! A New Secret Santa Adventure Begins! 🎁

Greetings, festive friend! 🌟 It's official - a new Secret Santa group has been born, and the holiday magic is in the air! 🎅✨
This group is now your cozy hub for spreading joy and surprises. Get ready for merry exchanges, mysterious gifts, and the spirit of giving! 🎄🎁 

                                 
Now others can also join by specifying this key: 
                    `%s`
                                 ''' 
                                 % state['shiphrator'].encrypt(bytes(str(group_id), 'utf-8')).decode('utf-8'),
                                 parse_mode='MarkDown')
                bot.send_message(chat_id=chat_id, text='''🎅 Ho Ho Hello, Dear Friend!

Santa is checking his list (twice, of course!), and he's curious about the wonderful individuals joining the festivities in this Secret Santa adventure! 🎁✨

Tell Santa a bit about yourself:''')

                state[user_id]['state'] = 'WRITING_INFO_ABOUT'
                state[user_id]['group_id'] = group_id
            else:
                bot.send_message(chat_id=chat_id, text='Sorry, something wrong happened! Try again... :(')
                state.pop(user_id)
        else:
            bot.send_message(chat_id=chat_id, text='Name is bad, please enter another one!')

    return handler


def extract_group_hash(bot: telebot.TeleBot, state: dict=None):

    def handler(message: types.Message):
        chat_id = message.chat.id
        user_id = message.from_user.id

        group_hash = bytes(message.text, encoding='utf-8')
        try:
            id = int(state['shiphrator'].decrypt(group_hash).decode('utf-8'))
            valid = validators.validate_joining(state['database'], id, user_id)
            if not valid:
                bot.send_message(chat_id=chat_id, text='Sorry, but you have already joined this group!')
                state.pop(user_id)
                return 
            
            state[user_id]['group_id'] = id
            state[user_id]['state'] = 'WRITING_INFO_ABOUT'

            bot.send_message(chat_id=chat_id, text='''🎅 Ho Ho Ho! Greetings, Beloved Secret Santas! 🎁

Santa is delighted to welcome each and every one of you to this enchanting Secret Santa group! 🌟 The holiday magic has gathered us all here for a season of joy, surprises, and spreading good cheer! 🎄✨

In this cozy corner of the North Pole (or, well, the internet), you'll discover the spirit of giving, the joy of receiving, and the magic of sharing smiles with your Secret Santa companions! 🎅🤶
                             
But before we start, I want to know more about you! Tell Santa a bit about yourself:''')
        except:
            bot.send_message(chat_id=chat_id, text='Sorry, key is incorrect :(')

            state.pop(user_id)

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
                             text='''Santa loves hearing about your festive spirit and holiday traditions! Now that you've shared a bit about yourself, how about letting Santa in on a little Christmas secret? 🤫✨

If you could have anything special on your Christmas Eve tree, what would it be? A sprinkle of stardust? A cozy blanket of snowflakes? Or perhaps a tiny elf creating mischief? 🎄🌟

Write down what you would prefer (optionally), if you do not want, just write 'I don't know': ''')
            state[user_id]['about'] = message.text
            state[user_id]['state'] = 'WRITING_INFO_DESIRES'
        else:
            bot.send_message(chat_id=chat_id,
                             text='Sorry, you must write about something! Try again:')
        
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
            user_name=message.from_user.username,
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