"""
# UTIL
## Exceptions
Contains different exceptions used by the bot.
"""

from discord        import Member, User
from scratchattach  import User, get_user, Project

class BotDatabase :
    """
    ## DB
    Bot AUTH Database. Allow to links Scratchers to Discord users.
    """
    
    empty_rank = {'projects' : {'views': None, 'loves': None, 'favorites': None},
                  'profile'  : {'followers': None},
                  'forum'    : {'posts': None}
                  }
    """
    ## DB
    Empty ranking sheet. Used to init rankings when creating a DB, or registering an user.
    """
    title_stat = {'projects' : {'views': "<:view:1394099432676655175> Vues", 'loves': "<:love:1394094482227724328> J'aimes", 'favorites': "<:favorite:1394097958353506445> Favoris", ':root' : "<:project:1394099406818771106> Projets"},
                  'profile'  : {'followers': "<:follow:1394094460660355153> Suiveurs", 'following': "<:following:1394094471922188430> Suit", ':root' : "<:account:1394097657982488778> Compte"},
                  'forum'    : {'posts': "<:post:1394094492096794855> Posts", 'topics' : "<:topic:1394094600108380221> Sujets", ':root' : "Forum"}
                  }
    """
    ## DB
    Text key associated with each board, category (`:root`) from stat.
    """

    def __init__(self, backup : str = None) :
        self.version  = 1
        self.rankings = {}
        self.db       = {}
        self.ranks_init()
        if backup is not None : 
            self.open()
            self.ranks_update()
        self.codes = {}
        
    ### RANKINGS
        
    def ranks_init(self) :
        """
        ## DB
        
        Init rankings (`self.ranking`). Create empty table for each board.
        """
        self.rankings = BotDatabase.empty_rank.copy()
        for category in self.rankings :
            for board in self.rankings[category] :
                self.rankings[category][board] = []
                
    def ranks_update(self) :
        """
        ## DB
        
        Update rankings for all boards, users.
        """
        print(f'RANK | upd :')
        rankings = { 'projects' : ['views', 'loves', 'favorites', None], 'profile' : ['followers', None], 'forum' : ['posts', None] }
        for category in rankings :
            for board in rankings[category] :
                if board is None : continue
                self.rankings[category][board] = self.__calc_rankings(path = category, board = board)
        print(f'RANK | upd ;')
        
    def __calc_rankings(self, path : str, board : str):
        """
        ## DB
        
        Calculate and update a ranking's `board`, belonging to category `path`.
        """
        # Imports
        from time import time
        # Data
        listID = self.db.keys()
        # Scripts
        print(f'RANK |     | calc [{path}][{board}], {len(listID)} entries')
        init_time = time()
        rankings  = []
        max_val  = 0
        for userID in listID :
            try :
                val     = int(self.db[userID]['stats'][path][board])
                max_val = max(val, max_val)
                rankings.append( (userID, val) )
            except :
                rankings.append( (userID, None) )
        rankings.sort(key = lambda x : x[1] if x is not None else max_val + 1, reverse = True)
        i = 1
        for userID, rank in rankings :
            self.db[userID]['ranks'][path][board] = i
            i += 1
        up_time = round((time() - init_time)*1000)/1000
        if up_time > 0.0 : print(f'RANK |     | calc DONE in {up_time} seconds')
        return rankings
    
    def __def_ranks(self, id : int):
        db_entry = self.user_get(id)
        db_entry['ranks'] = BotDatabase.empty_rank
        return
    
    def ranks_title(self, category : str, board : str = None) :
        """
        ## DB
        
        Return the key associated to a category, plus an optionnal board.
        """
        if not category in BotDatabase.title_stat :
            raise KeyError(f"\"{category}\" is not a rankings category")
        if board is None : 
            return BotDatabase.title_stat[category][':root']
        if not board in BotDatabase.title_stat[category] :
            raise KeyError(f"\"{board}\" is not a rankings board")
        return BotDatabase.title_stat[category][board]
        
    ### USERS
            
    def is_registered(self, user : int | Member | User) -> bool :
        """
        ## DB
        
        Return if `user` (either a `discord.Member | discord.User` or its ID) is registered.
        """
        if isinstance(user, int):
            return user in self.db
        if isinstance(user, (User, Member)) :
            return user.id in self.db
    
    def user_register(self, user_id : int, scratch_user : tuple[str, int]) :
        """
        ## DB
        
        Enregistre un utilisateur Discord / Scratch.
         - `user_id`      : identifiant de l'utilisateur Discord ;
         - `scratch_user` : tuple (`nom`, `id`).
         
        This do not backup DB, this means, if data is loss, user will not be registered from previous backups.
        """
        self.db[user_id] = {'id' : user_id, 'scratch' : {'id' : scratch_user[1], 'username' : scratch_user[0]}, 'stats' : {}, 'ranks' : {}}
        self.__def_ranks(user_id)
        self.__upd_stats(user_id)
    
    def user_remove(self, user : int | User | Member):
        """
        ## DB
        
        Remove an user (either a `discord.Member | discord.User` or its ID) from the database.
        
        This do not backup DB, if data is loss, as user will not be removed from previous backups, user will still be registered.
        """
        if isinstance(user, (Member, User)) :
            if user.id in self.db :
                del self.db[user.id]
        if isinstance(user, int) :
            if user in self.db :
                del self.db[user]
    
    def user_get(self, user : int | User | Member) -> dict :
        """
        ## DB
        
        Retourne l'entrée d'un utilisateur par son ID Discord.
        """
        if isinstance(user, int):
            if not user in self.db : raise KeyError(f'user id #{user} not in DB')
            return self.db[user]
        if isinstance(user, (User, Member)) :
            if not user.id in self.db : raise KeyError(f'user id #{user.id} not in DB')
            return self.db[user.id]
    
    def user_update(self, user : int | Member | User) :
        """
        ## DB
        
        Update one user (by ID) stats.
        """
        if isinstance(user, (Member, User)) :
            user = user.id
        self.__upd_stats(user)
    
    ### Generics
    
    def __len__(self) : 
        return len(self.db)
    
    def __iter__(self):
        for userID in self.db :
            try :
                yield (userID, self.db[userID]['scratch']['id'], self.db[userID]['scratch']['username'])
            except KeyError :
                continue
    
    def update(self) :
        """
        ## DB
        
        Mise à jour de la DB.
        `Attention` Gourmand en performances, et pour les APIs, ne pas spammer !
        """
        print(f'DB   | upd :')
        ## Updating Stats
        for userID in self.db : 
            print(f'DB         • {userID}')
            self.__upd_stats(userID)
        ## Calculating Ranks
        self.ranks_update()
        print(f'DB   | upd ;')
        
    ### STATS
    
    def __upd_stats(self, id : int):
        print('DB           • user_get')
        db_entry    = self.user_get(id)
        user : User = get_user(db_entry['scratch']['username'])
        stats = {'projects' : {'count' : 0, 'views' : 0, 'loves' : 0, 'favorites' : 0, 'remixs' : 0, 'remixed' : 0},
                 'profile'  : {'followers' : 0, 'following' : 0},
                 'forum'    : {'posts' : 0, 'topics' : 0, 'post_by_category' : {}}
                 }
        ## Get Projects Stats
        print('DB           • projects')
        project_count : int           = user.project_count()
        projects      : list[Project] = []
        stats['projects']['count']    = project_count
        for i in range(project_count) :
            project = user.projects(limit = 1, offset = i)[0]
            project.update()
            projects.append(project)
            stats['projects']['views']     += project.views
            stats['projects']['loves']     += project.loves
            stats['projects']['favorites'] += project.favorites
            stats['projects']['remixs']    += project.remix_count
            if project.remix_parent is not None : stats['projects']['remixed'] += 1
            print(f'DB             • {i+1}/{project_count}')
        ## Get Profile Stats
        stats['profile']['followers'] = user.follower_count()
        stats['profile']['following'] = user.following_count()
        ## Get Forum Stats
        # Planned
        ## Get Others Stats
        print('DB           • ocular')
        ocular = user.ocular_status()
        if   'status' in ocular : db_entry['bio']    = ocular['status']
        if   'color'  in ocular : db_entry['colour'] = ocular['color']
        elif 'colour' in ocular : db_entry['colour'] = ocular['colour']
        db_entry['stats'] = stats
        return
    
    ### Others
    
    def save(self):
        """save db into a backup"""
        # Imports
        from util.sub.database import backup_save
        from os                   import sep, rename, remove, path
        # Backup file
        print(f"DB   | save :")
        filepath = 'data' + sep + 'db'
        print(f"DB          • in {filepath}")
        # Moving old backup
        if path.exists(filepath + '.wL') :
            print(f"DB          • moving old")
            if path.exists(filepath + '_old.wL') :
                print(f"DB          • deleting former old")
                remove(filepath + '_old.wL')
            rename(filepath + '.wL', filepath + '_old.wL')
        # Creating backup
        print(f"DB          • saving")
        backup_save(self.db, 'db')
        print(f"DB   | save ; ")
        
    def open(self):
        """open a db backup and replace self by it"""
        # Imports
        from util.sub.database import backup_load
        # Scripts
        print(f"REGT | open :")
        print(f"REGT        • file is 'data/db.wL'")
        self.db = backup_load('db')
        print(f"REGT | open ; ")
            
    ### Auth Keys
            
    def add_key(self, key : int, user : Member | User) -> str :
        """Add a `key` to auth keys, and link it to `user`."""
        self.codes[key] = (user.id, None)
        return hex(key)[2:]
        
    def rem_key(self, key, user : tuple [str, int]) :
        """Remove a `key` from auth keys and register `user`."""
        if not key in self.codes : 
            raise KeyError('auth key does not exist')
        self.user_register(self.codes[key][0], user)
        del self.codes[key]
        
    def key_exist(self, key : int) :
        """Return if `key` exists."""
        return key in self.codes
    
    def key_user(self, key : int) :
        """Return the user associated with a `key.`"""
        if not key in self.codes :
            raise KeyError('auth key does not exist')
        return self.codes[key][0]

def buildBotDatabase():
    """Build BotDatabase from file if exist, else, from nil."""
    from os import path
    if path.exists(f'data/db.wL'):
        return BotDatabase('db')
    return BotDatabase()
