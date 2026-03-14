import telebot
import os
import base64
import tempfile
import cv2
from dotenv import load_dotenv
from AI_service import generate_leonardo_image
from db_service import DB_service
from pathlib import Path
from gigachat import GigaChat
from telebot import types


load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))
a = os.getenv("CREDENTIALS")
encoded_credentials = base64.b64encode(a.encode()).decode()

TEMP_FOLDER = Path(tempfile.gettempdir())
active_sessions = {} 

manager = DB_service(os.getenv('DATABASE'))
manager.create_tables()

bot.set_my_commands(
    commands=[
        telebot.types.BotCommand("start", "🚀 Запускает бота"),
    ]
)

def menu():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    bt1 = types.InlineKeyboardButton(text="MurArt_Samara_bot", callback_data='bt1')
    bt2 = types.InlineKeyboardButton(text="AI_assistant_bot", callback_data='bt2')
    bt3 = types.InlineKeyboardButton(text="Blur_bot", callback_data='bt3')
    bt4 = types.InlineKeyboardButton(text="Image_Generator_bot", callback_data='bt4')
    keyboard.row(bt1)
    keyboard.row(bt2)
    keyboard.row(bt3)
    keyboard.row(bt4)
    return keyboard

@bot.message_handler(commands=['start'])
def start_bot(message):
    a = f"""Привет, {message.from_user.first_name}!👋

<blockquote>Добро пожаловать в моё портфолио! Я — разработчик Telegram-ботов, и моя страсть к созданию удобных и полезных решений отражается в каждом проекте.

Здесь собраны мои разработки, которые продемонстрируют мои навыки в программирование ботов.

Приглашаю познакомиться с моим творчеством и оценить, насколько крутыми могут быть Telegram-боты! 🚀

Приятного путешествия по моему миру технологий и креатива!😊</blockquote>\n\n<strong>Жми на кнопку, чтобы увидеть мои разработки!</strong>"""
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    b = types.InlineKeyboardButton(text="📋Открыть меню", callback_data='b')
    keyboard.row(b)
    bot.send_message(message.chat.id, a, parse_mode='HTML', reply_markup=keyboard)
    
#Меню
@bot.callback_query_handler(func=lambda call: call.data == 'b')
def menu_bot(call):
    bot.edit_message_text(chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text='''🎯 Представляю вашему вниманию уникальный каталог моих Telegram-ботов! ✨

<blockquote>Выберите интересующего вас бота и отправляйтесь в захватывающее путешествие по функциональным возможностям моих разработок! 🚀</blockquote>''', reply_markup=menu(), parse_mode='HTML')
    
@bot.message_handler(commands=['stop'])
def stop_command(message):
    active_sessions.pop(message.chat.id, None)
    bot.send_message(message.chat.id, "Работа с консультантом остановлена.")

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
    active_sessions.pop(message.chat.id, None)
    bot.send_message(message.chat.id, "Работа с консультантом остановлена.")
    
@bot.callback_query_handler(func=lambda call: call.data == 'bt1')
def button1_bot(call):
    bot.edit_message_text(chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="""*🎨 Добро пожаловать в уличную галерею Самары! 🌆*\n
🧑‍🎨 Гигантские муралы оживают на стенах: они рассказывают истории нашего города, будят эмоции и манят в незабываемое приключение. 🗺️✨\n
✨ Готовы нырнуть в это искусство? Давайте вместе раскроем секреты самарских муралов, узнаем, кто их создаёт, и вдохнём новую жизнь в каждый уголок родного города! ⭐️🚀""", parse_mode='Markdown', reply_markup=start_button())

#AI_assistant_bot
@bot.callback_query_handler(func=lambda call: call.data == 'bt2')
def bt2_1(call):
    active_sessions[call.message.chat.id] = True
    bot.edit_message_text(chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f'''Привет👋!\n
<blockquote>Я твой консультант, и я готов помочь тебе разобраться в сложных ситуациях, дать полезные советы и предложить оптимальные решения. 🚀</blockquote>\n
Просто напиши своё сообщение, чтобы начать диалог!\n\nЧтобы закончить, напиши или нажми /stop, также, вы можете нажать на кнопку''', parse_mode='HTML', reply_markup=cm_back())
    
    @bot.message_handler(func=lambda message: bool(message.text.strip()))
    def user_message(message):
        if active_sessions.get(message.chat.id, False):
            user_prompt = f"{message.text}."
            
            with GigaChat(credentials=encoded_credentials, verify_ssl_certs=False) as giga:
                response = giga.chat(user_prompt)
                AI_answer = response.choices[0].message.content.strip()
            bot.send_message(message.chat.id, AI_answer, reply_markup=AI_keyboard(), parse_mode='Markdown')
            
            user_id = message.from_user.id
            chat_id = message.chat.id
            username = message.from_user.username
            manager.create_user(user_id, chat_id, username)
            manager.add_to_prompts(user_prompt, AI_answer)
        else:
            pass

