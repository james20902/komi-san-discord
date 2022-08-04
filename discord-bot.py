import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='?')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def sethex(ctx, hex: str):
    try:
        data = discord.Color(int(hex, 16))
        await set_color(ctx, data)
    except Exception as e:
        print(e)
        await ctx.send('something went wrong, maybe format was bad?')
        return

@bot.command()
async def setrgb(ctx, r: int, g: int, b: int):
    try:
        data = discord.Color.from_rgb(r, g, b)
        await set_color(ctx, data)
    except Exception:
        await ctx.send('something went wrong, maybe format was bad?')
        return

async def set_color(ctx, color_data):
    guild = ctx.guild
    user = ctx.author
    matching_role = None

    for Role in guild.roles:
        if Role.name == user.name:
            matching_role = Role

    if matching_role == None:
        try:
            matching_role = await guild.create_role(name=user.name)
            await user.add_roles(matching_role)
        except Exception:
            await ctx.send("couldn't create new role")
            return

    try:
        await matching_role.edit(color=color_data)
    except Exception:
        await ctx.send("failed to edit color data")
        return

    await ctx.send("color added")

bot.run('NoTokenForYou')