from discord.ext import commands, tasks
from bs4 import BeautifulSoup
from itertools import cycle
from discord.ext.commands import CommandNotFound
import os
import datetime
import discord
import requests
import heroku3
import json

# константы
bot = commands.Bot(command_prefix='$')
bot.remove_command('help')
dates_paunder = [4, 8, 12, 16, 20, 24, 28]
dates_bizwars = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
whitelist = ['retro', 722774766230175784, 720335924042661898, 'gpra', 740059477801173174]
blacklist = []
status = cycle(['Хочешь меня на свой сервер?', 'Тебе к retro#9860', 'Введи $help, чтобы узнать что я умею'])
flag = False
exp_table = ['08:32', '11:56', '15:20', '18:44', '22:08', '01:32', '04:56']

admins = [408605476365008897, 268053859866247188, 356429496410308611, 288612101671354378]

roles = {'🧙‍♂️': 751784325959123015,
         '🚗': 751783971146301470,
         '⛺': 751783634674909185,
         '🏢': 751784103686307840,
         '📦': 751784197986975847}

help_embed = discord.Embed(title='BOT BY RETRO', description='Йоу, быдло!')
help_embed.add_field(name='$help', value='вызвать это сообщение', inline=False)
help_embed.add_field(name='$ghetto [id территории]',
                     value='информация о территории гетто, без аргумента - общая статистка гетто', inline=False)
help_embed.add_field(name='$find [Имя Фамилия]', value='Информация о персонаже', inline=False)
help_embed.add_field(name='$dedtime', value='время на сервере(не очень точное)', inline=False)
help_embed.add_field(name='$carinfo [название тс]', value='информация о тс(цена и наличе в магазине)', inline=False)
help_embed.add_field(name='$info [тег пользователя]',
                     value='информация о пользователе, чтобы увидеть информаицию о пользователе нужно его тегнуть, без тега выведется информация о авторе',
                     inline=False)
help_embed.add_field(name='$top_money',
                     value='отсортированная таблица богачей, принемает два значения - кол-во денег(от и до), если значение одно, второе принемается за ноль',
                     inline=False)
help_embed.set_thumbnail(
    url='https://cdn.discordapp.com/avatars/706272473288671303/ee27442b2391ed48ae232d1404f03d29.webp?size=128')


# вспомогательные функции
def get_ghetto():
    table = json.loads(requests.get('https://dednet.ru/publicApi?method=getGhettoList').text)
    return table


def get_time():
    try:
        time = json.loads(requests.get('https://dednet.ru/publicApi?method=getDateTime').text)
        hours = time['hour']
        minutes = time['minute']
        date = f'{time["day"]}/{time["month"]}/{time["year"]}'
        restart = False
    except Exception as e:
        print("Error! " + str(e))
        hours = 0
        minutes = 0
        date = 0
        restart = True
    return hours, minutes, restart, date


def isonline(name):
    code = json.loads(requests.get('https://dednet.ru/publicApi?method=getOnline').text)
    flag = False
    for i in code:
        if i['name'] == name:
            flag = True
    return flag


def get_houses():
    table = json.loads(requests.get('https://dednet.ru/publicApi?method=getHouses').text)
    return table


def get_user_info(name):
    table = json.loads(requests.get(
        f'https://dednet.ru/publicApi?method=getUserInfo&name={name.split()[0].lower()}%20{name.split()[1].lower()}').text)
    return table


def get_business():
    table = json.loads(requests.get('https://dednet.ru/publicApi?method=getBusiness').text)
    return table


def get_business_for_exp():
    table = json.loads(requests.get('https://dednet.ru/publicApi?method=getBusiness').text)
    table = list(filter(lambda x: not x['is_buy'], table))
    return table


def get_yachts():
    table = json.loads(requests.get('https://dednet.ru/publicApi?method=getYachts').text)
    return table


def get_stocks():
    table = json.loads(requests.get('https://dednet.ru/publicApi?method=getStocks').text)
    return table


def get_stocks_for_exp():
    table = json.loads(requests.get('https://dednet.ru/publicApi?method=getStocks').text)
    table = list(filter(lambda x: not x['is_buy'], table))
    return table