#Blur_bot
@bot.callback_query_handler(func=lambda call: call.data == 'bt3')
def bt_3_1(call):
    bot.edit_message_text(chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f'''*Привет👋*!
Отправь мне любую картинку, и я сделаю её мягкой и загадочной, добавив лёгкую дымку.Получишь красивую и атмосферную фотографию *с эффектом блюра! ✨*
                ''', parse_mode='Markdown', reply_markup=cm_back())
    @bot.message_handler(content_types=['photo'])
    def handle_photo(message):
      file_id = message.photo[-1].file_id
      file_info = bot.get_file(file_id)
      downloaded_file = bot.download_file(file_info.file_path)

      temp_file = TEMP_FOLDER / f"{file_id}.jpg"
      with open(temp_file, 'wb') as f:
          f.write(downloaded_file)

      image = cv2.imread(str(temp_file))

      if image is None:
          bot.reply_to(message, "Не удалось распознать изображение.")
          return

      blurred_image = cv2.GaussianBlur(image, (15, 15), 0)
      pixelated_image = cv2.resize(blurred_image, (30, 30), interpolation=cv2.INTER_NEAREST)
      pixelated_image = cv2.resize(pixelated_image, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_NEAREST)
      processed_temp_file = TEMP_FOLDER / f"{file_id}_processed.jpg"
      cv2.imwrite(str(processed_temp_file), pixelated_image)

      with open(processed_temp_file, 'rb') as pf:
          bot.send_photo(message.chat.id, pf, caption='Ну а вот твоя картинка, окутанная лёгкой дымкой и загадочностью! 🖼️✨')

      temp_file.unlink(missing_ok=True)
      processed_temp_file.unlink(missing_ok=True)

