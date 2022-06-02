import pytesseract
from textblob import TextBlob
from PIL import Image
from config import token
import os

import telebot
bot = telebot.TeleBot(token, parse_mode=None)

# pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def parse_text_from_image(message):

    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    temp_file_name = 'photos/'+message.document.file_name
    with open(temp_file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    custom_config = r'--oem 3 --psm 1'
    img = Image.open(temp_file_name)


    text_image = pytesseract.image_to_string(img, lang='rus+eng', config=custom_config)

    text_image_new = ""
    for i in range(len(text_image)):
        if text_image[i] == "|":
            text_image_new += "I"
        else:
            text_image_new += text_image[i]

    os.remove(temp_file_name)

    bot.send_message(message.chat.id, f"Готово! Ваш текст:\n")
    bot.send_message(message.chat.id, f"{TextBlob(text_image_new).correct()}")


@bot.message_handler(content_types=['document'])
def parse_text(message):
    parse_text_from_image(message)



bot.polling(none_stop=True)