def get_condos():
    table = json.loads(requests.get('https://dednet.ru/publicApi?method=getCondos').text)
    return table


def get_condos_for_exp():
    table = json.loads(requests.get('https://dednet.ru/publicApi?method=getCondos').text)
    table = list(filter(lambda x: not x['is_buy'], table))
    return table


def get_person_from_banlist(name):
    table = json.loads(requests.get(
        f'https://dednet.ru/publicApi?method=getBanList&ban_to={name.split()[0].lower()}%20{name.split()[1].lower()}').text)
    return table


def instr(n):
    if len(str(n)) == 1:
        return f'0{n}'
    else:
        return f'{n}'


def inmoney(num):
    return '{:,}'.format(int(num))


def difer(list1, list2):
    res = []
    for i in list1:
        if i not in list2:
            res.append(i)
    for i in list2:
        if i not in list1:
            res.append(i)
    return res


def get_houses_for_exp():
    table = json.loads(requests.get('https://dednet.ru/publicApi?method=getHouses').text)
    table = list(filter(lambda x: not x['is_buy'], table))
    return table


def top_money_get():
    table = json.loads(requests.get('https://dednet.ru/publicApi?method=getUserTopMoney').text)
    for i in table:
        i['money'] = int(i['money'])
    return table


def get_car_image(name):
    table = json.loads(
        requests.get(f'https://dednet.ru/publicApi?method=getVehicleImage&name={name.capitalize()}').text)
    return table


def get_with_name(table, name):
    for i in table:
        if i["name"].lower() == name.lower():
            return dict(i)
    return False


def get_with_owner_name(table, name):
    for i in table:
        if i["owner_name"].lower() == name.lower():
            return dict(i)
    return False


def get_carlist():
    code = requests.get('https://dednet.ru/car-list').text
    soup = BeautifulSoup(code, features='lxml')
    rows = soup.find('div', class_='row')
    table = rows.find_all('div', class_='col s12 l3')
    carlist = {}
    for car in table:
        name = car.find('span', class_='card-title').text.lower()
        cost = car.find('a', class_='bw-text btn z-depth-0').text
        count = int(car.find('a', class_='bw-text btn z-depth-0 right').text.split()[0].split('/')[0])
        all_ = int(car.find('a', class_='bw-text btn z-depth-0 right').text.split()[0].split('/')[1])
        carlist.update({name: {'cost': cost, 'count': count, 'all': all_}})
    return carlist


data_cars = get_carlist().copy()
data_condos = get_condos_for_exp().copy()
data_stocks = get_stocks_for_exp().copy()
data_business = get_business_for_exp().copy()
data_houses = get_houses_for_exp().copy()


