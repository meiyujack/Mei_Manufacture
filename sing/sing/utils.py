def turn_row_into_tuple(obj: list)->list:
    """对有数字的行的集合"""
    return [tuple(x) for x in obj]