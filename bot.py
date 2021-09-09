import discord,time as t,streamlink,asyncio,re,random,os
from discord.embeds import EmptyEmbed
from discord import client
from six.moves import urllib
from discord.ext.commands.core import cooldown
from discord.ext import commands
from discord.ext.commands.errors import  MissingPermissions
from streamlink import PluginError
from discord.utils import get
import pymongo
from pymongo import MongoClient,ASCENDING, DESCENDING
from pprint import pprint
from discord.ext.commands import cooldown,BucketType,CommandOnCooldown
import re
password =  urllib.parse.quote_plus(os.getenv('password'))
cluster = pymongo.MongoClient(f"mongodb+srv://foeegarten:{password}@cluster0.ocpqw.mongodb.net/dbkeba?retryWrites=true&w=majority")
db = cluster.test
collection = cluster.dbkeba.health
client = commands.Bot(command_prefix="!",intents = discord.Intents.all(),help_command=None)
url_wasd = 'https://wasd.tv/kebabobka'
url_twitch ='https://www.twitch.tv/kebabobka'
async def send_message(channel_id: int,msg):
    channel = client.get_channel(channel_id)
    await channel.send(msg)
#
phrases_w = ['@everyone оо нихуя там кебабобка подрубил все бегом смотреть https://wasd.tv/kebabobka ','@everyone Ready steady хуй на блюде https://wasd.tv/kebabobka','@everyone идем массово чалавать песок https://wasd.tv/kebabobka','@everyone Эйбан рот ето подруб ода ода ода https://wasd.tv/kebabobka','@everyone Пацаны пацаны эй https://wasd.tv/kebabobka',
'@everyone Фиксируем прибыль https://wasd.tv/kebabobka ','@everyone Че тааааам https://wasd.tv/kebabobka','@everyone Че такой серьезный? - улыбнулся - воооо)))) https://wasd.tv/kebabobka','@everyone Оаоаоаоао ммммм подруб мммммм https://wasd.tv/kebabobka','@everyone Я...ммм...пук...подр....подруб....мммм....пук ... https://wasd.tv/kebabobka','@everyone Скука падлы покой дуры мы фанаты подруба кебабуры хдхдхдхдддд https://wasd.tv/kebabobka',
'@everyone ЛЭЙ ЛЭЙ НЕ ЖАЛЭЙ https://wasd.tv/kebabobka']
phrases_t = ['@everyone оо нихуя там кебабобка подрубил все бегом смотреть https://www.twitch.tv/kebabobka ','@everyone Ready steady хуй на блюде https://www.twitch.tv/kebabobka','@everyone идем массово чалавать песок https://www.twitch.tv/kebabobka','@everyone Эйбан рот ето подруб ода ода ода https://www.twitch.tv/kebabobka','@everyone Пацаны пацаны эй https://www.twitch.tv/kebabobka','@everyone Фиксируем прибыль https://www.twitch.tv/kebabobka ','@everyone Че тааааам https://www.twitch.tv/kebabobka','@everyone Че такой серьезный? - улыбнулся - воооо)))) https://www.twitch.tv/kebabobka','@everyone Оаоаоаоао ммммм подруб мммммм https://www.twitch.tv/kebabobka','@everyone Я...ммм...пук...подр....подруб....мммм....пук ... https://www.twitch.tv/kebabobka','@everyone Скука падлы покой дуры мы фанаты подруба кебабуры хдхдхдхдддд https://www.twitch.tv/kebabobka','@everyone ЛЭЙ ЛЭЙ НЕ ЖАЛЭЙ https://www.twitch.tv/kebabobka']

@client.listen('on_ready')
async def ready():
    for guild in client.guilds:
        for member in guild.members:
            role1 = discord.utils.get(ctx.guild.roles, name="Начальник отдела")
            role2 = discord.utils.get(ctx.guild.roles, name="Генеральный Директор")
            if role1 or role2 in member.roles:
                pass
            else:
                await member.kick()

token = os.getenv('tokenbot')
client.run(str(token))