# Команды бота
@bot.command()
async def restart(ctx):
    if ctx.message.author.id in admins:
        await ctx.send('Блинб...')
        heroku_conn = heroku3.from_key(os.environ.get('API-KEY'))
        app = heroku_conn.apps()['botbyretro']
        app.restart()


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
                    if from_ <= i['money'] <= to_:
                        money = inmoney(i['money'])
                        sorted_players.append(f'{i["name"]} - ${money}')
                if sorted_players:
                    await ctx.send('\n'.join(sorted_players))
                else:
                    await ctx.send('Увы, я ничего не нашёл.')
            else:
                await ctx.send('Что-то не так :(')
    except Exception as e:
        print(e)
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
            table = get_ghetto()
            The_Ballas_Gang = 0
            The_Families = 0
            Los_Santos_Vagos = 0
            Marabunta_Grande = 0
            Bloods = 0
            for i in table:
                if i['fraction_name'] == 'The Ballas Gang':
                    The_Ballas_Gang += 1
                elif i['fraction_name'] == 'The Families':
                    The_Families += 1
                elif i['fraction_name'] == 'Los Santos Vagos':
                    Los_Santos_Vagos += 1
                elif i['fraction_name'] == 'Marabunta Grande':
                    Marabunta_Grande += 1
                elif i['fraction_name'] == 'Bloods':
                    Bloods += 1
            await ctx.send(
                f'The Ballas Gang: {The_Ballas_Gang}\nBloods: {Bloods}\nThe Families: {The_Families}\nMarabunta Grande: {Marabunta_Grande}\nLos Santos Vagos: {Los_Santos_Vagos}')
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
async def dedtime(ctx):
    try:
        if ctx.message.channel.id in whitelist and ctx.message.author.id not in blacklist:
            time_ = get_time()
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
    if ctx.message.channel.id in whitelist and ctx.message.author.id not in blacklist:
        if arg:
            name_in_str = ' '.join(list(arg))
            house = get_with_owner_name(get_houses(), name_in_str)
            condos = get_with_owner_name(get_condos(), name_in_str)
            business = get_with_owner_name(get_business(), name_in_str)
            stock = get_with_owner_name(get_stocks(), name_in_str)
            stock_type = ''
            if stock:
                if stock['type'] == '0':
                    stock_type = 'Маленький'
                if stock['type'] == '1':
                    stock_type = 'Средний'
                if stock['type'] == '2':
                    stock_type = 'Большой'
            money = get_with_name(top_money_get(), name_in_str)
            online_info = get_user_info(name_in_str)
            yacht = get_with_owner_name(get_yachts(), name_in_str)
            if online_info:
                if isonline(name_in_str):
                    color = discord.Colour.green()
                else:
                    color = discord.Colour.red()

                if money:
                    money = f'Деньги ${inmoney(money["money"])}'
                else:
                    money = ''
                embed = discord.Embed(title=name_in_str.upper(),
                                      description=f'{money}',
                                      color=color)
                if house:
                    embed.add_field(name="Дом",
                                    value=f'Адрес: {house["address"]}, {house["street"]} {house["number"]}\nЦена: {inmoney(house["price"])}',
                                    inline=False)
                if condos:
                    embed.add_field(name="Квартира",
                                    value=f'Адрес: {condos["address"]}, {condos["street"]} {condos["number"]}\nЦена: {inmoney(condos["price"])}',
                                    inline=False)
                if business:
                    embed.add_field(name="Бизнес",
                                    value=f'Название: {business["name"]}\nЦена: {inmoney(business["price"])}',
                                    inline=False)
                if stock:
                    embed.add_field(name="Склад",
                                    value=f'Адрес: {stock["address"]}, {stock["street"]} {stock["number"]}\nЦена: {inmoney(stock["price"])}\nТип: {stock_type}',
                                    inline=False)
                embed.add_field(name="Статистика",
                                value=f'Наиграно часов за сегодня: {online_info["online_day"]}\nВсего наиграно часов: {online_info["online_all"]}\nСредний онлайн: {online_info["online_avg"]}',
                                inline=False)
                if yacht:
                    embed.add_field(name="Яхта",
                                    value=f'Название: {yacht["name"]}\nЦена: {inmoney(yacht["price"])}',
                                    inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send('Увы, я ничего не нашёл')

        else:
            await ctx.send('Что-то не так :(')
    else:
        pass


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
                                  description=f'{carlist[name]["cost"]}\n В наличии: {str(carlist[name]["count"])}/{str(carlist[name]["all"])}',
                                  colour=color)
            embed.set_image(url=get_car_image(name)["img_small"])
            await ctx.send(embed=embed)
        else:
            await ctx.send('Увы, я ничего не нашёл.')
    else:
        pass


# Цикличные задачи бота на занем плане
@tasks.loop(seconds=8)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


