import discord
from discord.ext import commands
import json
class Commands(commands.Cog):
    def __init__ (self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("All modules successfuly loaded!")
    @commands.command()
    async def close(self, ctx):
        '''Closing the Ticket'''
        with open('./data/channel-data.json') as n:
            data= json.load(n)
        if ctx.channel.name in data["openedtickets"]:
            with open('./data/channel-data.json', 'r') as n:
                data= json.load(n) 
            data["openedtickets"].remove(str(ctx.message.channel.name))
            with open('./data/channel-data.json', 'w') as n:
                json.dump(data, n)
            name = ctx.channel.name
            member = await self.client.fetch_user(name)
            embed = discord.Embed(title ="Your ticket has been **closed** by {}.".format(ctx.message.author.display_name) ,color = discord.Color.red(), timestamp = ctx.message.created_at)
            embed.set_footer(text = 'Thanks for reaching out to our Support.')
            await member.send(embed = embed)
            await ctx.channel.delete()
        else:
            await ctx.message.delete()
            await ctx.send("This is not a valid Ticket Channel which you can close.", delete_after = 30)

    @commands.command()
    async def setup(self, ctx):
        '''Setting up the Bot'''
        with open('./utilities/config.json') as f:
            config = json.load(f)
        categoryname = config["categoryName"]
        category = discord.utils.get(ctx.guild.categories, name = categoryname)
        if category in ctx.guild.categories:
            await ctx.send("This guild is already configured with the ModMail System.")
            await ctx.message.delete()
        elif category not in ctx.guild.categories:
            await ctx.guild.create_category(categoryname)
            category = discord.utils.get(ctx.guild.categories, name=categoryname)
            ticket_channel = await ctx.guild.create_text_channel(f"create-a-ticket", category = category)
            await ticket_channel.set_permissions(ctx.guild.default_role, send_messages=False, read_messages=True)
            await ticket_channel.send("If you want to contact the support, you can simply DM {}.".format(self.client.user.mention))  
            await ctx.send("I've configured the bot in this Server.")
def setup(client):
    client.add_cog(Commands(client))