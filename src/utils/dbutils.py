import sqlite3


def insert_group_name(database: sqlite3.Connection, group_name: str) -> bool:
    inserted = True

    return inserted