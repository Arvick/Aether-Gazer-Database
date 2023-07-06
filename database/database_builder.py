# This module creates the structure of the database, as well as inserts content into it
import sqlite3

def create_tables(connection:sqlite3.Connection):
    connection.execute('''
        CREATE TABLE IF NOT EXISTS modifier(
            name TEXT NOT NULL,
            modifier_name TEXT NOT NULL PRIMARY KEY,
            combat_type ENUM('Melee', 'Ranged') NULL,
            gen_zone ENUM('Olympus', 'Nile', 'Shinou', 'Yggdrasil', 'Asterim') NULL,
            dmg_type ENUM('Physical', 'Wind', 'Fire', 'Thunder', 'Shadow', 'Light', 'Ice', 'Water') NULL,
            combat_rsc ENUM('Rage', 'Energy', 'Traces', 'Divine Grace') NULL,
            sig_functor TEXT NOT NULL,
            access_key TEXT NOT NULL,
            normal_atk_name TEXT,
            skill1_name TEXT,
            skill2_name TEXT,
            skill3_name TEXT,
            ult_skill_name TEXT,
            dodge_skill_name TEXT
        ) STRICT;
        ''')
    connection.commit()
    connection.execute('''
    
    
    ''')




    



