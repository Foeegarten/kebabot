import discord,time as t,streamlink,asyncio,re,random,os
from discord import member
from discord import role
from discord.embeds import EmptyEmbed
from pymongo import mongo_client
from discord import client
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
@client.listen('on_raw_reaction_add')
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 848688425389129729:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g:g.id == guild_id,client.guilds)
        if payload.emoji.name == 'Hi':
            role = discord.utils.get(guild.roles,name='Клерк')
        if role is not None:
            member = discord.utils.find(lambda m:m.id==payload.user_id,guild.members)
            if member is not None:
                await member.add_roles(role)
@client.listen('on_raw_reaction_remove')
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 848688425389129729:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g:g.id == guild_id,client.guilds)
        if payload.emoji.name == 'Hi':
            role = discord.utils.get(guild.roles,name='Клерк')
        if role is not None:
            member = discord.utils.find(lambda m:m.id==payload.user_id,guild.members)
            if member is not None:
                await member.remove_roles(role)
            


#
@client.command()
async def anek(ctx):
    channel = discord.utils.get(client.get_all_channels(), id=830525102243971133)
    aneks = await channel.history().flatten()
    anek_ = random.choice(aneks)
    await ctx.send(anek_.content)

@client.listen('on_member_join')
async def on_member_join(member):
    post={
    "_id": member.id,
    "health":100,
    "points":0
    }
    if collection.count_documents({"_id":member.id})==0:
        collection.insert_one(post)
@client.listen('on_member_remove')
async def on_member_remove(member):
    await send_message(826967373432619047,f"{member.name} вышел")
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
async def slap(ctx,*,member:discord.Member=None):
    
    ydata = collection.find_one({"_id":ctx.message.author.id})
    data = collection.find_one({"_id":member.id})
    choice = random.randint(0,10)
    hit = random.randint(0,40)
    if ydata['health']<=0:
        embed = discord.Embed(title=f"{member.name}",colour=member.colour)
        embed.add_field(name='Ошибка',value='Вы мертвый, восстановите здоровье, иначе вы не сможете атаковать!')
        await ctx.send(embed=embed)
        raise Exception('dead')
    if data['health']<=0:
        embed = discord.Embed(title=f"{member.name}",colour=member.colour)
        embed.add_field(name='Ошибка',value='Ваш соперник мертв, лежачего не бьют!')
        await ctx.send(embed=embed)
        raise Exception('dead')
    if choice >= 4:
        choice_=random.randint(1,100)
        if choice_>=1 and choice_<35:
            hit = random.randint(1,40)
        elif choice_>=35 and choice_<70:
            hit = random.randint(40,60)
        elif choice_>=70 and choice_<95:
            hit = random.randint(60,80)
        elif choice_>=95 and choice_<=100:
            hit= data['health']
        if hit>data['health']:
            hit=data['health']
        collection.update_one({"_id":ctx.message.author.id},
            {"$set":{"points":ydata['points']+hit}})

        collection.update_one({"_id":member.id},
            {"$set":{"health":data["health"]-hit}})
        embed=discord.Embed(title=" ",colour=member.colour)
        embed.add_field(name="Атака",value=f"Вы шлепнули {member.name} по жопке и нанесли **{hit}** урона")
        embed.add_field(name="Поинты",value=f"Вы получили {hit} очков")
        await ctx.send(embed=embed)
    else:
        choice_=random.randint(1,100)
        if choice_>=1 and choice_<35:
            hit = random.randint(1,40)
        elif choice_>=35 and choice_<70:
            hit = random.randint(40,60)
        elif choice_>=70 and choice_<95:
            hit = random.randint(60,80)
        elif choice_>=95 and choice_<=100:
            hit= data['health']
        if hit>ydata['health']:
            hit=ydata['health']
        hit = random.randint(0,ydata['health'])
        collection.update_one({"_id":ctx.message.author.id},
            {"$set":{"health":ydata["health"]-hit}})
        embed=discord.Embed(title=" ",colour=member.colour)
        embed.add_field(name="Атака",value=f"Замахиваясь по жопке {member.name} вы промахнулись и попали по своей и нанесли себе **{hit}** урона")
        await ctx.send(embed=embed)
@client.command()
async def health(ctx,*,member:discord.Member=None):
    ydata = collection.find_one({"_id":member.id})
    embed=discord.Embed(title=" ",colour=ctx.message.author.colour)
    embed.add_field(name='Здоровье', value=f"У {member.name} {ydata['health']} здоровья")
    await ctx.send(embed=embed)
@client.command()
async def points(ctx,*,member:discord.Member=None):
    data = collection.find_one({"_id":member.id})
    await ctx.send(f"У {member.display_name} {data['points']} очков")
@client.command()
@cooldown(1,600,BucketType.user)
async def heal(ctx,*,member:discord.Member=None):
    ydata = collection.find_one({"_id":member.id})
    choice_=random.randint(1,100)
    if choice_>=1 and choice_<35:
        healint = random.randint(1,40)
    elif choice_>=35 and choice_<70:
        healint = random.randint(40,60)
    elif choice_>=70 and choice_<95:
        healint = random.randint(60,80)
    elif choice_>=95 and choice_<=100:
            healint= 100-ydata['health']
    if ydata['health']+healint >100:
        healint = random.randint(0,100-ydata['health'])
        collection.update_one({"_id":member.id},
            {'$set':{"health":ydata['health']+healint}})
        embed = discord.Embed(title=' ',colour=ctx.message.author.colour)
        embed.add_field(name='Здоровье',value=f"Вы отхилили {member.display_name} здоровье в размере {healint} единиц")
        await ctx.send(embed=embed)
        
    else:
        collection.update_one({"_id":member.id},
            {'$set':{"health":ydata['health']+healint}})
        embed = discord.Embed(title=' ',colour=ctx.message.author.colour)
        embed.add_field(name='Здоровье',value=f"Вы отхилили {member.display_name} здоровье в размере {healint} единиц")
        await ctx.send(embed=embed)
@client.listen('on_command_error')
async def on_command_error(ctx,exc):
    if isinstance(exc, CommandOnCooldown):
        msg = ' Еще не прошел кулдаун, попробуйте через {:.2f}s'.format(exc.retry_after)
        embed = discord.Embed(title=' ',colour=ctx.message.author.colour)
        embed.add_field(name='Ошибка',value=msg)
        await ctx.send(embed=embed)
    
@client.command()
async def avatar(ctx, *,  avamember : discord.Member=None):
    userAvatarUrl = avamember.avatar_url
    await ctx.send(userAvatarUrl)
@client.command()
@commands.has_permissions(administrator=True,manage_messages=True)  
async def reset(ctx):
    for guild in client.guilds:
        for member in guild.members:
            collection.update_one({"_id":member.id},
                {'$set':{"points":0}})
    await ctx.send('База данных обнулена успешно')
@client.command()
@cooldown(1,60,BucketType.user)
async def top(ctx):
    await ctx.send('Подождите некоторое время')
    spisok = []
    spiso4ek =[]
    embed = discord.Embed(title='Топ 10 ',colour=ctx.message.author.colour)
    for guild in client.guilds:
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
