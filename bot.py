from operator import truediv
import discord,time as t,streamlink,asyncio,re,random
from discord import client
from discord.ext.commands.core import cooldown
from discord.ext import commands
from discord.ext.commands.errors import CheckFailure, MissingPermissions
from streamlink import PluginError
from alpha import alphabet
from typing import Optional
from discord.utils import get
players = {}
client = commands.Bot(command_prefix="!",intents = discord.Intents.all(),help_command=None)
url = 'https://wasd.tv/kebabobka'
onlstream_ = False
ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        }
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
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
            await send_message(826967699082969088,random.choice(alphabet.phrases))
            print('[log] stream is online')
            await asyncio.sleep(15000)
        else:
            print('[log] stream is offline')
            await asyncio.sleep(120)
@client.command()
async def avatar(ctx, *, avamember:discord.Member=None):
    userAvatarUrl = avamember.avatar_url
    await ctx.send(userAvatarUrl)

@client.command(pass_context=True)
@commands.has_permissions(administrator=True,manage_messages=True)  
async def clear(ctx, amount:int):
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
   


@clear.error
async def clear_error(error, ctx):
    if isinstance(error, MissingPermissions):
        text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
        await send_message(ctx.message.channel, text)
async def send_message(channel_id:int,msg):
    channel = client.get_channel(channel_id)
    await channel.send(msg)


token = os.environ.get('BOT_TOKEN')
client.run(str(token)
