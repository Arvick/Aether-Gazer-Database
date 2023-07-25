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
from database_builder import create_connection

PATH_TO_DB = Path.cwd() / "aether_gazer.db"

def connection_decorator(func:function):
    pass

def _mod_search():
    pass


def _functor_search():
    pass


def _sigil_search():
    pass


def interface():
    connection:sqlite3.Connection = create_connection()



    connection.close()

if __name__ == "__main__":
    print(PATH_TO_DB)