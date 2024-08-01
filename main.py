import discord
from discord.ext import commands
import json
from data.database.database import init_db

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('.'), intents=discord.Intents().all())
        self.cogslist = ["cogs.stats_bot_setup", "assets.events.update_channels", "cogs.help"]

    async def setup_hook(self):
        for ext in self.cogslist:
            await self.load_extension(ext)

    async def on_ready(self):
        print(f"Logged in as {self.user.name}")
        print(f"Bot ID: {self.user.id}")
        print(f"Discord Version: {discord.__version__}")
        synced = await self.tree.sync()
        print(f"Slash CMDs Synced: {len(synced)} Commands")

        with open('data/config.json', 'r') as f:
            data = json.load(f)
            status = data['STATUS']
            activity_type = data['ACTIVITY']
            activity_name = data['ACTIVITY_NAME']

        activity = discord.Activity(type=getattr(discord.ActivityType, activity_type.lower()), name=activity_name)
        await self.change_presence(status=getattr(discord.Status, status.lower()), activity=activity)

with open('data/config.json', 'r') as f:
    data = json.load(f)
    TOKEN = data['TOKEN']

init_db()
client = Client()
client.run(TOKEN)
