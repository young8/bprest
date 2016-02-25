# -*- coding: utf-8 -*-
import json
import ConfigParser
from json import JSONEncoder
from flask import request, jsonify
from mysql import PyMysql
from . import api


cf = ConfigParser.ConfigParser()
cf.read("app/api_1_0/config.txt")
host = cf.get('mysql', 'host')
port = cf.getint('mysql', 'port')
user = cf.get('mysql', 'user')
passwd = cf.get('mysql', 'passwd')
database = cf.get('mysql', 'db')
db = PyMysql(host=host, user=user, passwd=passwd, db=database, port=port)


@api.route('/blueprint', methods=['GET'])
def get_all_blueprint():
    """
    get all blueprint
    """
    res = db.mysql_search_blueprint()
    return jsonify(res), 200


@api.route('/blueprint/<id>', methods=['GET'])
def get_one_blueprint(id):
    """
    get one blueprint
    as: /blueprint/1
    """
    res = db.mysql_search_one_blueprint(id)
    return jsonify(res), 200


@api.route('/blueprint', methods=['POST'])
def new_blueprint():
    """
    add new blueprint
    as: POST ... /blueprint
    """
    if not request.json:
        return jsonify({"info": "error", "message":
                        "request not have json data!", "result": {}}), 400
    name = request.json['name']
    components = request.json['components']
    rolename = request.json['rolename']
    content = JSONEncoder().encode(request.json['content'])
    if db.mysql_check_blueprint_byname(name).get("result") == 0:
        rowid = db.mysql_insert_one_blueprint(name, components, rolename,
                                              content)
        res = db.mysql_search_one_blueprint(rowid["result"])
        return jsonify(res), 2001
    else:
        return jsonify({"info": "error",
                        "message": "db have a record!", "result": {}}), 400


@api.route('/blueprint/<id>', methods=['PUT'])
def update_one_blueprint(id):
    """
    update one blueprint
    as: PUT ... /blueprint/1
    """
    if not request.json:
        return jsonify({"info": "error", "message":
                        "request not have json data!", "result": {}}), 400
    name = request.json['name']
    components = request.json['components']
    rolename = request.json['rolename']
    content = JSONEncoder().encode(request.json['content'])
    row = db.mysql_search_one_blueprint(id)
    # return jsonify(row["result"]), 222
    if row["result"]:
        rowid = db.mysql_update_one_blueprint(id, name, components, rolename,
                                              content)
        res = db.mysql_search_one_blueprint(int(rowid["result"]))
        return jsonify(res), 2002
    else:
        return jsonify({"info": "error",
                        "message": "db have not record!", "result": {}}), 400


@api.route('/blueprint/<id>', methods=['DELETE'])
def delete_one_blueprint(id):
    """
    delete one blueprint
    as: DELETE /blueprint/1
    """
    row = db.mysql_search_one_blueprint(id)
    if row["result"]:
        res = db.mysql_delete_one_blueprint(id)
        return jsonify(res), 2003
    else:
        return jsonify({"info": "error",
                        "message": "db have not record!", "result": {}}), 400


@api.route('/blueprintsave/<id>', methods=['GET'])
def save_blueprint(id):
    """
    save one blueprint to file
    as: GET /blueprintsave/1
    """
    res = {}
    path = "tmp/"
    blueprint = db.mysql_search_one_blueprint(id)
    if blueprint["result"]:
        components = blueprint["result"]["components"].split(',')
        components_tag = '_'.join(map((lambda x: x[:2]), components))
        roles = blueprint["result"]["rolename"].split(',')
        roles_tag = sum([int(x) for x in roles])
        blueprint_filename = "blueprint_{0}.{1}".format(components_tag, str(roles_tag))
        res["blueprint_file"] = blueprint_filename
        res["blueprint_path"] = path

        json.dump(json.loads(blueprint["result"]["content"]),
                  open(path + blueprint_filename, 'w'))
        return jsonify(res), 2004
    else:
        return jsonify({"info": "error",
                        "message": "db have not record!", "result": {}}), 400
