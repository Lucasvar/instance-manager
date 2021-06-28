import discord
from discord.ext import commands
import os
import requests
from dotenv import load_dotenv
import time
import datetime
import boto3
from collections import defaultdict
load_dotenv()

token = os.getenv('DISCORD_TOKEN_DEV')
profile_name = os.getenv('PROFILE_NAME')
region_name = os.getenv('REGION_NAME')
superRole = 'Tech Leader'

client = discord.Client()
session = boto3.Session()
bot = commands.Bot(command_prefix='$')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@bot.command(pass_context=True)
async def state(ctx, project):
    
    print(ctx.message.author.roles)
    ec2 = session.resource('ec2', region_name=region_name)
    instances = ec2.instances.filter(
        Filters=[   {'Name': 'tag:Project', 'Values': [project.lower()]},
                    {'Name': 'tag:environment', 'Values': ['develop']}
        ])

    for instance in instances:
        embed=discord.Embed(title=f' ', color= 0x20a75d if instance.state['Code'] == 16 else 0xc73c47)
        embed.add_field(name=f'{project} state', value=instance.state['Name'], inline=True)
        await ctx.send(embed=embed)


@bot.command(pass_context=True)
async def instance(ctx, project, state):
    dateTime = datetime.datetime.now()
    ec2 = session.resource('ec2', region_name=region_name)
    
    role_names = [role.name.lower().replace(" ", "") for role in ctx.message.author.roles]
    print(role_names)
    if project in role_names or superRole in role_names:
        print(f'[author]: {ctx.message.author.name} [message]: instance {project} {state} [datetime]: {dateTime}')
        instances = ec2.instances.filter(
            Filters=[   {'Name': 'tag:Project', 'Values': [project.lower()]},
                    {'Name': 'tag:environment', 'Values': ['develop']}
        ])

        embed=discord.Embed(title=f'Check the command syntax and try again', color= 0x000000)
        
        for instance in instances:
            if state.lower() == 'start':
                response = ec2.instances.filter(InstanceIds = [instance.id]).start()
                embed=discord.Embed(title=f'Starting Instance', color= 0x903e83)
                embed.add_field(name='Previous state', value=response[0]["StartingInstances"][0]["PreviousState"]["Name"], inline=True)
                embed.add_field(name='Current state', value=response[0]["StartingInstances"][0]["CurrentState"]["Name"], inline=True)
            if state.lower() == 'stop':
                response = ec2.instances.filter(InstanceIds = [instance.id]).stop()
                embed=discord.Embed(title=f'Stopping Instance', color= 0x711034)
                embed.add_field(name='Previous state', value=response[0]["StoppingInstances"][0]["PreviousState"]["Name"], inline=True)
                embed.add_field(name='Current state', value=response[0]["StoppingInstances"][0]["CurrentState"]["Name"], inline=True)
            if state.lower() == 'reboot':
                try:
                    response = ec2.instances.filter(InstanceIds = [instance.id]).reboot()
                    embed=discord.Embed(title=f'Rebooting instance {project}', color= 0x903e83)
                except Exception as error:
                    errorInfo = str(error).split(": ")[1]
                    embed=discord.Embed(title=f'{errorInfo}', color= 0x7A4A5C)


        try:
            await ctx.send(embed=embed)
            embed.Empty
        except UnboundLocalError as error:
            print(error)
    else:
        await ctx.send("You are not allowed to execute this command.")

bot.run(token)
