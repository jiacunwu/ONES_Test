import pymysql
import time
import random
import string


def email_invite(team_uuid, inviter_uuid):
    db = pymysql.connect(host='119.23.130.213',
                         user='onesdev',
                         password='onesdev',
                         database=database,
                         charset='utf8')
    cursor = db.cursor()
    num = string.digits + string.ascii_letters
    code = ''.join(random.sample(num, 32))
    email = ''.join(random.sample(num, 8)) + '@ones.ai'
    create_time = int(time.time())
    license_types = [1, 2, 3]

    sql = f"insert into invitation" \
          f"(code,team_uuid,inviter_uuid,email,create_time,status,license_types,is_set_team_administrator) " \
          f"values" \
          f"('{code}','{team_uuid}','{inviter_uuid}','{email}','{create_time}',2,'{license_types}',0); "
    cursor.execute(sql)
    db.commit()
    db.close()


def link_invite(link_invitation_uuid, team_uuid, org_uuid):
    db = pymysql.connect(host='119.23.130.213',
                         user='onesdev',
                         password='onesdev',
                         database=database,
                         charset='utf8')
    cursor = db.cursor()
    num = string.digits + string.ascii_letters
    uuid = ''.join(random.sample(num, 8))
    user_uuid = ''.join(random.sample(num, 8))
    email = ''.join(random.sample(num, 8)) + '@ones.ai'
    create_time = int(time.time())

    sql1 = f"insert into link_invitation_user" \
           f"(uuid,link_invitation_uuid,team_uuid,user_uuid,create_time) " \
           f"values" \
           f"('{uuid}','{link_invitation_uuid}','{team_uuid}','{user_uuid}','{create_time}'); "

    sql2 = f"insert into org_user" \
           f"(org_uuid,uuid,name,name_pinyin,email,password,channel,hash,access_time,status,verify_status,create_time," \
           f"modify_time,type,language) " \
           f"values" \
           f"('{org_uuid}','{user_uuid}','test','test','{email}'," \
           f"'$2a$10$w4SX51o4.9qWxGQ7HJJr8uwyU/gYLL78CaJAPmmBs0dowSyLaMk9O'," \
           f"'ukLWC127vblDOxS4bnTGKYUgHL73h9gh',0,0,1,1,'{create_time}','{create_time}',1,'zh'); "

    cursor.execute(sql1)
    cursor.execute(sql2)
    db.commit()
    db.close()


def email_invite_sql(team_uuid, inviter_uuid):
    num = string.digits + string.ascii_letters
    code = ''.join(random.sample(num, 32))
    email = ''.join(random.sample(num, 8)) + '@ones.ai'
    create_time = int(time.time())
    license_types = [1, 2, 3]

    sql = f"insert into invitation" \
          f"(code,team_uuid,inviter_uuid,email,create_time,status,license_types,is_set_team_administrator) " \
          f"values" \
          f"('{code}','{team_uuid}','{inviter_uuid}','{email}','{create_time}',2,'{license_types}',0)"

    for i in range(100):
        num = string.digits + string.ascii_letters
        code = ''.join(random.sample(num, 32))
        email = ''.join(random.sample(num, 8)) + '@ones.ai'
        create_time = int(time.time())
        license_types = [1, 2, 3]
        sql = sql + f",('{code}','{team_uuid}','{inviter_uuid}','{email}','{create_time}',2,'{license_types}',0)"
    sql = sql + ';'
    print(sql)


def link_invite_sql(link_invitation_uuid, team_uuid, org_uuid):
    num = string.digits + string.ascii_letters
    uuid = ''.join(random.sample(num, 8))
    user_uuid = ''.join(random.sample(num, 8))
    email = ''.join(random.sample(num, 8)) + '@ones.ai'
    create_time = int(time.time())

    sql1 = f"insert into link_invitation_user" \
           f"(uuid,link_invitation_uuid,team_uuid,user_uuid,create_time) " \
           f"values" \
           f"('{uuid}','{link_invitation_uuid}','{team_uuid}','{user_uuid}','{create_time}') "

    sql2 = f"insert into org_user" \
           f"(org_uuid,uuid,name,name_pinyin,email,password,channel,hash,access_time,status,verify_status,create_time," \
           f"modify_time,type,language) " \
           f"values" \
           f"('{org_uuid}','{user_uuid}','test','test','{email}'," \
           f"'$2a$10$w4SX51o4.9qWxGQ7HJJr8uwyU/gYLL78CaJAPmmBs0dowSyLaMk9O'," \
           f"'ukLWC127vblDOxS4bnTGKYUgHL73h9gh',0,0,1,1,'{create_time}','{create_time}',1,'zh') "

    for j in range(100):
        num = string.digits + string.ascii_letters
        uuid = ''.join(random.sample(num, 8))
        user_uuid = ''.join(random.sample(num, 8))
        email = ''.join(random.sample(num, 8)) + '@ones.ai'
        create_time = int(time.time())
        sql1 = sql1 + f",('{uuid}','{link_invitation_uuid}','{team_uuid}','{user_uuid}','{create_time}')"
        sql2 = sql2 + f",('{org_uuid}','{user_uuid}','test','test','{email}'," \
                      f"'$2a$10$w4SX51o4.9qWxGQ7HJJr8uwyU/gYLL78CaJAPmmBs0dowSyLaMk9O'," \
                      f"'ukLWC127vblDOxS4bnTGKYUgHL73h9gh',0,0,1,1,'{create_time}','{create_time}',1,'zh') "
    sql1 = sql1 + ';'
    sql2 = sql2 + ';'
    print(sql1 + '\n' + sql2)


database = 'project_p3044'

if __name__ == '__main__':
    for i in range(1):
        email_invite('SRqxswRd', '6VPE8jZ4')
        time.sleep(0.1)
    for i in range(2):
        link_invite('Hgv3d5zS', 'SRqxswRd', '6CDhRvCL')
        time.sleep(0.1)
