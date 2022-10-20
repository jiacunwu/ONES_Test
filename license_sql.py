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
    "项目管理": 1,
    "知识库管理": 2,
    "测试管理": 3,
    "流水线管理": 4,
    "项目集管理": 5,
    "企业级账号目录": 6,
    "工单管理": 7,
    "效能管理": 8,
    "产品管理": 10,
    "版本管理": 11,
    "工时管理": 12,
    "流程自动化": 13
}

database = 'project_p3063'

if __name__ == '__main__':
    # select('6njBbZNy')
    set_expire_time('6njBbZNy', 0)
    # set_multi_team('AtFhxSdE')
    # set_prise_type('6njBbZNy')
    # run_sql("update license set ")
    # new_license('6njBbZNy')
    # select('QHGMEaMN')
