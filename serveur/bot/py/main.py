#
#
#
#
#

################## Initialisation     ##################
### Imports packages
import scratchattach        as     sa
import discord
import discord.app_commands as     discord_cmd
from   discord.ext          import tasks
from   datetime             import time
from   zoneinfo             import ZoneInfo
### Imports local packages
import util.sub.session     as myself
import util.sub.exceptions  as bot_exceptions
### Vérification de l'intégrité des données
if not myself.filled :
    raise RuntimeError('bot_data.py is unfilled')

################## Translations       ##################

from util.translations import Translations, get_partial_emoji
translations = Translations()

################## Historique         ##################
from util.logger import log_init
log_init()

################## Base de donnée     ##################
from util.auth import buildBotDatabase
auth_db = buildBotDatabase()

################## Session Scratch    ##################
ScratchSession = sa.login(myself.scratcher[0], myself.scratcher[1])

################## Authentification   ##################
print("AUTH | init :")

auth         = ScratchSession.connect_scratch_cloud(myself.auth_project_id)
auth_project = sa.get_project(myself.auth_project_id)
auth_events  = auth.events()

@auth_events.event
def on_ready() :
    # event handler ready
    print(f"AUTH        • auth running on {myself.auth_project_id} as {myself.scratcher[0]}")
    print(f"AUTH | init ;")

@auth_events.event
def on_set(activity : sa.CloudActivity) :
    # event on_set registered
    print(f"AUTH | Activity")
    key = activity.value
    # check for sys activity
    if key in ['0', '1', '2', '3', 0, 1, 2, 3] :
        print(f"AUTH |          | pass [sys]")
        return
    # check if activity can be a key
    try               : key = int(key)
    except ValueError :
        print(f"AUTH |          | pass [no int]")
        auth.set_var("auth", 3)
        return
    # check if key exist
    if not auth_db.key_exist(key) : 
        print(f"AUTH |          | pass [no key]")
        auth.set_var("auth", 3)
        return
    # identify actor
    activity.load_log_data()
    author = activity.actor()
    if author is None :
        author = activity.actor()
        if author is None :
            print(f"AUTH |          | pass [fail to identify actor]")
            auth.set_var("auth", 3)
            return
    # respond & register & del key
    print(f"AUTH |          | registering {author.username} [id:{author.id}] as <@{auth_db.key_user(key)}>")
    auth.set_var("auth", 1)
    auth_db.rem_key(key, (author.username, author.id))
    return
    
auth_events.start()

################## Bot                ##################

################## Commandes slash    ##################

################## Fonctions          ##################

## Scratch

def get_link_profile(username : str) -> str :
    """Retourne le lien vers le profil du scratcheur."""
    return f'https://scratch.mit.edu/users/{username}/'

def get_md_link_profile(username : str, title : str = None) -> str :
    """Retourne un lien formaté MarkDown vers le profil du scratcheur."""
    if title is None : title = username
    return f'[{title}](https://scratch.mit.edu/users/{username}/)'

def get_avatar_link(username : str) -> str :
    """Retourne le lien vers l'avateur du scratcheur."""
    user = sa.get_user(username)
    return f"{user.icon_url}"

## Utilitaires

def get_rank_text(txt : str) -> str:
    """Retourne un texte formaté MarkDown pour un rang donné. Considère None comme non classé.""" 
    if txt is None : return "`non classé`"
    return f"`{txt}`"

def get_lang(guild : discord.Guild) :
    """Return the guild if not found, or `en` (English) if not found."""
    if guild.id in bot.config :
        if 'language' in bot.config[guild.id] :
            return bot.config[guild.id]['language']
    return 'en'

################## Client             ##################
### Création du client

from util.bot import ScratchPortals

bot = ScratchPortals()

################## Configurations     ##################

from util.configure import config_load, config_save, config_guild_add

from util.bot import mainGuilds

mainGuildsObj = [discord.Object(guildID, type = discord.Guild) for guildID in mainGuilds]

################## Commandes          ##################

