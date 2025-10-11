import discord  
from nospace import token 
from nospace import serverID 
from discord.ext import commands
from discord import app_commands #importing two files from discord.py to enable slash commands

class Client(commands.Bot): #it will be commands.Bot instead of discord.Clients to make it accept slash commands

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

        try:
            guild = discord.Object(id=serverID)
            synced = await self.tree.sync(guild=guild)
            print(f'Sync Complete\n{len(synced)} command synced to guild {guild.id}') #trying to sync slash command

        except Exception as e:
            print(f'Error: {e}') #taking the error here



    async def on_message(self, message):
       print(f'Message from {message.author}: {message.content}')
       
       if message.author == self.user:  
           return
       
       if message.content.startswith('^911'):
           await message.channel.send(f'https://tenor.com/view/cartoon-tom-and-jerry-on-phone-tom-fbi-gif-17292737')
           
       
       
       
       if message.content.startswith('^hello'):
           await message.channel.send(f'hello {message.author}!')


 
intents = discord.Intents.default()

intents.message_content = True
client = Client(command_prefix="^", intents=intents) #modified the previous command and added a command_prefix; for some reason we still have to include it even to run / cmds


GUILD_ID = discord.Object(id=serverID)


@client.tree.command(name="run", description="Slash cmds run check!", guild=GUILD_ID)
async def run(interaction: discord.Interaction):
    await interaction.response.send_message("Slash cmds are working fine!") #making a slash command 



client.run(token)
