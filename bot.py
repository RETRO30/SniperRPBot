from discord.ext import commands
import os

bot = commands.Bot(command_prefix='>>')


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


@bot.command(pass_context=True)
async def calctime(ctx, *arg):
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
            for i in time_table:
                await ctx.send(i)
        else:
            await ctx.send('Что-то не то :thinking:\nДля получения справки о командах введите: >>showhelp')
    else:
        await ctx.send('Что-то не то :thinking:\nДля получения справки о командах введите: >>showhelp')

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
            for i in time_table:
                await ctx.send(i)
        else:
            await ctx.send('Что-то не то :thinking:\nДля получения справки о командах введите: >>showhelp')
    else:
        await ctx.send('Что-то не то :thinking:\nДля получения справки о командах введите: >>showhelp')


@bot.command()
async def showhelp(ctx):
    await ctx.send('Команды:'
                   '\n    >>showhelp - справка'
                   '\n    >>calctime - расчёт времени'
                   '\n        Вариации:'
                   '\n            -nights [время первой ночи(когда в игре 23:00)]'
                   '\n            -exp [время запуска сервера(по МСК)]')



bot.run(os.environ.get('BOT_TOKEN'))
