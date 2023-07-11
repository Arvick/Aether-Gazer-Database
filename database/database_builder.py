# This module creates the structure of the database, as well as inserts content into it
import sqlite3
# images?
# TODO: table for aether codes
# TODO: Separate tables to hold Skill Descs + 
# TODO: enable PRAGMA foreign_keys = ON; somwhere when creating connection
def create_tables(connection:sqlite3.Connection):
    # creates the tables to be used in the DB
    connection.execute('''
        CREATE TABLE IF NOT EXISTS modifier(
            name TEXT NOT NULL CHECK (length(name) > 0),
            modifier_name TEXT NOT NULL UNIQUE CHECK (length(modifier_name) > 0) PRIMARY KEY,
            combat_type ENUM('Melee', 'Ranged') NULL,
            gen_zone ENUM('Olympus', 'Nile', 'Shinou', 'Yggdrasil', 'Asterim') NULL,
            dmg_type ENUM('Physical', 'Wind', 'Fire', 'Thunder', 'Shadow', 'Light', 'Ice', 'Water') NULL,
            combat_rsc ENUM('Rage', 'Energy', 'Traces', 'Divine Grace') NULL,
            access_key TEXT NOT NULL CHECK (length(access_key) > 0),
            normal_atk_name TEXT NOT NULL CHECK (length(normal_atk_name) > 0),
            skill1_name TEXT NOT NULL CHECK (length(skill1_name) > 0),
            skill2_name TEXT NOT NULL CHECK (length(skill2_name) > 0),
            skill3_name TEXT NOT NULL CHECK (length(skill3_name) > 0),
            ult_skill_name TEXT NOT NULL CHECK (length(ult_skill_name) > 0),
            dodge_skill_name TEXT NOT NULL CHECK (length(dodge_skill_name) > 0),
        ) STRICT;
        ''')
    connection.commit()
    connection.execute('''
        CREATE TABLE IF NOT EXISTS sigil(
            set_name TEXT NOT NULL PRIMARY KEY CHECK (length(set_name) > 0),
            set_effects TEXT NOT NULL
        ) STRICT;
    ''')
    connection.execute('''
        CREATE TABLE IF NOT EXISTS sigil_modifier(
            modifier_name TEXT NOT NULL CHECK (length(modifier_name) > 0),
            set_name TEXT NOT NULL CHECK (length(set_name) > 0),
            odd_or_even ENUM('Odd', 'Even') NULL,
            PRIMARY KEY (modifier_name, odd_or_even),
            FOREIGN KEY (modifier_name) REFERENCES modifier(modifier_name),
            FOREIGN KEY (set_name) REFERENCES sigil(set_name)
        ) STRICT;
    ''')
    # each tier has their own access key/functor atk boosts
    # use modifier_name to get the "name" column
    connection.execute('''
        CREATE TABLE IF NOT EXISTS functor(
            functor_name TEXT NOT NULL CHECK (length(functor_name) > 0),
            gen_zone ENUM('Olympus', 'Nile', 'Shinou', 'Yggdrasil', 'Asterim') NULL,
            tier UNSIGNED INTEGER NOT NULL CHECK (tier >=3 AND tier <= 5),
            functor_power_desc TEXT NOT NULL CHECK (length(functor_power_desc) > 0),
            functor_lore TEXT NOT NULL CHECK (length(functor_lore) > 0),
            sig_modifier TEXT NOT NULL UNIQUE CHECK (length(modifier_name) > 0),
            PRIMARY KEY (functor_name, modifier_name),
            FOREIGN KEY (sig_modifier) REFERENCES modifier(modifier_name)
        ) STRICT;
    ''')





    



