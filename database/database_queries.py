"""This module holds functions that make queries to the database, and returns the results."""

'''modifier: search by:
1. real name
2. modifier name
3. gen zone
4. meele vs physical
5. element
6. resource


functor: search by
1. name
2. gen zone
3. reccomended modifier
4. rarity

sigil: search by
1. name
2. keywords (something like "give me any sigil sets who have this keyword in their description")
'''
from pathlib import Path
import sqlite3
from modifier_class import Modifier


PATH_TO_DB = Path.cwd() / "aether_gazer.db"

def connection_decorator(func):
    """A decorator function that creates a connection to the database,
    executes the function, then closes the connection"""
    def execute(*args, **kwargs):
        connection:sqlite3.Connection = sqlite3.connect(PATH_TO_DB)
        result = func(connection, *args, **kwargs)
        connection.close()
        return result
    return execute

#TODO: write class for Modifier
#TODO: Separate classes/modules/tests for sigils, functors
'''
SELECT s.set_name, s.set_effects, sm.odd_or_even FROM sigil AS s
INNER JOIN sigil_modifier AS sm ON sm.set_name = s.set_name
WHERE sm.modifier_name = "Rahu";
'''

@connection_decorator
def _mod_search(connection:sqlite3.Connection, args:dict[str:str|int]) -> list[dict[str|int]]:
    """Makes a SELECT query to the 'modifier' table and returns the infomration of each 
    result in the form of dictionaries."""
    query_result = connection.execute(
        f'''SELECT modifier_name, name, combat_type, gen_zone,
            dmg_type, combat_rsc, access_key
                FROM modifier
                WHERE {'=? AND '.join([f'{key}' for key in args.keys()])}=?;''',
                list(args.values()))
    results = []
    latest = query_result.fetchone()
    while latest is not None:
        results.append(Modifier(*latest).give_repr())
        latest = query_result.fetchone()
    for idx in range(len(results)):
        query_result = connection.execute(f'''
        SELECT s.set_name, s.set_effects, sm.odd_or_even FROM sigil AS s
        INNER JOIN sigil_modifier AS sm ON sm.set_name = s.set_name
        WHERE sm.modifier_name =?;''', [results[idx]["codename"]])
        new_results = sorted(query_result.fetchall(), key = lambda x: x [-1])
        results[idx] |= {
            "recommended sigil set: even": f"{new_results[0][0]}: {new_results[0][1]}",
            "recommended sigil set: odd": f"{new_results[1][0]}: {new_results[1][1]}"
        }
    for idx in range(len(results)):
        query_result = connection.execute
    return results


@connection_decorator
def _functor_search():
    # TODO: add dict for ATK boosts based on rarity
    pass


@connection_decorator
def _sigil_search():
    pass


def interface():
    pass

if __name__ == "__main__":
    print(PATH_TO_DB)
    print(_mod_search({"name": "Asura"}))
    

    #TODO: unpack param names and tuple into a new dict 