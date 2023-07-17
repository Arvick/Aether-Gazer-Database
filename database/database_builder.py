# This module creates the structure of the database, as well as inserts content into it
import sqlite3
from pathlib import Path
# images?
# TODO: table for aether codes
# TODO: Separate tables to hold Skill Descs + 
# TODO: separate creation of each table into its own function?
def _create_tables(connection:sqlite3.Connection) -> None:
    """creates the tables to be used in the DB"""
    _SQL_STATEMENTS = ['''
        CREATE TABLE IF NOT EXISTS modifier(
            name TEXT NOT NULL CHECK (length(name) > 0),
            modifier_name TEXT NOT NULL UNIQUE CHECK (length(modifier_name) > 0),
            combat_type TEXT NOT NULL CHECK (combat_type IN ('Melee', 'Ranged')),
            gen_zone TEXT NOT NULL CHECK (gen_zone IN ('Olympus', 'Nile', 'Shinou', 'Yggdrasil', 'Asterim')),
            dmg_type TEXT NOT NULL CHECK (dmg_type IN ('Physical', 'Wind', 'Fire', 'Thunder', 'Shadow', 'Light', 'Ice', 'Water')),
            combat_rsc TEXT NOT NULL CHECK (combat_rsc IN ('Rage', 'Energy', 'Traces', 'Divine Grace')),
            access_key TEXT NOT NULL CHECK (length(access_key) > 0),
            normal_atk_name TEXT NOT NULL CHECK (length(normal_atk_name) > 0),
            skill1_name TEXT NOT NULL CHECK (length(skill1_name) > 0),
            skill2_name TEXT NOT NULL CHECK (length(skill2_name) > 0),
            skill3_name TEXT NOT NULL CHECK (length(skill3_name) > 0),
            ult_skill_name TEXT NOT NULL CHECK (length(ult_skill_name) > 0),
            dodge_skill_name TEXT NOT NULL CHECK (length(dodge_skill_name) > 0),            
            PRIMARY KEY (modifier_name, name)
        ) STRICT; ''',
        '''
        CREATE TABLE IF NOT EXISTS sigil(
            set_name TEXT NOT NULL PRIMARY KEY CHECK (length(set_name) > 0),
            set_effects TEXT NOT NULL CHECK (length(set_effects) > 0)
        ) STRICT; ''',
        '''
        CREATE TABLE IF NOT EXISTS sigil_modifier(
            modifier_name TEXT NOT NULL CHECK (length(modifier_name) > 0),
            set_name TEXT NOT NULL CHECK (length(set_name) > 0),
            odd_or_even TEXT NOT NULL CHECK (odd_or_even IN ('Odd', 'Even')),
            PRIMARY KEY (modifier_name, odd_or_even),
            FOREIGN KEY (modifier_name) REFERENCES modifier(modifier_name),
            FOREIGN KEY (set_name) REFERENCES sigil(set_name)
        ) STRICT; ''',
        '''
        CREATE TABLE IF NOT EXISTS functor(
            functor_name TEXT NOT NULL UNIQUE CHECK (length(functor_name) > 0),
            gen_zone TEXT NOT NULL CHECK (gen_zone IN ('Olympus', 'Nile', 'Shinou', 'Yggdrasil', 'Asterim')),
            tier INTEGER NOT NULL CHECK (tier >=3 AND tier <= 5),
            functor_power_desc TEXT NOT NULL CHECK (length(functor_power_desc) > 0),
            functor_lore TEXT NOT NULL CHECK (length(functor_lore) > 0),
            sig_modifier TEXT NOT NULL UNIQUE CHECK (length(sig_modifier) > 0),
            PRIMARY KEY (functor_name, sig_modifier),
            FOREIGN KEY (sig_modifier) REFERENCES modifier(modifier_name)
        ) STRICT; ''',
        '''
        CREATE TABLE IF NOT EXISTS skill(
            skill_name TEXT NOT NULL CHECK (length(skill_name) > 0),
            skill_desc TEXT NOT NULL CHECK (length(skill_desc) > 0),
            slot TEXT NOT NULL CHECK (slot IN ('normal_atk', 'skill1', 'skill2', 'skill3', 'ult_skill', 'dodge_skill')),
            skill_cd INTEGER NOT NULL CHECK (skill_cd >= 0),
            skill_cost_type TEXT NOT NULL CHECK (skill_cost_type IN ('Rage', 'Energy', 'Traces', 'Divine Grace')),
            skill_cost_quant INTEGER NOT NULL CHECK (skill_cost_quant >= 0),
            skill_type TEXT NOT NULL CHECK (skill_type IN ('Evolving', 'Set-up', 'Divergent', 'Switch', 'Channeling', 'Charge')),
            modifier_name TEXT NOT NULL UNIQUE CHECK (length(modifier_name) > 0),
            PRIMARY KEY (skill_name, modifier_name),
            FOREIGN KEY (modifier_name) REFERENCES modifier(modifier_name)
        ) STRICT; ''',
        '''
        CREATE TABLE IF NOT EXISTS aether_codes(
            ac_type TEXT NOT NULL CHECK (ac_type IN ('RED', 'YELLOW', 'BLUE')),
            ac_slot INTEGER NOT NULL CHECK (ac_slot >= 1 AND ac_slot <= 3),
            ac_desc TEXT NOT NULL CHECK (length(ac_desc) > 0),
            modifier_name TEXT NOT NULL UNIQUE CHECK (length(modifier_name) > 0),
            PRIMARY KEY (modifier_name, ac_type, ac_slot),
            FOREIGN KEY (modifier_name) REFERENCES modifier(modifier_name)
        ) STRICT;
    ''']
    # for functor: # each tier has their own access key/functor atk boosts
    # use modifier_name to get the "name" column
    for statement in _SQL_STATEMENTS:
        connection.execute(statement)
        connection.commit()