@tasks.loop(seconds=15)
async def exp1():
    try:
        global data_cars, data_houses, data_stocks, data_condos, data_business
        new_data_houses = get_houses_for_exp().copy()
        channel = bot.get_channel(740139945574006805)
        if len(data_houses) < len(new_data_houses):
            for house in difer(data_houses, new_data_houses):
                channel.send(
                    f'||<@&751783634674909185>||\n**Дом**\nАдрес: {house["address"]}, {house["street"]} {house["number"]}\nЦена: {inmoney(house["price"])}')
        data_houses = new_data_houses.copy()
        new_data_houses.clear()

        new_data_condos = get_condos_for_exp().copy()
        channel = bot.get_channel(740139945574006805)
        if len(data_condos) < len(new_data_condos):
            for condo in difer(data_condos, new_data_condos):
                channel.send(
                    f'||<@&751783634674909185>||\n**Квартира**\nАдрес: {condo["address"]}, {condo["street"]} {condo["number"]}\nЦена: {inmoney(condo["price"])}')
        data_condos = new_data_condos.copy()
        new_data_condos.clear()

        new_data_stocks = get_stocks_for_exp().copy()
        channel = bot.get_channel(750019039014944918)
        if len(data_stocks) < len(new_data_stocks):
            for stock in difer(data_stocks, new_data_stocks):
                stock_type = ''
                if stock:
                    if stock['type'] == '0':
                        stock_type = 'Маленький'
                    if stock['type'] == '1':
                        stock_type = 'Средний'
                    if stock['type'] == '2':
                        stock_type = 'Большой'
                channel.send(
                    f'||<@&751784197986975847>||\n**Склад**\nАдрес: {stock["address"]}, {stock["street"]} {stock["number"]}\nЦена: {inmoney(stock["price"])}\nТип: {stock_type}')
        data_stocks = new_data_stocks.copy()
        new_data_stocks.clear()

        new_data_business = get_business_for_exp().copy()
        channel = bot.get_channel(750019394750513223)
        if len(data_business) < len(new_data_business):
            for busines in difer(data_condos, new_data_business):
                channel.send(
                    f'||<@&751784103686307840>||\n**Бизнес**Название: {business["name"]}\nЦена: {inmoney(business["price"])}')
        data_business = new_data_business.copy()
        new_data_business.clear()

        new_data_cars = get_carlist().copy()
        channel = bot.get_channel(740139877743722527)
        for car in data_cars.keys():
            if data_cars[car]['count'] < new_data_cars[car]['count']:
                info = f'**{car.upper()}**\n{new_data_cars[car]["cost"]}\nВ наличии: {str(new_data_cars[car]["count"])}/{str(new_data_cars[car]["all"])} (+{new_data_cars[car]["count"] - data_cars[car]["count"]})'
                embed = discord.Embed()
                embed.set_image(url=get_car_image(car)["img_small"])
                if car in ['thrax', 'zentorno', 't20', 'dubsta3', 'nero', 'nero2', 'shotaro', 'zorya']:
                    user = bot.get_guild(693811598338555944).get_member(268053859866247188)
                    await user.send(f'{info}', embed=embed)
                    await channel.send(f'||<@&751783971146301470>||\n{info}', embed=embed)
                else:
                    await channel.send(f'||<@&751783971146301470>||\n{info}', embed=embed)
        data_cars = new_data_cars.copy()
        new_data_cars.clear()
    except Exception as e:
        print(e)


@tasks.loop(seconds=60)
async def exp2():
    global exp_table
    now = datetime.datetime.utcnow()
    hour = now.time().hour
    minute = now.time().minute
    channel = bot.get_channel(733887346898108499)
    if minute + 5 < 60:
        if hour + 3 < 24:
            time_ = f'{instr(hour + 3)}:{instr(minute + 5)}'
            if time_ in exp_table:
                await channel.send(f'||<@&712655260266790912>|| слёт через 5 минут')
        else:
            time_ = f'{instr(hour + 3 - 24)}:{instr(minute + 5)}'
            if time_ in exp_table:
                await channel.send(f'||<@&712655260266790912>|| слёт через 5 минут')
    else:
        if hour + 4 < 24:
            time_ = f'{instr(hour + 4)}:{instr(minute + 5 - 60)}'
            if time_ in exp_table:
                await channel.send(f'||<@&712655260266790912>|| слёт через 5 минут')
        else:
            time_ = f'{instr(hour + 4 - 24)}:{instr(minute + 5 - 60)}'
            if time_ in exp_table:
                await channel.send(f'||<@&712655260266790912>|| слёт через 5 минут')


# События

@bot.event
async def on_ready():
    print('We are in the system!')
    print(f'User: {bot.user.name}')
    print('Starting background tasks...')
    try:
        change_status.start()
        exp1.start()
        exp2.start()
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
