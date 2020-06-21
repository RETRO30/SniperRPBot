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
dates_paunder = [4, 8, 12, 16, 20, 24, 28]
dates_bizwars = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
whitelist = [693811598338555944, 700064448911507456, 717732783753134100]
blacklist = [580478163344162819, 723656787089424406, 723559013035540540, 305584796946530304]
status = cycle(['Хочешь меня на свой сервер?', 'Тебе к retro#9860', 'Введи >>help, чтобы узнать что я умею'])
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
            [Имя или фамилия владельца, название, цена(знак доллара перед суммой, сотни отделять запятыми), адрес]
    >>deathtime - время на сервере(не очень точное)
    >>isonline - проверить есть ли игрок онлайн
        Аргументы(Что-то одно):
                [Имя Фамилия]```'''


# вспомогательные функции
def dead_time():
    try:
        code = requests.get('https://dednet.ru/servers').text
        soup = BeautifulSoup(code, features='lxml')
        string = soup.find('div', class_='col s12')
        time_on_ded = str(string.find_next('label'))[7:-8].split(' ')[2].split(':')
        hours = time_on_ded[0]
        minutes = time_on_ded[1]
        restart = False
    except Exception as e:
        print("Error! " + str(e))
        hours = 0
        minutes = 0
        restart = True
    return hours, minutes, restart


def online():
    code = requests.get('https://dednet.ru/servers').text
    soup = BeautifulSoup(code, features='lxml')
    table = soup.find('div', class_='col s12', id='monitoring')
    rows = table.find_all('tr')[1:]
    online_players = []
    for i in rows:
        if i:
            online_players.append(str(i).split('\n')[2].split('>')[1].split('<')[0])
    clean_online_players = []
    for i in online_players:
        if i:
            clean_online_players.append(i)
    return clean_online_players


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
    try:
        if ctx.message.guild.id in whitelist and ctx.message.author.id not in blacklist:
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
        else:
            await ctx.send('Похоже сервер не был добавлен в мой whitelist или вы были внесены blacklist :(')
    except Exception:
        await ctx.send('Я не умею отвечать в лс :(')


@bot.command()
async def ghetto_stats(ctx):
    try:
        if ctx.message.guild.id in whitelist and ctx.message.author.id not in blacklist:
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
            ghetto_stats = {'The Ballas Gang': 0, 'Bloods': 0, 'The Families': 0, 'Marabunta Grande': 0,
                            'Los Santos Vagos': 0}
            for i in ghetto_table:
                if i in colors_ghetto.keys():
                    ghetto_stats[colors_ghetto[i]] += 1
            string = ''
            for band, amount in ghetto_stats.items():
                string += f'{band}: {amount}\n'
            await ctx.send(string)
        else:
            await ctx.send('Похоже сервер не был добавлен в мой whitelist или вы были внесены blacklist :(')
    except Exception:
        await ctx.send('Я не умею отвечать в лс :(')


@bot.command()
async def help(ctx):
    try:
        if ctx.message.guild.id in whitelist and ctx.message.author.id not in blacklist:
            global help_text
            await ctx.send(help_text)
        else:
            await ctx.send('Похоже сервер не был добавлен в мой whitelist или вы были внесены blacklist :(')
    except Exception:
        await ctx.send('Я не умею отвечать в лс :(')


@bot.command()
async def deathtime(ctx):
    try:
        if ctx.message.guild.id in whitelist and ctx.message.author.id not in blacklist:
            time_ = dead_time()
            if time_[2]:
                await ctx.send('Что-то не так')
            else:
                await ctx.send(f'Времея в игре: {time_[0]}:{time_[1]}')
        else:
            await ctx.send('Похоже сервер не был добавлен в мой whitelist или вы были внесены blacklist :(')
    except Exception:
        await ctx.send('Я не умею отвечать в лс :(')

@bot.command(pass_context=True)
async def find(ctx, *arg):
    try:
        if ctx.message.guild.id in whitelist and ctx.message.author.id not in blacklist:
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
                    embed = discord.Embed(title=i["Название"], description=f'Владелец: {i["Владелец"]}\nЦена: {i["Цена"]}\nАдрес: {i["Адрес"]}')
                    await ctx.send(embed=embed)
        else:
            await ctx.send('Похоже сервер не был добавлен в мой whitelist или вы были внесены blacklist :(')
    except Exception:
        await ctx.send('Я не умею отвечать в лс :(')


@bot.command(pass_context=True)
async def isonline(ctx, *arg):
    try:
        if ctx.message.guild.id in whitelist and ctx.message.author.id not in blacklist:
            try:
                name = ' '.join(arg)
                players = online()
                if name in players:
                    await ctx.send(f'{name} онлайн!')
                else:
                    await ctx.send(f'{name} не онлайн!')
            except Exception as e:
                print("Error! " + str(e))
                await ctx.send('Что-то не так')
        else:
            await ctx.send('Похоже сервер не был добавлен в мой whitelist или вы были внесены blacklist :(')
    except Exception:
        await ctx.send('Я не умею отвечать в лс :(')


# Цикличные задачи бота на занем плане
@tasks.loop(seconds=60)
async def notifications():
    now = datetime.datetime.utcnow()
    day = now.date().day
    hour = now.time().hour + 3
    minute = now.time().minute
    # ghosts
    channel = bot.get_channel(717735581957881886)
    if day in dates_paunder and hour == 19 and minute == 30:
        await channel.send(
            '<@&717749640052604928> Йоу, птичка напела, что через 30 минут доставят грузовик "Pounder" с очень вкусным грузом.')

    # yakuza
    channel = bot.get_channel(700852534398419074)
    if (day in dates_bizwars or day in dates_paunder) and hour == 18 and minute == 30:
        await channel.send('<@&700079783836385428> начинаем отписывать в <#714139823606333441>')
    if hour == 19 and minute == 30:
        if day in [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]:
            await channel.send('<@&700079783836385428> собираемся на мулы сразу после бизвара. Место сбора 7-ая амунация.')
        else:
            await channel.send('<@&700079783836385428> собираемся на мулы в 20:00 по МСК. Сбор 7-ая амунация. Пишите в <#714139823606333441> что вам выдать.')



@tasks.loop(seconds=30)
async def notifications2():
    global flag, id_for_notif
    time_ = dead_time()
    if time_:
        if time_[0] == '22' and not flag:
            flag = True

            # ghosts
            channel = bot.get_channel(717735581957881886)
            await channel.send(f'''<@&717749640052604928> Собираемся на грузы. Место сбора - кольцо Миррор-Парка. Сейчас в игре {instr(time_[0])}:{instr(time_[1])}''')

            # yakuza
            channel = bot.get_channel(700852534398419074)
            await channel.send(f'''<@&700079783836385428> 'Собираемся на грузы - *"сейчас будет рп"* (с) Карандаш. Сбор - 7-ая амунация. Сейчас в игре {instr(time_[0])}:{instr(time_[1])}''')

        elif time_[0] != '22':
            flag = False


@tasks.loop(seconds=8)
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
                embed = discord.Embed(title=i[0], description=f'{i[1]}\n{i[2]}')
                await channel.send(f'<@&712655260266790912>', embed=embed)
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
