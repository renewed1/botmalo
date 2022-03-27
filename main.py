import telebot
import os

CHAT_ID=os.environ["CHAT_ID"]
TOKEN = os.environ["TOKEN"]
text_msg='Здравствуйте, {0}.\n\nМы готовы принять Ваш заказ.\nДля удобства отправьте его по форме ниже:\n\n1. Ваш заказ.\n2. Имя\n3. Время, через которое вы хотите забрать заказ.\n4. В кофейне или с собой.\n\nНапример:\n\n1. Капучинка 0.2 на миндальном. И десертик хочу. Можно фото витрины?\n2. Для Катерины.\n3. К 15:45\n4. В кофейне, потому что это экологично и не надо тратить бумажный стакан🌱'
def findChatId(text, caption):
    if(text!=None):
        res=text.split('(#ID')
    else:
        res=caption.split('(#ID')
    return res[1].replace(')','')
# Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN)
# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, text_msg.format(m.from_user.first_name))

# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(m):
    if(int(CHAT_ID)!=m.chat.id):
        bot.send_message(int(CHAT_ID),text='{0}\n\n[{1} {2}](tg://user?id={3}) (#ID{4})'.format(m.text,m.from_user.first_name,m.from_user.last_name,m.from_user.id,m.chat.id),parse_mode="Markdown")
    else:
        if(m.reply_to_message!=None):
            bot.send_message(findChatId(m.reply_to_message.text, m.reply_to_message.caption),text=m.text)
        else:
            bot.send_message(int(CHAT_ID),text='Необходимо переслать сообщение пользователя, для которого предназначен ответ')


@bot.message_handler(content_types=["photo"])
def handle_photo(m):
    if(int(CHAT_ID)==m.chat.id):
        if(m.reply_to_message!=None):
            if(m.caption!=None):
                bot.send_photo(chat_id=findChatId(m.reply_to_message.text, m.reply_to_message.caption),photo=m.photo[0].file_id, caption=m.caption)
            else:
                bot.send_photo(chat_id=findChatId(m.reply_to_message.text, m.reply_to_message.caption),photo=m.photo[0].file_id)
        else:
            bot.send_message(int(CHAT_ID),text='Необходимо переслать сообщение пользователя, для которого предназначен ответ')
    else:
        if(m.caption!=None):
            bot.send_photo(int(CHAT_ID),photo=m.photo[0].file_id,caption='{0}\n\n[{1} {2}](tg://user?id={3}) (#ID{4})'.format(m.caption,m.from_user.first_name,m.from_user.last_name,m.from_user.id,m.chat.id),parse_mode="Markdown")
        else:
            bot.send_photo(int(CHAT_ID),photo=m.photo[0].file_id,caption='[{0} {1}](tg://user?id={2}) (#ID{3})'.format(m.from_user.first_name,m.from_user.last_name,m.from_user.id,m.chat.id),parse_mode="Markdown")

# Запускаем бота
bot.polling(none_stop=True, interval=1)