### Création des Groupes de commandes
class Compte(discord.app_commands.Group) : 
    # Lier un compte Scratch
    @discord_cmd.checks.has_permissions(use_application_commands = True)
    @discord.app_commands.command(name="lier", description="Lie un compte Scratch à votre compte Discord.")
    async def lier(self, interaction : discord.Interaction):
        # Vérifier si l'utilisateur est déjà lié
        if auth_db.is_registered(interaction.user) :
            db_entry = auth_db.user_get(interaction.user)
            username = db_entry['scratch']['username']
            resp_embed = bot.buildEmbed('info', title  = "Compte déjà lié",
                                                des    = "Il n'est possible de lier qu'**un seul compte Scratch par compte Discord**.",
                                                fields = [("Votre compte Scratch", f"Le compte Scratch actuellement lié à votre compte Discord est **[{username}]({get_link_profile(username)})**.")],
                                                thumb  = get_avatar_link(username)
                                                )
            await interaction.response.send_message(embed = resp_embed, ephemeral = True)
            return 
        # Trouver une clé
        cle = (interaction.user.id % (16**10))
        # Ajout de la clé dans auth_codes
        key = auth_db.add_key(cle, interaction.user)
        # Embed privé
        await interaction.response.send_message(embed = bot.buildEmbed('info',
                                                                       title = "Lier un compte Scratch",
                                                                       des   = f"Voici votre clé d'authentification, elle vous permet de lier un compte Scratch à votre compte Discord. Ne la communiquez à personne, elle est confidentielle.\n\n`{key}`\n\nUtilisez [le projet d'authentification]({auth_project.url}) pour utiliser cette clé et lier un compte Scratch à votre compte Discord."),
                                                ephemeral = True)
        return
    ###############################
    # Délier un compte Scratch
    @discord_cmd.checks.has_permissions(use_application_commands = True)
    @discord_cmd.command(name="délier", description="Délie votre compte Scratch de votre compte Discord.")
    async def délier(self, interaction : discord.Interaction):
        # Vérifier si l'utilisateur est lié
        if not auth_db.is_registered(interaction.user) :
            await interaction.response.send_message(embed = bot.buildEmbed('info', title = 'Compte non lié', des = "Votre compte n'a pas été lié."), ephemeral = True)
            return 
        # Get database entry, shortcuts
        db_entry = auth_db.user_get(interaction.user.id)
        db_username = db_entry['scratch']['username']
        # build Embed
        conf_embed    = bot.buildEmbed('confirmation', title = "Délier un compte Scratch", des = f"Voulez-vous vraiment délier votre compte Scratch **{db_username}** ?", thumb = get_avatar_link(db_username))
        conf_embed_ok = bot.buildEmbed('confirmation', title = "Délier un compte Scratch", des = f"Le compte Scratch **{db_username}** n'est plus lié à votre compte Discord.")
        conf_embed_no = bot.buildEmbed('confirmation', title = "Délier un compte Scratch", des = f"Action annulée, votre compte Scratch **{db_username}** est toujours lié à votre compte Discord.")
        # ask for confirmation
        conf = await bot.confirmation(interaction = interaction, embed = conf_embed, success = conf_embed_ok, cancel = conf_embed_no, buttons = ("Délier", "Annuler"))
        if not conf : return
        auth_db.user_remove(interaction.user)
    ###############################
    # Obtenir des informations sur le compte d'un utilisateur Discord
    @discord_cmd.checks.has_permissions(use_application_commands = True)
    @discord_cmd.command(name="profil", description="Obtenir des informations sur un compte Discord, et son compte Scratch associé.")
    async def profil(self, interaction : discord.Interaction, member : discord.Member = None):
        if member is None : member = interaction.user
        ### Get database entry, sortcuts
        try               :
            db_entry    = auth_db.user_get(member.id)
        except KeyError   :
            await interaction.response.send_message(embed = bot.buildEmbed('error', title = 'Entrée base de Donnée AUTH manquante', des = f"<@{member.id}> n'a pas lié son compte."), ephemeral = True)
            return
        try : 
            sc_username = db_entry['scratch']['username']
            sc_id       = db_entry['scratch']['id']
            sc_stats    = db_entry['stats']
            sc_ranks    = db_entry['ranks']
        except KeyError as e :
            await interaction.response.send_message(embed = bot.buildEmbed('error', title = 'Entrée base de Donnée AUTH incomplète', des = f"Données de <@{member.id}> manquantes.\n```py\n{e}\n```"), ephemeral = True)
            return 
        try :
            sc_color = db_entry['colour']
        except KeyError : 
            sc_color = ScratchPortals.embed_colors['scratch']
        try :
            sc_bio   = db_entry['bio']
        except KeyError : 
            sc_bio   = '*Aucun statut sur ocular*.'
        ### Build fields
        fields = []
        # - bio
        fields.append(("Bio", sc_bio, False))
        # - projects
        if int(sc_stats['projects']['count']) > 0 :
            fields.append(("<:project:1394099406818771106> Projets",   "", False))
            fields.append(("<:view:1394099432676655175> Vues",        f"`{sc_stats['projects']['views']}`",     True))
            fields.append(("<:love:1394094482227724328> J'aimes",     f"`{sc_stats['projects']['loves']}`",     True))
            fields.append(("<:favorite:1394097958353506445> Favoris", f"`{sc_stats['projects']['favorites']}`", True))
        # - profile
        fields.append(("<:account:1394097657982488778> Compte",   "", False))
        fields.append(("<:follow:1394094460660355153> Suiveurs", f"`{sc_stats['profile']['followers']}` scratcheurs", True))
        fields.append(("<:following:1394094471922188430> Suit",  f"`{sc_stats['profile']['following']}` scratcheurs", True))
        fields.append(("<:post:1394094492096794855> Posts",      f"`{sc_stats['forum']['posts']}` recensés",          True))
        # - ranks
        fields.append(("<:ranking:1394099421133668402> Rangs",        "", False))
        fields.append(("<:view:1394099432676655175> par Vues",       f"#`{get_rank_text(sc_ranks['projects']['views'])}`",    True))
        fields.append(("<:love:1394094482227724328> par J'aimes",    f"#`{get_rank_text(sc_ranks['projects']['loves'])}`",    True))
        fields.append(("<:follow:1394094460660355153> par Suiveurs", f"#`{get_rank_text(sc_ranks['profile']['followers'])}`", True))
        ### Build embed
        embed_cm = bot.buildEmbed('info',
                                  title  = f"Scratcheur {sc_username}",
                                  des    = f"Informations sur {get_md_link_profile(sc_username)} :",
                                  colour = discord.Color(0).from_str(sc_color),
                                  thumb  = get_avatar_link(sc_username),
                                  fields = fields
                                  )
        await interaction.response.send_message(embed = embed_cm)
        return
    ###############################
    # Obtenir les mieux classés d'un classement donné
    @discord_cmd.checks.has_permissions(use_application_commands = True)
    @discord_cmd.command(name="rangs", description="Obtenir les classements locaux.")
    async def rangs(self, interaction : discord.Interaction, page : int = None):
        from util.sub.process  import find_my
        from util.sub.database import database_get_by_path
        
        pagesize = 10
        
        lang     = get_lang(interaction.guild)
        
        rankings = auth_db.rankings
        max_page = (len(auth_db) // pagesize) + 1
        
        def get_page(page):
            if page is None     : page = 1
            if page <  1        : page = 1
            if page >  max_page : page = max_page
            if page * pagesize > len(auth_db) : 
                sel_range = ((page - 1) * pagesize, len(auth_db))
            else : 
                sel_range = ((page - 1) * pagesize, page * pagesize)
            return (page, sel_range)
                
        def build_embeds(limit) -> tuple[list[tuple[str, str]], dict[str, discord.Embed]] :
            rk_e = {}
            rk_b = []
            for c in rankings :
                for b in rankings[c] :
                    # Save board
                    ranksID = f"{c}/{b}"
                    rk_b.append((ranksID, translations.get(f"words/scratch/{ranksID}", lang), get_partial_emoji(b)))
                    # Gen embed
                    gen_embed = def_embed.copy()
                    # - ranks text
                    ranks = ""
                    for i in range(limit[0], limit[1]) :
                        userID = rankings[c][b][i][0]
                        ranks += f"#`{i+1}` ~ " + f"<@{userID}>" + "\n"
                    # - ranks field
                    gen_embed.add_field(name = f"{auth_db.ranks_title(c, b)}", value = ranks, inline = False)
                    # Save embed
                    rk_e[ranksID] = gen_embed
            return (rk_b, rk_e)
                
        page_items = [(':root', translations.get('texts/pager/podium', lang), '🏆'), (':mine', translations.get('texts/pager/minePage', lang), '⏺️'), (':back', translations.get('texts/pager/previousPage', lang), '⬅️'), (':next', translations.get('texts/pager/nextPage', lang), '➡️'), ('!exit', translations.get('words/exit', lang), '🛑')]
        
        await interaction.response.send_message(embed = bot.buildEmbed('info', title = "Classements", des = "Génération des classements, veuillez patienter."))
        
        # Loop
        button_focus = None
        run          = True
        while run :
            # Check page
            page, entries_range = get_page(page)
            # Build default embed
            def_embed = bot.buildEmbed('info', 'Classements', f"Classements, de la **{entries_range[0] + 1}e** place à la **{entries_range[1]}e** place.")
            # Genereate board, embeds
            ranks_build  = build_embeds(entries_range)
            ranks_boards = ranks_build[0]
            ranks_embeds = ranks_build[1]
            if button_focus is None : button_focus = ranks_boards[0][0]
            # Generate view
            ranks_view = bot.ChoiceView(ranks_boards + page_items, button_focus)
            # Edit message
            await interaction.edit_original_response(embed = ranks_embeds[button_focus], view = ranks_view)
            # Manage view interactions
            timeout = await ranks_view.wait()
            if timeout :
                run = False
            elif ranks_view.value == '!exit' :
                run = False
            elif ranks_view.value == ':root' : 
                page = 1
            elif ranks_view.value == ':mine' : 
                tmp = find_my(interaction.user.id, database_get_by_path(rankings, button_focus), at = 0)
                if tmp is not None : 
                    page = (tmp // 1) + 1
                else : 
                    interaction.followup.send(embed = bot.buildEmbed('error', "Impossible de vous trouver dans les classements", des = "Vous n'avez pas lié de compte Scratch, ou n'êtes pas encore indexé."))
            elif ranks_view.value == ':back' : 
                if page > 1 : 
                    page -= 1
            elif ranks_view.value == ':next' : 
                if page < max_page : 
                    page += 1
            else : 
                button_focus = ranks_view.value
            # loop 
        await interaction.edit_original_response(view = None)
        return
        
    ###############################
    
class Admin(discord.app_commands.Group) :
    # Sauvegarder les Auth
    @discord_cmd.checks.has_permissions(administrator = True)
    @discord_cmd.command(name="sauver", description="Sauvegarde les authentifications.")
    async def sauver(self, interaction : discord.Interaction):
        if not discord.app_commands.checks.has_permissions(administrator = True): 
            await interaction.response.send_message(embed = bot.buildEmbed('error', title = 'Permissions insuffisantes', des = 'Vous ne disposez pas de permission suffisantes pour exécuter cette commande'), ephemeral = True)
            return
        auth_db.save()
        await interaction.response.send_message(embed = bot.buildEmbed('info', title = f'Sauvegarde de la Base de Donnée AUTH', des = 'Données sauvegardées manuellement.'))
    ###############################
    # Informations sur les Auths
    @discord_cmd.checks.has_permissions(administrator = True)
    @discord_cmd.command(name="authinfo", description="Consulter les authentifications enregistrées.")
    async def authinfo(self, interaction : discord.Interaction, début : int = 0, plage : int = 10):
        if not discord.app_commands.checks.has_permissions(administrator = True): 
            await interaction.response.send_message(embed = bot.buildEmbed('error', title = 'Permissions insuffisantes', des = 'Vous ne disposez pas de permission suffisantes pour exécuter cette commande'), ephemeral = True)
            return
        auth_list = [cp for cp in auth_db]
        auth_list_len = len(auth_list)
        plage = max(min(25, plage), 10)
        début = max(0, début)
        if début >= auth_list_len :
            await interaction.response.send_message(embed = bot.buildEmbed('error', title = 'Base de Donnée AUTH', des = f"**Erreur** : Index de début de pagination (`{début}`) en dehors des données (`{auth_list_len}`)."), ephemeral = True)
            return
        fin          : int           = min(début + plage, auth_list_len)
        auth_extract : list          = sorted(auth_list, key = (lambda x : str(x[1]).lower()) )[début:fin]
        emb_list     : discord.Embed = bot.buildEmbed('info', title = f'Base de Donnée AUTH', des = f'Authenfications enregistrées [{début + 1} ~ {fin} / {auth_list_len} ].')
        for discordID, scratchID, scratchNAME in auth_extract : 
            emb_list.add_field(name = f"{scratchNAME} ~ #`{scratchID}`", value = f"<@{discordID}> ~ `{discordID}` ({get_md_link_profile(scratchNAME, 'profil')})", inline = True)
        await interaction.response.send_message(embed = emb_list)
        return
    ###############################
    # Afficher les données brutes d'une entrée de la DB
    @discord_cmd.checks.has_permissions(administrator = True)
    @discord_cmd.command(name="entrée", description="Obtenir les donnes brutes d'une authenfication.")
    async def entrée(self, interaction : discord.Interaction, member : discord.Member = None):
        if not discord.app_commands.checks.has_permissions(administrator = True): 
            await interaction.response.send_message(embed = bot.buildEmbed('error', title = 'Permissions insuffisantes', des = 'Vous ne disposez pas de permission suffisantes pour exécuter cette commande'), ephemeral = True)
            return
        if member is None : member = interaction.user
        from json import dumps
        try             :
            memberID   = member.id
            memberDATA = auth_db.user_get(memberID)
            emb      = bot.buildEmbed('info', title = 'Entrée Base de Donnée AUTH', des = f"Entrée de <@{memberID}> :\n```JSON\n{dumps(memberDATA, indent = 4, ensure_ascii = False)}\n```")
            await interaction.response.send_message(embed = emb, ephemeral = True)
        except KeyError : 
            await interaction.response.send_message(embed = bot.buildEmbed('error', title = 'Entrée base de Donnée AUTH manquante', des = f"<@{memberID}> n'a pas lié son compte."), ephemeral = True)
        return
    ###############################
    # Éteindre le bot
    @discord_cmd.checks.has_permissions(administrator = True)
    @discord_cmd.command(name="éteindre", description="Éteint le bot.")
    async def éteindre(self, interaction : discord.Interaction):
        if not discord.app_commands.checks.has_permissions(administrator = True): 
            await interaction.response.send_message(embed = bot.buildEmbed('error', title = 'Permissions insuffisantes', des = 'Vous ne disposez pas de permission suffisantes pour exécuter cette commande'), ephemeral = True)
            return
        conf_embed    = bot.buildEmbed('confirmation', title = f"Éteindre {bot.user.name}",          des = "Voulez-vous vraiment éteindre le bot ?")
        conf_embed_ok = bot.buildEmbed('confirmation', title = f"Éteindre {bot.user.name} (annulé)", des = "Le bot reste en ligne.")
        conf_embed_no = bot.buildEmbed('confirmation', title = f"Éteindre {bot.user.name}",          des = "Le bot va progressivement être mis hors-ligne.")
        conf = await bot.confirmation(interaction = interaction, embed = conf_embed, success = conf_embed_ok, cancel = conf_embed_no, buttons = ("Maintenir en ligne", "Éteindre"))
        if conf : return
        bot.before_close(auth_db, auth, translations)
        await bot.close()
        return
    ###############################
    
class Configure(discord.app_commands.Group) :
    # Définir un salon d'accueil
    @discord_cmd.checks.has_permissions(manage_guild = True)
    @discord_cmd.command(name="accueil", description="Définir un salon d'accueil. Le bot y accueillera vos nouveaux membres. Laisser vide pour désactiver.")
    async def accueil(self, interaction : discord.Interaction, salon : discord.TextChannel = None):
        if not discord.app_commands.checks.has_permissions(manage_guild = True): 
            await interaction.response.send_message(embed = bot.buildEmbed('error', title = 'Permissions insuffisantes', des = 'Vous ne disposez pas de permission suffisantes pour exécuter cette commande'), ephemeral = True)
            return
        if salon is None : 
            bot.config[guild.id]['welcome']['channel'] = None
            await interaction.response.send_message(embed = bot.buildEmbed('info', title = "Configuration [salon d'accueil]", des = "Fonctionnalité désactivée."))
        if not isinstance(salon, (discord.TextChannel)) : 
            await interaction.response.send_message(embed = bot.buildEmbed('error', title = "Configuration [salon d'accueil]", des = f"Impossible de définir le salon d'accueil.\nType incorrect : `{type(channel)}`."), ephemeral = True)
            return
        guild = salon.guild
        if not guild.id in bot.config : raise bot_exceptions.UnknowGuildError(self, guild)
        bot.config[guild.id]['welcome']['channel'] = salon.id
        await interaction.response.send_message(embed = bot.buildEmbed('info', title = "Configuration [salon d'accueil]", des = f"Le nouveau salon d'accueil est <#{salon.id}>."))
        return
    ###############################
    # Définir un salon d'accueil
    @discord_cmd.checks.has_permissions(manage_guild = True)
    @discord_cmd.command(name = "langue", description = "Choisir la langue du serveur.")
    async def langue(self, interaction : discord.Interaction):
        if not discord.app_commands.checks.has_permissions(manage_guild = True): 
            await interaction.response.send_message(embed = bot.buildEmbed('error', title = 'Permissions insuffisantes', des = 'Vous ne disposez pas de permission suffisantes pour exécuter cette commande'), ephemeral = True)
            return
        lang = get_lang(interaction.guild)
        
        lang_embed   = bot.buildEmbed('info', title = translations.get('commands/configure/language/eTitle', lang), des = translations.get('commands/configure/language/eField', lang))
        lang_choices = []
        for langID, entry in translations.LANG_DATA.items() :
            lang_choices.append( (langID, entry['name'], entry['emoji']) )
        
        lang_choices.append(('!exit', translations.get('words/exit', lang), '🛑'))
        
        lang_view  = bot.ChoiceView(lang_choices, lang)
        
        await interaction.response.send_message(embed = lang_embed, view = lang_view)
        
        timeout = await lang_view.wait()
        
        if timeout : 
            return
        if lang_view.value == '!exit' :
            return
        
        lang = lang_view.value
        
        bot.config[interaction.guild.id]['language'] = lang
        fullname = translations.LANG_DATA[lang]['name']
        
        await interaction.edit_original_response(embed = bot.buildEmbed('info', title = translations.get('commands/configure/language/eTitle', lang), des = translations.get('commands/configure/language/eDefined', lang, language = lang, fullname = fullname)), view = None)
        
        return
    ###############################

### Ajout des Groupes de commandes

bot.tree.add_command(   Compte(name = "compte",     description = "Informations sur un compte Scratch"), guilds = mainGuildsObj)
bot.tree.add_command(    Admin(name = "admin",      description = "Commandes administrateurs"),          guilds = mainGuildsObj)
bot.tree.add_command(Configure(name = "configure",  description = "Configurer le bot"),                  guilds = mainGuildsObj)

################## Time events       ##################

@tasks.loop(time = time(hour = 0, minute = 19, tzinfo = ZoneInfo('Europe/Paris')))
async def midnight_works():
    print('TIME | midnight works :')
    print('     • auth_db save ')
    auth_db.save()
    print('     • auth_db update ')
    auth_db.update()
    print('     • configure save ')
    config_save(bot.config)
    print('TIME | midnight works ;')
    
@midnight_works.before_loop
async def before():
    await bot.wait_until_ready()
    # await the bot trigger on_ready

################## Discord events    ##################

@bot.event
async def on_ready():
    print(f'BOT  | init :')
    print(f'BOT         • configure')
    # Get Configuration
    bot.config = config_load(bot)
    # Update main
    for guild in mainGuildsObj :
        try : 
            await bot.tree.sync(guild = guild)
            print(f"BOT           • sync {guild.id}")
        except discord.Forbidden : 
            print(f"BOT           • deny {guild.id}")
        except Exception as e : 
            print(f"BOT           • lost traceback {e}")
    print(f'BOT         • sync all guilds is disabled')
    # Update all
    # bot.tree.sync()
    print(f'BOT         • starting time events')
    midnight_works.start()
    print(f'BOT         • running as <@{bot.user.id}>')
    print(f"BOT  | init ;")
    
@bot.event
async def on_guild_join(guild : discord.Guild):
    print(f"BOT  | new guild : {guild.name} #{guild.id}")
    config_guild_add(bot.config, guild)

@bot.event
async def on_member_join(member : discord.Member):
    if member.id == bot.user.id :
        return
    try             :
        channelID = bot.config[member.guild.id]['welcome']['channel']
        if channelID is None : return
        channel   = member.guild.get_channel(channelID)
    except KeyError :
        raise bot_exceptions.UnknowGuildError('@events.on_member_join', member.guild)
    from util.sendable import image_welcome
    await image_welcome(member, channel)
    return
    
################## Gestion des Erreurs ##################

#bot.on_command_error()

# Gérer • MissingPermissions
#       • MissingAnyRole
#       • MissingRole
#       • NoPrivateMessage
#       • CheckFailure
#       • TranslationError
#       • TransformerError
#       • CommandInvokeError
#       • CommandSyncFailure
# Local • UnknowGuildError (guild is not registered)
#       • UnknowUserError  (user not in AUTH database)
#       • UnknowEmbedError (embed model)
#       • NoButtonsError   (view no buttons)

################## Exécution du Bot ##################

bot.run(token = myself.token, log_handler = None)
