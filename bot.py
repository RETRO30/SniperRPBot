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
                    time[0] += 1
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
            for i in time_table:
                await ctx.send(i)
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
                   '\n    >>help - справка'
                   '\n    >>calctime - расчёт времени'
                   '\n        Вариации:'
                   '\n            -nights [время на сервере(например: 06:00, 17:00)] [время по МСК]'
                   '\n            -exp [время запуска сервера(по МСК)]')

bot.run(os.environ.get('BOT_TOKEN'))
