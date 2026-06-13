import time
import threading
import schedule
import os, random
import requests
from telebot import TeleBot
from telebot import types

kom = '''Привет! Я твой Telegram бот. Напиши что-нибудь! Доступные команды:
  /hello - поприветсвует вас
  /bye - попращается с вами
  /password - сгенерирует вам надежный пароль
  /set <секунды> - засекает таймер на указанное время
  /гтset - останавливает таймер
  /heh <кол-во> - повторяет he указанное вами количество раз
  /heta - подбрасывает монетку
  /send - ссылка на курс'''
MEME_RARE_WEIGHTS = {
    'common': 5,   # часто
    'uncommon': 3, # средне
    'rare': 1,     # редко
    'epic': 0.5    # очень редко
}
MEME_RARITY_MAP = {
    '/home/animals/grinch.png': 'common',
    '/home/animals/kapibara.jpg': 'epic',
    '/home/mems/mem1.jpg': 'rare',
    '/home/mems/mem2.jpg': 'epic',
    '/home/mems/mem3.jpg': 'uncommon',
    '/home/rare/rare1.jpg': 'rare',
    '/home/rare/rare2.png': 'epic'
}
API_TOKEN = '8713972546:AAGJ0X9uJzymKoojyKIsTiIPpqBIpr0X2dA'
bot = TeleBot(API_TOKEN)

# Словарь для хранения таймеров по chat_id
active_timers = {}


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, f"{kom}")

def weighted_choice(files_list, rarity_map, weights):
    """
    Выбирает файл с учётом редкости (весов)
    """
    choices_with_weights = []
    for file in files_list:
        rarity = rarity_map.get(file, 'common')  # по умолчанию common
        weight = weights[rarity]
        choices_with_weights.extend([file] * int(weight * 10))  # умножаем для лучшей точности
    return random.choice(choices_with_weights) if choices_with_weights else None

def load_category_images(category):
    """
    Загружает изображения для указанной категории
    Возвращает список файлов
    """
    category_path = os.path.join('/home', category)
    if os.path.exists(category_path) and os.path.isdir(category_path):
        return [f for f in os.listdir(category_path) if os.path.isfile(os.path.join(category_path, f))]
    else:
        print(f"Папка для категории '{category}' не найдена")
        return []
@bot.message_handler(commands=['mem'])
def send_photo_url(message):
    # Загружаем все мемы (без категории)
    all_memes = load_category_images('/home/mems')
    if not all_memes:
        bot.reply_to(message, "Нет доступных мемов!")
        return

    # Выбираем мем с учётом редкости
    selected_file = weighted_choice(all_memes, MEME_RARITY_MAP, MEME_RARE_WEIGHTS)
    if selected_file:
        file_path = os.path.join('/home', '/home/mems', selected_file)
        with open(file_path, 'rb') as f:
            bot.send_photo(message.chat.id, f)
    else:
        bot.reply_to(message, "Не удалось выбрать мем!")
@bot.message_handler(commands=['animals'])
def send_animals_meme(message):
    # Загружаем мемы с животными
    animal_memes = load_category_images('/home/animals')
    if not animal_memes:
        bot.reply_to(message, "Нет мемов с животными!")
        return

    # Выбираем мем с животными с учётом редкости
    selected_file = weighted_choice(animal_memes, MEME_RARITY_MAP, MEME_RARE_WEIGHTS)
    if selected_file:
        file_path = os.path.join('/home', '/home/animals', selected_file)
        with open(file_path, 'rb') as f:
            bot.send_photo(message.chat.id, f)
            # Показываем редкость выбранного мема
            rarity = MEME_RARITY_MAP.get(selected_file, 'common')
            rarity_text = {
                'common': 'Обычный мем',
                'uncommon': 'Необычный мем',
                'rare': 'Редкий мем!',
                'epic': 'Эпический мем!!!'
            }.get(rarity, 'Мем')
            bot.send_message(message.chat.id, rarity_text)
    else:
        bot.reply_to(message, "Не удалось выбрать мем с животным!")

def get_duck_image_url():
      url = 'https://api.waifu.im/random/?category=genshin'
      res = requests.get(url)
      data = res.json()
      return data['url']


@bot.message_handler(commands=['duck'])
def duck(message):
    '''По команде duck вызывает функцию get_duck_image_url и отправляет URL изображения утки'''
    image_url = get_duck_image_url()
    bot.reply_to(message, image_url)

