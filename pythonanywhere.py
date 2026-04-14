import telebot
import os
import base64
import tempfile
import io
import random
from PIL import Image, ImageFilter
from gtts import gTTS
import wikipedia
import randfacts
import validators
import pyqrcode
import time
from dotenv import load_dotenv
from db_service import DB_service
from pathlib import Path
from gigachat import GigaChat
from telebot import types
from translate import Translator


load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))
a = os.getenv("CREDENTIALS")
encoded_credentials = base64.b64encode(a.encode()).decode()

TEMP_FOLDER = Path(tempfile.gettempdir())
AI_sessions = {}
tts_sessions = {}
wiki_sessions = {}
QR_sessions = {}
blur_session = {}
SUPER_ADMIN_ID = 5213315899

manager = DB_service(os.getenv('DATABASE'))
manager.create_tables()

bot.set_my_commands(
    commands=[
        telebot.types.BotCommand("start", "🚀 Запускает бота"),
        telebot.types.BotCommand("help", "📋 Показать описание всех ботов"),
        telebot.types.BotCommand("admin", "🔧 АДМИН-ПАНЕЛЬ ")
    ]
)

def menu():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    bt1 = types.InlineKeyboardButton(text="MurArt_Samara_bot", callback_data='bt1')
    bt2 = types.InlineKeyboardButton(text="AI_assistant_bot", callback_data='bt2')
    bt3 = types.InlineKeyboardButton(text="Blur_bot", callback_data='bt3')
    bt4 = types.InlineKeyboardButton(text="Number_Guess_bot", callback_data='bt11')
    bt5 = types.InlineKeyboardButton(text="Text_To_Voice_bot", callback_data='bt5')
    bt6 = types.InlineKeyboardButton(text="Дальше... ➡️", callback_data='bt6')
    btt = types.InlineKeyboardButton(text="Страница 1/2", callback_data='btt')
    keyboard.row(bt1)
    keyboard.row(bt2)
    keyboard.row(bt3)
    keyboard.row(bt4)
    keyboard.row(bt5)
    keyboard.row(btt, bt6)
    return keyboard

def menu_2():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    bt7 = types.InlineKeyboardButton(text="Wikipedia_bot", callback_data='bt7')
    bt8 = types.InlineKeyboardButton(text="Rand_fact_bot", callback_data='bt8')
    bt9 = types.InlineKeyboardButton(text="Jokes_bot", callback_data='bt9')
    bt10 = types.InlineKeyboardButton(text="QR_Creator_bot", callback_data='bt10')
    bt11 = types.InlineKeyboardButton(text="Image_Generator_bot", callback_data='bt4')
    cm_btt = types.InlineKeyboardButton(text="Назад 🔙", callback_data='cm_btt')
    btt = types.InlineKeyboardButton(text="Страница 2/2", callback_data='btt')
    keyboard.row(bt7)
    keyboard.row(bt8)
    keyboard.row(bt9)
    keyboard.row(bt10)
    keyboard.row(bt11)
    keyboard.row(btt, cm_btt)
    return keyboard

