# -*- coding: utf-8 -*-

# import json
from json import JSONEncoder
from flask import request, jsonify
from . import api

from mysql import PyMysql
# from util import map_3, map_7, map_8

import ConfigParser


cf = ConfigParser.ConfigParser()
cf.read("app/api_1_0/config.txt")

host = cf.get('mysql', 'host')
port = cf.getint('mysql', 'port')
user = cf.get('mysql', 'user')
passwd = cf.get('mysql', 'passwd')
database = cf.get('mysql', 'db')


db = PyMysql(host=host, user=user, passwd=passwd, db=database, port=port)


@api.route('/plans', methods=['GET'])
def get_all_plans():
    """
    get all plan
    """
    res = db.mysql_search()
    return jsonify(res), 200


@api.route('/plans/', methods=['POST'])
def new_plan():
    """
    add new plan
    """
    if not request.json:
        return jsonify({"result": "error", "message": "request not have json data!"}), 400
    name = request.json['name']
    description = request.json['description']
    master = int(request.json['master'])
    slave = int(request.json['slave'])
    components = request.json['components']
    if len(db.mysql_search_one(name).get("result")) == 0:
        res = db.mysql_insert(name, description, master, slave, components)
        return jsonify(res), 201
    else:
        return jsonify({"result": "error", "message": "db have a record!"}), 400


@api.route('/plans/<name>', methods=['GET'])
def get_one_plan(name):
    """
    get one plan
    param: plan name, as: /plans/P01
    """
    res = db.mysql_search_one(name)
    return jsonify(res), 200


@api.route('/plans/<name>', methods=['DELETE'])
def delete_plan(name):
    """
    delete one plan
    param: plan name, as: /plans/P01
    """
    res = db.mysql_delete(name)
    return jsonify(res), 201


@api.route('/plans/<name>', methods=['PUT'])
def update_plan(name):
    """
    update one plan
    param: plan name, as: /plans/P01
    """
    if not request.json:
        return jsonify({"result": "error", "message": "request not have json data!"}), 400
    description = request.json['description']
    master = int(request.json['master'])
    slave = int(request.json['slave'])
    components = request.json['components']
    blueprint = JSONEncoder().encode(request.json['blueprint'])
    hostmapping = JSONEncoder().encode(request.json['hostmapping'])
    res = db.mysql_update(name, description, master, slave, components, blueprint, hostmapping)
    return jsonify(res), 201


@api.route('/plans/<int:master>/<int:slave>/<components>', methods=['GET'])
def get_plan(master, slave, components):
    """
    get one plan's blueprint and hostmapping
    """
    components = components.split(',')
    res = db.mysql_get_plan(master, slave, components)
    return jsonify(res), 200
