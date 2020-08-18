from discord.ext import commands, tasks
import os
from selenium import webdriver
from bs4 import BeautifulSoup
import datetime
from itertools import cycle
import discord
import requests
from discord.ext.commands import CommandNotFound

# константы
bot = commands.Bot(command_prefix='$')
bot.remove_command('help')
dates_paunder = [4, 8, 12, 16, 20, 24, 28]
dates_bizwars = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
whitelist = ['retro', 722774766230175784, 'Apelsin', 731047569114791976, 'ukrain mafia', 738791491585048736, 'gpra', 740059477801173174]
blacklist = [580478163344162819, 612074024117469184, 305584796946530304, 304853315177545728, 168770786570534912,
             353910133010464769, 365094849961132032, 304853315177545728, 530347941609734145, 480114691004170250]
status = cycle(['Хочешь меня на свой сервер?', 'Тебе к retro#9860', 'Введи $help, чтобы узнать что я умею'])
flag = False
exp_table = ['08:32', '11:56', '15:20', '18:44', '22:08', '01:32', '04:56']

roles = {'☮️': 712655260266790912}

help_embed = discord.Embed(title='BOT BY RETRO', description='Йоу, быдло!')
help_embed.add_field(name='$help', value='вызвать это сообщение')
help_embed.add_field(name='$ghetto', value='статистика захватов территорий гетто')
help_embed.add_field(name='$find [параметр поиска]', value='найти недвижимость')
help_embed.add_field(name='$deathtime', value='время на сервере(не очень точное)')
help_embed.add_field(name='$isonline', value='проверить есть ли игрок онлайн')
help_embed.add_field(name='$carinfo [название тс]', value='информация о тс(цена и наличе в магазине)')
help_embed.add_field(name='$info [тег пользователя]',
                     value='информация о пользователе, чтобы увидеть информаицию о пользователе нужно его тегнуть, без тега выведется информация о авторе')
help_embed.add_field(name='$top_money', value='отсортированная таблица богачей, принемает два значения - кол-во денег(от и до), если значение одно, второе принемается за ноль')
help_embed.set_thumbnail(
    url='https://cdn.discordapp.com/avatars/706272473288671303/ee27442b2391ed48ae232d1404f03d29.webp?size=128')


# вспомогательные функции
def dead_time():
    try:
        code = requests.get('https://dednet.ru/servers').text
        soup = BeautifulSoup(code, features='lxml')
        string = soup.find('div', class_='col s12')
        time_on_ded = str(string.find('label'))[7:-8].split(' ')[2].split(':')
        date_on_ded = str(string.find('label'))[7:-8].split(' ')[3]
        hours = time_on_ded[0]
        minutes = time_on_ded[1]
        date = date_on_ded
        restart = False
    except Exception as e:
        print("Error! " + str(e))
        hours = 0
        minutes = 0
        date = 0
        restart = True
    return hours, minutes, restart, date


def online():
    code = requests.get('https://dednet.ru/servers').text
    soup = BeautifulSoup(code, features='lxml')
    table = soup.find('div', class_='col s12', id='monitoring')
    rows = table.find_all('tr')[1:]
    online_players = []
    for i in rows:
        if i:
            online_players.append(
                str(i).split('\n')[2].replace('<span class="green-text">', '').replace('<span class="amber-text">',
                                                                                       '').split('>')[1].split('<')[0])
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

def top_money_get():
    code = requests.get('https://dednet.ru/servers').text
    soup = BeautifulSoup(code, features='lxml')
    table = soup.find('div', class_='col s12', id='top-money')
    rows = table.find_all('tr')[1:]
    top_money_players = []
    for i in rows:
        i = str(i).replace('<td>', '').replace('</td>', '').split('\n')
        top_money_players.append([str(i[2]), str(i[3]),  int(str(i[3])[1:].replace(',', ''))])
    return top_money_players


def get_carlist():
    code = requests.get('https://dednet.ru/car-list').text
    soup = BeautifulSoup(code, features='lxml')
    rows = soup.find('div', class_='row')
    table = rows.find_all('div', class_='col s12 l3')
    carlist = {}
    for car in table:
        image = 'https://dednet.ru/' + str(car.find('div', class_='card-image')).split('"')[7]
        name = car.find('span', class_='card-title').text.lower()
        cost = car.find('a', class_='bw-text btn z-depth-0').text
        count = int(car.find('a', class_='bw-text btn z-depth-0 right').text.split()[0].split('/')[0])
        carlist.update({name: {'cost': cost, 'count': count, 'image': image}})
    return carlist


data = collect_for_exp().copy()
data_cars = get_carlist()