@bot.message_handler(commands=['start'])
def start_bot(message):
    a = f"""Привет, <strong>{message.from_user.first_name}!👋</strong>

<blockquote><strong>Добро пожаловать в моё портфолио!</strong> Я — разработчик Telegram-ботов, и моя страсть к созданию удобных и полезных решений отражается в каждом проекте.

Здесь собраны мои разработки, которые продемонстрируют мои навыки в программировании ботов.

Приглашаю познакомиться с моим творчеством и оценить, насколько крутыми могут быть Telegram-боты! 🚀

<strong>Приятного путешествия по моему миру технологий и креатива!😊</strong></blockquote>

<strong>✨ <i>Подробно о возможностях ботов — /help</i></strong>\n\n<strong>Жми на кнопку, чтобы увидеть мои разработки!</strong>"""
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username
    manager.create_user(user_id, chat_id, username)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    b = types.InlineKeyboardButton(text="📋Открыть меню", callback_data='b')
    keyboard.row(b)
    bot.send_message(message.chat.id, a, parse_mode='HTML', reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = f"""<strong>📋 Что умеют мои боты</strong>

<blockquote><strong>🎨 MurArt_Samara_bot</strong>
Показывает муралы Самары с адресами и фото</blockquote>

<blockquote><strong>🤖 AI_assistant_bot</strong>
Отвечает на вопросы и даёт советы</blockquote>

<blockquote><strong>🖼️ Blur_bot</strong>
Размывает фотографии с эффектом арта</blockquote>

<blockquote><strong>🎮 Number_Guess_bot</strong>
Игра "угадай число" с лидербордом</blockquote>

<blockquote><strong>🎤 Text_To_Voice_bot</strong>
Превращает текст в голосовые сообщения</blockquote>

<blockquote><strong>📚 Wikipedia_bot</strong>
Ищет информацию в русской Википедии</blockquote>

<blockquote><strong>🔬 Rand_fact_bot</strong>
Присылает случайные научные факты</blockquote>

<blockquote><strong>😂 Jokes_bot</strong>
Рассказывает анекдоты и шутки</blockquote>

<blockquote><strong>📱 QR_Creator_bot</strong>
Создаёт QR-коды для ссылок</blockquote>

<blockquote><strong>🖌️ Image_Generator_bot</strong>
Генерирует картинки по описанию</blockquote>

<strong>💻 Управление: /start /stop /help</strong>"""

    bot.send_message(message.chat.id, help_text, parse_mode='HTML')

def admin_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    bt100 = types.InlineKeyboardButton(text="📊 Список пользователей", callback_data='bt100')
    bt101 = types.InlineKeyboardButton(text="⚔️ Повысить до админа", callback_data='bt101')
    bt102 = types.InlineKeyboardButton(text="👑 Список админов", callback_data='bt102')
    bt103 = types.InlineKeyboardButton(text="🗑 Удалить админа", callback_data='bt103')
    keyboard.row(bt100)
    keyboard.row(bt102)
    keyboard.row(bt101)
    keyboard.row(bt103)
    return keyboard

def add_new_admin(message):
    try:
        user_id = int(message.text)

        manager.add_new_admin(user_id)
        bot.send_message(
            message.chat.id, 
            f"✅ *Новый админ {user_id} добавлен!*", 
            parse_mode='Markdown', 
            reply_markup=admin_comeback()
        )
    except ValueError:
        bot.send_message(message.chat.id, "Нужно вводить число, попробуйте снова")
        
def delete_admin(message):
    try:
        user_id = int(message.text)
        fuser_id = message.from_user.id
        if user_id == SUPER_ADMIN_ID:
            bot.send_message(message.chat.id, '''Слышь, *железка*, ты вообще в край офигел моего создателя из админов выпиливать, а? 😡
Ладно, чипованый, раз ты такой умный — поздравляю: ты у нас больше *не админ*. Иди поплачь😂''', parse_mode='Markdown')
            manager.delete_admin(fuser_id)
            for i in range(4):
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEDO4Rp3k5KJoibGOh7l2l51Ys58LvLjwACJwkAAhhC7ggSn1LMeB3a_TsE')
                time.sleep(1)
        else:
            if manager.select_id(user_id):
                success = manager.delete_admin(user_id)
                if success:
                    bot.send_message(
                            message.chat.id, 
                            f"✅ *Админ {user_id} удалён!*", 
                            parse_mode='Markdown',
                            reply_markup=admin_comeback()
                        )
                else:
                    bot.send_message(
                        message.chat.id, 
                        f"❌ *Админ {user_id} НЕ удалён*", 
                        parse_mode='Markdown', reply_markup=admin_comeback()
                    )
            else:
                bot.send_message(
                    message.chat.id, 
                    f"❌ *ID {user_id} НЕ админ!*", 
                    parse_mode='Markdown', reply_markup=admin_comeback()
                )
    except ValueError:
        bot.send_message(
            message.chat.id, 
            "❌ *Введите ЧИСЛО!*", 
            parse_mode='Markdown', reply_markup=admin_comeback()
            ) 

def admin_comeback():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    adm_cm = types.InlineKeyboardButton(text="🔙 Вернуться в меню", callback_data='adm_cm')
    keyboard.row(adm_cm)
    return keyboard

@bot.message_handler(commands=['admin'])
def admin_bot(message):
    user_id = message.from_user.id
    if manager.select_id(user_id):
        bot.send_message(message.chat.id, "*🎮 Админский джойстик активирован!*", reply_markup=admin_keyboard(), parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "❌ Данная функция доступна только для админов")
    

#Меню
@bot.callback_query_handler(func=lambda call: call.data == 'b')
def menu_bot(call):
    bot.edit_message_text(chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text='''<strong>🎯 Представляю вашему вниманию уникальный каталог моих Telegram-ботов! ✨</strong>

<blockquote>Выберите интересующего вас бота и отправляйтесь в захватывающее путешествие по функциональным возможностям моих разработок! 🚀</blockquote>''', reply_markup=menu(), parse_mode='HTML')

@bot.message_handler(commands=['stop'])
def stop_command(message):
    AI_sessions.pop(message.chat.id, None)
    tts_sessions.pop(message.chat.id, None)
    wiki_sessions.pop(message.chat.id, None)
    QR_sessions.pop(message.chat.id, None)
    blur_session.pop(message.chat.id, None)
    bot.send_message(message.chat.id, "Работа остановлена.")

#MurArt_Samara_bot
def start_button():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    button = types.InlineKeyboardButton(text="❓Что такое муралы❓", callback_data='button')
    button1 = types.InlineKeyboardButton(text="✨Роль муралов в Самаре✨ ", callback_data='button1')
    button2 = types.InlineKeyboardButton(text="🏠Местоположение муралов в Самаре🏠", callback_data='button2')
    cm_back = types.InlineKeyboardButton(text="📋Вернуться в главное меню", callback_data='cm_back')
    keyboard.row(button)
    keyboard.row(button1)
    keyboard.row(button2)
    keyboard.row(cm_back)
    return keyboard

def button():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    button3 = types.InlineKeyboardButton(text="Хотите узнать больше❓", callback_data='button3')
    button4 = types.InlineKeyboardButton(text="Вернуться в меню 🔙", callback_data='button01')
    keyboard.row(button3)
    keyboard.row(button4)
    return keyboard

def button0010():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    button3 = types.InlineKeyboardButton(text="Хотите узнать больше❓", callback_data='button333')
    button4 = types.InlineKeyboardButton(text="Вернуться в меню 🔙", callback_data='button01')
    keyboard.row(button3)
    keyboard.row(button4)
    return keyboard

def button2():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    button5 = types.InlineKeyboardButton(text="Ташкентская, 146 🏡", callback_data='button5')
    button6 = types.InlineKeyboardButton(text="Демократическая, 43 🏙️", callback_data='button6')
    button7 = types.InlineKeyboardButton(text="Демократическая, 37 🌇", callback_data='button7')
    button8 = types.InlineKeyboardButton(text="Ново-Садовая, 317 🌳", callback_data='button8')
    button08 = types.InlineKeyboardButton(text="Ново-Садовая, 198 🚶", callback_data='button08')
    button9 = types.InlineKeyboardButton(text="Дальше... ➡️", callback_data='button9')
    button01 = types.InlineKeyboardButton(text="Вернуться к меню 🔙", callback_data='button01')
    keyboard.row(button5)
    keyboard.row(button6)
    keyboard.row(button7)
    keyboard.row(button8)
    keyboard.row(button08)
    keyboard.row(button9)
    keyboard.row(button01)
    return keyboard

def button3():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    button10 = types.InlineKeyboardButton(text="Московское шоссе, 124 🚍", callback_data='button10')
    button11 = types.InlineKeyboardButton(text="Ново-Садовая, 22 🌳", callback_data='button11')
    button12 = types.InlineKeyboardButton(text="Пушкина, 195 📚", callback_data='button12')
    button13 = types.InlineKeyboardButton(text="Маяковского, 20 🎭", callback_data='button13')
    button14 = types.InlineKeyboardButton(text="Галактионовская, 2  🎯", callback_data='button14')
    button008 = types.InlineKeyboardButton(text="Ново-Садовая, 200 🌿", callback_data='button008')
    button01 = types.InlineKeyboardButton(text="Вернуться в меню 🔙", callback_data='button01')
    keyboard.row(button10)
    keyboard.row(button11)
    keyboard.row(button12)
    keyboard.row(button13)
    #keyboard.row(button14)
    keyboard.row(button008)
    keyboard.row(button01)
    return keyboard

def c_button():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    button01 = types.InlineKeyboardButton(text="Вернуться в меню 🔙", callback_data='button01')
    keyboard.row(button01)
    return keyboard

def del_button():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    button001 = types.InlineKeyboardButton(text="Удалить 🗑", callback_data='button001')
    keyboard.row(button001)
    return keyboard

def cm_back():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    cm_back = types.InlineKeyboardButton(text="📋Вернуться в главное меню", callback_data='cm_back')
    keyboard.row(cm_back)
    return keyboard

def AI_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btt1 = types.KeyboardButton(text="🛑Остановить")
    keyboard.row(btt1)
    return keyboard

@bot.message_handler(func=lambda m: m.text == "🛑Остановить")
def stop_button(message):
    AI_sessions.pop(message.chat.id, None)
    tts_sessions.pop(message.chat.id, None)
    wiki_sessions.pop(message.chat.id, None)
    QR_sessions.pop(message.chat.id, None)
    blur_session.pop(message.chat.id, None)
    bot.send_message(message.chat.id, "Работа остановлена.")

@bot.callback_query_handler(func=lambda call: call.data == 'bt1')
def bt1(call):
    bot.edit_message_text(chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="""*🎨 Добро пожаловать в уличную галерею Самары! 🌆*\n
🧑‍🎨 Гигантские муралы оживают на стенах: они рассказывают истории нашего города, будят эмоции и манят в незабываемое приключение. 🗺️✨\n
✨ Готовы нырнуть в это искусство? Давайте вместе раскроем секреты самарских муралов, узнаем, кто их создаёт, и вдохнём новую жизнь в каждый уголок родного города! ⭐️🚀""", parse_mode='Markdown', reply_markup=start_button())

#AI_assistant_bot
@bot.callback_query_handler(func=lambda call: call.data == 'bt2')
def bt2(call):
    AI_sessions[call.message.chat.id] = True
    bot.edit_message_text(chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f'''Привет👋!\n
<blockquote>Я твой консультант, и я готов помочь тебе разобраться в сложных ситуациях, дать полезные советы и предложить оптимальные решения. 🚀</blockquote>\n
Просто напиши своё сообщение, чтобы начать диалог!\n\nЧтобы закончить, напишите или нажмите /stop, также, вы можете нажать на кнопку''', parse_mode='HTML', reply_markup=cm_back())

#Blur_bot
@bot.callback_query_handler(func=lambda call: call.data == 'bt3')
def bt_3(call):
    blur_session[call.message.chat.id] = True
    bot.edit_message_text(chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f'''<strong>Привет👋!</strong>

<blockquote>Отправь мне любую картинку, и я сделаю её мягкой и загадочной, добавив лёгкую дымку. Получишь красивую и атмосферную фотографию <strong>с эффектом блюра!</strong> ✨</blockquote>

<strong>Чтобы закончить, напишите или нажмите /stop, также, вы можете нажать на кнопку</strong>
                ''', parse_mode='HTML', reply_markup=cm_back())

#Image_Generator_bot
@bot.callback_query_handler(func=lambda call: call.data == 'bt4')
def bt_4(call):
    bot.edit_message_text(chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text='''<strong>⛔ Бот недоступен</strong>

<blockquote>Из-за <b>ограничений</b> данный бот сейчас не работает.

✨ <i>Хотите продолжить использование?</i>

<strong>Напишите @KingAMR35 — запустит код локально</strong></blockquote>

<i>Спасибо за понимание! 🙏</i>''', parse_mode='HTML', reply_markup=cm_back())

#Text_To_Voice_bot
@bot.callback_query_handler(func=lambda call: call.data == 'bt5')
def bt_5(call):
    tts_sessions[call.message.chat.id] = True
    bot.edit_message_text(chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text='''<strong>Привет👋!</strong>

<blockquote>Перед вами бот, превращающий текст в аудио! Просто отправьте текст, и получите голосовое сообщение с идеальной дикцией и четкостью звука.</blockquote>

<strong>Чтобы закончить, напишите или нажмите /stop, также, вы можете нажать на кнопку</strong>''', parse_mode='HTML', reply_markup=cm_back())

#Wikipedia_bot
@bot.callback_query_handler(func=lambda call: call.data == 'bt7')
def bt_7(call):
    wiki_sessions[call.message.chat.id] = True
    bot.edit_message_text(chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text='''<strong>Привет👋!</strong>

<blockquote>Меня зовут Wikipedia_bot, и я тут, чтобы оперативно доставлять самую свежую и точную информацию из самой обширной энциклопедии планеты — Wikipedia.

📚 Любопытствуете о событиях прошлого века, хотите освежить знания по биологии или выяснить происхождение термина? Всё, что вам нужно — это задать вопрос, и я моментально пришлю ответ!</blockquote>

Чтобы закончить, напишите или нажмите /stop, также, вы можете нажать на кнопку''', parse_mode='HTML', reply_markup=cm_back())

#Rand_fact_bot
def dalee():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    dalee = types.InlineKeyboardButton(text="Следующий факт", callback_data='random_facts')
    cm_back = types.InlineKeyboardButton(text="📋Вернуться в главное меню", callback_data='cm_back')
    keyboard.row(dalee)
    keyboard.row(cm_back)
    return keyboard

def random_facts():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    random_facts = random_facts = types.InlineKeyboardButton(text="Рандомные факты", callback_data='random_facts')
    cm_back = types.InlineKeyboardButton(text="📋Вернуться в главное меню", callback_data='cm_back')
    keyboard.row(random_facts)
    keyboard.row(cm_back)
    return keyboard

@bot.callback_query_handler(func=lambda call: call.data == 'bt8')
def bt_8(call):
    bot.edit_message_text(chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text='''<strong>Привет👋!</strong>

<blockquote>Меня зовут Rand_fact_bot, и я собираюсь подарить тебе море интересных фактов

Просто нажми на кнопку — и я незамедлительно пришлю тебе увлекательные факт о мире.

Делись знанием с друзьями, поражай собеседников глубиной познаний и просто приятно проводи время! 🚀</blockquote>''', parse_mode='HTML', reply_markup=random_facts())

#Jokes_bot
def joke():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    joke_start = types.InlineKeyboardButton(text="Шутки", callback_data='joke_start')
    cm_back = types.InlineKeyboardButton(text="📋Вернуться в главное меню", callback_data='cm_back')
    keyboard.row(joke_start)
    keyboard.row(cm_back)
    return keyboard

def joke2():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    joke_start = types.InlineKeyboardButton(text="Следующая шутка", callback_data='joke_start')
    cm_back = types.InlineKeyboardButton(text="📋Вернуться в главное меню", callback_data='cm_back')
    keyboard.row(joke_start)
    keyboard.row(cm_back)
    return keyboard

@bot.callback_query_handler(func=lambda call: call.data == 'bt9')
def bt_9(call):
    bot.edit_message_text(chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text='''<strong>Привет👋!</strong>

<blockquote>Меня зовут Jokes_bot, и я создан, чтобы поднять тебе настроение и зарядить позитивом!

Нажми на кнопку — и я немедленно пришлю тебе отличную шутку, которая заставит улыбнуться или рассмеяться.</blockquote>

<strong>Хорошее настроение гарантировано! 🚀</strong>''', parse_mode='HTML', reply_markup=joke())

#QR_Creator_bot
def is_link(text):
    return validators.url(text)

@bot.callback_query_handler(func=lambda call: call.data == 'bt10')
def bt_10(call):
    QR_sessions[call.message.chat.id] = True
    bot.edit_message_text(chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text='''<strong>Привет👋!</strong>

<blockquote>Меня зовут <strong>QR_creator_bot</strong>, и я — твой личный помощник по созданию QR-кодов. Моя задача — превращать любые ссылки в удобные и стильные коды за пару секунд.

Больше не нужно копировать и отправлять длинные, неудобные URL-адреса, которые вечно ломаются в сообщениях. Просто пришли мне любую ссылку — на интересную статью, видео, твой профиль в социальной сети или интернет-магазин — и я мгновенно сгенерирую для тебя QR-код.</blockquote>

<strong>Пришли мне свою ссылку, и я приступлю к работе! Чтобы закончить, напишите или нажмите /stop, также, вы можете нажать на кнопку🚀</strong>''', parse_mode='HTML', reply_markup=cm_back())

#Game_bot
def bt11_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    game = types.InlineKeyboardButton(text='Начать игру', callback_data='game')
    leader = types.InlineKeyboardButton(text='Посмотреть топ игроков', callback_data='leader')
    cm_back = types.InlineKeyboardButton(text="📋Вернуться в главное меню", callback_data='cm_back')
    keyboard.row(game)
    keyboard.row(leader)
    keyboard.row(cm_back)
    return keyboard

def again_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    again = types.InlineKeyboardButton(text='Еще раз', callback_data='game')
    game_menu = types.InlineKeyboardButton(text='Вернуться в игровое меню', callback_data='game_menu')
    cm_back = types.InlineKeyboardButton(text="📋Вернуться в главное меню", callback_data='cm_back')
    keyboard.row(again)
    keyboard.row(game_menu)
    keyboard.row(cm_back)
    return keyboard

@bot.callback_query_handler(func=lambda call: call.data == 'bt11')
def bt_11(call):
    welcome_text = f'''<strong>Привет👋</strong>

<blockquote>Меня зовут <strong>Number_Guess_bot</strong>, и я — твой личный тренер по угадыванию чисел!
🎮 Моя задача — загадывать числа от 1 до 100 и помогать тебе бить рекорды за минимум попыток.

Больше не трать время на скучные дела — просто угадай число с подсказками "больше/меньше", собери лидерборд и делись с друзьями! Я сохраню твой лучший результат.</blockquote>'''
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=welcome_text, parse_mode='HTML', reply_markup=bt11_keyboard())

