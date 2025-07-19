"""
# Process

Some utils to process data.
"""


def find_my(id, tab : list[tuple], at : int = 0):
    """
    # Process
    
    Find an id in a list of tuples. User is at `tuple[at]`. Returns its index.
    """
    for i in range(len(tab)) : 
        entry = tab[i]
        if len(entry) > at : 
            if entry[at] == id :
                return i
    return None