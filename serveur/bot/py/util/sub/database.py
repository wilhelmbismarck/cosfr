"""
# Database

Build, manage and save python `dict` as wL files.
"""

def backup_load(file : str) -> dict :
    """
    # Database
    ## Backups / Load
    
    Open and parse `data/{file}.wL` and return the result dict.
    Check if all registered guilds still have the bot. 
    """
    # Imports
    from wLpylib.parser import loads
    from pathlib        import Path
    # file parse
    path = Path(f"data/{file}.wL")
    if not path.exists() :
        return {}
    return loads(path)

def backup_save(database : dict, file : str, do_lines : bool = False) :
    """
    # Database
    ## Backups / Save
    
    Save database dict to `data/{file}.wL`.
    """
    # Imports
    from wLpylib.exporter import exports, ExportConfig
    from pathlib          import Path
    # file export
    path = Path(f"data/{file}.wL")
    exports(database, path, ExportConfig(src = {'do_lines' : do_lines}))
    
def database_check_integrity(database : dict, corrector : dict) -> dict:
        """
        # Database
        ## Check / Integrity
        
        Recursively corrects `database : dict` by adding missing keys from `corrector : dict`.
        If a value is a dictionary, it is recursively corrected.
        """
        for key, default_value in corrector.items():
            if key not in database :
                database[key] = default_value
            elif isinstance(default_value, dict) and isinstance(database[key], dict):
                database_check_integrity(database[key], default_value)
        return database
    
def database_get_by_path(database : dict, path : str, raiseErrors : bool = False) -> str | int | dict :
    """
    # Database
    ## Get / by Path
    
    Get key following `path`. Do not raise `KeyError` for a missing key, as keys are added as empty dicts if needed.
    
    For instance, `guilds/int:1234/id` = `['guilds'][1234]['id']` while `guilds/1234/id` = `['guilds']['1234']['id']`).
    """
    paths = [""]
    write = "str"
    for i in range(len(path)) :
        lt = path[i]
        if   lt == '/' : 
            if write != "str" : 
                if   write == "int"   : paths[-1] = int(paths[-1])
                elif write == "float" : paths[-1] = float(paths[-1])
                else                  : raise ValueError(f"path type \"{write}\" is not supported")
            paths.append("")
            write = "str"
        elif lt == ':' :
            if len(paths[-1]) > 0 :
                write     = paths[-1]
                paths[-1] = ""
        else : 
            paths[-1] += lt
    build = ""
    for key in paths : 
        if not key in database : 
            if raiseErrors :
                raise KeyError(f"`{key}` do not reach any dict key, at `{build}`.")
            else : 
                database[key] = {}
        if   isinstance(database[key], tuple) :
            if database[key][0] == 'redirect' :
                key = database[key][1]
        elif isinstance(database[key], dict)  :
            if   False in database[key] and True in database[key] : 
                if database[key][False] == 'redirect' :
                    key = database[key][True]
            elif 0 in database[key] and 1 in database[key] :
                if database[key][0] == 'redirect' :
                    key = database[key][1]
        build += str(key) + "/"
        database = database[key]
    return database
