import pymysql
import time


def select(org_uuid: str):
    db = pymysql.connect(host='119.23.130.213',
                         user='onesdev',
                         password='onesdev',
                         database=database,
                         charset='utf8')

    cursor = db.cursor()

    sql = f"SELECT * FROM license WHERE org_uuid='{org_uuid}'"
    print(sql)

    cursor.execute(sql)
    result = cursor.fetchall()

    for data in result:
        print(data)

    db.close()


def set_expire_time(org_uuid, license_type=0, edition='enterprise-trial'):
    db = pymysql.connect(host='119.23.130.213',
                         user='onesdev',
                         password='onesdev',
                         database=database,
                         charset='utf8')

    cursor = db.cursor()
    expire_time = int(time.time()) + 10

    if license_type == 0:
        sql = f"update license set " \
              f"expire_time={expire_time} where org_uuid='{org_uuid}' AND expire_time>100;"
        print(sql)
    else:
        sql = f"update license set " \
              f"expire_time={expire_time} where org_uuid='{org_uuid}' AND type={license_type} AND edition='{edition}';"
        print(sql)

    cursor.execute(sql)
    db.commit()
    db.close()


def set_multi_team(org_uuid):
    db = pymysql.connect(host='119.23.130.213',
                         user='onesdev',
                         password='onesdev',
                         database=database,
                         charset='utf8')

    cursor = db.cursor()
    sql = f"update organization set visibility=1 where uuid='{org_uuid}';"
    cursor.execute(sql)
    db.commit()
    db.close()


def new_license(uuid, license_type=0, edition='enterprise'):
    expire_time = int(time.time()) + 3600000
    db = pymysql.connect(host='119.23.130.213',
                         user='onesdev',
                         password='onesdev',
                         database=database,
                         charset='utf8')
    cursor = db.cursor()
    if license_type == 0:
        for i in range(1, 14):
            if i != 9:
                sql = f"insert into license(org_uuid,type,edition,add_type,scale,expire_time) " \
                      f"values('{uuid}',{i},'{edition}',1,100,{expire_time}); "
                cursor.execute(sql)
        db.commit()
        db.close()
    else:
        sql = f"insert into license(org_uuid,type,edition,add_type,scale,expire_time) " \
              f"values('{uuid}',{license_type},'{edition}',1,100,{expire_time}); "
        cursor.execute(sql)
        db.commit()
        db.close()


def set_prise_type(uuid):
    db = pymysql.connect(host='119.23.130.213',
                         user='onesdev',
                         password='onesdev',
                         database=database,
                         charset='utf8')
    cursor = db.cursor()
    sql = f"update organization set type=2 where uuid='{uuid}';"
    cursor.execute(sql)
    db.commit()
    db.close()


def run_sql(sql):
    db = pymysql.connect(host='119.23.130.213',
                         user='onesdev',
                         password='onesdev',
                         database=database,
                         charset='utf8')

    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    result = cursor.fetchall()
    for i in result:
        print(i)
    db.close()


license_type_list = {
    "????????????": 1,
    "???????????????": 2,
    "????????????": 3,
    "???????????????": 4,
    "???????????????": 5,
    "?????????????????????": 6,
    "????????????": 7,
    "????????????": 8,
    "????????????": 10,
    "????????????": 11,
    "????????????": 12,
    "???????????????": 13
}

database = 'project_master'

if __name__ == '__main__':
    # select('6njBbZNy')
    set_expire_time('32FcyJbF', 0)
    # set_multi_team('AtFhxSdE')
    # set_prise_type('6njBbZNy')
    # run_sql("update license set ")
    # new_license('6njBbZNy')
    # select('QHGMEaMN')
