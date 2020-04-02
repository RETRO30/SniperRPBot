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
async def calc(ctx, arg):
    time = [int(arg.split(':')[0]), int(arg.split(':')[1])]
    time_table = []
    for i in range(8):
        time_table.append(f'{instr(time[0])}:{instr(time[1])}')
        if time[1] + 24 >= 60:
            time[0] += 4
            time[1] = time[1] + 24 - 60
        else:
            time[1] += 24
            time[0] += 3
    for i in time_table:
        await ctx.send(i)


bot.run(os.environ.get('BOT_TOKEN'))
