from discord.ext import commands, tasks
import os
from selenium import webdriver
from bs4 import BeautifulSoup
import datetime
from itertools import cycle
import discord
import requests

# константы
bot = commands.Bot(command_prefix='>>')
bot.remove_command('help')
dates = [4, 8, 12, 16, 20, 24, 28]
status = cycle(['Хочешь меня на свой сервер?', 'Тебе к retro#9860', 'Введи >>help, чтобы узнать что я умею'])
id_for_notif = {700852534398419074: {'role': '<@&700079783836385428>',
                                     'text': 'Собираемся на грузы - *"сейчас будет рп"* (с) Карандаш. Сбор - 7-ая амунация. Сейчас в игре'},
               699631174519357571:  {'role': '<@&699626003760414761>',
                                     'text': 'Собираемся на грузы, баласята, в 01:00. Сбор - 6-ая амунация. Сейчас в игре'}}
flag = False
exp_table = ['08:32', '11:56', '15:20', '18:44', '22:08', '01:32', '04:56']

help_text = '''```Команды:
    >>help - справка
    >>calc_time - расчёт времени
        Аргументы:
            -nights [время на сервере(например: 06:00, 17:00)] [время по МСК]
            -exp [время запуска сервера(по МСК)]
    >>ghetto_stats - статистика захватов территорий гетто
    >>find - найти недвижимость
        Аргументы(Что-то одно):
            [Имя или фамилия владельца, название, цена(знак доллара перед суммой, сотни отделять запятыми), адрес] ```'''


# вспомогательные функции
def dead_time():
    try:
        code = requests.get('https://dednet.ru/servers').text
        soup = BeautifulSoup(code, features='lxml')
        string = soup.find('div', class_='col s12')
        time_on_ded = str(string.find_next('label'))[7:-8].split(' ')[2].split(':')
        hours = time_on_ded[0]
        minutes = time_on_ded[1]
    except Exception as e:
        print("Error! " + str(e))
        hours = 0
        minutes = 0
    return hours, minutes


def collect():
    code = requests.get('https://dednet.ru/map').text
    code = code.split('\n')
    not_sorted_table = code[-12].split(';')
    code.clear()
    sorted_table = []

    for i in range(len(not_sorted_table)):
        not_sorted_table[i] = not_sorted_table[i][
                              not_sorted_table[i].rfind('(') + 2:not_sorted_table[i].rfind(')') - 1]
        not_sorted_table[i] = not_sorted_table[i].replace('<span class=\\"green-text\\">', '')
        not_sorted_table[i] = not_sorted_table[i].replace('</span>', '')
    for i in not_sorted_table:
        if i[i.find('<b>'):i.find('</b>')]:
            sorted_table.append({'Название': i[i.find('<b>') + 3:i.find('</b>')],
                                 'Владелец': i[i.find('Владелец: '):i.find('<br>Цена:')][10:],
                                 'Цена': i[i.find('Цена: '):].split('<br>')[0][6:],
                                 'Адрес': i[i.find('Цена: '):].split('<br>')[1][7:]})
    return sorted_table


def instr(n):
    if len(str(n)) == 1:
        return f'0{n}'
    else:
        return f'{n}'


def difer(list1, list2):
    res = []
    for i in list1:
        if i not in list2:
            res.append(i)
    for i in list2:
        if i not in list1:
            res.append(i)
    return res


def collect_for_exp():
    code = requests.get('https://dednet.ru/map?pfrom=1&pto=100000000&onlyFree=on').text
    code = code.split('\n')
    not_sorted_table = code[-12].split(';')
    code.clear()
    sorted_table = []

    for i in range(len(not_sorted_table)):
        not_sorted_table[i] = not_sorted_table[i][not_sorted_table[i].rfind('(') + 2:not_sorted_table[i].rfind(')') - 1]
    for i in not_sorted_table:
        if i[i.find('<b>'):i.find('</b>')]:
            sorted_table.append([i[i.find('<b>') + 3:i.find('</b>')],
                                 i[i.find('Цена: '):].split('<br>')[0],
                                 i[i.find('Цена: '):].split('<br>')[1]])
    return sorted_table


data = collect_for_exp().copy()


