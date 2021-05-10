import discord
import os
import requests
from dotenv import load_dotenv
import time

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

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$instance') and message.content != '$instance help':
        print(client.user.avatar_url)
        text = message.content.split()
        project = text[1]
        state = text[2]
        role_names = [role.name for role in message.author.roles]
        if project not in projects or state not in states:
            await message.channel.send(f'Ocurrio un problema, revisa que los argumentos sean correctos')
        else:
            roleCheck = True if 'test' in role_names else False
            if roleCheck:
                response = requests.post(f'{jenkinsUrl}/job/instance-manager/buildWithParameters?token={jenkinsToken}&PROJECT={project}&STATE={state}', auth=(authName, authToken))
                if response:
                    statusInfo = 'Iniciando' if state == 'start' else 'Parando'
                    await message.channel.send(f'{statusInfo} la instancia de {project}')
                else:
                    await message.channel.send(f'Ocurrio un problema')
            else:
                await message.channel.send(f'No tenes los permisos suficientes para ejecutar este comando')
                
    if message.content.startswith('$instance help'):
        embed=discord.Embed(title='Instance Manager Help', description='mensaje de ayuda del bot Instance Manager', color=0x68cf7e)
        embed.set_author(name=client.user.display_name, url='', icon_url=client.user.avatar_url)
        embed.set_thumbnail(url=client.user.avatar_url)
        embed.add_field(name='$instance project state', value='Este comando se utiliza para gestionar el estasdo de las instancias de desarrollo, se debe reemplazar _project_  por **crm**, **folclass** o **webpj** \n y _state_ por **start** o **stop**', inline=False)
        embed.add_field(name= 'ejemplo', value='**$instance folclass start** \n _esto incia la instancia de desarollo del proyecto Folclass_', inline=False)
        # embed.set_footer(text=time.ctime(time.time()))
        await message.channel.send(embed=embed)
        
client.run(token)

