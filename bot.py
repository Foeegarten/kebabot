import discord,time as t,streamlink,asyncio,re,random,os
from pymongo import mongo_client
from discord import client
from discord.ext.commands.core import cooldown
from discord.ext import commands
from discord.ext.commands.errors import CheckFailure, MissingPermissions
from streamlink import PluginError
from typing import Optional
from discord.utils import get
import pymongo
from pymongo import MongoClient
from pprint import pprint
from discord.ext.commands import cooldown,BucketType,MissingRequiredArgument,CommandOnCooldown

cluster = pymongo.MongoClient("mongodb+srv://foeegarten:agranat2314A@cluster0.ocpqw.mongodb.net/dbkeba?retryWrites=true&w=majority")
db = cluster.test
collection = cluster.dbkeba.health
client = commands.Bot(command_prefix="!",intents = discord.Intents.all(),help_command=None)
url = 'https://wasd.tv/kebabobka'
onlstream_ = False
async def send_message(channel_id: int,msg):
    channel = client.get_channel(channel_id)
    await channel.send(msg)
phrases = ['@everyone оо нихуя там кебабобка подрубил все бегом смотреть https://wasd.tv/kebabobka ','@everyone Ready steady хуй на блюде https://wasd.tv/kebabobka','@everyone идем массово чалавать песок https://wasd.tv/kebabobka','@everyone Эйбан рот ето подруб ода ода ода https://wasd.tv/kebabobka','@everyone Пацаны пацаны эй https://wasd.tv/kebabobka',
'@everyone Фиксируем прибыль https://wasd.tv/kebabobka ','@everyone Че тааааам https://wasd.tv/kebabobka','@everyone Че такой серьезный? - улыбнулся - воооо)))) https://wasd.tv/kebabobka','@everyone Оаоаоаоао ммммм подруб мммммм https://wasd.tv/kebabobka','@everyone Я...ммм...пук...подр....подруб....мммм....пук ... https://wasd.tv/kebabobka','@everyone Скука падлы покой дуры мы фанаты подруба кебабуры хдхдхдхдддд https://wasd.tv/kebabobka',
'@everyone ЛЭЙ ЛЭЙ НЕ ЖАЛЭЙ https://wasd.tv/kebabobka']
@client.listen('on_ready')
async def ready():
    for guild in client.guilds:
        for member in guild.members:
            post={
                "_id": member.id,
                "health":100,
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
@client.listen('on_member_join')
async def on_member_join(member):
    post={
    "_id": member.id,
    "health":100
    }
    if collection.count_documents({"_id":member.id})==0:
        collection.insert_one(post)
@client.listen('on_message')
async def on_message(message):
    if '<:nails:839113505713553408>' in message.content:
        await message.add_reaction('<:nails:839113505713553408>')
@client.command(pass_context=True)
@commands.has_permissions(administrator=True,manage_messages=True)  
async def clear(ctx, amount: int):
    try:

        await ctx.channel.purge(limit=amount)
    except MissingPermissions as err:
        ctx.send('Вы не администратор')
@client.command()
@cooldown(1,30,BucketType.user)
async def slap(ctx,*,member:discord.Member=None):
    ydata = collection.find_one({"_id":ctx.message.author.id})
    data = collection.find_one({"_id":member.id})
    choice = random.randint(0,10)
    hit = random.randint(0,40)
    if choice < 7:
        if hit>100-data['health']:
            hit = random.randint(0,100-data['health'])
            collection.update_one({"_id":member.id},
                {"$set":{"health":data["health"]-hit}})
            await ctx.send(f"Вы шлепнули {member} по жопке и нанесли {hit} урона")
            await ctx.send(f"У {member} теперь {data['health']) хп}"
        else:
            await ctx.send('Ваш противник уже мертвый')
        
    else:
        if hit>100-ydata['health']:
            hit = random.randint(0,100-ydata['health'])
            collection.update_one({"_id":ctx.message.author.id},
                {"$set":{"health":ydata["health"]-hit}})
            await ctx.send(f"Замахиваясь по жопке {member} вы промахнулись и попали по своей и нанесли себе {hit} урона")
        else:
            await ctx.send('Вы мертвы')
@client.command()
async def health(ctx):
    ydata = collection.find_one({"_id":ctx.message.author.id})
    await ctx.send(f"У вас {ydata['health']} здоровья")

@client.command()
@cooldown(1,120,BucketType.user)
async def heal(ctx):
    ydata = collection.find_one({"_id":ctx.message.author.id})
    
    healint = random.randint(1,30)
    if ydata['health']+healint >100:
        healint = random.randint(0,100-ydata['health'])
        collection.update_one({"_id":ctx.message.author.id},
            {'$set':{"health":ydata['health']+healint}})
        await ctx.send(f"Вы отхилили себе здоровье в размере {healint} единиц")
        
    else:
        collection.update_one({"_id":ctx.message.author.id},
            {'$set':{"health":ydata['health']+healint}})
        await ctx.send(f"Вы отхилили себе здоровье в размере {healint} единиц")
@client.listen('on_command_error')
async def on_command_error(ctx,exc):
    if isinstance(exc, CommandOnCooldown):
        await ctx.send('Еще не прошел кулдаун для данной команды')
    

@client.command()
async def info(ctx,member:discord.Member=None):
    if not member:
        member = ctx.author
        roles = [role for role in ctx.author.roles]
    else:
        roles=[role for role in member.roles]
        embed = discord.Embed(title=f"{member}",colour=member.colour,timestamp=ctx.message.created_at)
        embed.set_author(name='Информация о пользователе: ')
        embed.add_field(name='ID: ',value=member.id,inline=False)
        embed.add_field(name='Имя пользователя: ',value=member.display_name,inline=False)
        embed.add_field(name='Статус сейчас: ',value=str(member.status).title(),inline=False)
        embed.add_field(name='Аккаунт создан: ',value=member.created_at.strftime("%a,%d,%B,%Y,%I,%M"),inline=False)
        embed.add_field(name='Зашел на сервер: ',value=member.joined_at.strftime("%a,%d,%B,%Y,%I,%M"),inline=False)
        embed.add_field(name=f'Роли [{len(roles)}] ',value="** **".join([role.mention for role in roles]),inline=False)
        await ctx.send(embed=embed)
token = os.getenv('tokenbot')
client.run(str(token))
