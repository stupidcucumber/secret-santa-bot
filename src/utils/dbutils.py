import sqlite3


def create_database(name: str='default.db'):
    database = sqlite3.connect(name)

    cursor = database.cursor()

    cursor.execute(
        '''
            CREATE TABLE groups (
                group_id INTEGER,
                admin_id INTEGER,
                name TEXT,

                PRIMARY KEY(group_id)
            )
        '''
    )

    cursor.execute(
        '''
            CREATE TABLE groups_users (
                entry_id INTEGER,
                group_id INTEGER,
                santa_id INTEGER,
                user_id INTEGER,
                about TEXT,
                desired TEXT,

                PRIMARY KEY(entry_id),
                FOREIGN KEY(group_id) REFERENCES groups(group_id)
            )
        '''
    )  

    cursor.close()

    return database


def insert_group_name(database: sqlite3.Connection, group_name: str, admin_id: int) -> int:
    cursor = database.cursor()
    cursor.execute(
        '''
            INSERT INTO groups (admin_id, name) VALUES (%d, "%s")
        ''' % (admin_id, group_name)
    )
    if cursor.rowcount == 0:
        return -1

    id = cursor.lastrowid

    cursor.close()

    return id


def insert_into_groups_users(database: sqlite3.Connection, group_id: int, user_id: int, about: str, desired: str) -> int:
    cursor = database.cursor()

    cursor.execute(
        '''
            INSERT INTO groups_users (group_id, santa_id, user_id, about, desired)
            VALUES (%d, null, %d, "%s", "%s")
        ''' % (group_id, user_id, about, desired)
    )

    if cursor.rowcount == 0:
        return -1
    
    id = cursor.lastrowid

    cursor.close()

    return id