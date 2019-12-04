import core.exceptions as exceptions


class DBConnector(object):
    def __init__(self, host, uname, pwd, port=3306, dbtype='mysql'):
        self._dbtype = dbtype

        if dbtype in ('mysql', 'mssql'):
            self._module = __import__(eval('py' + dbtype))
        else:
            raise exceptions.DatabaseNotSupported

        self._db = self._module.connect(host, uname, pwd, port)
        self._cursor = self._db.cursor()

    def exec(self, sql) -> tuple:
        try:
            self._cursor.execute(sql)
            if sql[:6].upper() == 'SELECT':
                return self._cursor.fetchall()
            else:
                self._db.commit()

        except Exception:
            self._db.rollback()
            raise exceptions.DatabaseExecError

    def __del__(self):
        self._cursor.close()
        self._db.close()
