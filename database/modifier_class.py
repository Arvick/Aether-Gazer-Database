"""This module contains the class for Modifiers for keeping track of/returning each one's information."""


class Modifier:

    def __init__(self, *, codename:str, name:str, combat_type:str, gen_zone:str,
                 dmg_type:str, combat_rsc:str, access_key:str) -> None:
        self._codename = codename
        self._name = name
        self._combat_type = combat_type
        self._gen_zone = gen_zone
        self._dmg_type = dmg_type
        self._combat_rsc = combat_rsc
        self._access_key = access_key
    
    
    