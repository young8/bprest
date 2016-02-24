# -*- coding: utf-8 -*-

# import json
import MySQLdb


class PyMysql:

    conn = None
    cur = None

    def __init__(self, host='localhost', user='root', passwd='root', db='bprest', port=3306):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.port = port
        print host, user, passwd, db, port

    def __open(self):
        try:
            self.conn = MySQLdb.connect(db=self.db, user=self.user, passwd=self.passwd, host=self.host, port=self.port)
            self.cur = self.conn.cursor()
        except MySQLdb.Error as e:
            print "Error %d: %s" % (e.args[0], e.args[1])

    def __close(self):
        self.cur.close()
        self.conn.close()

    def mysql_insert(self, name, description, master, slave, components):
        self.__open()
        self.cur.execute("INSERT INTO plans (name, description, master, slave, components) VALUES ('%s', '%s', %d, %d,'%s')" % (name, description, master, slave, components))
        self.conn.commit()
        self.__close()

        return {"result": name}

    def mysql_search(self):
        fields = ["name", "description", "master", "slave", "components"]
        result = []
        sql = "SELECT " + ', '.join(fields) + " FROM plans;"
        self.__open()
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        if rows:
            for line in rows:
                t = dict(zip(tuple(fields), line))
                result.append(t)
        self.__close()

        return {"result": result}

    def mysql_search_one(self, name):
        t = {}
        fields = ["name", "description", "master", "slave", "components", "blueprint", "hostmapping"]
        sql = "SELECT " + ', '.join(fields) + " FROM plans WHERE name='%s';" % name
        self.__open()
        self.cur.execute(sql)
        row = self.cur.fetchone()
        if row:
            t = dict(zip(tuple(fields), row))
        self.__close()

        return {"result": t}

    def mysql_get_plan(self, master, slave, components):
        t = {}
        fields = ["blueprint", "hostmapping"]
        components = ','.join(components)
        sql = "SELECT " + ', '.join(fields) + " FROM plans WHERE master=%d and slave=%d and components='%s';" % (master, slave, components)
        self.__open()
        self.cur.execute(sql)
        row = self.cur.fetchone()
        if row:
            t = dict(zip(tuple(fields), row))
        self.__close()

        return {"result": t}

    def mysql_delete(self, name):
        sql = "DELETE FROM plans WHERE name='%s';" % name
        self.__open()
        self.cur.execute(sql)
        self.conn.commit()
        self.__close()

        return {"result": name}

    def mysql_update(self, name, description, master, slave, components, blueprint, hostmapping):
        self.__open()
        self.cur.execute(("UPDATE plans SET description='%s',master=%d, slave=%d, components='%s', blueprint='%s', hostmapping='%s' WHERE name='%s'") %
                         (description, master, slave, components, MySQLdb.escape_string(blueprint), MySQLdb.escape_string(hostmapping), name))
        self.conn.commit()
        self.__close()

        return {"result": name}
