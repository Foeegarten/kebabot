import discord,time as t,streamlink,asyncio,re,random,os
from discord import member
from discord import role
from discord.embeds import EmptyEmbed
from pymongo import mongo_client
from discord import client
from six.moves import urllib
from discord.ext.commands.core import cooldown
from discord.ext import commands
from discord.ext.commands.errors import CheckFailure, MissingPermissions
from streamlink import PluginError
from typing import Optional
from discord.utils import get
import pymongo
from pymongo import MongoClient,ASCENDING, DESCENDING
from pprint import pprint
from discord.ext.commands import cooldown,BucketType,MissingRequiredArgument,CommandOnCooldown
import requests, bs4
import re
password =  urllib.parse.quote_plus(os.getenv('password'))
cluster = pymongo.MongoClient(f"mongodb+srv://foeegarten:{password}@cluster0.ocpqw.mongodb.net/dbkeba?retryWrites=true&w=majority")
db = cluster.test
collection = cluster.dbkeba.health
url = 'https://wasd.tv/kebabobka'
onlstream_ = False
phrases = ['@everyone оо нихуя там кебабобка подрубил все бегом смотреть https://wasd.tv/kebabobka ','@everyone Ready steady хуй на блюде https://wasd.tv/kebabobka','@everyone идем массово чалавать песок https://wasd.tv/kebabobka','@everyone Эйбан рот ето подруб ода ода ода https://wasd.tv/kebabobka','@everyone Пацаны пацаны эй https://wasd.tv/kebabobka',
'@everyone Фиксируем прибыль https://wasd.tv/kebabobka ','@everyone Че тааааам https://wasd.tv/kebabobka','@everyone Че такой серьезный? - улыбнулся - воооо)))) https://wasd.tv/kebabobka','@everyone Оаоаоаоао ммммм подруб мммммм https://wasd.tv/kebabobka','@everyone Я...ммм...пук...подр....подруб....мммм....пук ... https://wasd.tv/kebabobka','@everyone Скука падлы покой дуры мы фанаты подруба кебабуры хдхдхдхдддд https://wasd.tv/kebabobka',
'@everyone ЛЭЙ ЛЭЙ НЕ ЖАЛЭЙ https://wasd.tv/kebabobka']
async def send_message(channel_id: int,msg):
    channel = client.get_channel(channel_id)
    await channel.send(msg)
bot = commands.Bot(command_prefix="!")
bot.load_extension("SomeCommands")
@bot.command()
@cooldown(1,60,BucketType.user)
async def top(ctx):
    await ctx.send('Подождите некоторое время')
    spisok = []
    spiso4ek =[]
    embed = discord.Embed(title='Топ 10 ',colour=ctx.message.author.colour)
    for guild in bot.guilds:
        for member in guild.members:
            data = collection.find_one({"_id":member.id})
            spisok.append(data['points'])
    spisok = set(spisok)
    spisok=sorted(spisok,reverse=True)
    for x in range(10):
        pointy = collection.find_one({"points":spisok[x]})
        spiso4ek.append(f"У {(client.get_user(pointy['_id'])).display_name} {pointy['points']} очков")
    embed.add_field(name=' ',value= '\n'.join(spiso4ek))
    await ctx.send( '\n'.join(spiso4ek))
@bot.event
async def on_ready():
    for guild in bot.guilds:
        for member in guild.members:
            post={
                "_id": member.id,
                "health":100,
                "points":0
                }
            if collection.count_documents({"_id":member.id})==0:
                collection.insert_one(post)
    print('bot is ready')
    while True:
        try:
            streams = streamlink.streams(url)
            onlstream = True
        except PluginError as err:
            onlstream = False
        if onlstream==True:
            print('[log] stream is online')
            await send_message(826967699082969088,random.choice(phrases))
            await asyncio.sleep(15000)
        else:
            print('[log] stream is offline')
            await asyncio.sleep(120)
@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 849558564740530206:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g:g.id == guild_id,bot.guilds)
        if payload.emoji.name == 'Hi':
            role = discord.utils.get(guild.roles,name='Клерк')
        if role is not None:
            member = discord.utils.find(lambda m:m.id==payload.user_id,guild.members)
            if member is not None:
                await member.add_roles(role)
@bot.event
async def on_member_join(member):
    post={
    "_id": member.id,
    "health":100,
    "points":0
    }
    if collection.count_documents({"_id":member.id})==0:
        collection.insert_one(post)
@bot.event
async def on_member_remove(member):
    await send_message(826967373432619047,f"{member.name} вышел")
@bot.event
async def on_command_error(ctx,exc):
    if isinstance(exc, CommandOnCooldown):
        msg = ' Еще не прошел кулдаун, попробуйте через {:.2f}s'.format(exc.retry_after)
        embed = discord.Embed(title=' ',colour=ctx.message.author.colour)
        embed.add_field(name='Ошибка',value=msg)
        await ctx.send(embed=embed)
token = os.getenv('tokenbot')
bot.run(str(token))
