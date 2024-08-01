import discord
from discord.ext import commands, tasks
from discord import app_commands
from data.database.database import add_guild, remove_guild, guild_exists

class Stats_Bot_Setup(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.checks.has_permissions(manage_guild=True)
    @app_commands.command(name="setup", description="Sets up the counters")
    @app_commands.describe(
        channel_type="Select the type of channel to create",
        configuration="Select the configuration of counters"
    )
    @app_commands.choices(
        channel_type=[
            app_commands.Choice(name="Voice Channel", value="voice"),
            app_commands.Choice(name="Text Channel", value="text"),
            app_commands.Choice(name="Announcement Channel", value="announcement"),
            app_commands.Choice(name="Stage Channel", value="stage")
        ],
        configuration=[
            app_commands.Choice(name="Default Counters", value="default"),
            app_commands.Choice(name="Default, Channels and Roles", value="channels_roles"),
            app_commands.Choice(name="Default Boosts", value="boosts")
        ]
    )
    async def setup(self, interaction: discord.Interaction, channel_type: app_commands.Choice[str], configuration: app_commands.Choice[str]):
        guild = interaction.guild

        if guild_exists(guild.id):
            embed = discord.Embed(title="Setup Error", description="Setup has already been done. Use /reset_setup to reset.", color=discord.Color.red())
            await interaction.response.send_message(embed=embed)
            return

        add_guild(guild.id)

        category = await guild.create_category(name="Server Stats")

        await category.edit(position=0)

        member_count = guild.member_count
        online_members = sum(1 for member in guild.members if member.status != discord.Status.offline)
        bot_count = sum(1 for member in guild.members if member.bot)
        channel_count = len(guild.channels)
        role_count = len(guild.roles)
        boost_count = guild.premium_subscription_count

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=True, send_messages=False, connect=False)
        }

        if channel_type.value == "voice":
            await guild.create_voice_channel(name=f"Members: {member_count}", overwrites=overwrites, category=category)
        elif channel_type.value == "text":
            await guild.create_text_channel(name=f"Members: {member_count}", overwrites=overwrites, category=category)
        elif channel_type.value == "announcement":
            await guild.create_text_channel(name=f"Members: {member_count}", type=discord.ChannelType.news, overwrites=overwrites, category=category)
        elif channel_type.value == "stage":
            await guild.create_stage_channel(name=f"Members: {member_count}", overwrites=overwrites, category=category)

        if configuration.value == "default":
            await guild.create_voice_channel(name=f"Online Members: {online_members}", overwrites=overwrites, category=category)
            await guild.create_voice_channel(name=f"Bots: {bot_count}", overwrites=overwrites, category=category)
        elif configuration.value == "channels_roles":
            await guild.create_voice_channel(name=f"Online Members: {online_members}", overwrites=overwrites, category=category)
            await guild.create_voice_channel(name=f"Bots: {bot_count}", overwrites=overwrites, category=category)
            await guild.create_voice_channel(name=f"Total Channels: {channel_count}", overwrites=overwrites, category=category)
            await guild.create_voice_channel(name=f"Total Roles: {role_count}", overwrites=overwrites, category=category)
        elif configuration.value == "boosts":
            await guild.create_voice_channel(name=f"Online Members: {online_members}", overwrites=overwrites, category=category)
            await guild.create_voice_channel(name=f"Bots: {bot_count}", overwrites=overwrites, category=category)
            await guild.create_voice_channel(name=f"Total Boosts: {boost_count}", overwrites=overwrites, category=category)

        embed = discord.Embed(title="Setup Complete", description="Counters have been set up!", color=discord.Color.green())
        await interaction.response.send_message(embed=embed)

    @app_commands.checks.has_permissions(manage_guild=True)
    @app_commands.command(name="reset_setup", description="Resets the setup")
    @app_commands.describe(
        action="Select whether to delete the channels or reset the counters"
    )
    @app_commands.choices(
        action=[
            app_commands.Choice(name="Delete Channels", value="delete"),
            app_commands.Choice(name="Reset Counters", value="reset")
        ]
    )
    async def reset_setup(self, interaction: discord.Interaction, action: app_commands.Choice[str]):
        guild = interaction.guild

        if action.value == "delete":
            category = discord.utils.get(guild.categories, name="Server Stats")
            if category:
                for channel in category.channels:
                    await channel.delete()
                await category.delete()
            remove_guild(guild.id)
            embed = discord.Embed(title="Reset Complete", description="Channels and category have been deleted and setup has been reset.", color=discord.Color.green())
            await interaction.response.send_message(embed=embed)
        elif action.value == "reset":
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

            embed = discord.Embed(title="Reset Complete", description="Counters have been reset.", color=discord.Color.green())
            await interaction.response.send_message(embed=embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Stats_Bot_Setup(client))
