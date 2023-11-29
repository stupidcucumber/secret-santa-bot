import sqlite3


def create_database(name: str='default.db'):
    database = sqlite3.connect(name, check_same_thread=False)

    cursor = database.cursor()

    cursor.execute(
        '''
            CREATE TABLE groups (
                group_id INTEGER,
                admin_id INTEGER,
                name TEXT,

                PRIMARY KEY(group_id)
            );
        '''
    )

    cursor.execute(
        '''
            CREATE TABLE groups_users (
                entry_id INTEGER,
                group_id INTEGER,
                santa_id INTEGER,
                user_id INTEGER,
                user_name TEXT,
                about TEXT,
                desired TEXT,

                PRIMARY KEY(entry_id),
                FOREIGN KEY(group_id) REFERENCES groups(group_id)
            )
        '''
    )  

    cursor.close()
    database.commit()

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
    database.commit()

    return id


def insert_into_groups_users(database: sqlite3.Connection, group_id: int, user_id: int, user_name: str, about: str, desired: str) -> int:
    cursor = database.cursor()

    cursor.execute(
        '''
            INSERT INTO groups_users (group_id, santa_id, user_id, user_name, about, desired)
            VALUES (%d, null, %d, "%s", "%s", "%s")
        ''' % (group_id, user_id, user_name, about, desired)
    )

    if cursor.rowcount == 0:
        return -1
    
    id = cursor.lastrowid

    cursor.close()
    database.commit()

    return id


def get_all_created_groups(database: sqlite3.Connection, user_id: int) -> int:
    cursor = database.cursor()

    result = cursor.execute(
        '''
            SELECT name, group_id FROM groups WHERE admin_id = %d
        ''' % user_id
    ).fetchall()

    cursor.close()

    return result


def get_group_names(database: sqlite3.Connection, user_id: int) -> list:
    cursor = database.cursor()

    result = cursor.execute(
        '''
            SELECT g.name, g.group_id
            FROM groups_users gu
            INNER JOIN groups g ON g.group_id = gu.group_id  
            WHERE gu.user_id = %d
        ''' % user_id
    ).fetchall()

    cursor.close()

    return result


def get_group_ids(database: sqlite3.Connection, user_id: int) -> list:
    cursor = database.cursor()

    result = cursor.execute(
        '''
            SELECT DISTINCT group_id FROM groups_users WHERE user_id = %d
        ''' % user_id
    ).fetchall()

    cursor.close()

    return [int(x[0]) for x in result]


def get_all_recipients(database: sqlite3.Connection, user_id: int) -> list:
    cursor = database.cursor()

    result = cursor.execute(
        '''
            SELECT g.name, user_name, about, desired 
            FROM groups_users gu
            INNER JOIN groups g ON g.group_id = gu.group_id 
            WHERE santa_id=%d
        ''' % user_id
    ).fetchall()

    cursor.close()

    return result


def randomize_santas(database: sqlite3.Connection, group_id: int) -> bool:
    

    return True