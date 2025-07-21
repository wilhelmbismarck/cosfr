from discord.ext.commands import Bot
from discord.ui import View, button, Button
from discord import Interaction, Guild, Intents, Colour, Embed, ButtonStyle, PartialEmoji

from util.sub.exceptions import *
from util.translations   import Translations

mainGuilds = [1160187652184735815, 1242127738702135316]

class ScratchPortals(Bot):
    """Scratch Portals"""
    
    embed_models = ('info', 'error', 'confirmation')
    embed_colors = {'error' : "#b21948", 'info' : "#e8dcff", 'confirmation' : "#009b50", 'scratch' : '#855cd6', 'scratch_alt' : '#ffab19'}

    def __init__(self, name : str = "Scratch Portals") :
        botIntents = Intents.default()
        # Intents
        botIntents.messages        = True
        botIntents.message_content = True
        botIntents.members         = True
        botIntents.guilds          = True
        # Self
        self.botName = name
        self.config  = {}
        self.transl  = Translations()
        super().__init__('?', intents = botIntents)
        
    def tr(self, guild : Guild, path : str, transform : tuple = (True, False), args : dict = {}) :
        """
        # ScratchPortals
        ## get Translation
        
        Return the translation of `path` according to `guild` language.-
        - `transform` -> transform tuple (see `translations.py`) ;
        - `args` -> a dict of values, for custom entries ;
        """
        lang = self.__safe_language(guild)
        return self.transl.get(path, lang, transform, args)
    
    def number(self, guild : Guild, number : int | str) :
        """
        # ScratchPortals
        ## get Number
        
        Return a stylised number.
        """
        lang = self.__safe_language(guild)
        sep  = self.transl.LANG_DATA[lang]['num sep']
        if isinstance(number, int) : 
            number = str(number)
        build = ""
        for i in range(0, len(number), 3) :
            if i > 0 : 
                build = build + sep
            if i + 3 < len(number):
                build = build + number[i : i + 3]
            else : 
                build = build + number[i : ]
        return build
                         
    def buildEmbed(self, model : str = "info", title : str = "Embed", des : str = "Contenu de l'Embed", thumb : str = None, image : str = None, footer : tuple[str, str] = None, fields : list[tuple[str, str, bool]] = None, colour : Colour = None) :
        """
        # ScratchPortals
        ## buildEmbed
        
        Allow to easily build `discord.Embeds`.
        """
        if not model in ScratchPortals.embed_models :
            raise UnknowEmbedError(model)
        if colour is None : 
            colour = Colour(0).from_str(ScratchPortals.embed_colors[model])
        buildEmbed = Embed(title = title, description = des, colour = colour)
        if fields is not None :
            for field in fields :
                if len(field) == 3 : is_inline = field[2]
                else               : is_inline = False
                buildEmbed.add_field(name = field[0], value = field[1], inline = is_inline)
        if thumb is not None : 
            buildEmbed.set_thumbnail(url = thumb)
        if image is not None : 
            buildEmbed.set_image(url = image)
        if footer is not None : 
            buildEmbed.set_footer(text = footer[0], icon_url = footer[1])
        buildEmbed.set_author(name = self.user.name, icon_url = self.user.avatar.url)
        return buildEmbed
    
    def embedNewLine(self, embed : Embed, remaining : int = None) :
        """
        # ScratchPortals
        ## buildEmbed ~ NewLine
        
        """
        if remaining is None :
            embed.add_field(name = "", val = "", inline = False)
        else : 
            for i in range(remaining):
                embed.add_field(name = "", val = "", inline = True)
    
    async def confirmation(self, interaction : Interaction, embed : Embed, success : Embed = None, cancel : Embed = None, buttons : tuple = ("Confirmer", "Annuler")) -> bool :
        """
        ## Confirmation
        Ask confirmation for an act, returns `bool`.
        
        All args, except `interaction : discord.Interaction` and `embed : discord.Embed`, are `* : tuple[str, str]`.
        """
        if success is None : 
            success = self.buildEmbed('confirmation', title = 'Confirmation acquise', des = "L'action va être effectuée, veuillez patienter.")
        if cancel  is None : 
            cancel  = self.buildEmbed('confirmation', title = 'Confirmation refusée', des = "Exécution annulée.")
        # ("Confirmation acquise", "L'action va être effectuée.")
        # ("Action annulée", "L'action ne sera pas exécutée.")
        
        ## Classe ConfirmationView
        class ConfirmationView(View):
            def __init__(self, success : tuple, cancel : tuple, buttons : tuple):
                super().__init__(timeout = 10)
                self.value   = False
                self.success = success
                self.embed   = embed
                self.cancel  = cancel

            @button(label = buttons[0], style = ButtonStyle.success)
            async def confirm(self, interaction : Interaction, button : Button):
                self.value = True
                await interaction.response.edit_message(embed = self.success, view = None, delete_after = 60)
                self.stop()

            @button(label = buttons[1], style = ButtonStyle.danger)
            async def cancel(self, interaction : Interaction, button : Button):
                self.value = False
                await interaction.response.edit_message(embed = self.cancel, view = None, delete_after = 60)
                self.stop()
        # Build View     
        conf = ConfirmationView(success, cancel, buttons)
        # Await send, User interaction
        await interaction.response.send_message(embed = embed, view = conf)
        await conf.wait()
        # Safe return
        return conf.value
    
    class ChoiceView(View):
        """
        # ChoiceView
        
        A `discord.View` allowing users to make a choice.
        """
        
        def __init__(self, choices : list[tuple[str, str, str | PartialEmoji]], currentID : int = None, page : int = None, page_range : tuple[int, int] = None):
            """
            A `ChoiceView` allows the user to choose an item.
            
            - `choices` is a `list` of `tuple[str, str]` where tuple's first item is its ID and second item is its label ;
            - `currentID` is the currently selected item's ID ;
            
            When a item is chosen, its ID is returned.
            There should always be an exit choice.
            """
            super().__init__(timeout = 60)
            
            if currentID is None : currentID = choices[0][1]
            self.value = currentID
            
            for choiceID, label, emoji in choices :
                if   choiceID == currentID : 
                    button = Button(label = label, style = ButtonStyle.green, disabled = True, emoji = emoji)
                elif choiceID[0] == '!' : 
                    button = Button(label = label, style = ButtonStyle.danger, emoji = emoji)
                elif choiceID[0] == ':' : 
                    disable = False
                    if page is not None and page_range is not None : 
                        if   choiceID in [':root', ':back'] and page == page_range[0]: 
                            disable = True
                        elif choiceID in [':last', ':next'] and page == page_range[1]:
                            disable = True
                    button = Button(label = label, style = ButtonStyle.primary, emoji = emoji, disabled = disable)
                else :
                    button = Button(label = label, style = ButtonStyle.secondary, emoji = emoji)
                button.callback = self.returnID(choiceID)
                self.add_item(button)
                
        def returnID(self, choiceID : int):
            async def callback(interaction : Interaction):
                self.value = choiceID
                self.stop()
                await interaction.response.defer()
            return callback   
    
    def before_close(self, auth_db, auth_cloud, translations):
        """
        # ScratchPortals
        ## Before Close
        
        Tasks to run before closing
        """
        print('MAIN | close :')
        print('BOT          • saving auth database :')
        auth_db.save()
        print('AUTH         • Scloud disconnecting')
        auth_cloud.disconnect()
        print('BOT          • saving configs')
        from util.configure import config_save
        config_save(self.config)
        print('BOT          • saving translations')
        translations.backup_save()
        print('MAIN | close ;')
        
    async def missing_permissions(self, interaction : Interaction):
        """
        # ScratchPortals
        ## Missing permissions embed
    
        Gen & send a `missing perms` embed.
        """
        await interaction.response.send_message(embed = self.buildEmbed('error', title = self.tr(interaction.guild, 'commands/sys/no_perms/eTitle')), des = self.tr(interaction.guild, 'commands/sys/no_perms/eField'), view = None, ephemeral = True)
        
    def __safe_language(self, guild : Guild) :
        if guild.id in self.config :
            lang = self.config[guild.id]['language']
        else : 
            lang = 'fr'
        return lang
