# StatsBot Discord Bot

StatsBot is a Discord bot designed to provide server statistics through fancy counters. It is easy to set up, fully customizable, and updates automatically. This documentation will guide you through the setup, usage, and customization of StatsBot.

## Features

- **Fancy Counters**: Automatically updating counters for server statistics.
- **Easy Setup**: Set up the bot with a single command.
- **Fully Customizable**: Rename counters like normal Discord channels.
- **Dynamic Channel Creation**: Create various types of channels for counters.

## Table of Contents

- Installation
- Configuration
- Commands
  - /setup
  - /reset_setup
  - /help
- Customization
- Database
- Contributing
- License

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/KickingKats/StatsBot.git
    cd StatsBot
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a `config.json` file in the `data` directory with the following content:
    ```json
    {
        "TOKEN": "YOUR_BOT_TOKEN",
        "STATUS": "online",
        "ACTIVITY": "watching",
        "ACTIVITY_NAME": "server stats"
    }
    ```

5. Initialize the database:
    ```sh
    python -c "from data.database.database import init_db; init_db()"
    ```

6. Run the bot:
    ```sh
    python main.py
    ```

## Configuration

The `config.json` file in the `data` directory contains the bot's configuration settings. Update the values as needed:

- `TOKEN`: Your bot's token from the Discord Developer Portal.
- `STATUS`: The bot's status (e.g., online, idle, dnd).
- `ACTIVITY`: The type of activity (e.g., playing, streaming, listening, watching).
- `ACTIVITY_NAME`: The name of the activity.

## Commands

### /setup

Sets up the counters. Options:

- **channel_type**: Select the type of channel to create (Voice Channel, Text Channel, Announcement Channel, Stage Channel).
- **configuration**: Select the configuration of counters (Default Counters, Default, Channels and Roles, Default Boosts).

### /reset_setup

Resets the setup. Options:

- **action**: Select whether to delete the channels or reset the counters (Delete Channels, Reset Counters).

### /help

Displays information about all commands.

## Customization

All counters created by the bot are easy to customize. Simply rename the counters like normal Discord channels, and the bot will pick up the changes. The bot will always update the first number in the name, so it needs at least one number to work.

## Database

The bot uses an SQLite database to store guild IDs. The database is located in the `data/database` directory. The following functions are used to interact with the database:

- `init_db()`: Initializes the database.
- `add_guild(guild_id)`: Adds a guild ID to the database.
- `remove_guild(guild_id)`: Removes a guild ID from the database.
- `guild_exists(guild_id)`: Checks if a guild ID exists in the database.
- `get_guilds()`: Retrieves all guild IDs from the database.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes. Make sure to follow the coding standards and include tests for any new features or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
