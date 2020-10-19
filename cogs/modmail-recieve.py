import discord
from discord.ext import commands
import json
class ModMailR(commands.Cog):
    def __init__ (self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("")
    @commands.Cog.listener()
    async def on_message(self, message):
        
        #Checks if the DM'er is one of the Bot User.
        if message.author.id == self.client.user.id:
            return
        #Checks if the DM'er is a bot or no,
        if message.author != message.author.bot:
            if not message.guild: #Checks if the message is in a Guild or no.
                #Loads up the Database.
                with open('./data/channel-data.json') as f:
                    data = json.load(f)
                with open('./utilities/config.json') as n:
                    config = json.load(n)
                #Checks if the user's ticket is already opened, if it is, then it proceeds.    
                if str(message.author.id) in data["openedtickets"]:
                    serverID = config["serverID"]
                    server = self.client.get_guild(serverID)
                    categoryname = config["categoryName"]
                    category = discord.utils.get(server.categories, name = categoryname)
                    if category not in server.categories:
                        await message.author.send("The guild is not yet configured for the ModMail, please ask an Administrator to run the **{}setup** in the server. ".format(config["prefix"]))
                    else:
                        channel = discord.utils.get(server.channels, name = f"{message.author.id}")
                        embed = discord.Embed(color = discord.Color.orange(), timestamp = message.created_at)
                        embed.add_field(name = "Message from {}".format(message.author), value = f"{message.content}")
                        embed.set_footer(text = 'Please use links to transfer images & files.')
                        await channel.send(embed=embed)  
                #If it's not, then it'll create an entry for user.
                elif str(message.author.id) not in data["openedtickets"]:
                    with open('./utilities/config.json') as y:
                        config = json.load(y)  
                    serverID = config["serverID"]
                    server = self.client.get_guild(serverID)
                    categoryname = config["categoryName"]
                    category = discord.utils.get(server.categories, name = categoryname)
                    if category not in server.categories:
                        await message.author.send("The guild is not yet configured for the ModMail, please ask an Administrator to run the **{}setup** in the server. ".format(config["prefix"]))
                    else:
                        embed = discord.Embed(title = 'Support will be with you Shortly.', color = discord.Color.green(), timestamp = message.created_at)
                        embed.set_footer(text ="Please use links to transfer Images & Files.")
                        await message.author.send(embed = embed)
                        with open('./data/channel-data.json', 'r') as n:
                            data= json.load(n) 
                        data["openedtickets"].append(str(message.author.id))
                        with open('./data/channel-data.json', 'w') as n:
                            json.dump(data, n)
                        channel = await server.create_text_channel(f"{message.author.id}", category=category)  
                        await channel.set_permissions(server.default_role, send_messages=False, read_messages=False)      
                        await channel.send(f"{message.author.display_name} opened a Ticket!")
                        embed = discord.Embed(color = discord.Color.orange(), timestamp = message.created_at)
                        embed.add_field(name = "Message from {}".format(message.author), value = f"{message.content}")
                        embed.set_footer(text = 'Please use links to transfer images & files.')
                        await channel.send(embed=embed)
                    
        else:
            pass         

def setup(client):
    client.add_cog(ModMailR(client))