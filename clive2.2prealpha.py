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
           await message.channel.send(f'*hello {message.author}!*')



    async def on_message_delete(self, message):
        print(f'{message.author} deleted \"{message.content}\"')

        await message.channel.send(f'**{message.author}** just deleted a message : \"||{message.content}||\"')


    async def on_member_join(self, member):
        try:
            print(f'{member.name} has been added to the Server')

            add_send = discord.utils.get(member.guild.text_channels, name='general')


            await add_send.send(f'**{member.name}** just landed outta nowhere. Welcome :saluting_face:')
        
        except Exception as e:
            print(f'Error in member_add: {e}') 


    async def on_member_remove(self, member):
        try:
            print(f'{member.name} has been removed from the Server')

            remove_send = discord.utils.get(member.guild.text_channels, name='general')

            await remove_send.send(f'**{member.name}** just flew away. Goodbye :saluting_face:')

        except Exception as e:
            print(f'Error in member_remove: {e}') 

 
intents = discord.Intents.default()
intents.members = True


intents.message_content = True
client = Client(command_prefix="^", intents=intents)


GUILD_ID = discord.Object(id=serverID)


@client.tree.command(name="run", description="Slash cmds run check!", guild=GUILD_ID)
async def run(interaction: discord.Interaction):
    await interaction.response.send_message("Slash cmds are working fine!") 



@client.tree.command(name="nerd", description="identifies a nerd when it sees one!", guild=GUILD_ID)
async def nerd(interaction: discord.Interaction, nerd: str):  #a branch; we can have multiple branches like (nerd: str, type: int, etc etc)
    await interaction.response.send_message(f'\"{nerd}\" :nerd:') 



@client.tree.command(name="yt", description="test skelly model", guild=GUILD_ID)
async def yt(interaction: discord.Interaction):
    embed = discord.Embed(title="Video Name", url="https://chatgpt.com/", description="Video description", color=0xff0000)
    embed.set_thumbnail(url="https://play-lh.googleusercontent.com/6am0i3walYwNLc08QOOhRJttQENNGkhlKajXSERf3JnPVRQczIyxw2w3DxeMRTOSdsY")
    embed.add_field(name="Likes", value="2.3M or smth idk", inline=False)
    embed.add_field(name="Comments", value="2.3K or smth idk", inline=False)
    embed.add_field(name="Shares", value="203 or smth idk", inline=False) #when set false, inline ensures that nothing else continues on same line except that field
    embed.set_footer(text="Results may varry")
    embed.set_author(name=interaction.user.name, url="https://www.youtube.com/", icon_url="https://play-lh.googleusercontent.com/6am0i3walYwNLc08QOOhRJttQENNGkhlKajXSERf3JnPVRQczIyxw2w3DxeMRTOSdsY")
    await interaction.response.send_message(embed=embed)





client.run(token)







#pending. . . . . . . .
