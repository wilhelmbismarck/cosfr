"""
# UTIL
## Exceptions
Contains different exceptions used by the bot.
"""

from discord import Guild, User, Member
from discord.app_commands import Command, AppCommandError

class UnknowGuildError(AppCommandError):
    """
    ## UnknowGuildError
    Unknow GUILD - the bot does not have registered the guild.
    """
    def __init__(self, command : Command | str, guild : Guild):
        """Guild is not registered in configure."""
        self.message = f"unknow guild : `{guild.id}` ~ \"{guild.name}\""
        if isinstance(command, str)     : self.message += f' at `{command}`'
        if isinstance(command, Command) : self.message += f' cmd `{command.name}`'
        super().__init__(command, self)
        
class UnknowUserError(AppCommandError):
    """
    ## UnknowUserError
    Unknow USER - member / user is not registered.
    """
    def __init__(self, command : Command | str, guild : Guild, user : User | Member):
        """User | Member is not registered in db"""
        self.message = f"unknow guild : `{guild.id}` ~ \"{guild.name}\""
        super().__init__(command, self)
        
class UnknowEmbedError(Exception):
    """
    ## UnknowEmbedError
    Unknow EMBED - model do not exist.
    """
    def __init__(self, model : str) :
        self.message = f"unknow embed model : \"{model}\""
        super().__init__(self.message)
        
class NoButtonsError(Exception):
    """
    ## NoButtonsError
    View error - no buttons provided.
    """
    def __init__(self, message : str) :
        self.message = message
        super().__init__(self.message)
        
class TranslationKeyError(Exception):
    """
    ## TranslationKeyError
    Translation error - key does not exist.
    """
    def __init__(self, key : str) :
        self.message = f"key {key} does not exist"
        super().__init__(self.message)
        
class TranslationMissingValueError(Exception):
    """
    ## TranslationMissingValueError
    Translation error - key is not provided for current language.
    """
    def __init__(self, key : str, language : str) :
        self.message = f"key {key} is not provided for lang \"{language}\""
        super().__init__(self.message)
        
class TranslationLangError(Exception):
    """
    ## TranslationLangError
    Translation error - lang does not exist.
    """
    def __init__(self, language : str) :
        self.message = f"language \"{language}\" does not exist"
        super().__init__(self.message)

class TranslationCustomValueError(Exception):
    """
    ## TranslationCustomValueError
    Translation error - custom kwarg does not exist / too long.
    """
    def __init__(self, arg : str, i : int = 0) :
        self.message = f"custom value \"{arg}\" (at {i}) does not exist or is too long"
        super().__init__(self.message)