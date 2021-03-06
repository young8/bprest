# -*- coding: utf-8 -*-
import os
import time
import json
import ConfigParser
from json import JSONEncoder
from flask import request, jsonify
from mysql import PyMysql
from . import api


"""
mysql config
"""
cf = ConfigParser.ConfigParser()
cf.read("app/api_1_0/config.txt")
host = cf.get('mysql', 'host')
port = cf.getint('mysql', 'port')
user = cf.get('mysql', 'user')
passwd = cf.get('mysql', 'passwd')
database = cf.get('mysql', 'db')
db = PyMysql(host=host, user=user, passwd=passwd, db=database, port=port)

"""
publish config
"""
publish_file = cf.get('publish', 'publish_file')
publish_source = cf.get('publish', 'publish_source')
publish_target = cf.get('publish', 'publish_target')


@api.route('/hostmapping', methods=['GET'])
def get_all_hostmapping():
    """
    get all hostmapping
    """
    res = db.mysql_search_hostmapping()
    return jsonify(res), 200


@api.route('/hostmapping/<id>', methods=['GET'])
def get_one_hostmapping(id):
    """
    get one hostmapping
    as: /hostmapping/1
    """
    res = db.mysql_search_one_hostmapping(id)
    return jsonify(res), 200


@api.route('/hostmapping', methods=['POST'])
def new_hostmapping():
    """
    add new hostmapping
    as: POST ... /hostmapping
    """
    if not request.json:
        return jsonify({"info": "error", "message":
                        "request not have json data!", "result": {}}), 400
    rolename = request.json['rolename']
    content = JSONEncoder().encode(request.json['content'])
    if db.mysql_check_hostmapping_byname(rolename).get("result") == 0:
        rowid = db.mysql_insert_one_hostmapping(rolename, content)
        res = db.mysql_search_one_hostmapping(rowid["result"])
        return jsonify(res), 200
    else:
        return jsonify({"info": "error",
                        "message": "db have a record!", "result": {}}), 400


@api.route('/hostmapping/<id>', methods=['PUT'])
def update_one_hostmapping(id):
    """
    update one hostmapping
    as: PUT ... /hostmapping/1
    """
    if not request.json:
        return jsonify({"info": "error", "message":
                        "request not have json data!", "result": {}}), 400
    rolename = request.json['rolename']
    content = JSONEncoder().encode(request.json['content'])
    row = db.mysql_search_one_hostmapping(id)
    # return jsonify(row["result"]), 222
    if row["result"]:
        rowid = db.mysql_update_one_hostmapping(id, rolename, content)
        res = db.mysql_search_one_hostmapping(int(rowid["result"]))
        return jsonify(res), 200
    else:
        return jsonify({"info": "error",
                        "message": "db have not record!", "result": {}}), 400


@api.route('/hostmapping/<id>', methods=['DELETE'])
def delete_one_hostmapping(id):
    """
    delete one hostmapping
    as: DELETE /hostmapping/1
    """
    row = db.mysql_search_one_hostmapping(id)
    if row["result"]:
        res = db.mysql_delete_one_hostmapping(id)
        return jsonify(res), 200
    else:
        return jsonify({"info": "error",
                        "message": "db have not record!", "result": {}}), 400


@api.route('/hostmappingsave/<id>', methods=['GET'])
def save_hostmapping(id):
    """
    save one hostmapping to file
    as: GET /hostmappingsave/1
    """
    res = {}
    hostmapping = db.mysql_search_one_hostmapping(id)
    if hostmapping["result"]:
        roles = hostmapping["result"]["rolename"].split(',')
        roles_tag = sum([int(x) for x in roles])
        hostmapping_filename = "hostmapping.{0}".format(str(roles_tag))
        release_file = publish_source + hostmapping_filename
        db.mysql_release_one_hostmapping(id, release_file, time.strftime('%Y-%m-%d %H:%M:%S'))
        res = db.mysql_search_one_hostmapping(id)
        json.dump(json.loads(hostmapping["result"]["content"]), open(publish_source + hostmapping_filename, 'w'))
        return jsonify(res), 200
    else:
        return jsonify({"info": "error",
                        "message": "db have not record!", "result": {}}), 400


@api.route('/hostmappingremove/<id>', methods=['GET'])
def remove_hostmapping(id):
    """
    remove one hostmapping
    as: GET /hostmappingremove/1
    """
    res = {}
    hostmapping = db.mysql_search_one_hostmapping(id)
    if hostmapping["result"]:
        release_file = hostmapping["result"]["release_file"]
        db.mysql_release_one_hostmapping(id, None, None)
        res = db.mysql_search_one_hostmapping(id)
        os.remove(release_file)

        return jsonify(res), 200
    else:
        return jsonify({"info": "error",
                        "message": "db have not record!", "result": {}}), 400
