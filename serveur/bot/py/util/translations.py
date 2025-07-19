"""
# Translations


"""

from util.sub.exceptions import TranslationKeyError, TranslationLangError, TranslationMissingValueError, TranslationCustomValueError

class Translations :
    """
    # Translations
    
    Allow the bot to be multilingual.
    """
    
    LANG_DATA = {'fr' : {'name' : 'Français', 'emoji' : '🇫🇷'},
                 'en' : {'name' : 'English',  'emoji' : '🇬🇧'},
                 }

    LANG_LIST = set(LANG_DATA.keys())

    empty_sheet = {'words'      : {'scratcher'  : "",
                                   'scratchers' : "",
                                   'user'       : "",
                                   'users'      : "",
                                   'member'     : "",
                                   'members'    : "",
                                   'channel'    : "",
                                   'channels'   : "",
                                   'guild'      : "",
                                   'guilds'     : "",
                                   'close'      : "",
                                   'closed'     : "",
                                   'rank'       : "",
                                   'ranks'      : "",
                                   'ranking'    : "",
                                   'rankings'   : "",
                                   'report'     : "",
                                   'reported'   : "",
                                   'edit'       : "",
                                   'exit'       : "",
                                   'thumb'      : "",
                                   'image'      : "",
                                   'scratch' : {'project'  : {':root' : "", 'love' : "", 'loves' : "", 'like' : ('redirect', 'love'), 'likes' : ('redirect', 'loves'), 'favorite' : "", 'favorites' : "", 'view' : "", 'views' : "", 'remix' : "", 'remixs' : "", 'remixed' : "", 'instructions' : "", 'credits' : "", 'shared' : ""},
                                                'projects' : ('redirect', 'project'),
                                                'studio'   : {':root' : "", "curator" : "", "curators" : "", "manager" : "", "managers" : "", "host" : "", "hosts" : "", "join" : "", 'activity' : ""},
                                                'studios'  : ('redirect', 'project'),
                                                'profile'  : {':root' : "", "follower" : "", "followers" : "", "following" : "", "pfp" : ""},
                                                'forum'    : {':root' : "", "topic" : "", "topics" : "", "post" : "", "posts" : "", "category" : "", "categories" : "", 'owner' : ""},
                                                'comment'  : {':root' : "", "comments" : "", "reply" : "", 'author' : ""},
                                                'comments' : ('redirect', 'comment'),
                                                ':root'    : ""
                                                },
                                   },
                   
                   'texts'      : {'about'    : "",
                                   'scratch'  : {'project' : {':root' : "", 'enableComments' : "", 'disableComments' : "", 'likeProject' : "", 'favoriteProject' : "", 'remixProject' : "", 'remixCredit' : "", 'disabledComments' : "", 'shareProject' : "", 'unshareProject' : ""},
                                                'studio'   : {':root' : "", "changeStudioHost" : "", "inviteCurator" : "", "promoteCurator" : "", "removeCurator" : "", "removeManager" : "", "openStudio" : "", "enableOpenStudio" : "", "disableOpenStudio" : "", "addProjectToStudio" : "", "followStudio" : "", 'unfollowStudio' : "", 'leaveStudio' : ""},
                                                'profile'  : {':root' : "", "followScratcher" : "", "unfollowScratcher" : "", "aboutMe" : ('redirect', "AM"), "AM" : "","whatI'mWorkingOn" : ('redirect', "WIWO"), "whatImWorkingOn" : ('redirect', "WIWO"), "WIWO" : "", "featuredProject" : "", "activity" : "", "sharedProjects" : "", "loveProjects" : "", "likeProjects" : ('redirect', "loveProjects"), "favoriteProjects" : "", "followingStudios" : "", "curatingStudios" : "", "enableComments" : "", "disableComments" : ""},
                                                'forum'    : {':root' : "", "createTopic" : "", "followTopic" : "", "closeTopic" : "", "sendPost" : "", "editPost" : "", "quotePost" : "", 'changeSign' : ""},
                                                ':root'    : ""
                                                },
                                   'pager'    : {'nextPage'     : "",
                                                 'previousPage' : "",
                                                 'minePage'     : "",
                                                 'firstPage'    : "",
                                                 'podium'       : "",
                                                 'lastPage'     : "",
                                                 ':root'        : ""
                                                }
                                   },
                   
                   'commands'   : {'configure'  :   {'welcome'  : {":root"     : "",
                                                                   "des"       : "",
                                                                   "eTitle"    : "",
                                                                   "eTypeErr"  : "",
                                                                   "eDisabled" : "",
                                                                   "eDefined"  : "",
                                                                   },
                                                     'language' : {":root"    : "",
                                                                   "des"      : "",
                                                                   "eTitle"   : "",
                                                                   "eField"   : "",
                                                                   "eDefined" : "",
                                                                   },
                                                     ':root' : "",
                                                     'des'   : "",
                                                     },
                                   
                                    'admin'     :   {
                                                     },
                                    
                                    'account'   :   {
                                                     },
                                    
                                    'sys'       :   {'no_perms' : {":root"  : "",
                                                                   "eTitle" : "",
                                                                   "eField" : ""
                                                                   }
                                                     } ,
                                    ':root'     : "commands"
                                   }
                   }
    
    def __init__(self):
        """
        # Translations
        
        Init translations as a class. Automatically search for `data/translations.wL` and load it, or follow `empty_sheet` template for each language.
        """
        self.db = {}
        self.backup_load()
    
    # Get
    
    def get(self, path : str, lg : str, transform : tuple = (True, False), **kwargs) :
        """
        # Translations
        ## Get
        
        Get an key folowing `path` (see `util.sub.database.database_get_by_path`) in `language`.
        
        ### Transform tuple
        The `transform` tuple manage text stylising. Optionnal.
        1. upper first (default : `True`)
        2. add point   (default : `False`)
        """
        from util.sub.database import database_get_by_path
        if not lg in self.LANG_LIST :
            raise TranslationLangError(lg)
        try :
            entry : str = database_get_by_path(self.db[lg], path, True)
        except KeyError :
            raise TranslationKeyError(path)
        if entry == "" : 
            raise TranslationMissingValueError(path, lg)
        if transform[0] :
            entry = entry.capitalize()
        if transform[1] :
            entry += '.'
        if '{' in entry and '}' in entry :
            build = ""
            i     = 0 
            while i < len(entry):
                lt = entry[i]
                if lt == '{' :
                    mem = i
                    i   = entry.find('}', i + 1, i + 19) 
                    if i == -1 : 
                        end = mem + 16
                        if end >= len(entry) : end = len(entry)
                        raise TranslationCustomValueError(entry[mem : mem + 16], mem)
                    else : 
                        name = entry[mem + 1 : i]
                        if not name in kwargs :
                            raise TranslationCustomValueError(name, mem)
                        build += str(kwargs[name])
                else : 
                    build += lt
                i += 1
            entry = build
        return entry

    # Keys
    
    def translations_key_new(self, category : str, key : str, values : dict) : 
        for lang in self.LANG_LIST :
            if not category in self.db : 
                self.db[lang][category] = {}
            if lang in values : 
                tr = values[lang]
            else              : 
                tr = "translation.missing"
            self.db[lang][category][key] = tr
    
    # Backups
    
    def backup_load(self) :
        """
        # Translations
        
        Open and parse `data/translations.wL` and return the result dict.  
        Check each language integrity.  
        """
        from util.sub.database import backup_load, database_check_integrity
        tr = backup_load('translations')
        for lang in self.LANG_LIST : 
            if lang not in tr :
                tr[lang] = {}
            database_check_integrity(tr[lang], self.empty_sheet)
        self.db = tr

    def backup_save(self) :
        """
        # Translations
        
        Save translations dict to `data/translations.wL`.
        """
        from util.sub.database import backup_save
        backup_save(self.db, 'translations', True)

