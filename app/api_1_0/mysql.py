# -*- coding: utf-8 -*-
# import json
import MySQLdb


class PyMysql:

    conn = None
    cur = None

    def __init__(self, host='localhost', user='root', passwd='root',
                 db='bprest', port=3306):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.port = port

    def __open(self):
        try:
            self.conn = MySQLdb.connect(db=self.db, user=self.user,
                                        passwd=self.passwd,
                                        host=self.host, port=self.port)
            self.cur = self.conn.cursor()
        except MySQLdb.Error as e:
            print "Error %d: %s" % (e.args[0], e.args[1])

    def __close(self):
        self.cur.close()
        self.conn.close()

    def mysql_insert_one_blueprint(self, name, components, rolename, content):
        self.__open()
        self.cur.execute("INSERT INTO blueprint (name, components, rolename, content) VALUES ('%s', '%s', '%s', '%s')" % (name, components, rolename, content))
        rowid = self.conn.insert_id()
        self.conn.commit()
        self.__close()

        return {"result": rowid}

    def mysql_search_blueprint(self):
        fields = ["id", "name", "content", "rolename", "components"]
        result = []
        sql = "SELECT " + ', '.join(fields) + " FROM blueprint;"
        self.__open()
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        if rows:
            for line in rows:
                t = dict(zip(tuple(fields), line))
                result.append(t)
        self.__close()

        return {"result": result}

    def mysql_search_one_blueprint(self, id):
        t = {}
        fields = ["id", "name", "components", "rolename", "content"]
        sql = "SELECT " + ', '.join(fields) + " FROM blueprint WHERE id=%s;" % id
        self.__open()
        rows = self.cur.execute(sql)
        if rows == 0:
            return {"result": t}
        row = self.cur.fetchone()
        if row:
            t = dict(zip(tuple(fields), row))
        self.__close()

        return {"result": t}

    def mysql_check_blueprint_byname(self, name):
        t = 0
        sql = "SELECT * FROM blueprint WHERE name='%s';" % name
        self.__open()
        rows = self.cur.execute(sql)
        if rows > 0:
            t = 1
        self.__close()

        return {"result": t}

    def mysql_delete_one_blueprint(self, id):
        sql = "DELETE FROM blueprint WHERE id=%s;" % id
        self.__open()
        self.cur.execute(sql)
        self.conn.commit()
        self.__close()

        return {"result": id}

    def mysql_update_one_blueprint(self, id, name, components, rolename, content):
        self.__open()
        self.cur.execute(("UPDATE blueprint SET name='%s', components='%s', rolename='%s', content='%s' WHERE id=%s") %
                         (name, components, rolename, MySQLdb.escape_string(content), id))
        self.conn.commit()
        self.__close()

        return {"result": id}
