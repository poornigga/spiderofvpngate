# -*- coding: utf-8 -*-

import os
import json
import time

import sae
import sae.const
import MySQLdb

import bottle
from bottle import run
from bottle import route
from bottle import request
from bottle import response
from bottle import default_app


title_5pn = ['ip', 'country', 'host', 'quality',
             'info', 'perfor', 'ssl5pn', 'open5pn', 'uptimes']

DEV_ROOT = os.path.realpath(os.path.dirname(__file__))


@route('/upload', method='POST')
def push_contents():
    try:
        bingo = json.load(request.body)

        conn = db_open()
        c = conn.cursor()

        try:
            for item in bingo:
                c.execute("""INSERT INTO 5pn VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (item['ip'], item['country'], item[
                          'host'], item['quality'], item['info'], item['perfor'], item['ssl5pn'], item['open5pn'], time.time()))

            conn.commit()
        except:
            conn.rollback()

        db_clear()
        return {'code': 200, 'content': 'success'}

    except Exception as e:
        return e


daysf = 24.0 * 60 * 60


def db_clear():
    try:
        conn = db_open()
        c = conn.cursor()
        delstr = 'delete from 5pn where uptimes < %s'
        c.execute(delstr, (time.time() - daysf))
        c.commit()
        conn.close()

    except Exception as e:
        return e


def fmt_output(data):
    if not data:
        return []

    lines = []
    for row in data:
        section = {}
        for idx, col in enumerate(row):
            section[title_5pn[idx]] = col
        del section['uptimes']
        lines.append(section)

    return lines


def db_open():
    try:
        db = MySQLdb.connect(host=sae.const.MYSQL_HOST,
                             user=sae.const.MYSQL_USER,
                             passwd=sae.const.MYSQL_PASS,
                             db=sae.const.MYSQL_DB,
                             port=int(sae.const.MYSQL_PORT))
    except Exception as e:
        return e
    return db


def db_fetch(sql, arg0=False, fetchnum=-1):
    if not sql:
        return []

    conn = db_open()
    c = conn.cursor()
    if arg0:
        c.execute(sql, (arg0))
    else:
        c.execute(sql)

    result = []
    if fetchnum == -1:
        result = c.fetchall()
    else:
        result = c.fetchmany(fetchnum)
    conn.close()
    return fmt_output(result)


@route('/fast', method='GET')
def find_item():
    query_str = 'select * from 5pn order by quality desc'
    content = db_fetch(query_str, fetchnum=20)
    if not content:
        return {'status': 'Faild'}
    return {'status': 'ok', 'content': content, 'count': len(content)}


@route('/new', method='GET')
def callback():
    ct = '10'
    if 'num' in request.GET.keys():
        ct = request.GET['num']

    query_str = 'select * from 5pn order by uptimes desc'
    lines = db_fetch(query_str, fetchnum=int(ct))
    if not lines:
        return {'status': 'Faild'}
    return {'status': 'ok', 'content': lines, 'count': len(lines)}


@route('/country', method='GET')
def query_data():
    try:
        ct = request.GET['key']
        qrystr = 'select * from 5pn where country = %s'
        lines = db_fetch(qrystr, arg0=ct)
        if not lines:
            return {'status': 'Faild'}

        return {'status': 200, 'content': lines, 'count': len(lines)}
    except Exception as e:
        return e


app = default_app()
