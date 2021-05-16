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

session = boto3.Session(profile_name=profile_name)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def instance(ctx):
    ec2 = session.resource('ec2', region_name='us-east-1')
    running_instances = ec2.instances.filter(Filters=[
        {
            'Name': 'instance-state-name',
            'Values': ['running']
        }
    ])
    ec2info = defaultdict()
    for instance in running_instances:
        for tag in instance.tags:
            if 'Name' in tag['Key']:
                name = tag['Value']
    # Add instance info to a dictionary         
        ec2info[instance.id] = {
            'Name': name,
            'Type': instance.instance_type,
            'State': instance.state['Name'],
            'Private IP': instance.private_ip_address,
            'Public IP': instance.public_ip_address,
            'Launch Time': instance.launch_time
            }

    attributes = ['Name', 'Type', 'State', 'Private IP', 'Public IP', 'Launch Time']
    s=''
    embed=discord.Embed(title="Instances Running", color=0x20a75d)
    flag = True
    for instance_id, instance in ec2info.items():
        for key in attributes:
            embed.add_field(name=key, value=instance[key], inline=flag)
            # flag= True
            #  s+=str("{0}: {1}\n".format(key, instance[key]))
        # s+=str("\n")
        # flag = False
    # print(s)
    # await message.channel.send(s)
    # await ctx.send(s)
    await ctx.send(embed=embed)
    # await ctx.send(print(running_instances))
    # s3 = session.resource('s3')
    # for bucket in s3.buckets.all():
    #     print(bucket.name)

    # ec2 = boto3.resource('ec2')
    # instances = ec2.instances.filter(
    # Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    # for instance in instances:
    #     await ctx.send(print(instance.id, instance.instance_type))


@bot.command()
async def state(ctx, project):
    ec2 = session.resource('ec2', region_name='us-east-1')
    # instances = ec2.instances.filter(Filters=[
    #     {
    #         'Name': 'Project',
    #         'Values': [project.lower()]
    #     }
    # ])
    instances = ec2.instances.filter(
        Filters=[{'Name': 'tag:Project', 'Values': [project.lower()]}])
    for instance in instances:
        print(instance.state['Name'])
        embed=discord.Embed(title=f' ', color= 0x20a75d if instance.state['Code'] == 16 else 0xc73c47)
        embed.add_field(name=f'{project} state', value=instance.state['Name'], inline=True)
        await ctx.send(embed=embed)
    
bot.run(token)
