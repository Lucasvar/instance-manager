import discord
from discord.ext import commands
import os
import requests
from dotenv import load_dotenv
import time
import boto3
from collections import defaultdict
load_dotenv()
token = os.getenv('DISCORD_TOKEN_DEV')
jenkinsToken = os.getenv('JENKINS_TOKEN_DEV')
jenkinsUrl = os.getenv('JENKINS_URL_DEV')
authName = os.getenv('AUTH_NAME_DEV')
authToken = os.getenv('AUTH_TOKEN_DEV')
profile_name = os.getenv('PROFILE_NAME')
region_name = os.getenv('REGION_NAME')

projects = ['crm', 'folclass', 'webpj']
states = ['start', 'stop']
rolesProjects = ['CRM', 'Folclass', 'Web PJ']
client = discord.Client()
bot = commands.Bot(command_prefix='$')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    # await bot.change_presence(status=discord.Status.idle, activity=game)

session = boto3.Session(profile_name=profile_name)


@bot.command(pass_context=True)
async def state(ctx, project):
    ec2 = session.resource('ec2', region_name=region_name)
    instances = ec2.instances.filter(
        Filters=[{'Name': 'tag:Project', 'Values': [project.lower()]}])

    for instance in instances:
        embed=discord.Embed(title=f' ', color= 0x20a75d if instance.state['Code'] == 16 else 0xc73c47)
        embed.add_field(name=f'{project} state', value=instance.state['Name'], inline=True)
        await ctx.send(embed=embed)

bot.run(token)
