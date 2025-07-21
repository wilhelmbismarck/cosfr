"""
# Configure

Configure is a database designed to store each servers settings.
"""

from discord  import Guild
from util.bot import ScratchPortals

empty_config = {'welcome'      : {'channel' : None},
                'scratch news' : {'channel' : None},
                'language'     : 'fr'
                }

from util.sub.database import backup_load, backup_save, database_check_integrity

def config_load(bot : ScratchPortals = None) -> dict :
    """
    # Configuration
    
    Open and parse `data/configure.wL` and return the result dict.
    Check if all registered guilds still have the bot. 
    """
    config = backup_load('configure')
    if bot is not None :
        for guildID in config   :
            config_guild_check(bot, config, guildID)
        for guild in bot.guilds :
            config_build(bot, config, guild)
    return config

def config_save(config : dict) :
    """
    # Configuration
    
    Save config dict to `data/configure.wL`.
    """
    backup_save(config, 'configure')
    
def config_build(bot : ScratchPortals, config, guild : Guild):
    """
    # Configuration
    
    Build and fix guild entry.
    """
    # if guild registered : check integrity
    if guild.id in config : 
        database_check_integrity(config[guild.id], empty_config)
        return 'already registered'
    # else : add guild
    config_guild_add(config, guild)
    return 'registered'
    
def config_guild_add(config : dict, guild : Guild):
    """
    # Configuration
    
    Add a guild to config. Return config dict.
    """
    # already registered ?
    if guild.id in config : return config
    # register guild
    config[guild.id] = {'welcome'      : {'channel' : None},
                        'scratch news' : {'channel' : None}
                        }
    return config

def config_guild_check(bot, config : dict, guild : Guild | int) -> bool :
    """
    # Configuration
    
    Check if a registered guild kicked the bot, in this case, remove the Guild entry.
    Return if the guild is present
    """
    # Check guild
    if isinstance(guild, Guild) : guild = guild.id
    # Scripts
    result = bot.get_guild(guild)
    if result is not None :
        return True
    del config[guild]
    return False
