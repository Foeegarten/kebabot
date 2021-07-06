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
            post={
                "_id": member.id,
                "money":100
                }
            if collection.count_documents({"_id":member.id})==0:
                collection.insert_one(post)
    print('bot is ready')
    while True:
        try:
            streams_t = streamlink.streams(url_twitch)
            if streams_t =={}:
                raise PluginError
            onlstream_twitch = True
        except PluginError as err:
            onlstream_twitch = False
        try:
            streams_w = streamlink.streams(url_wasd)
            if streams_w =={}:
                raise PluginError
            onlstream_wasd = True
        except PluginError as err:
            onlstream_wasd = False

        if onlstream_wasd==True or onlstream_twitch==True:
            
            if onlstream_wasd==True:
                print('[log] stream on wasd is online')
                await send_message(826967699082969088,random.choice(phrases_w))
                onlstream_wasd=False
                
            if onlstream_twitch==True:
                print('[log] stream on twitch is online')
                await send_message(826967699082969088,random.choice(phrases_t))
                onlstream_twitch=False
            await asyncio.sleep(15000)
        else:
            print('[log] stream is offline')
            await asyncio.sleep(120)
#
@client.command()
async def anek(ctx):
    channel = discord.utils.get(client.get_all_channels(), id=830525102243971133)
    aneks = await channel.history().flatten()
    anek_ = random.choice(aneks)
    await ctx.send(anek_.content)

@client.listen('on_member_join')
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles,id=827141363769278475)
    await member.add_roles(role)
@client.listen('on_member_remove')
async def on_member_remove(member):
    await send_message(826967373432619047,f"{member.name} вышел")
@client.listen('on_message')
async def on_message(message):
    value=1
    if 'жид'in message.content or 'Жид' in message.content or 'ЖИд' in message.content or 'ЖиД' in message.content or 'ЖИД' in message.content :
        channel = message.channel
        await channel.purge(limit=1)
    if '<:nails:839113505713553408>' in message.content:
        await message.add_reaction('<:nails:839113505713553408>')
    data=collection.find_one({"_id":message.author.id})
    collection.update_one({"_id":message.author.id},
        {"$set":{"money":data['money']+value}})
@client.command(pass_context=True)
@commands.has_permissions(administrator=True,manage_messages=True)  
async def clear(ctx, amount: int):
    try:

        await ctx.channel.purge(limit=amount)
    except MissingPermissions as err:
        ctx.send('Вы не администратор')
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
@client.command()
async def balance(ctx):
    data=collection.find_one({"_id":ctx.message.author.id})
    await ctx.send(f"Ваш баланс {data['money']} монет")
@client.command()
async def flip(ctx,amount:int):
    if amount>0:
        coin=random.randint(1,2)
        data= collection.find_one({"_id":ctx.message.author.id})
        if data['money']>=amount:
            if coin==1:
                collection.update_one({"_id":ctx.message.author.id},
                {"$set":{"money":data['money']-amount}})
                collection.update_one({"_id":ctx.message.author.id},
                {"$set":{"money":data['money']+amount}})
                await ctx.send(f"Выпала решка,начислено {amount} монет")
            if coin==2:
                collection.update_one({"_id":ctx.message.author.id},
                {"$set":{"money":data['money']-amount}})
                await ctx.send(f"Выпал орел,снято {amount} монет")
    else:
        await ctx.send('Выберите число больше 0')
token = os.getenv('tokenbot')
client.run(str(token))
