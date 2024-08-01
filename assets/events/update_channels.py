import discord
from discord.ext import tasks, commands
from data.database.database import get_guilds

class UpdateChannels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_counters.start()

    @tasks.loop(minutes=5)
    async def update_counters(self):
        guild_ids = get_guilds()
        for guild_id in guild_ids:
            guild = self.bot.get_guild(guild_id)
            if guild:
                member_count = guild.member_count
                online_members = sum(1 for member in guild.members if member.status != discord.Status.offline)
                bot_count = sum(1 for member in guild.members if member.bot)
                channel_count = len(guild.channels)
                role_count = len(guild.roles)
                boost_count = guild.premium_subscription_count

                for channel in guild.channels:
                    if "Members:" in channel.name:
                        await channel.edit(name=f"Members: {member_count}")
                    elif "Online Members:" in channel.name:
                        await channel.edit(name=f"Online Members: {online_members}")
                    elif "Bots:" in channel.name:
                        await channel.edit(name=f"Bots: {bot_count}")
                    elif "Total Channels:" in channel.name:
                        await channel.edit(name=f"Total Channels: {channel_count}")
                    elif "Total Roles:" in channel.name:
                        await channel.edit(name=f"Total Roles: {role_count}")
                    elif "Total Boosts:" in channel.name:
                        await channel.edit(name=f"Total Boosts: {boost_count}")

    @update_counters.before_loop
    async def before_update_counters(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(UpdateChannels(bot))
