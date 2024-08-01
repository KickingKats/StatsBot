import discord
from discord.ext import commands
from discord import app_commands


class Help(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="help", description="Displays information about all commands")
    async def help_cmd(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Help", description="List of available commands", color=discord.Color.blue())

        embed.add_field(name="/setup",
                        value="Sets up the counters. Options:\n- **channel_type**: Voice Channel, Text Channel, Announcement Channel, Stage Channel\n- **configuration**: Default Counters, Default, Channels and Roles, Default Boosts",
                        inline=False)
        embed.add_field(name="/reset_setup",
                        value="Resets the setup. Options:\n- **action**: Delete Channels, Reset Counters", inline=False)
        embed.add_field(name="/help", value="Displays this help message", inline=False)

        embed.set_footer(text="StatsBot | Your server stats assistant")

        await interaction.response.send_message(embed=embed)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Help(client))
