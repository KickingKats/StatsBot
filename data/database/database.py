import sqlite3

def init_db():
    conn = sqlite3.connect('data/database/database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS guilds (guild_id INTEGER PRIMARY KEY)''')
    conn.commit()
    conn.close()

def add_guild(guild_id):
    conn = sqlite3.connect('data/database/database.db')
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)', (guild_id,))
    conn.commit()
    conn.close()

def remove_guild(guild_id):
    conn = sqlite3.connect('data/database/database.db')
    c = conn.cursor()
    c.execute('DELETE FROM guilds WHERE guild_id = ?', (guild_id,))
    conn.commit()
    conn.close()

def guild_exists(guild_id):
    conn = sqlite3.connect('data/database/database.db')
    c = conn.cursor()
    c.execute('SELECT 1 FROM guilds WHERE guild_id = ?', (guild_id,))
    exists = c.fetchone() is not None
    conn.close()
    return exists

def get_guilds():
    conn = sqlite3.connect('data/database/database.db')
    c = conn.cursor()
    c.execute('SELECT guild_id FROM guilds')
    guilds = c.fetchall()
    conn.close()
    return [guild[0] for guild in guilds]