@bot.message_handler(commands=['image'])
def send_photo_url(message):
    # Используйте корректный URL с правильным протоколом
    with open('/home/7db1cbd86f633f441295fd5919bc80c1.png', 'rb') as f:
        bot.send_photo(message.chat.id, f)

#@bot.message_handler(commands=['mem'])
#def send_photo_url(message):
    # Используйте корректный URL с правильным протоколом
    #file = random.choice(img)
    #with open(f'/home/images/{file}', 'rb') as f:
        #bot.send_photo(message.chat.id, f)

@bot.message_handler(commands=['hello'])
def send_hello(message):
    bot.reply_to(message, "Привет! Как дела?")

@bot.message_handler(commands=['bye'])
def send_bye(message):
    bot.reply_to(message, "Пока! Удачи!")

@bot.message_handler(commands=['emodji'])
def send_bye(message):
    bot.reply_to(message, r_emojie())

 # Обработчик команды '/heh'
@bot.message_handler(commands=['heh'])
def send_heh(message):
    count_heh = int(message.text.split()[1]) if len(message.text.split()) > 1 else 5
    bot.reply_to(message, "he" * count_heh)

def send_and_delete_sticker(chat_id, sticker_id, duration):
    # Отправляем стикер
    sent_message = bot.send_sticker(chat_id, sticker_id)
    message_id = sent_message.message_id

    # Задерживаем отправку на заданное время
    time.sleep(duration)

    # Удаляем сообщение
    bot.delete_message(chat_id, message_id)

@bot.message_handler(commands=['heta'])
def send_bye(message):
    bot.reply_to(message,"Подбрасыва монетку..." )
    send_and_delete_sticker(chat_id=7376229459, sticker_id="CAACAgIAAxkBAAERRLdqEQ3_hHxB2Cyn2xCZr3Q9oU0-PAAC6XsAAlIn8UkcYZAWJ44MtDsE", duration=3)
    bot.reply_to(message, ran_coin())

@bot.message_handler(commands=['password'])
def send_pass(message):
    bot.reply_to(message, gen_pass(20))
@bot.message_handler(commands=['send'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Сайт kondland", url='https://learn.kodland.org/ru/my-courses/1740/at-class')
    markup.add(button1)
    bot.send_message(message.chat.id, "Привет, {0.first_name}! Нажми на кнопку и перейди на сайт".format(message.from_user), reply_markup=markup)

def beep(chat_id) -> None:
    """Send the beep message."""
    try:
        bot.send_message(chat_id, text='Beep!')
    except Exception as e:
        print(f"Error sending beep to {chat_id}: {e}")

def run_scheduler():
    """Отдельный поток для планировщика."""
    while True:
        try:
            schedule.run_pending()
        except Exception as e:
            print(f"Scheduler error: {e}")
        time.sleep(1)

@bot.message_handler(commands=['set'])
def set_timer(message):
    args = message.text.split()
    if len(args) > 1 and args[1].isdigit():
        sec = int(args[1])
        # Валидация: ограничение от 1 до 3600 секунд (1 час)
        if 1 <= sec <= 3600:
            # Удаляем старый таймер, если есть
            if message.chat.id in active_timers:
                schedule.clear(message.chat.id)
            # Устанавливаем новый таймер
            job = schedule.every(sec).seconds.do(beep, message.chat.id).tag(message.chat.id)
            active_timers[message.chat.id] = job
            bot.reply_to(message, f"Timer set for {sec} seconds!")
        else:
            bot.reply_to(message, 'Please use a value between 1 and 3600 seconds.')
    else:
        bot.reply_to(message, 'Usage: /set <seconds>')

@bot.message_handler(commands=['unset'])
def unset_timer(message):
    schedule.clear(message.chat.id)
    if message.chat.id in active_timers:
        del active_timers[message.chat.id]
    bot.reply_to(message, 'Timer cancelled!')

@bot.message_handler(content_types=['text', 'photo', 'files'])
def give_photo(message):
    if message.content_type == 'photo':
        bot.send_message(message.chat.id, text="Интересно!")



if __name__ == '__main__':
    # Запускаем планировщик в отдельном потоке
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    # Запускаем бота
    bot.infinity_polling()



