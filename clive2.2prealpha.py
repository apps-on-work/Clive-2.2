import discord  # We need the discord.py library to interact with the Discord API and create the bot.
# prealpha.py
from nospace import token # Your bot token goes here
# Make a python file called 'nospace' and declare a variable called token in it
# Assign your bot token to that variable


class Client(discord.Client):
                                # This class inherits from discord.Client, meaning it will inherit all the functionality 
    # of discord.py's base Client class. We'll be able to override methods to add custom behavior.


    async def on_ready(self):
                                 # 'async' indicates this is an asynchronous function, meaning it runs in the background.
        # 'self' refers to the instance of the class, in this case, it's the bot client.


        print(f'Logged on as {self.user}!')
                                                 # This prints a message to the console once the bot has connected.
        # self.user gives us the bot's user object, which includes its username and other info.


    async def on_message(self, message):
                                             # Again, 'async' is used because it's an asynchronous function.
        # The 'message' parameter contains the message object that the bot receives.


        print(f'Message from {message.author}: {message.content}')
                                                                     # This prints the content of the received message to the console.
        # message.author refers to the person who sent the message.
        # message.content gives the actual text content of the message.




intents = discord.Intents.default()
                                        # discord.Intents.default() provides a set of default intents. These are basic event handlers 
# like reacting to messages, users joining, and other general data.


intents.message_content = True
                                    # By default, the bot won't be able to read the content of messages unless we explicitly enable this intent.
# intents.message_content = True allows the bot to access the content (text) of messages.
# This is required for the bot to respond to messages or print their content as we're doing in on_message.




client = Client(intents=intents)
                                    # Here, we're creating an instance of our custom Client class. 
# We pass the 'intents' object to this instance to ensure that the bot has access to the required events, 
# specifically the ability to read message content.





client.run(token) 
                                                                                        # client.run() is the method that starts the bot and connects it to Discord.
# The argument passed to client.run() is the bot's token (a secret key provided by Discord).
# It’s very important that you **never** expose your bot token publicly, as anyone with the token can control your bot.




#main code for setting up the bot.

#End of file
