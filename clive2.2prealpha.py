import discord  
from nospace import token 


class Client(discord.Client):

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
    async def on_message(self, message):
       print(f'Message from {message.author}: {message.content}')
       
       if message.author == self.user:  
           return #stops the bot from replying to itself like whatif it uses it's trigger cmd, that'd cause it to stuck in a endless loop
       
       if message.content.startswith('^911'):
           await message.channel.send(f'https://tenor.com/view/cartoon-tom-and-jerry-on-phone-tom-fbi-gif-17292737')
           #heheheheheh
       
       
       
       if message.content.startswith('^hello'):
           await message.channel.send(f'hello {message.author}!')
           #so if message content startswith ^hello, send hello(persons name) into that channel only.
           #await: Pauses the function until the coroutine is done (in this case, sending the message).


 
intents = discord.Intents.default()

intents.message_content = True

client = Client(intents=intents)

client.run(token)