# Команды бота
@bot.command(pass_context=True)
async def top_money(ctx, *arg):
    try:
        if ctx.message.channel.id in whitelist and ctx.message.author.id not in blacklist:
                arg = list(arg)
                if len(arg):
                    if len(arg) == 1:
                        from_ = 0
                        to_ = int(arg[0])
                    else:
                        from_ = min(int(arg[0]), int(arg[1]))
                        to_ = max(int(arg[0]), int(arg[1]))
                    players = top_money_get()
                    sorted_players = []
                    for i in players:
                        if from_ <= i[2] <= to_:
                            sorted_players.append(f'{i[0]} - {i[1]}')
                    if sorted_players:
                        await ctx.send('\n'.join(sorted_players))
                    else:
                        await ctx.send('Увы, я ничего не нашёл.')
                else:
                    await ctx.send('Что-то не так :(')
    except Exception:
        await ctx.send('Что-то не так :(')

@bot.command(pass_context=True)
async def calc_time(ctx, *arg):
    try:
        if ctx.message.channel.id in whitelist and ctx.message.author.id not in blacklist:
            if arg:
                arg = list(arg)
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
                    await ctx.send('Что-то не то :thinking:\nДля получения справки о командах введите: $help')
            else:
                await ctx.send('Что-то не то :thinking:\nДля получения справки о командах введите: $help')
        else:
            pass
    except Exception:
        await ctx.send('Что-то не так :(')


@bot.command()
async def ghetto(ctx):
    try:
        if ctx.message.channel.id in whitelist and ctx.message.author.id not in blacklist:
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
            pass
    except Exception as e:
        print(e)
        await ctx.send('Что-то не так :(')


@bot.command()
async def help(ctx):
    try:
        if ctx.message.channel.id in whitelist and ctx.message.author.id not in blacklist:
            global help_embed
            await ctx.send(embed=help_embed)
        else:
            pass
    except Exception:
        await ctx.send('Что-то не так :(')


@bot.command()
async def deathtime(ctx):
    try:
        if ctx.message.channel.id in whitelist and ctx.message.author.id not in blacklist:
            time_ = dead_time()
            if time_[2]:
                await ctx.send('Что-то не так')
            else:
                embed = discord.Embed(title=f'{time_[0]}:{time_[1]}', description=time_[3])
                await ctx.send(embed=embed)
        else:
            pass
    except Exception:
        await ctx.send('Что-то не так :(')


@bot.command(pass_context=True)
async def find(ctx, *arg):
    try:
        if ctx.message.channel.id in whitelist and ctx.message.author.id not in blacklist:
            arg = ' '.join(list(arg))
            if arg.lower() != 'склад' and arg.lower() != 'дом' and arg.lower() != 'нет':
                pass
            else:
                arg = ''
            table = collect()
            players = top_money_get()
            money = ''
            for i in players:
                if i[0].lower() == arg.lower():
                    money = i[1]
            embed = discord.Embed(title='Деньги',
                                  description=money)
            await ctx.send(embed=embed)
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
                    embed = discord.Embed(title=i["Название"],
                                          description=f'Владелец: {i["Владелец"]}\nЦена: {i["Цена"]}\nАдрес: {i["Адрес"]}')
                    await ctx.send(embed=embed)
        else:
            pass
    except Exception:
        await ctx.send('Что-то не так :(')


@bot.command(pass_context=True)
async def info(ctx, *arg):
    try:
        if ctx.message.channel.id in whitelist and ctx.message.author.id not in blacklist:
            arg = list(arg)
            if len(arg) == 0:
                user = ctx.author
            else:
                user = ctx.guild.get_member(int(arg[0][3:-1]))
            name = user.name
            nick = user.nick
            avatar = user.avatar_url
            activity = user.activity
            date_join = user.joined_at.strftime("%A %d-%B-%y %H:%M")
            date_created = user.created_at.strftime("%A %d-%B-%y %H:%M")
            if not activity:
                description = 'Гоняет лысого'
            else:
                description = activity.name
            if nick:
                user_embed = discord.Embed(title=f'{name.upper()}, более известный как {nick.upper()}',
                                           description=description)
            else:
                user_embed = discord.Embed(title=f'{name.upper()}', description=description)
            user_embed.add_field(name='Сидит тут с:', value=date_join)
            user_embed.add_field(name='Вылупился:', value=date_created)
            user_embed.set_image(url=avatar)
            user_embed.set_footer(text='А это его ебало')
            await ctx.send(embed=user_embed)
        else:
            pass
    except Exception:
        await ctx.send('Что-то не так :(')


@bot.command(pass_context=True)
async def carinfo(ctx, *arg):
    if ctx.message.channel.id in whitelist and ctx.message.author.id not in blacklist:
        name = list(arg)[0].lower()
        carlist = get_carlist()
        if name in carlist.keys():
            if carlist[name]["count"] == 0:
                color = discord.Colour.red()
            else:
                color = discord.Colour.green()
            embed = discord.Embed(title=name.upper(),
                                  description=f'{carlist[name]["cost"]}\n В наличии: {str(carlist[name]["count"])}',
                                  colour=color)
            embed.set_image(url=carlist[name]['image'])
            await ctx.send(embed=embed)
        else:
            await ctx.send('Увы, я ничего не нашёл.')
    else:
        pass


