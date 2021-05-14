import discord
from discord.ext import commands
import os
import requests
from dotenv import load_dotenv
import time
import boto3

load_dotenv()
token = os.getenv('DISCORD_TOKEN_DEV')
jenkinsToken = os.getenv('JENKINS_TOKEN_DEV')
jenkinsUrl = os.getenv('JENKINS_URL_DEV')
authName = os.getenv('AUTH_NAME_DEV')
authToken = os.getenv('AUTH_TOKEN_DEV')

projects = ['crm', 'folclass', 'webpj']
states = ['start', 'stop']
rolesProjects = ['CRM', 'Folclass', 'Web PJ']
client = discord.Client()
bot = commands.Bot(command_prefix='$')

@client.event
async def on_ready():
    # print('We have logged in as {0.user}'.format(client))
    game = discord.Game('Developing the API')
    await bot.change_presence(status=discord.Status.idle, activity=game)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def instance(ctx):
    await ctx.send('Instance command!')



bot.run(token)
