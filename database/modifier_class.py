"""This module contains the class for Modifiers for keeping track of/returning each one's information."""
from dataclasses import dataclass, asdict

@dataclass(frozen=True, kw_only=True)
class Modifier:
    codename: str
    name: str
    combat_type: str
    gen_zone: str
    dmg_type: str
    combat_rsc: str
    access_key: str

    def give_repr(self):
        return asdict(self)
    