@bot.command(pass_context=True)
async def isonline(ctx, *arg):
    try:
        if ctx.message.channel.id in whitelist and ctx.message.author.id not in blacklist:
            try:
                name = ' '.join(arg)
                players = online()
                if name in players:
                    embed = discord.Embed(colour=discord.Colour.green(), title=f'{name} онлайн!')
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(colour=discord.Colour.red(), title=f'{name} не онлайн!')
                    await ctx.send(embed=embed)
            except Exception as e:
                print("Error! " + str(e))
                await ctx.send('Что-то не так :(')
        else:
            pass
    except Exception:
        await ctx.send('Что-то не так :(')


# Цикличные задачи бота на занем плане
@tasks.loop(seconds=60)
async def notifications():
    now = datetime.datetime.utcnow()
    day = now.date().day
    hour = now.time().hour + 3
    minute = now.time().minute

    # Apelsin
    channel = bot.get_channel(732336335356166235)
    if hour == 18 and minute == 30:
        await channel.send('@everyone Через 30 минут начнёт движение колонна грузовиков набитых взрывчаткой C4')
    if hour == 19 and minute == 30 and day in dates_paunder:
        await channel.send('@everyone Через 30 минут появятся паундеры')
    else:
        if hour == 20 and minute == 0:
            await channel.send('@everyone  Через 30 минут появятся мулы.')


@tasks.loop(seconds=30)
async def notifications2():
    global flag, id_for_notif
    time_ = dead_time()
    if time_:
        if time_[0] == '22' and not flag:
            flag = True

            # apelsin
            channel = bot.get_channel(732336335356166235)
            await channel.send(f'''@everyone Скоро грузы. Сейчас в игре {instr(time_[0])}:{instr(time_[1])}''')

            # ukrain mafia
            channel = bot.get_channel(738792481566752871)
            await channel.send(
                f'''<@&739426439417298974> <@&739425880320770150> Скоро грузы, братья. Сейчас в игре {instr(time_[0])}:{instr(time_[1])}''')

        elif time_[0] != '22':
            flag = False


@tasks.loop(seconds=8)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


@tasks.loop(seconds=15)
async def notifications3():
    try:
        global data, data_cars
        channel = bot.get_channel(740139945574006805)
        new_data = collect_for_exp().copy()
        if len(new_data):
            if len(data) < len(new_data):
                for i in difer(data, new_data):
                    info = f'**{i[0]}**\n{i[1]}\n{i[2]}'
                    await channel.send(f'<@&712655260266790912> {info}')
            data = new_data.copy()

        new_data_cars = get_carlist()
        channel = bot.get_channel(740139877743722527)
        for car in data_cars.keys():
            if data_cars[car]['count'] < new_data_cars[car]['count']:
                info = f'**{car.upper()}**\n{new_data_cars[car]["cost"]}\nВ наличии: {str(new_data_cars[car]["count"])} (+{new_data_cars[car]["count"] - data_cars[car]["count"]})'
                embed = discord.Embed()
                embed.set_image(url=new_data_cars[car]['image'])
                if car in ['thrax', 'zentorno', 't20', 'dubsta3', 'nero', 'nero2', 'shotaro']:
                    user = bot.get_guild(693811598338555944).get_member(268053859866247188)
                    await user.send(f'{info}', embed=embed)
                    await channel.send(f'<@&712655260266790912>\n{info}', embed=embed)
                else:
                    await channel.send(f'<@&712655260266790912>\n{info}', embed=embed)
        data_cars = new_data_cars.copy()
    except Exception as e:
        print(e)


@tasks.loop(seconds=60)
async def notifications4():
    global exp_table
    now = datetime.datetime.utcnow()
    hour = now.time().hour
    minute = now.time().minute
    channel = bot.get_channel(733887346898108499)
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


# События

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


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error


@bot.event
async def on_raw_reaction_add(payload):
    try:
        if payload.message_id == 739772302421655584:
            channel = bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            member = discord.utils.get(message.guild.members, id=payload.user_id)
            emoji = str(payload.emoji)
            role = discord.utils.get(message.guild.roles, id=roles[emoji])
            await member.add_roles(role)
    except Exception:
        pass


@bot.event
async def on_raw_reaction_remove(payload):
    try:
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = discord.utils.get(message.guild.members, id=payload.user_id)
        emoji = str(payload.emoji)
        role = discord.utils.get(message.guild.roles, id=roles[emoji])
        await member.remove_roles(role)
    except Exception:
        pass


# Запуск бота
bot.run(os.environ.get('BOT_TOKEN'))
