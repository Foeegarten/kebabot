import discord,time as t,streamlink,asyncio,re,random,os
from discord import client
from discord.ext.commands.core import cooldown
from discord.ext import commands
from discord.ext.commands.errors import CheckFailure, MissingPermissions
from streamlink import PluginError
from typing import Optional
from discord.utils import get
players = {}
client = commands.Bot(command_prefix="!",intents = discord.Intents.all(),help_command=None)
url = 'https://wasd.tv/kebabobka'
onlstream_ = False
async def send_message(channel_id: int,msg):
    channel = client.get_channel(channel_id)
    await channel.send(msg)
phrases = ['@everyone оо нихуя там кебабобка подрубил все бегом смотреть https://wasd.tv/kebabobka ','@everyone Ready steady хуй на блюде https://wasd.tv/kebabobka','@everyone идем массово чалавать песок https://wasd.tv/kebabobka','@everyone Эйбан рот ето подруб ода ода ода https://wasd.tv/kebabobka','@everyone Пацаны пацаны эй https://wasd.tv/kebabobka',
'@everyone Фиксируем прибыль https://wasd.tv/kebabobka ','@everyone Че тааааам https://wasd.tv/kebabobka','@everyone Че такой серьезный? - улыбнулся - воооо)))) https://wasd.tv/kebabobka','@everyone Оаоаоаоао ммммм подруб мммммм https://wasd.tv/kebabobka','@everyone Я...ммм...пук...подр....подруб....мммм....пук ... https://wasd.tv/kebabobka','@everyone Скука падлы покой дуры мы фанаты подруба кебабуры хдхдхдхдддд https://wasd.tv/kebabobka',
'@everyone ЛЭЙ ЛЭЙ НЕ ЖАЛЭЙ https://wasd.tv/kebabobka']
@client.command()
async def help(ctx):
    embed=discord.Embed(title="Комманды", color=0xff0000)
    embed.add_field(name="help", value="Вызывает это сообщение", inline=False)
    embed.add_field(name="avatar @user", value="Бот пришлет аватар пользователя", inline=True)
    embed.add_field(name="clear кол-во", value="Комманда только для администраторов,очищает чат на количество сообщений", inline=True)
    await ctx.send(embed=embed)
    
@client.command() 
async def ping(ctx):
    await ctx.send('pong')
@client.listen('on_message')
async def on_message(message):
    if message.author == client.user:
        return
    if 'секс' in message.content or 'поебемся' in message.content or 'ебаться' in message.content or 'хорни' in message.content or 'трахаться' in message.content or 'выебу' in message.content or 'виебу' in message.content or 'трахну' in message.content or 'сиськи' in message.content or 'попу' in message.content or 'попа' in message.content or 'анал' in message.content or '69' in message.content or 'ебля' in message.content or 'оргия' in message.content or 'свингер пати' in message.content or 'порно' in message.content or  'прон' in message.content or 'хентай' in message.content or 'нюдс' in message.content or 'нюдсы' in message.content  or 'сиси' in message.content or 'пися' in message.content or 'вагина' in message.content or 'ваджайна' in message.content or 'пизда' in message.content or 'ебаца' in message.content or 'ебатися' in message.content or 'стояк' in message.content or 'потекла' in message.content or 'теку' in message.content or 'смазка' in message.content or 'презерватив' in message.content or 'оргазм' in message.content or 'кончил' in message.content or 'сперма' in message.content or 'конча' in message.content or 'анус' in message.content or 'вуайерист' in message.content or 'куколд' in message.content or 'фурри' in message.content or 'чайный пакетик' in message.content or 'вульва' in message.content or 'клитор' in message.content or 'мошонка' in message.content or 'футфетиш' in message.content or 'фетиш' in message.content or 'ножки' in message.content or 'сосочки' in message.content or 'кок' in message.content:
        await message.channel.send('<:booba:839869013064548383>')
    if 'Подруб' in message.content or'подруб' in message.content  or'во сколько' in message.content or'Во сколько' in message.content or'в какое время' in message.content or'В какое время' in message.content or'Стрим' in message.content or'стрим' in message.content or'стримить' in message.content or'Стримить' in message.content or'след стрим' in message.content or'как часто подрубаешь' in message.content or'Как часто подрубаешь' in message.content or'подрубать' in message.content or'Подрубать' in message.content or'запуск' in message.content or'Запуск' in message.content or'запускаешь' in message.content or'Запускаешь' in message.content:
        await message.channel.send('Расписание стримов Кебабусика: Вторник,Четверг,Суббота ровно в 20:00 по Московскому времени')
    if message.content.startswith('<:nails:839113505713553408>'):
        await message.channel.send('<:nails:839113505713553408>')
@client.listen('on_ready')
async def ready():
    print('bot is ready')
    while True:
        try:
            streams = streamlink.streams(url)
            onlstream = True
        except PluginError as err:
            onlstream = False
        await doin(onlstream)
async def doin(onlstream):
    while True:
        if onlstream==True:
            print('[log] stream is online')
            await send_message(826967699082969088,random.choice(phrases))
            await asyncio.sleep(15000)
        else:
            print('[log] stream is offline')
            await asyncio.sleep(120)
@client.command()
async def avatar(ctx, *,  avamember : discord.Member=None):
    userAvatarUrl = avamember.avatar_url
    await ctx.send(userAvatarUrl)

@client.command(pass_context=True)
@commands.has_permissions(administrator=True,manage_messages=True)  
async def clear(ctx, amount: int):
    try:

        await ctx.channel.purge(limit=amount)
    except MissingPermissions as err:
        ctx.send('Вы не администратор')
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
