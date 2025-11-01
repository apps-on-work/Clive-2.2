import discord  
import re
import aiohttp
from nospace import token 
from nospace import serverID 
from nospace import YoutubeAPI # get an API for YT, YouTube Data API v3 (10k quota at free tier so use accordingly ;-;)
#pip install google-api-python-client (get this)
from googleapiclient.discovery import build
from discord.ext import commands
from discord import app_commands
from datetime import datetime


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



@client.tree.command(name="ud", description="Urban Dictionary test skelly model", guild=GUILD_ID)
async def ud(interaction: discord.Interaction, ud: str):
    embed = discord.Embed(title="What was searched", url="https://chatgpt.com/", description="dictionary content", color=0x0eed4e) #no url
    embed.set_thumbnail(url="https://play-lh.googleusercontent.com/6am0i3walYwNLc08QOOhRJttQENNGkhlKajXSERf3JnPVRQczIyxw2w3DxeMRTOSdsY") #remove
    embed.add_field(name="Search results for:", value=f'\"{ud}\"', inline=False) #when set false, inline ensures that nothing else continues on same line except that field
    embed.set_footer(text="This is satire\n© Urban Dictionary") #no offense and give ud credit
    embed.set_author(name=interaction.user.name, url="https://www.youtube.com/", icon_url="https://play-lh.googleusercontent.com/6am0i3walYwNLc08QOOhRJttQENNGkhlKajXSERf3JnPVRQczIyxw2w3DxeMRTOSdsY") #no url and icon=pfp
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="udsearch", description="Look for answers in Urban Dictionary", guild=GUILD_ID)
async def udsearch(interaction: discord.Interaction, udsearch: str):

    await interaction.response.defer()

    url = (f"https://api.urbandictionary.com/v0/define?term={udsearch}")

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                data = await response.json(content_type=None)

        except aiohttp.ContentTypeError: #JSON file error check cuz the other method wasn't working
            await interaction.followup.send("Urban Dictionary is currently not responding.")
            return

    if not data["list"]:
        await interaction.followup.send('No info')
        return

    entry = data["list"][0]
    definition = entry["definition"]
    title = entry["word"]
    example = entry["example"]

    if len(definition) > 1000:
        definition = definition[:822] + "-"

    embed = discord.Embed(title=f'**{title}**', color=0x0eed4e)
    embed.add_field(name="Definition:", value=f'\"*{definition}*\"', inline=False)
    embed.add_field(name="Example:", value=f'\"*{example}*\"', inline=False) #when set false, inline ensures that nothing else continues on same line except that field
    embed.set_footer(text="This is satire\n© Urban Dictionary")
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
    await interaction.followup.send(embed=embed)


def parse_duration(duration):
    pattern = re.compile(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?')
    match = pattern.match(duration)
    if not match:
        return "No info"
    hours, minutes, seconds = match.groups()
    hours = int(hours) if hours else 0
    minutes = int(minutes) if minutes else 0
    seconds = int(seconds) if seconds else 0
    if hours:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes}:{seconds:02d}"

def format_compact_number(num_str):
    try:
        num = int(num_str)
    except (ValueError, TypeError):
        return "No info"

    if num >= 1_000_000_000:
        return f"{num/1_000_000_000:.1f}B".rstrip("0").rstrip(".")
    elif num >= 1_000_000:
        return f"{num/1_000_000:.1f}M".rstrip("0").rstrip(".")
    elif num >= 1_000:
        return f"{num/1_000:.1f}K".rstrip("0").rstrip(".")
    return str(num)



@client.tree.command(name="ytsearch", description="Recommends you crisp YT vids based on your search. Response cap(1-3)", guild=GUILD_ID)
async def ytsearch(interaction: discord.Interaction, ytsearch: str, response_limit: int):
    if response_limit < 1:
        response_limit = 1
    elif response_limit > 3:
        response_limit = 3
    
    await interaction.response.defer()  # in case API takes time

    #Youtube API client
    youtube = build("youtube", "v3", developerKey=YoutubeAPI)

    # search for vids
    request = youtube.search().list(part="snippet", q=ytsearch, type="video", maxResults=response_limit)  # no of results, can change
    response = request.execute()

    if not response['items']:
        await interaction.followup.send("No results found.")
        return

    embeds = []
    for video in response['items']:
        video_id = video['id']['videoId']
        snippet = video['snippet']

        title = snippet['title']
        url = f"https://www.youtube.com/watch?v={video_id}"
        channelname = snippet['channelTitle']
        thumbnail = snippet['thumbnails']['high']['url']
        published_at = snippet.get('publishedAt', 'No info')
        description = snippet.get('description', 'No info')
        channel_id = snippet["channelId"]
        channel_request = youtube.channels().list(part="snippet", id=channel_id)
        channel_response = channel_request.execute()
        channel_info = channel_response["items"][0]["snippet"]
        channelurl = f"https://www.youtube.com/channel/{channel_id}"
        channelthumbnail = channel_info['thumbnails']['high']['url']

        try:
            dt = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
            published_date = dt.strftime("%Y-%m-%d")
            published_time = dt.strftime("%H:%M:%S")
        except Exception:
            published_date = published_at
            published_time = "No Info"

        #for more info like views, likes, duration, we need to call another API
        stats_request = youtube.videos().list(part="statistics,contentDetails", id=video_id)
        
        stats_response = stats_request.execute()
        stats = stats_response['items'][0]['statistics']
        details = stats_response['items'][0]['contentDetails']

        views = format_compact_number(stats.get('viewCount', 'No info'))
        likes = format_compact_number(stats.get('likeCount', 'No info'))
        duration = parse_duration(details.get('duration', 'No info'))  # ISO 8601 format changed

        embed = discord.Embed(title=title, url=url, description=description, color=0xff0000)

        embed.set_thumbnail(url=thumbnail)
        embed.add_field(name="Views", value=f'{views}', inline=False)
        embed.add_field(name="Likes", value=f'{likes}', inline=False)
        embed.add_field(name="Duration", value=f'{duration}', inline=False)
        embed.add_field(name="Published", value=f'Date: {published_date}\nTime: {published_time}', inline=False)
        embed.set_footer(text="Clive 2.2\nAll rights reserved!") #not the search youtube python lib >:(
        embed.set_author(name=channelname, url=channelurl, icon_url=channelthumbnail)

        await interaction.followup.send(embed=embed)


client.run(token)




#pending. . . . . . . . .
