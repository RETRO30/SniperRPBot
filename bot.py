from discord.ext import commands, tasks
import os
from selenium import webdriver
from bs4 import BeautifulSoup
import datetime
from itertools import cycle
import discord
import requests

bot = commands.Bot(command_prefix='>>')
dates = [4, 8, 12, 16, 20, 24, 28]
status = cycle(['БАЛЛАС', 'СОТКА'])


def dead_time():
    code = requests.get('https://dednet.ru/servers').text
    soup = BeautifulSoup(code, features='lxml')
    string = soup.find('div', class_='col s12')
    time_on_ded = str(string.find_next('label'))[7:-8].split(' ')[2].split(':')
    hours = time_on_ded[0]
    minutes = time_on_ded[1]
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
            sorted_table.append([i[i.find('<b>') + 3:i.find('</b>')],
                                 i[i.find('Владелец: '):i.find('<br>Цена:')],
                                 i[i.find('Цена: '):].split('<br>')[0],
                                 i[i.find('Цена: '):].split('<br>')[1]])
    return sorted_table


def instr(n):
    if len(str(n)) == 1:
        return f'0{n}'
    else:
        return f'{n}'


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    notifications.start()
    change_status.start()
    notifications2.start()


@bot.command(pass_context=True)
async def calc_time(ctx, *arg):
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
            await ctx.send('Что-то не то :thinking:\nДля получения справки о командах введите: >>show_help')

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
            await ctx.send('Что-то не то :thinking:\nДля получения справки о командах введите: >>show_help')
    else:
        await ctx.send('Что-то не то :thinking:\nДля получения справки о командах введите: >>show_help')


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
async def show_help(ctx):
    await ctx.send('Команды:'
                   '\n    >>show_help - справка'
                   '\n    >>calc_time - расчёт времени'
                   '\n        Вариации:'
                   '\n            -nights [время на сервере(например: 06:00, 17:00)] [время по МСК]'
                   '\n            -exp [время запуска сервера(по МСК)]'
                   '\n    >>ghetto_stats - статистика захватов территорий гетто')


@bot.command()
async def set_for_notif(ctx):
    global ctx_for_notif
    print('Понял, принял')
    await ctx.send('Понял, принял')
    ctx_for_notif = ctx


@bot.command(pass_context=True)
async def find(ctx, *arg):
    arg = list(arg)
    table = collect()
    property_ = []
    for i in table:
        if f'Владелец: {arg[0]} {arg[1]}' in i:
            property_.append(i)
    if len(property_) == 0:
        await ctx.send(
            'Я не нашёл дом или склад у этого игрока, или вы ввели имя и фамилию не сущестувющего персонажа')
    else:
        for i in property_:
            await ctx.send(f'```\n{i[0]}\n{i[1]}\n{i[2]}\n{i[3]}```')


@tasks.loop(seconds=60)
async def notifications():
    now = datetime.datetime.utcnow()
    day = now.date().day
    hour = now.time().hour + 3
    minute = now.time().minute
    print(f'{day} {hour}:{minute}')
    channel = bot.get_channel(699631174519357571)
    if day in dates and hour == 19 and minute == 30:
        await channel.send(f'''@THE BALLAS GANG
 Йоу, нигеры, птичка напела, что через 30 минут доставят грузовик "Pounder" с очень вкусным грузом. Вооружайтесь, закупайте броники(только в амуниции №6).''')


@tasks.loop(seconds=30)
async def notifications2():
    channel = bot.get_channel(707282177833828443)
    print(f'{instr(dead_time()[0])}:{instr(dead_time()[1])} {flag}')
    if dead_time()[0] == '22' and not flag:
        await channel.send(f'''Быдло, на грузы поедете? Время {instr(dead_time()[0])}:{instr(dead_time()[1])}''')
        flag = True
    if dead_time()[0] != '22':
        flag = False


@tasks.loop(seconds=5)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


bot.run(os.environ.get('BOT_TOKEN'))