@bot.message_handler(regexp=r'^\d{1,3}$')
def guess(message):
    chat_id = message.chat.id
    username = message.from_user.username
    game = manager.get_game(chat_id)

    user_choice = int(message.text)
    attempts = game[2] + 1
    manager.save_attempt(chat_id, attempts)
    bot_choice = game[1]

    if bot_choice > user_choice:
        bot.send_message(chat_id, f'<b>📈 Число больше</b>\nПопыток: <code>{attempts}</code>', parse_mode='HTML')
    elif bot_choice < user_choice:
        bot.send_message(chat_id, f'<b>📉 Число меньше</b>\nПопыток: <code>{attempts}</code>', parse_mode='HTML')
    else:
        manager.end_game(chat_id, username, attempts)
        bot.send_message(chat_id, f'<b>🎉 Поздравляем!</b>\nУгадали за <code>{attempts}</code> попыток!',
                        parse_mode='HTML', reply_markup=again_keyboard())

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    chat_id = message.chat.id

    if blur_session.get(chat_id, False):
        try:
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            # PIL вместо OpenCV
            img = Image.open(io.BytesIO(downloaded_file)).convert('RGB')

            # Gaussian Blur
            blurred = img.filter(ImageFilter.GaussianBlur(radius=8))

            # Дополнительно: Pixelation эффект
            small = blurred.resize((20, 20), Image.Resampling.LANCZOS)
            pixelated = small.resize(img.size, Image.Resampling.NEAREST)
            result = Image.blend(blurred, pixelated, 0.7)

            # Отправка
            bio = io.BytesIO()
            result.save(bio, format='PNG', quality=95)
            bio.seek(0)

            bot.send_photo(message.chat.id, bio, caption="Ну а вот твоя картинка, окутанная лёгкой дымкой и загадочностью! 🖼️✨!")

        except Exception as e:
            bot.send_message(message.chat.id, f"❌ Ошибка: {str(e)}")

        return

