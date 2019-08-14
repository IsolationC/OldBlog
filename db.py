import pymysql


def query(sql, params=()):
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='12345',
                         db='myblog',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)

    cursor = db.cursor()
    try:
        cursor.execute(sql, params)
        result = cursor.fetchone()

        return result

    except Exception as e:
        print(e)
    finally:
        db.close()
    return None


def query_all(sql, params=()):
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='12345',
                         db='myblog',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)

    cursor = db.cursor()
    try:
        cursor.execute(sql, params)
        result = cursor.fetchall()

        return result

    except Exception as e:
        print(e)
    finally:
        db.close()
    return None


def update(sql, params=()):

    db = pymysql.connect(host='localhost',
                         user='root',
                         password='12345',
                         db='myblog',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)

    cursor = db.cursor()

    try:
        cursor.execute(sql, params)
        db.commit()
        return cursor.rowcount
    except Exception as e:
        print(e)
        db.rollback()
    finally:
        db.close()
