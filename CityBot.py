import telebot
from random import randint

with open('FileForBot.txt', 'r', encoding='utf-8') as f:
    data = f.read().split('\n')
final = False
used = []
num = 0

bot = telebot.TeleBot('7164977033:AAFQjolFAYAKZKuBnh4GDjH9EG4FR1RrnvU')


@bot.message_handler(commands=['start'])
def start(message):
    global final
    global num
    bot.reply_to(message, "Привет! Я бот для игры в города, напиши первый город и я продолжу \nДля "
                          "получения более подробной информации используйте /help")
    used.clear()
    final = False
    num = 0



@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "/clear — позволяет начать игру с начала\n"
                          "/score — показывает количество названых игроком городов\n"
                          "/used — выводит список названных городов")


@bot.message_handler(commands=['clear'])
def clean(message):
    global final
    global num
    used.clear()
    num = 0
    final = False
    bot.reply_to(message, 'список использованных городов очищен, игра начинается заново')


@bot.message_handler(commands=['score'])
def score(message):
    bot.reply_to(message, 'Игроком названо городов: ' + str(num))


@bot.message_handler(commands=['used'])
def use(message):
    print(used)
    # print(used.sort())
    # print(', '.join(sorted(used)))
    if len(used) == 0:
        bot.reply_to(message, 'Список городов пуст')
    else:
        bot.reply_to(message, ', '.join(sorted(used)))


@bot.message_handler(commands=['stop'])
def stop(message):
    sys.exit(0)

def examination(message, st):
    if st.lower() in [elem.lower() for elem in data]:
        if st not in used:
            print(final)
            if st[0] == final or not final:
                return True
            else:
                bot.reply_to(message, '<<город должен начинаться на "' + final.upper() + '">>')
                return False
        else:
            bot.reply_to(message, '<<город уже был назван>>')
            print(used)
            return False
    else:
        bot.reply_to(message, '<<не является известным городом>>')
        return False


def last_and_initial(st):
    t = []
    for i in range(len(st) - 1, -1, -1):
        if len(t) == 0:
            for elem in [elem.lower() for elem in data]:
                if elem[0] == st[i]:
                    t.append(elem)
        else:
            return st[i + 1]


@bot.message_handler(content_types=['text'])
def texting(message):
    global final
    global num
    s = message.text
    st = s.lower()
    if examination(message, st):  # проверка
        used.append(s)
        num += 1
        final = last_and_initial(st)
        print(final)
        t = []
        for elem in data:
            low_elem = elem.lower()
            if low_elem[0] == final:
                t.append(elem)
        # print(t)
        city = t[randint(0, len(t) - 1)]
        final = last_and_initial(city)
        print(final)
        used.append(city)
        bot.send_message(message.from_user.id, city)

    # bot.send_message(message.from_user.id, message.text)


bot.polling(none_stop=True)