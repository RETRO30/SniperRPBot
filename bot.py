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
async def calc(ctx, *arg):
    arg = list(arg)
    time_on_server = [int(arg[0].split(':')[0]), int(arg[0].split(':')[1])]
    time_in_msc = [int(arg[1].split(':')[0]), int(arg[1].split(':')[1])]
    if time_on_server[1] != 0:
        time_in_msc[1] += int(0.6 * (60 - time_on_server[1]) * 0.8)
        time_on_server[1] = 0
    time_table = []
    for i in range(180):
        if time_on_server[0] == 23:
            time_table.append(
                f'{instr(time_on_server[0])}:{instr(time_on_server[1])}'
                f' - '
                f'{instr(time_in_msc[0])}:{instr(time_in_msc[1])}'
        )
        if time_in_msc[1] + 8 >= 60:
            time_in_msc[1] = (time_in_msc[1] + 8) - 60
            if time_in_msc[0] + 1 == 24:
                time_in_msc[0] = 0
            else:
                time_in_msc[0] += 1
        else:
            time_in_msc[1] += 8

        if time_on_server[0] + 1 == 24:
            time_on_server[0] = 0
        else:
            time_on_server[0] += 1

    for i in time_table:
        await ctx.send(i)


bot.run(os.environ.get('BOT_TOKEN'))
