from . import dbutils


def validate_group_name(text: str) -> bool:
    if text.strip() == '':
        return False
    
    return True


def validate_about(text: str) -> bool:
    if text.strip() == '':
        return False
    
    return True


def validate_joining(database, group_id: int, user_id: int) -> bool:
    group_ids = dbutils.get_group_ids(database=database, user_id=user_id)

    for id in group_ids:
        if id == group_id:
            return False
        
    return True