def selecting_option(options:tuple[str], prompt:str) -> str:
    """A general-purpose function for listing out a series of options (with enumerate), and selecting a choice.
    The chosen option is returned. A prompt can be included for readability."""
    for index, option in enumerate(options):
        print(index, option)
    choice = input(prompt).strip()
    if "." not in choice:
        try:
            return options[int(choice)]
        except ValueError:
            pass
    print(f"Error: {choice} is not a valid option.")
    raise ValueError


def insert_modifier(connection:sqlite3.Connection) -> int:
    """For inserting data into the table 'modifier'.
    This function will ask for the parameters as outlined by the SQL table.
    If an error code arises while accepting data/inserting into the DB, a error code (1) is returned."""
    try:
        name = input("Enter the real name of the modifier here: ").strip()
        modifier_name = input("Enter the name of the modifier (NOT their original name) here: ").strip()
        combat_type = selecting_option(('Melee', 'Ranged'), "Enter the option that corresponds to the Modifier's combat type: ")
        gen_zone = selecting_option(('Olympus', 'Nile', 'Shinou', 'Yggdrasil', 'Asterim'), "Enter the option that corresponds to the Gen-Zone of the modifier: ")
        dmg_type = selecting_option(('Physical', 'Wind', 'Fire', 'Thunder', 'Shadow', 'Light', 'Ice', 'Water'), "Enter the option that corresponds to the modifier's damage type: ")
        combat_rsc = selecting_option(('Rage', 'Energy', 'Traces', 'Divine Grace'), "Enter the option that corresponds to the modifier's combat type: ")
        access_key = input("Enter the name of the Modifier's Access Key: ").strip()
        normal_atk_name = input("Enter the name of the Normal Attack: ").strip()
        skill1_name = input("Enter the name of Skill 1: ").strip()
        skill2_name = input("Enter the name of Skill 2: ").strip()
        skill3_name = input("Enter the name of Skill 3: ").strip()
        ult_skill_name = input("Enter the name of the Ultimate Skill: ").strip()
        dodge_skill_name = input("Enter the name of the Dodge Skill: ").strip()
        connection.execute(f'''INSERT INTO modifier
            ({', '.join(tuple(column for column in locals().keys() if column != 'connection'))}) VALUES ({', '.join(tuple("?" for column in locals().keys() if column != 'connection'))});''',
            tuple(value for value in locals().values() if isinstance(value, str)))
        connection.commit()
        return 0
    except ValueError:
        return 1
    except sqlite3.Error as e:
        print("An Error occured while inserting into the Database: ", str(e))
        return 1



