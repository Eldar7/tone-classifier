#!/usr/bin/python

def get_score_columns(task_type):
    if (task_type == 'bank'):
        return ['sberbank', 'vtb', 'gazprom', 'alfabank', 'bankmoskvy', 'raiffeisen', 'uralsib', 'rshb']
    if (task_type == 'ttk'):
        return ['beeline', 'mts', 'megafon', 'tele2', 'rostelecom', 'komstar', 'skylink']

def next_row(cursor, expected_score, vector_type):
    # filtering rows
    if vector_type == 'train':
        notFound = True
        while notFound:
            notFound = False
            next_row = cursor.fetchone()
            if next_row is not None:
                # skip text and id
                for i in range(2, len(next_row)):
                    if next_row[i] != None and is_int(next_row[i]) and expected_score != int(next_row[i]):
                        notFound = True
                        break
            else:
                break
    elif vector_type == 'test':
        next_row = cursor.fetchone()
    return next_row

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def get(task_type, cursor, table, score, limit):
    if (task_type == 'bank'):
        cursor.execute("""SELECT text, id, sberbank, vtb, gazprom, alfabank,
            bankmoskvy, raiffeisen, uralsib, rshb FROM %s WHERE
            (sberbank=\'%d\' OR vtb=\'%d\' OR gazprom=\'%d\' OR alfabank=\'%d\' OR bankmoskvy=\'%d\'
            OR raiffeisen=\'%d\' OR uralsib=\'%d\' OR rshb=\'%d\') LIMIT(\'%d\');"""%(table,
            score, score, score, score, score, score, score, score, limit))
    elif (task_type == 'ttk'):
        cursor.execute("""SELECT text, id, beeline, mts, megafon,
            tele2, rostelecom, komstar, skylink FROM %s WHERE
            (beeline=\'%d\' OR mts=\'%d\' OR megafon=\'%d\' OR tele2=\'%d\' OR rostelecom=\'%d\'
            OR komstar=\'%d\' OR skylink=\'%d\') LIMIT(\'%d\')"""%(table,
            score, score, score, score, score, score, score, limit))
