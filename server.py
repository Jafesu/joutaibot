import discord
import requests
import socket
#import string
#import aiohttp
from discord.utils import get
from discord.utils import find
from discord.ext import commands, tasks
import json
import mysql.connector as mysql
from mysql.connector import errorcode
#from PIL import Image
#import re
import os
from requests.exceptions import Timeout

intents = discord.Intents.default()
intents.members = True

#client = discord.Client(intents=intents)
token = ''
sql = {}
cnx = ''
commandPrefix = '/js'
bot = commands.Bot(command_prefix='/js ')
serverIP = '147.135.36.19'
serverPort = '30120'

def init():
    global token
    global sql

    f = open('config/bot.json')
    data = json.load(f)
    token = data['token']
    f.close()


    f = open('config/sql.json')
    sql = json.load(f)
    f.close()
    f.close()
    sqlInit()


def sqlInit():
    global bot
    global commandPrefix
    try:
        cnx = mysql.connect(user=sql['user'], password=sql['pass'],
                            host=sql['host'],
                            database=sql['database'],
                            auth_plugin='mysql_native_password')
        print("Database Connected")
    except mysql.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()

def srvStatus():
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
       s.settimeout(1)
       s.connect((serverIP, int(serverPort)))
       return True
   except:
       return False

@bot.command()
@commands.cooldown(rate=1, per=30)
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
@commands.cooldown(rate=1, per=30)
async def status(ctx):
    if srvStatus():
        p = requests.get(f"http://{serverIP}:{serverPort}/players.json")
        i = requests.get(f"http://{serverIP}:{serverPort}/info.json")
    
        server = i.json()
        maxPlayers = server['vars']['sv_maxClients']
        serverName = server['vars']['sv_projectName']
        serverName = serverName.replace("^4","")
        serverName = serverName.replace("^5","")
        serverName = serverName.replace("^0","")
        players = p.json()
        playerCount = len(players)
        newMsg = discord.Embed(title=serverName,
            description=f"Server Status: Online",
                                   color=discord.Color.green())
        newMsg.add_field(name="Player Count", value=playerCount, inline=True)
        newMsg.add_field(name="Max Players", value=maxPlayers)
    else:
        newMsg = discord.Embed(title="Joutai State Roleplay - Revamped",
            description=f"Server Status: Offline",
                                   color=discord.Color.red())
    await ctx.send(embed=newMsg)

@bot.command()
@commands.cooldown(rate=1, per=30)
async def rules(ctx):
    rulesMsg = discord.Embed(title="Joutai State Roleplay **|** 状態 **|** Server & Discord Rules",
            description="",
            color=discord.Color.green())
    rulesMsg.add_field(name="**JSRP Server & Discord Rules**", value='Breaking the following rules will result in severe punishment',inline=False)
    rulesMsg.add_field(name="**Voice**", value='```Voice chat is required to interact here. Please configure it in your settings properly so you can speak with your fellow citizens properly.```',inline=False)
    rulesMsg.add_field(name="**Roleplay**", value='```This is a Role-play server. Every action you take must coincide with your character or role play situation.```',inline=False)
    rulesMsg.add_field(name="**Preserve your life**", value='```No one really wants to just die. You need to take actions to preserve your life in the game via roleplay or common sense. ```',inline=False)
    rulesMsg.add_field(name="**New Life Rule**", value='```If you are downed and picked up by an EMT, you will be injured and cannot run off, you need to act it out. If you re-spawn or “die”, you will be unable to recall the situation and cannot take revenge.```',inline=False)
    rulesMsg.add_field(name="**Single Agency Policy**", value='```If your character is a part of a public or government agency, you cannot join another agency unless you leave the current agency.```',inline=False)
    rulesMsg.add_field(name="**Uniforms** **- Bannable offence**", value='```Law Enforcement, Fire Department, Emergency Medical Service, and Military uniforms are off limits to normal citizens. If you are seen wearing them, you will be only warned once.```',inline=False)
    rulesMsg.add_field(name="**Medical Services** **- Bannable offence**", value='```If there is one EMT on the server, they are not to be killed, harmed, or obstructed from reviving a citizen.```',inline=False)
    rulesMsg.add_field(name="**Reports**", value='```If you find a bug or have an issue with another player, create a report at the reports channel and the staff will respond. If you message the dev team, you will be directed to create a ticket.```',inline=False)
    rulesMsg.add_field(name="**RDM/VDM** **- Bannable offence**", value='```We DO NOT tolerate random acts of violence on this server. Regarding rule #2, it needs to be roleplay. If you are just here to cause senseless violence without any RP, you will be deported from the city.```',inline=False)
    rulesMsg.add_field(name="**Malicious Behavior** **- Bannable offence**", value='```Any kind of bullying, harassment, or actions with malicious intent to harm another player verbally or emotionally, will not be tolerated by any means.```',inline=False)
    rulesMsg.add_field(name="**Poaching**", value="```If you are here to try and convince people to join another server, either leave or we'll make you leave. No one wants their DMs spammed about joining other servers. If they want to join another server, they'll do it themselves.```",inline=False)
    rulesMsg.add_field(name="**Meta-gaming** **- Bannable offence**", value='```Using any known information that was not gathered by the character that you are playing is considered meta-gaming and is not tolerated on the game server or discord. This can be considered by using knowledge from another character, cop baiting, and other unfair advantages that the character would not have.```',inline=False)
    await ctx.send(embed=rulesMsg)

@bot.command()
@commands.cooldown(rate=1, per=30)
async def laws(ctx):
    rulesMsg = discord.Embed(title="Laws of the Land",
            description="",
            color=discord.Color.green())
    rulesMsg.add_field(name="City Laws", value='```1. Law #1 \n2. Law #2 \n3. Law #3 \n4. Law #4```',inline=False)
    rulesMsg.add_field(name="County Laws", value='```1. Law #1 \n2. Law #2 \n3. Law #3 \n4. Law #4```',inline=False)
    await ctx.send(embed=rulesMsg)


@bot.command()
@commands.cooldown(rate=1, per=30)
async def apps(ctx):
    rulesMsg = discord.Embed(title="L.S. Bureaucratic Applications",
            description="",
            color=discord.Color.green())
    rulesMsg.add_field(name="Joutai State Agency Application", value='[Apply Here](https://forms.gle/JDj78bRbTREvMZMf7)',inline=False)
    rulesMsg.add_field(name="Joutai State Citizen's Business Application", value='[Apply Here](https://forms.gle/RDUeLusQGyQqh9fF8)',inline=False)
    await ctx.send(embed=rulesMsg)


init()
bot.run(token)



# rulesMsg.add_field(name="", value='``` ```',inline=False)