emojis = {'account'   : ("account", 1394097657982488778),
          'favorite'  : ("favorite", 1394097958353506445),
          'favorites' : ('favorite', 'redirect'),
          'follow'    : ("follow", 1394094460660355153),
          'follows'   : ('follow', 'redirect'),
          'followers' : ('follow', 'redirect'),
          'following' : ("following", 1394094471922188430),
          'love'      : ("love", 1394094482227724328),
          'loves'     : ('love', 'redirect'),
          'like'      : ('love', 'redirect'),
          'likes'     : ('love', 'redirect'),
          'post'      : ("post", 1394094492096794855),
          'posts'     : ('post', 'redirect'),
          'project'   : ("project", 1394099406818771106),
          'projects'  : ('project', 'redirect'),
          'ranking'   : ("ranking", 1394099421133668402),
          'rankings'  : ('ranking', 'redirect'),
          'remix'     : ("remix", 1394094547314675752),
          'remixs'    : ('remix', 'redirect'),
          'remixed'   : ("remixed", 1394094575504851064),
          'remixing'  : ('remixed', 'remixed'),
          'studio'    : ("studio", 1394099443665600656),
          'studios'   : ('studio', 'redirect'),
          'topic'     : ("topic", 1394094600108380221),
          'topics'    : ('topic', 'redirect'),
          'view'      : ("view", 1394099432676655175),
          'views'     : ('view', 'redirect'),
          }
        
def __get_entry_from_key(key : str) :
    """
    # Emoji
    ## Get entry from key
    
    Return the entry corresponding to `key`. Support custom values, such as `redirect` (redirections).
    """
    if key not in emojis :
        raise KeyError(f"emoji {key} does not exist")
    else :
        entry = emojis[key]
        if isinstance(entry[1], str) :
            if entry[1] == 'redirect' :
                return __get_entry_from_key(entry[0])
        else : 
            return entry
        
def get_emoji(key : str) -> str :
    """
    # Emoji
    
    Return the custom emoji MarkDown (`str`) corresponding to `key`. Raises `KeyError` if key does not point at an entry.
    """
    # Get emoji
    entry = __get_entry_from_key(key)
    # Return MarkDown
    return f"<:{entry[0]}:{entry[1]}>"

def get_partial_emoji(key : str):
    """
    # Emoji
    
    Return a `discord.PartialEmoji` corresponding to `key`. Raises `KeyError` if key does not point at an entry.
    """   
    # Get emoji 
    entry = __get_entry_from_key(key)
    # Imports
    from discord import PartialEmoji
    # Return PartialEmoji
    return PartialEmoji(name = entry[0], id = entry[1])
