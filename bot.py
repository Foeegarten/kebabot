import discord,time as t,streamlink,asyncio,re,random,os
from discord import client
from discord.ext.commands.core import cooldown
from discord.ext import commands
from discord.ext.commands.errors import CheckFailure, MissingPermissions
from streamlink import PluginError
from typing import Optional
from discord.utils import get
client = commands.Bot(command_prefix="!",intents = discord.Intents.all(),help_command=None)
url = 'https://wasd.tv/kebabobka'
onlstream_ = False
async def send_message(channel_id: int,msg):
    channel = client.get_channel(channel_id)
    await channel.send(msg)
def health():
    global health1 
    health1 = 100
    global health2
    health2 = 100

phrases = ['@everyone оо нихуя там кебабобка подрубил все бегом смотреть https://wasd.tv/kebabobka ','@everyone Ready steady хуй на блюде https://wasd.tv/kebabobka','@everyone идем массово чалавать песок https://wasd.tv/kebabobka','@everyone Эйбан рот ето подруб ода ода ода https://wasd.tv/kebabobka','@everyone Пацаны пацаны эй https://wasd.tv/kebabobka',
'@everyone Фиксируем прибыль https://wasd.tv/kebabobka ','@everyone Че тааааам https://wasd.tv/kebabobka','@everyone Че такой серьезный? - улыбнулся - воооо)))) https://wasd.tv/kebabobka','@everyone Оаоаоаоао ммммм подруб мммммм https://wasd.tv/kebabobka','@everyone Я...ммм...пук...подр....подруб....мммм....пук ... https://wasd.tv/kebabobka','@everyone Скука падлы покой дуры мы фанаты подруба кебабуры хдхдхдхдддд https://wasd.tv/kebabobka',
'@everyone ЛЭЙ ЛЭЙ НЕ ЖАЛЭЙ https://wasd.tv/kebabobka']
@client.listen('on_ready')
async def ready():
    health()
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
async def attack(ctx,*,member:discord.Member=None):
     choose = random.choice(1,2)
     if choose ==1:
         health1 -= random.randint(0,40)
         await ctx.send(f'Вы пропустили удар ваше здоровье равно {health1}')
     else:
        health2 -= random.randint(0,40)
        await ctx.send(f'Вы успешно ударили {member} и у него теперь {health2} здоровья')



@client.command()
async def info(ctx,*,member:discord.Member=None):
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
