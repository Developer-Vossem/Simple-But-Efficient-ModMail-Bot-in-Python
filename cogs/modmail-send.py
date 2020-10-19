import discord
from discord.ext import commands
import json
class ModMailS(commands.Cog):
    def __init__ (self, client):
        self.client = client
    @commands.Cog.listener()
    async def on_ready(self):
        print("")

    @commands.Cog.listener()
    async def on_message(self, message):
        if str(message.channel.type) != "private":
            #Checking if the author is not the bot itself.
            if message.author != self.client.user:
                #Checks if the author is not any other bot.
                if message.author != message.author.bot:
                    #Opening the config file to get Server ID.
                    with open('./utilities/config.json') as n:
                        config = json.load(n)
                    #If message is from that Server, it'll proceed.
                    if message.guild.id == config["serverID"]:
                        categoryname = config["categoryName"]
                        serverID = config["serverID"]
                        server = self.client.get_guild(serverID)
                        category = discord.utils.get(server.categories, name = categoryname)
                        if message.channel.category == category:
                            with open('./data/channel-data.json') as f:
                                data = json.load(f)
                            if str(message.channel.name) in data["openedtickets"]:
                                name = message.channel.name
                                member = await self.client.fetch_user(name)
                                embed = discord.Embed(color = discord.Color.magenta(), timestamp = message.created_at)
                                embed.add_field(name = "Message from {}".format(message.guild), value = f"{message.content}")
                                embed.set_footer(text = 'Please use links to transfer images & files.')
                                await member.send(embed=embed)
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                else:
                    pass








def setup(client):
    client.add_cog(ModMailS(client))