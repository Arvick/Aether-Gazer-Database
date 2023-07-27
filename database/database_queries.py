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
import json
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


def _add_sigils(results:list[dict[str:str]], connection:sqlite3.Connection,
                        statement:str,/) -> None:
    """adds the reccomended sigil sets to each modifier result"""
    for idx in range(len(results)):
        query_result = connection.execute(statement, [results[idx]["codename"]])
        new_results = sorted(query_result.fetchall(), key = lambda x: x [-1])
        results[idx] |= {
            "rec_sigils":{
                "even": {"name": new_results[0][0],
                        "effect": new_results[0][1]},
                "odd": {"name": new_results[1][0],
                        "effect": new_results[1][1]}
            }
        }


def _add_functor(results:list[dict[str:str]], connection:sqlite3.Connection,
                        statement:str,/) -> None:
    """adds the signature functor to each modifier result"""
    for idx in range(len(results)):
        query_result = connection.execute(
            statement, [results[idx]["codename"]])
        functor_res = query_result.fetchone()
        results[idx] |= {
            "sig_functor":{
                "name": functor_res[0],
                "effect": functor_res[1],
                "lore":functor_res[2]
            }
        }


def _add_skill(results:list[dict[str:str]], connection:sqlite3.Connection,
                        statement:str,/) -> None:
    """adds the skills of each modifier to each result"""
    for idx in range(len(results)):
        query_result = connection.execute(statement, [results[idx]["codename"]])
        skill_res = query_result.fetchone()
        results[idx]["skills"] = {}
        while skill_res is not None:
            results[idx]["skills"] |= {
                skill_res[2]: {
                    "name": skill_res[0],
                    "effect": skill_res[1],
                    "skill_cd": skill_res[3] if skill_res[3] else "N/A",
                    "skill_cost_type": skill_res[4] if skill_res[4] else "N/A",
                    "skill_cost_quant": skill_res[5] if skill_res[5] else "N/A",
                    "skill_type": skill_res[6] if skill_res[6] else "N/A"
                }
            }
            skill_res = query_result.fetchone()


def _add_aether_codes(results:list[dict[str:str]], connection:sqlite3.Connection,
                        statement:str,/) -> None:
    """adds all aether codes to each modifier results"""
    for idx in range(len(results)):
        query_result = connection.execute(
            statement, [results[idx]["codename"]])
        ac_res = query_result.fetchone()
        results[idx]["aether_codes"] = {"red":{}, "blue":{}, "yellow":{}}
        while ac_res is not None:
            results[idx]["aether_codes"][ac_res[0].lower()][ac_res[1]] = ac_res[2]
            ac_res = query_result.fetchone()


@connection_decorator
def _mod_search(connection:sqlite3.Connection, args:dict[str:str|int], /) -> list[dict[str|int]]:
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
    _add_sigils(results, connection, '''
        SELECT s.set_name, s.set_effects, sm.odd_or_even FROM sigil AS s
        INNER JOIN sigil_modifier AS sm ON sm.set_name = s.set_name
        WHERE sm.modifier_name =?;''')
    _add_functor(results, connection, '''SELECT functor_name, functor_power_desc, functor_lore FROM functor
        WHERE sig_modifier = ?;''')
    _add_skill(results, connection, '''SELECT skill_name, skill_desc, slot,
    skill_cd, skill_cost_type, skill_cost_quant, skill_type FROM skill WHERE modifier_name = ?;''')
    _add_aether_codes(results, connection, '''SELECT ac_type, ac_slot, ac_desc FROM aether_codes
            WHERE modifier_name =?;''')
    return results


@connection_decorator
def _functor_search(connection:sqlite3.Connection, args:dict[str:str|int], /) -> list[dict[str|int]]:
    """Sends a SELECT query to the database, and returns all functors that meet the criteria."""
    _RARITY_ATK_BOOST = {
        3: (10, 30),
        4: (15, 60),
        5: (20, 100)
    }
    query_result = connection.execute(
        f'''SELECT * FROM functor WHERE {'=? AND '.join([f'{key}' for key in args.keys()])}=?;''',
                list(args.values()))
    results = []
    latest = query_result.fetchone()
    while latest is not None:
        temp_res = {
            "name": latest[0],
            "gen_zone": latest[1],
            "rarity": latest[2],
            "access_key_boost": f'{_RARITY_ATK_BOOST[latest[2]][0]}%',
            "atk_boost": _RARITY_ATK_BOOST[latest[2]][1],
            "functor_desc": latest[3],
            "functor_lore": latest[4],
            "sig_modifier": latest[5] if latest[5] else "N/A"
        }
        results.append(temp_res)
        latest = query_result.fetchone()
    return results


@connection_decorator
def _sigil_search():
    pass


def interface():
    pass

if __name__ == "__main__":
    print(PATH_TO_DB)
    print(json.dumps(_mod_search({"name": "Asura"}), indent=4, ensure_ascii=False))
    print(json.dumps(_functor_search({"gen_zone": "Asterim"}), indent = 2, ensure_ascii=False))