#Image_Generator_bot
@bot.callback_query_handler(func=lambda call: call.data == 'bt4')
def bt_4_1(call):
    bot.edit_message_text(chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text='''*Привет👋!*\n\n
✨ Добро пожаловать в мир *ИИ-генерации!*\n
Напиши мне какую-нибудь фразу и я сгенерирую её!🎨''', parse_mode='Markdown', reply_markup=cm_back())
    
    @bot.message_handler(func=lambda message: message.chat.id == call.message.chat.id)
    def AI_prompt(message):
        prompt = message.text
        chat_id = message.chat.id
        username = message.from_user.username
        bot.send_chat_action(chat_id, 'typing')
        bot.send_message(message.chat.id, "Подождите, идёт отправка фото🔄")
        bot.send_chat_action(chat_id, 'upload_photo')
        
        image_buffer, status = generate_leonardo_image(prompt)
        
        manager.leonardo_AI(prompt, username)
        
        if image_buffer:
            bot.send_photo(
                chat_id=chat_id,
                photo=image_buffer,
                caption=f"✨ *{prompt}*\n\n{status}",
                parse_mode='Markdown'
            )
        else:
            bot.send_message(chat_id, f"❌ Ошибка: {status}")

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
            with open('images\\1.png', 'rb') as f:  
                bot.send_photo(call.message.chat.id, f, caption="""*🎨 «Будущее»*\n
С этим муралом художник Дмитрий Горшков стал финалистом фестиваля стрит-арта Приволжского федерального округа «ФормАт». 
По словам автора, Венера на картине символизирует жизненный опыт, а дирижабль — движение вперёд. 
Эта работа вдохновляет задуматься о том, что ждут в будущем школьники и какие цели ставят перед собой. 🌟""", parse_mode='Markdown', reply_markup=del_button())

        elif call.data == 'button6':
            with open('images\\2.png', 'rb') as f:  
                bot.send_photo(call.message.chat.id, f, caption="""*🚀 Мурал в честь Юрия Гагарина*\n
Этот потрясающий мурал посвящен первому космонавту Юрию Алексеевичу Гагарину. 
Яркое произведение служит не только почтением выдающемуся человеку, но и символом космической гордости России, поскольку именно Самара заслуженно носит звание Космической столицы. 
Важно отметить, что мурал привлекает внимание горожан и гостей к истории космонавтики и научному прогрессу нашей страны. 🌍⭐""", parse_mode='Markdown', reply_markup=del_button()
            )

        elif call.data == 'button7':
            with open('images\\3.png', 'rb') as f:  
                bot.send_photo(call.message.chat.id, f, caption="""*👾 Лев Яшин*\n 
Этот мурал увековечил легендарного советского футболиста Льва Яшина, знаменитого своими невероятными вратарскими талантами и признанного одним из лучших голкиперов мира. 
Произведение подчеркивает значимость Яшина как спортивного кумира и выражает уважение к его огромному вкладу в российскую футбольную культуру. 
Его волевые качества и страсть к победам служат источником вдохновения, призывая заниматься спортом и гордиться успехами российского футбола. 🌟
""", parse_mode='Markdown', reply_markup=del_button()
            )

        elif call.data == 'button8':
            with open('images\\4.png', 'rb') as f:  
                bot.send_photo(call.message.chat.id, f, caption="""*🌿 «Чистый воздух»*\n
Этот мурал не только придает городу красоту, но и несет глубокое символическое послание. 
Появившись в эпоху пандемии COVID-19, он становится важным напоминанием о ценности здоровья и охраны природы. 
Рассматривая мурал с детьми, полезно обсудить важность чистого воздуха и его влияние на благополучие человека. 🤸☘️
""", parse_mode='Markdown', reply_markup=del_button()
            )

        elif call.data == 'button008':
            with open('images\\5.png', 'rb') as f:  
                bot.send_photo(call.message.chat.id, f, caption="""*🩺 «Благодарность врачам»*\n
Этот мурал демонстрирует искреннее уважение к медикам, проявившим героизм и самоотверженность в борьбе с пандемией COVID-19. 
Детям можно рассказать о важности профессии врача и огромной роли медиков в нашем обществе, подчёркивая, насколько они важны для защиты здоровья населения. 
Можно затронуть тему влияния медицинского труда на наше сообщество, особенно в трудные времена, когда требуется дополнительная помощь и забота. 
Дети смогут поделиться своим пониманием значения здоровья, выразить своё отношение к нему и осознать ценность благодарности тем, кто ежедневно заботиться о людях. 💝
""", parse_mode='Markdown', reply_markup=del_button()
            )
        
        elif call.data == 'button08':
            with open('images\\6.png', 'rb') as f:  
                bot.send_photo(call.message.chat.id, f, caption="""*🌥️ «Девушка, сидящая на облаках»*\n
Приближаясь к этому муралу, начните разговор о его смысле и эмоциях, которые он вызывает. 
Задайте детям вопросы о том, что они видят на картинке: кто эта девушка, почему она расположилась на облаках и какое настроение, по их мнению, это передает? 
Расскажите о символизме облаков, символизирующих мечты, надежду и свободу. 
Такое обсуждение способствует развитию творческого мышления детей и учит глубже понимать искусство в городском пространстве. 🌟
""", parse_mode='Markdown', reply_markup=del_button()
            )

        elif call.data == 'button10':
            with open('images\\7.png', 'rb') as f:  
                bot.send_photo(call.message.chat.id, f, caption="""*✈️ Александр Петрович Мамкин*\n
Мурал посвящён подвигу лётчика А.П. Мамкина, который в Великую Отечественную войну эвакуировал 90 детей с оккупированных территорий. 
Несмотря на жестокие испытания, он сумел посадить поврежденный самолёт и спасти малышей. 
Важно показать детям, что подобные поступки отдельных героев способны кардинально повлиять на судьбу множества людей.
Вместе обсудим, каким образом память о таких персонажах передается через искусство и почему это имеет огромное значение для сохранения национальной культуры. 🌟
""", parse_mode='Markdown', reply_markup=del_button()
            )

        elif call.data == 'button11':
            with open('images\\8.png', 'rb') as f:  
                bot.send_photo(call.message.chat.id, f, caption="""*🌍 Герои народного ополчения*\n
Мурал прославляет героев народного ополчения, служа украшением города и одновременно напоминанием о важном историческом событии, когда народ объединился для защиты Отечества. 
Обращаясь к детям рядом с этим муралом, предложите обсудить День народного единства: что он значит, какие события произошли тогда в истории России. 
Важно вспомнить, кем были герои народного ополчения, какие подвиги они совершали и как их храбрость продолжает вдохновлять современников. 🦸
""", parse_mode='Markdown', reply_markup=del_button()
            )

        elif call.data == 'button12':
            with open('images\\9.png', 'rb') as f:  
                bot.send_photo(call.message.chat.id, f, caption="""*🎨 «Воспоминание»*\n
Яркий и эмоциональный мурал приглашает зрителей погрузиться в размышления о человеческой памяти. 
Девушка на картине воплощает воспоминания разных моментов жизни, создающих мозаику характера и мировоззрения. 
Образ наполнен чувствами и деталями, вызывая ассоциации и вдохновляя на диалог. 
Со школьниками можно обсудить, какие важные события остаются в их памяти и почему одни эпизоды запоминаются сильнее других. 🌟
""", parse_mode='Markdown', reply_markup=del_button()
            )

        elif call.data == 'button13':
            with open('images\\11.png', 'rb') as f:  
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

bot.infinity_polling()