def insert_sigil(connection:sqlite3.Connection) -> int:
    """This function handles inserting of data into the sigil table.
    It will ask for the name of the sigil set, as well as its effects.
    If an error occurs when attempting to insert data, an error code is returned."""
    '''set_name TEXT NOT NULL PRIMARY KEY CHECK (length(set_name) > 0),
            set_effects TEXT NOT NULL CHECK (length(set_effects) > 0)'''
    try:
        set_name = input("Enter the name of the sigil set: ").strip()
        set_effects = input("Enter the effects of the sigil set: ").strip()
        connection.execute(f'''INSERT INTO sigil
            ({', '.join(tuple(column for column in locals().keys() if column != 'connection'))}) VALUES ({', '.join(tuple("?" for column in locals().keys() if column != 'connection'))});''',
            tuple(value for value in locals().values() if isinstance(value, str)))
        connection.commit()
        return 0
    except sqlite3.Error as e:
        print("An Error occured while inserting into the Database: ", str(e))
        return 1



def insert_sigil_modifier() -> int:
    pass


def insert_functor() -> int:
    pass


def insert_skill() -> int:
    pass


def insert_aether_code() -> int:
    pass


def insert_data(connection:sqlite3.Connection) -> int:
    """A central function for handling SQL queries
    for inserting data.
    This function will redirect to 1 of 6 functions, each for the different tables.
    
    After the operation is completed, a code will be sent back to the user.
    0 = success, 1 = failure."""
    _OPTIONS_TO_TABLES = {
        1:insert_modifier,
        2:insert_sigil,
        3:insert_sigil_modifier,
        4:insert_functor,
        5:insert_skill,
        6:insert_aether_code
    }
    print("Which table would you like to insert data into?")
    for key,value in _OPTIONS_TO_TABLES.items():
        print(key, value.__name__)
    try:
        response = input("Please enter the ID for the table you wish to interact with. ").strip()
        if "." not in response and 1 <= int(response) <= 6:
            print("You'll now be asked to enter the corresponding data into the table. Follow all prompts.")
            call:int = _OPTIONS_TO_TABLES[int(response)](connection)
            return call
        print("Error: Invalid Response.")
    except ValueError:
        print("Error: Invalid Response.")
    return 1

def form_statement():
    pass


def create_connection() -> sqlite3.Connection:
    """creates a Sqlite3 Connection to be used for inserting data."""
    Path.touch(Path.cwd() / "aether_gazer.db")
    connection = sqlite3.connect(Path.cwd() / "aether_gazer.db")
    connection.execute("PRAGMA foreign_keys = ON;")
    connection.commit()
    return connection


def _main():
    print("Welcome to the AG Database Builder. Would you like to \
insert data into the databases?")
    response = input("Enter Y to proceed, else enter anything else. ").strip().capitalize()
    connection = create_connection()
    _create_tables(connection)
    while response == "Y":
        call:int = insert_data(connection)
        if not call:
            print("Operation successful.")
        else:
            print("Operation failed. See reasons above")
        response = input("Would you like to continue? \
Enter Y to proceed, else enter anything else. ").strip().capitalize()
    connection.close()

    
if __name__ == "__main__":
    _main()