# Команды бота
@bot.command(pass_context=True)
async def calc_time(ctx, *arg):
    if arg:
        arg = list(arg)
        if arg[0] == '-nights':
            if len(arg) == 3 and int(arg[1].split(':')[1]) == 0:
                time_on_server = [int(arg[1].split(':')[0]), int(arg[1].split(':')[1])]
                time = [int(arg[2].split(':')[0]), int(arg[2].split(':')[1])]
                if time_on_server[0] % 2 == 0:
                    deltatime = ((22 - time_on_server[0]) // 2) * 17
                    h = deltatime // 60
                    m = deltatime % 60
                    if time[0] + h > 24:
                        time[0] = time[0] + h - 24
                    else:
                        time[0] += h
                    if time[1] + m > 60:
                        time[0] = time[0] + 1
                        time[1] = time[1] + m - 60
                    else:
                        time[1] += m
                    time_on_server = [22, 0]
                else:
                    deltatime = ((23 - time_on_server[0]) // 2) * 17
                    h = deltatime // 60
                    m = deltatime % 60
                    if time[0] + h > 24:
                        time[0] = time[0] + h - 24
                    else:
                        time[0] += h
                    if time[1] + m > 60:
                        time[0] = time[0] + 1
                        time[1] = time[1] + m - 60
                    else:
                        time[1] += m
                    time_on_server = [23, 0]

                time_table = [f'{instr(time_on_server[0])}:{instr(time_on_server[1])}:']
                for i in range(8):
                    time_table.append(f'{i + 1}. {instr(time[0])}:{instr(time[1])}')
                    if time[1] + 24 >= 60:
                        if time[0] + 4 >= 24:
                            time[0] = time[0] + 4 - 24
                        else:
                            time[0] += 4
                            time[1] = time[1] + 24 - 60
                    else:
                        time[1] += 24
                        if time[0] + 3 >= 24:
                            time[0] = time[0] + 3 - 24
                        else:
                            time[0] += 3
                await ctx.send('\n'.join(time_table))
            else:
                await ctx.send('Что-то не то :thinking:\nДля получения справки о командах введите: >>help')

        elif arg[0] == '-exp':
            if len(arg) == 2:
                time = [int(arg[1].split(':')[0]), int(arg[1].split(':')[1])]
                time_table = []
                for i in range(8):
                    time_table.append(f'{instr(time[0])}:{instr(time[1])}')
                    if time[1] + 24 >= 60:
                        if time[0] + 4 >= 24:
                            time[0] = time[0] + 4 - 24
                        else:
                            time[0] += 4
                            time[1] = time[1] + 24 - 60
                    else:
                        time[1] += 24
                        if time[0] + 3 >= 24:
                            time[0] = time[0] + 3 - 24
                        else:
                            time[0] += 3
                await ctx.send('\n'.join(time_table))
            else:
                await ctx.send('Что-то не то :thinking:\nДля получения справки о командах введите: >>help')
        else:
            await ctx.send('Что-то не то :thinking:\nДля получения справки о командах введите: >>help')
    else:
        await ctx.send('Что-то не то :thinking:\nДля получения справки о командах введите: >>help')


@bot.command()
async def ghetto_stats(ctx):
    GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google-chrome-stable'
    CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.binary_location = GOOGLE_CHROME_PATH
    browser = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=chrome_options)
    browser.get('https://dednet.ru/map')
    code = browser.page_source
    browser.close()

    soup = BeautifulSoup(code, features='lxml')
    page = soup.find('svg', class_='leaflet-zoom-animated')
    all_territories = page.find_all_next('g')
    ghetto_table = []
    for territory in all_territories:
        args = str(territory.find('path')).split()
        color = ''
        for arg in args:
            if arg.startswith('fill='):
                color = arg
        ghetto_table.append(color)
    colors_ghetto = {'fill="#673AB7"': 'The Ballas Gang',
                     'fill="#f44336"': 'Bloods',
                     'fill="#4CAF50"': 'The Families',
                     'fill="#2196F3"': 'Marabunta Grande',
                     'fill="#FFEB3B"': 'Los Santos Vagos'}
    ghetto_stats = {'The Ballas Gang': 0, 'Bloods': 0, 'The Families': 0, 'Marabunta Grande': 0, 'Los Santos Vagos': 0}
    for i in ghetto_table:
        if i in colors_ghetto.keys():
            ghetto_stats[colors_ghetto[i]] += 1
    string = ''
    for band, amount in ghetto_stats.items():
        string += f'{band}: {amount}\n'
    await ctx.send(string)


@bot.command()
async def help(ctx):
    global help_text
    await ctx.send(help_text)


@bot.command(pass_context=True)
async def find(ctx, *arg):
    arg = ' '.join(list(arg))
    table = collect()
    property_ = []
    for i in table:
        for j in i.items():
            if not arg.isalpha():
                if arg.lower() == j[1].lower():
                    property_.append(i)
            elif arg.lower() in j[1].lower():
                property_.append(i)
    if len(property_) == 0:
        await ctx.send(
            'Увы, я ничего не нашёл.')
    else:
        for i in property_:
            await ctx.send(
                f'```\n{i["Название"]}\nВладелец: {i["Владелец"]}\nЦена: {i["Цена"]}\nАдрес: {i["Адрес"]}```')


# Цикличные задачи бота на занем плане
@tasks.loop(seconds=60)
async def notifications():
    now = datetime.datetime.utcnow()
    day = now.date().day
    hour = now.time().hour + 3
    minute = now.time().minute
    if day in dates and hour == 19 and minute == 30:
        for i, j in id_for_notif.items():
            channel = bot.get_channel(i)
            await channel.send(f'''{j['role']}
 Йоу, птичка напела, что через 30 минут доставят грузовик "Pounder" с очень вкусным грузом. Вооружайтесь, закупайте броники.''')


@tasks.loop(seconds=30)
async def notifications2():
    global flag, id_for_notif
    time_ = dead_time()
    if time_:
        if time_[0] == '22' and not flag:
            flag = True
            for i, j in id_for_notif.items():
                channel = bot.get_channel(i)
                await channel.send(f'''{j['role']} {j['text']} {instr(time_[0])}:{instr(time_[1])}''')
        elif time_[0] != '22':
            flag = False


@tasks.loop(seconds=5)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


@tasks.loop(seconds=30)
async def notifications3():
    global data
    new_data = collect_for_exp().copy()
    if len(new_data):
        channel = bot.get_channel(707282293924036679)
        if len(data) < len(new_data):
            for i in difer(data, new_data):
                await channel.send(f'<@&712655260266790912>\n```{i[0]}\n{i[1]}\n{i[2]}```')
        data = new_data.copy()


@tasks.loop(seconds=60)
async def notifications4():
    global exp_table
    now = datetime.datetime.utcnow()
    hour = now.time().hour
    minute = now.time().minute
    channel = bot.get_channel(707282293924036679)
    if minute + 5 < 60:
        if hour + 3 < 24:
            time_ = f'{instr(hour + 3)}:{instr(minute + 5)}'
            if time_ in exp_table:
                await channel.send(f'<@&712655260266790912> слёт через 5 минут')
        else:
            time_ = f'{instr(hour + 3 - 24)}:{instr(minute + 5)}'
            if time_ in exp_table:
                await channel.send(f'<@&712655260266790912> слёт через 5 минут')
    else:
        if hour + 4 < 24:
            time_ = f'{instr(hour + 4)}:{instr(minute + 5 - 60)}'
            if time_ in exp_table:
                await channel.send(f'<@&712655260266790912> слёт через 5 минут')
        else:
            time_ = f'{instr(hour + 4 - 24)}:{instr(minute + 5 - 60)}'
            if time_ in exp_table:
                await channel.send(f'<@&712655260266790912> слёт через 5 минут')
    print(time_)


# Логирование
@bot.event
async def on_ready():
    print('We are in the system!')
    print(f'User: {bot.user.name}')
    print('Starting background tasks...')
    try:
        change_status.start()
        notifications.start()
        notifications2.start()
        notifications3.start()
        notifications4.start()
    except Exception as e:
        print("Error! " + str(e))
    else:
        print('Success!')

# Запуск бота
bot.run(os.environ.get('BOT_TOKEN'))