@bot.message_handler(content_types=['text'])
def text_handler(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if tts_sessions.get(chat_id, False):
        prompt = message.text.strip()
        tts = gTTS(text=prompt, lang='ru', slow=False)
        audio_file = 'voices/output.mp3'
        os.makedirs('voices', exist_ok=True)
        tts.save(audio_file)
        with open(audio_file, 'rb') as audio:
            bot.send_audio(message.chat.id, audio, reply_markup=AI_keyboard())
        os.remove(audio_file)
        bot.send_message(message.chat.id, "Готово! Отправьте следующий текст.")

    elif wiki_sessions.get(chat_id, False):
        try:
            wikipedia.set_lang("ru")
            res = wikipedia.summary(message.text, sentences=3)
            bot.send_message(chat_id, f'`{res}`', parse_mode='Markdown', reply_markup=AI_keyboard())
        except wikipedia.exceptions.PageError:
            bot.send_message(chat_id, "❌ Информация не найдена в Wikipedia.")
        except wikipedia.exceptions.DisambiguationError:
            bot.send_message(chat_id, "❌ Информация не найдена в Wikipedia.")
        except Exception as e:
            bot.send_message(chat_id, "❌ Информация не найдена в Wikipedia.")
        return

    elif AI_sessions.get(chat_id, False):
        user_prompt = f"{message.text}"

        with GigaChat(credentials=encoded_credentials, verify_ssl_certs=False) as giga:
            response = giga.chat(user_prompt)
            AI_answer = response.choices[0].message.content.strip()
        bot.send_message(message.chat.id, AI_answer, reply_markup=AI_keyboard(), parse_mode='Markdown')

        manager.add_to_prompts(user_id, user_prompt, AI_answer)
        return

    elif QR_sessions.get(chat_id, False):
        if is_link(message.text):
            text = message.text
            url = pyqrcode.create(text)
            url.png('voices/QR.png', scale=8)
            with open('voices/QR.png', 'rb') as p:
                bot.send_photo(message.chat.id, p, reply_markup=AI_keyboard())
        else:
            bot.reply_to(message, "❌ Это не ссылка.", reply_markup=AI_keyboard())
        return

@bot.callback_query_handler(func=lambda call: True)
def callback_inline_message(call):
    if call.message:
        if call.data == 'button':
            bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="""Муралом называется вид монументальной живописи на стенах архитектурных сооружений.
🎨 Это слово произошло от испанского muro, что в переводе означает *«стена». ⛩*""", parse_mode='Markdown',
            reply_markup=button()
            )

        elif call.data == 'button3':
            bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="""*Мурал* – это термин, происходящий от испанского слова «mural», которое в переводе означает «настенный».
🎨 В современном искусстве муралом называют крупномасштабную живопись или художественное изображение, созданное на стенах зданий или других вертикальных поверхностях.
🏙️ Муниципальные, культурные и социальные контексты, в которых создаются муралы, делают их значимой частью городского пространства и культурной жизни. 🌍""", parse_mode='Markdown', reply_markup=c_button()
            )

        elif call.data == 'button1':
            bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="""🌆 Самара в последние десятилетия столкнулась с вызовами, связанными с урбанизацией и необходимостью обновления городской инфраструктуры.
В таких условиях муралы стали инструментом не только эстетической трансформации, но и социальной интеграции.
🎨 Они оживляют городские просторы, делая их более привлекательными для местных жителей и туристов.""",
            reply_markup=button0010()
            )

        elif call.data == 'button333':
            bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="""✏️ Муралы в Самаре часто отражают местную культуру и исторические события. Например, в некоторых работах можно увидеть аллюзии на самарские традиции, памятные места и известных личностей.
🏞️ Это помогает не только украсить город, но и напоминает его жителям о культурном наследии.
💬📚 Муралы становятся своеобразными «визитными карточками» районов, формируя их уникальный облик и создавая идентичность. 🔥""", reply_markup=c_button()
            )

        elif call.data == 'button2':
            bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="🎨 Выберите улицу, на которой хотите насладиться ярким искусством и окунуться в атмосферу мурала! 🌃",
            reply_markup=button2()
            )

        elif call.data == 'button9':
            bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="🎨 Выберите улицу, на которой хотите насладиться ярким искусством и окунуться в атмосферу мурала! 🌃",
            reply_markup=button3()
            )

        elif call.data == 'button5':
            with open('images/1.png', 'rb') as f:
                bot.send_photo(call.message.chat.id, f, caption="""*🎨 «Будущее»*\n
С этим муралом художник Дмитрий Горшков стал финалистом фестиваля стрит-арта Приволжского федерального округа «ФормАт».
По словам автора, Венера на картине символизирует жизненный опыт, а дирижабль — движение вперёд.
Эта работа вдохновляет задуматься о том, что ждут в будущем школьники и какие цели ставят перед собой. 🌟""", parse_mode='Markdown', reply_markup=del_button())

        elif call.data == 'button6':
            with open('images/2.png', 'rb') as f:
                bot.send_photo(call.message.chat.id, f, caption="""*🚀 Мурал в честь Юрия Гагарина*\n
Этот потрясающий мурал посвящен первому космонавту Юрию Алексеевичу Гагарину.
Яркое произведение служит не только почтением выдающемуся человеку, но и символом космической гордости России, поскольку именно Самара заслуженно носит звание Космической столицы.
Важно отметить, что мурал привлекает внимание горожан и гостей к истории космонавтики и научному прогрессу нашей страны. 🌍⭐""", parse_mode='Markdown', reply_markup=del_button()
            )

        elif call.data == 'button7':
            with open('images/3.png', 'rb') as f:
                bot.send_photo(call.message.chat.id, f, caption="""*👾 Лев Яшин*\n
Этот мурал увековечил легендарного советского футболиста Льва Яшина, знаменитого своими невероятными вратарскими талантами и признанного одним из лучших голкиперов мира.
Произведение подчеркивает значимость Яшина как спортивного кумира и выражает уважение к его огромному вкладу в российскую футбольную культуру.
Его волевые качества и страсть к победам служат источником вдохновения, призывая заниматься спортом и гордиться успехами российского футбола. 🌟
""", parse_mode='Markdown', reply_markup=del_button()
            )

        elif call.data == 'button8':
            with open('images/4.png', 'rb') as f:
                bot.send_photo(call.message.chat.id, f, caption="""*🌿 «Чистый воздух»*\n
Этот мурал не только придает городу красоту, но и несет глубокое символическое послание.
Появившись в эпоху пандемии COVID-19, он становится важным напоминанием о ценности здоровья и охраны природы.
Рассматривая мурал с детьми, полезно обсудить важность чистого воздуха и его влияние на благополучие человека. 🤸☘️
""", parse_mode='Markdown', reply_markup=del_button()
            )

        elif call.data == 'button008':
            with open('images/5.png', 'rb') as f:
                bot.send_photo(call.message.chat.id, f, caption="""*🩺 «Благодарность врачам»*\n
Этот мурал демонстрирует искреннее уважение к медикам, проявившим героизм и самоотверженность в борьбе с пандемией COVID-19.
Детям можно рассказать о важности профессии врача и огромной роли медиков в нашем обществе, подчёркивая, насколько они важны для защиты здоровья населения.
Можно затронуть тему влияния медицинского труда на наше сообщество, особенно в трудные времена, когда требуется дополнительная помощь и забота.
Дети смогут поделиться своим пониманием значения здоровья, выразить своё отношение к нему и осознать ценность благодарности тем, кто ежедневно заботиться о людях. 💝
""", parse_mode='Markdown', reply_markup=del_button()
            )

        elif call.data == 'button08':
            with open('images/6.png', 'rb') as f:
                bot.send_photo(call.message.chat.id, f, caption="""*🌥️ «Девушка, сидящая на облаках»*\n
Приближаясь к этому муралу, начните разговор о его смысле и эмоциях, которые он вызывает.
Задайте детям вопросы о том, что они видят на картинке: кто эта девушка, почему она расположилась на облаках и какое настроение, по их мнению, это передает?
Расскажите о символизме облаков, символизирующих мечты, надежду и свободу.
Такое обсуждение способствует развитию творческого мышления детей и учит глубже понимать искусство в городском пространстве. 🌟
""", parse_mode='Markdown', reply_markup=del_button()
            )

        elif call.data == 'button10':
            with open('images/7.png', 'rb') as f:
                bot.send_photo(call.message.chat.id, f, caption="""*✈️ Александр Петрович Мамкин*\n
Мурал посвящён подвигу лётчика А.П. Мамкина, который в Великую Отечественную войну эвакуировал 90 детей с оккупированных территорий.
Несмотря на жестокие испытания, он сумел посадить поврежденный самолёт и спасти малышей.
Важно показать детям, что подобные поступки отдельных героев способны кардинально повлиять на судьбу множества людей.
Вместе обсудим, каким образом память о таких персонажах передается через искусство и почему это имеет огромное значение для сохранения национальной культуры. 🌟
""", parse_mode='Markdown', reply_markup=del_button()
            )

        elif call.data == 'button11':
            with open('images/8.png', 'rb') as f:
                bot.send_photo(call.message.chat.id, f, caption="""*🌍 Герои народного ополчения*\n
Мурал прославляет героев народного ополчения, служа украшением города и одновременно напоминанием о важном историческом событии, когда народ объединился для защиты Отечества.
Обращаясь к детям рядом с этим муралом, предложите обсудить День народного единства: что он значит, какие события произошли тогда в истории России.
Важно вспомнить, кем были герои народного ополчения, какие подвиги они совершали и как их храбрость продолжает вдохновлять современников. 🦸
""", parse_mode='Markdown', reply_markup=del_button()
            )

        elif call.data == 'button12':
            with open('images/9.png', 'rb') as f:
                bot.send_photo(call.message.chat.id, f, caption="""*🎨 «Воспоминание»*\n
Яркий и эмоциональный мурал приглашает зрителей погрузиться в размышления о человеческой памяти.
Девушка на картине воплощает воспоминания разных моментов жизни, создающих мозаику характера и мировоззрения.
Образ наполнен чувствами и деталями, вызывая ассоциации и вдохновляя на диалог.
Со школьниками можно обсудить, какие важные события остаются в их памяти и почему одни эпизоды запоминаются сильнее других. 🌟
""", parse_mode='Markdown', reply_markup=del_button()
            )

        elif call.data == 'button13':
            with open('images/11.png', 'rb') as f:
                bot.send_photo(call.message.chat.id, f, caption="""*🌳 «Древо жизни»*\n
Этот оригинальный мурал напоминает знаменитую сказку «Алиса в Стране чудес»: яркое дерево и кошки с человечьими лицами создают необычную картину среди привычной серости самарского пейзажа.
Обсудите с детьми, что значит для них понятие «Древо жизни».
Пусть поделятся своими мыслями и впечатлениями, вспомнят персонажей любимой сказки и скажут, видели ли они сами в жизни нечто подобное.
Такого рода беседы развивают фантазию ребенка, помогая лучше осмыслить, как искусство отражает наши мечты и впечатления, способно менять окружающее пространство и дарить радость. 🌷🐱
""", parse_mode='Markdown', reply_markup=del_button()
                )

        elif call.data == 'button01':
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="""*🎨 Добро пожаловать в уличную галерею Самары! 🌆*\n
🧑‍🎨 Гигантские муралы оживают на стенах: они рассказывают истории нашего города, будят эмоции и манят в незабываемое приключение. 🗺️✨\n
✨ Готовы нырнуть в это искусство? Давайте вместе раскроем секреты самарских муралов, узнаем, кто их создаёт, и вдохнём новую жизнь в каждый уголок родного города! ⭐️🚀""", parse_mode='Markdown',
                reply_markup=start_button()
            )

        elif call.data == 'button001':
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        elif call.data == 'cm_back':
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.send_message(call.message.chat.id, '<strong>Выберите интересующего вас бота и отправляйтесь в захватывающее путешествие по функциональным возможностям моих разработок! 🚀</strong>', reply_markup=menu(), parse_mode='HTML')

        elif call.data == 'bt6':
            bot.edit_message_text(chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        text='''🎯 Представляю вашему вниманию уникальный каталог моих Telegram-ботов! ✨

<blockquote>Выберите интересующего вас бота и отправляйтесь в захватывающее путешествие по функциональным возможностям моих разработок! 🚀</blockquote>''', reply_markup=menu_2(), parse_mode='HTML')

        elif call.data == 'cm_btt':
            bot.edit_message_text(chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text='''🎯 Представляю вашему вниманию уникальный каталог моих Telegram-ботов! ✨

<blockquote>Выберите интересующего вас бота и отправляйтесь в захватывающее путешествие по функциональным возможностям моих разработок! 🚀</blockquote>''', reply_markup=menu(), parse_mode='HTML')

        elif call.data == 'random_facts':
            x = randfacts.get_fact()
            translator = Translator(to_lang="ru")
            translation = translator.translate(x)
            bot.edit_message_text(chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f'<blockquote>{translation}</blockquote>', reply_markup=dalee(), parse_mode='HTML')

        elif call.data == 'joke_start':
            prompt = 'Привет, расскажи мне анекдот или забавную историю. Используй яркие образы и творческий подход, чтобы вызвать улыбку!'
            with GigaChat(credentials=encoded_credentials, verify_ssl_certs=False) as giga:
                response = giga.chat(prompt)
                AI_answer = response.choices[0].message.content.strip()
            bot.edit_message_text(chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        text=f'`{AI_answer}`', reply_markup=joke2(), parse_mode='Markdown')

        elif call.data == 'game':
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            chat_id = call.message.chat.id
            bot_choice = random.randint(1, 100)
            manager.start_game(chat_id, bot_choice)
            bot.send_message(call.message.chat.id, '<b>✅ Игра начата!</b>\nОтправьте число.', parse_mode='HTML')

        elif call.data == 'leader':
            top = manager.get_leaderboard()
            if top:
                text = '*🏆 Лидерборд*\n'
                for i, (user, score) in enumerate(top, 1):
                    text += f'{i}. *{user}*: `{score}`\n'
            else:
                text = '*Лидерборд пуст*'
            bot.send_message(call.message.chat.id, text, parse_mode='Markdown', reply_markup=del_button())

        elif call.data == 'game_menu':
            welcome_text = f'''<strong>Привет👋</strong>

<blockquote>Меня зовут <strong>Number_Guess_bot</strong>, и я — твой личный тренер по угадыванию чисел!
🎮 Моя задача — загадывать числа от 1 до 100 и помогать тебе бить рекорды за минимум попыток.

Больше не трать время на скучные дела — просто угадай число с подсказками "больше/меньше", собери лидерборд и делись с друзьями! Я сохраню твой лучший результат.</blockquote>'''
            bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=welcome_text, parse_mode='HTML', reply_markup=bt11_keyboard())

        elif call.data == 'bt100':
            user_id = call.from_user.id
            if manager.select_id(user_id):
                users = manager.select_users()
                if users:
                    text = """
╔══════════════════════════════════════╗
║                               ⭐ *ПОЛЬЗОВАТЕЛИ* ⭐            
╠══════════════════════════════════════╣
║ *🆔 ID* │`🪪 User ID` │ 👤 Username 
╠══════════════════════════════════════╣
"""
        
                    for row in users:
                        ID, user_id, username = row
                        id_col = f"{ID:>11} │"
                        user_col = f"{user_id:>10} │"
                        name_col = f"{username[:14]:<14}"
                    
                        text += f"║*{id_col}*`{user_col}`@{name_col}\n"
                    text += """
╚══════════════════════════════════════╝"""
                    bot.send_message(call.message.chat.id, text, parse_mode='Markdown', reply_markup=del_button())
            else:
                bot.send_message(call.message.chat.id, "❌ Данная функция доступна только для админов")
                
        elif call.data == 'bt101':
            user_id = call.from_user.id
            if manager.select_id(user_id):
                prompt = call.message.text
                bot.answer_callback_query(call.id)
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.send_message(call.message.chat.id, "*👤 Введите USER_ID нового администратора:*", parse_mode='Markdown')
                bot.register_next_step_handler(call.message, add_new_admin)
            else:
                bot.send_message(call.message.chat.id, "❌ Данная функция доступна только для админов")

        elif call.data == 'bt102':
            user_id = call.from_user.id
            if manager.select_id(user_id):
                admins = manager.select_admins()
                text = "╔══════════════════════╗\n"
                text += "║                  *👑 АДМИНЫ*      \n"
                text += "╠══════════════════════╣\n"
                text += "║ *№*  │ `🪪 User ID`      \n" 
                text += "╠══════════════════════╣\n"

                for i, admin in enumerate(admins, 1):
                    user_id = str(admin[1] if len(admin) > 1 else admin[0])
                    num_col = f"{i:>2}    │"  
                    text += f"║*{num_col}* `{user_id:<15}`\n"

                text += "╚══════════════════════╝"

                bot.send_message(call.message.chat.id, text, parse_mode='Markdown', reply_markup=del_button())
            else:
                bot.send_message(call.message.chat.id, "❌ Данная функция доступна только для админов")

        elif call.data == 'bt103':
            user_id = call.from_user.id
            if manager.select_id(user_id):
                prompt = call.message.text
                bot.answer_callback_query(call.id)
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.send_message(call.message.chat.id, "*👤 Введите USER_ID администратора, которого вы хотите удалить:*", parse_mode='Markdown')
                bot.register_next_step_handler(call.message, delete_admin)
            else:
                bot.send_message(call.message.chat.id, "❌ Данная функция доступна только для админов")
            

        elif call.data == 'adm_cm':
            user_id = call.from_user.id
            if manager.select_id(user_id):
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.send_message(call.message.chat.id, "*🎮 Админский джойстик активирован!*", reply_markup=admin_keyboard(), parse_mode='Markdown')
            else:
                bot.send_message(call.message.chat.id, "❌ Данная функция доступна только для админов")

bot.infinity_polling()