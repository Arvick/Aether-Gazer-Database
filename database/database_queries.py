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


PATH_TO_DB = Path.cwd() / "aether_gazer.db"

def connection_decorator(func:function):
    """A decorator function that creates a connection to the database,
    executes the function, then closes the connection"""
    def execute(*args, **kwargs):
        connection:sqlite3.Connection = sqlite3.connect(PATH_TO_DB)
        result = func(connection, *args, **kwargs)
        connection.close()
        return result
    return execute


@connection_decorator
def _mod_search():
    pass


@connection_decorator
def _functor_search():
    pass


@connection_decorator
def _sigil_search():
    pass


def interface():
    pass

if __name__ == "__main__":
    print(PATH_TO_DB)