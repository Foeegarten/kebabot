from discord.ext import commands # Again, we need this imported
import discord,time as t,streamlink,asyncio,re,random,os
from discord import member
from discord import role
from discord.embeds import EmptyEmbed
from pymongo import mongo_client
from discord import client
from six.moves import urllib
from discord.ext.commands.core import command, cooldown
from discord.ext import commands
from discord.ext.commands.errors import CheckFailure, MissingPermissions
from streamlink import PluginError
from typing import Optional
from discord.utils import get
import pymongo
from pymongo import MongoClient,ASCENDING, DESCENDING
from pprint import pprint
from discord.ext.commands import bot, cooldown,BucketType,MissingRequiredArgument,CommandOnCooldown
import requests, bs4
import re
bot = commands.Bot(command_prefix="!")
cluster = pymongo.MongoClient(f"mongodb+srv://foeegarten:freakinshop@cluster0.ocpqw.mongodb.net/dbkeba?retryWrites=true&w=majority")
db = cluster.test
collection = cluster.dbkeba.health
class SomeCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    ######################################################################
    @commands.command()
    @cooldown(1,60,BucketType.user)
    async def top(self,ctx):
        await ctx.send('Подождите некоторое время')
        spisok = []
        spiso4ek =[]
        for guild in bot.guilds:
            for member in guild.members:
                data = collection.find_one({"_id":member.id})
                spisok.append(data['points'])
        spisok = set(spisok)
        spisok=sorted(spisok,reverse=True)
        for x in range(10):
            pointy = collection.find_one({"points":spisok[x]})
            spiso4ek.append(f"У {(bot.get_user(pointy['_id'])).display_name} {pointy['points']} очков")
        await ctx.send( '\n'.join(spiso4ek))
    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        await ctx.send(f"{round(self.bot.latency * 1000)}ms")
    ######################################################################
    @commands.command(name='anek')
    async def anek(self,ctx):
        channel = discord.utils.get(bot.get_all_channels(), id=830525102243971133)
        aneks = await channel.history().flatten()
        anek_ = random.choice(aneks)
        await ctx.send(anek_.content)
    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True,manage_messages=True)  
    async def clear(self,ctx, amount: int):
        try:

            await ctx.channel.purge(limit=amount)
        except MissingPermissions as err:
            ctx.send('Вы не администратор')
    @commands.command()
    @cooldown(1,60,BucketType.user)
    async def slap(self,ctx,*,member:discord.Member=None):
    
        ydata = collection.find_one({"_id":ctx.message.author.id})
        data = collection.find_one({"_id":member.id})
        choice = random.randint(0,10)
        hit = random.randint(0,40)
        if ctx.message.author.id == member.id:
            await ctx.send("Вы не можете ударить себя по жопке")
            raise Exception('nonono')
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
    @commands.command()
    async def health(self,ctx,*,member:discord.Member=None):
        ydata = collection.find_one({"_id":member.id})
        embed=discord.Embed(title=" ",colour=ctx.message.author.colour)
        embed.add_field(name='Здоровье', value=f"У {member.name} {ydata['health']} здоровья")
        await ctx.send(embed=embed)
    @commands.command()
    async def points(self,ctx,*,member:discord.Member=None):
        data = collection.find_one({"_id":member.id})
        await ctx.send(f"У {member.display_name} {data['points']} очков")
    @commands.command()
    async def alive(self,ctx):
        alive = []
        for guild in bot.guilds:
            for member in guild.members:
                data = collection.find_one({"_id":member.id})
                if data['health']>0:
                    alive.append(member.display_name)
        await ctx.send('\n'.join(alive))
    @commands.command()
    @cooldown(1,60,BucketType.user)
    async def heal(self,ctx,*,member:discord.Member=None):
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
    @commands.command()
    async def avatar(self,ctx, *,  avamember : discord.Member=None):
        userAvatarUrl = avamember.avatar_url
        await ctx.send(userAvatarUrl)
    @commands.command()
    @commands.has_permissions(administrator=True,manage_messages=True)  
    async def reset(ctx):
        for guild in client.guilds:
            for member in guild.members:
                collection.update_one({"_id":member.id},
                    {'$set':{"points":0}})
        await ctx.send('База данных обнулена успешно')

def setup(bot: commands.Bot):
    bot.add_cog(SomeCommands(bot))
