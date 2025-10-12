import discord  
from nospace import token 
from nospace import serverID 
from discord.ext import commands
from discord import app_commands 

class Client(commands.Bot): 

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

        try:
            guild = discord.Object(id=serverID)
            synced = await self.tree.sync(guild=guild)
            print(f'Sync Complete\n{len(synced)} command synced to guild {guild.id}') 

        except Exception as e:
            print(f'Error: {e}') 



    async def on_message(self, message):
       print(f'Message from {message.author}: {message.content}')
       
       if message.author == self.user:  
           return
       
       if message.content.startswith('^911'):
           await message.channel.send(f'https://tenor.com/view/cartoon-tom-and-jerry-on-phone-tom-fbi-gif-17292737')
       
       
       if message.content.startswith('^hello'):
           await message.channel.send(f'hello {message.author}!')



    async def on_message_delete(self, message):
        print(f'{message.author} deleted \"{message.content}\"')

        await message.channel.send(f'{message.author} just a message ||{message.content}||')


 
intents = discord.Intents.default()

intents.message_content = True
client = Client(command_prefix="^", intents=intents)


GUILD_ID = discord.Object(id=serverID)


@client.tree.command(name="run", description="Slash cmds run check!", guild=GUILD_ID)
async def run(interaction: discord.Interaction):
    await interaction.response.send_message("Slash cmds are working fine!") 



@client.tree.command(name="nerd", description="identifies a nerd when it sees one!", guild=GUILD_ID)
async def nerd(interaction: discord.Interaction, nerd: str):  #a branch; we can have multiple branches like (nerd: str, type: int, etc etc)
    await interaction.response.send_message(f'\"{nerd}\" :nerd:') 



client.run(token)







#pending. . . . . . . . .
