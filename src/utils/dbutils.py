import sqlite3
import numpy as np


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
                chat_id INTEGER,
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


def insert_into_groups_users(database: sqlite3.Connection, group_id: int, 
                             santa_id: int, chat_id:int, 
                             user_name: str, 
                             about: str, 
                             desired: str) -> int:
    cursor = database.cursor()

    cursor.execute(
        '''
            INSERT INTO groups_users (group_id, santa_id, user_id, chat_id, user_name, about, desired)
            VALUES (%d, %d, null, %d, "%s", "%s", "%s")
        ''' % (group_id, santa_id, chat_id, user_name, about, desired)
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
            WHERE gu.santa_id = %d
        ''' % user_id
    ).fetchall()

    cursor.close()

    return result


def get_group_ids(database: sqlite3.Connection, user_id: int) -> list:
    cursor = database.cursor()

    result = cursor.execute(
        '''
            SELECT DISTINCT group_id FROM groups_users WHERE santa_id = %d
        ''' % user_id
    ).fetchall()

    cursor.close()

    return [int(x[0]) for x in result]


def get_all_recipients(database: sqlite3.Connection, user_id: int) -> list:
    cursor = database.cursor()

    users = cursor.execute(
        '''
            SELECT user_id, group_id
            FROM groups_users
            WHERE santa_id = %d and user_id IS NOT NULL
        ''' % user_id
    ).fetchall()
    print(users)

    result = []
    
    for user_id, group_id in users:
        temp = cursor.execute(
            '''
                SELECT g.name, user_name, about, desired 
                FROM groups_users gu
                INNER JOIN groups g ON g.group_id = gu.group_id 
                WHERE santa_id = %d and gu.group_id = %d
            ''' % (user_id, group_id)
        ).fetchall()
        result.extend(temp)

    cursor.close()

    return result


def update_user_id(database: sqlite3.Connection, santa_id: int, user_id: int, group_id: int) -> int:
    result = 0
    cursor = database.cursor()

    cursor.execute(
        '''
            UPDATE groups_users
            SET user_id = %d
            WHERE santa_id = %d and group_id = %d
        ''' % (santa_id, user_id, group_id)
    )

    if cursor.rowcount == 0:
        result = -1

    database.commit()
    cursor.close()

    return result


def randomize_santas(database: sqlite3.Connection, group_id: int) -> list:
    cursor = database.cursor()

    santas = cursor.execute(
        '''
            SELECT santa_id
            FROM groups_users
            WHERE group_id = %d
        ''' % group_id
    ).fetchall()

    print(santas)
    santas = [santa[0] for santa in santas]

    if len(santas) < 2:
        return []
        
    used = []
    for santa_id in santas:
        users = [id for id in santas if id != santa_id and id not in used]
        user_id = np.random.choice(users)
        if update_user_id(database, santa_id=santa_id, user_id=user_id, group_id=group_id) != -1:
            used.append(user_id) 

    recipient_ids_chat_ids = cursor.execute(
        '''
            SELECT user_id, chat_id
            FROM groups_users
            WHERE group_id = %d
        ''' % group_id
    ).fetchall()
    print(recipient_ids_chat_ids)

    recipients_info = []
    for recipient_id, _ in recipient_ids_chat_ids:
        temp_recipient = cursor.execute(
            '''
                SELECT user_name, g.name, about, desired
                FROM groups_users gu
                INNER JOIN groups g ON g.group_id = gu.group_id
                WHERE gu.group_id = %d and gu.santa_id = %d and gu.user_id IS NOT NULL
            ''' % (group_id, recipient_id)
        ).fetchall()
        recipients_info.extend(temp_recipient)

    chat_ids = [recipient[1] for recipient in recipient_ids_chat_ids]
    recipients = [[chat_ids[index], *recipient] for index, recipient in enumerate(recipients_info)]
    print(recipients_info)

    return recipients # chat_id, user_name,  group_name, about, description