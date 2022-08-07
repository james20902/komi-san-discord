import discord
import requests
import json
import os
from http import HTTPStatus
from discord.ext import commands

bot = commands.Bot(command_prefix='?')

bot_token = os.environ["KOMI_PY_KEY"]
steam_token = os.environ["KOMI_STEAM_KEY"]

steam_info_file = open("steamdb.json", "w")


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
    except Exception:
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


@bot.command()
async def registersteam(ctx):
    get_player_data(1)


@bot.command()
async def getsteaminfo(ctx, steamid: str):
    resp = requests.get(
        "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + steam_token + "&steamids=" + steamid)
    if resp.status_code == 200:
        steam_player_info = resp.json().get("response").get("players")[0]
        print(steam_player_info)
        constructed_embed = discord.Embed(
            color=0x00ff00,
            title=steam_player_info.get("personaname"))
        constructed_embed.add_field(
            name="field1name", value="field1value", inline=False)
        constructed_embed.set_image(url=steam_player_info.get("avatarmedium"))
        await ctx.send(embed=constructed_embed)
    else:
        await ctx.send("failed to get data from steamwebapi")


def get_player_data(players):
    playerstr = ""
    for playerid in players:
        playerstr += playerid + ","
    resp = requests.get(
        "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + steam_token + "&steamids=" + playerstr)
    if resp.status_code is HTTPStatus.OK:
        return json.loads(resp.json())
    return None


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

bot.run(bot_token)
