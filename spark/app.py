# -*- coding: utf-8 -*-
import json
import requests

from em import mail_main
from htmlp import parser_url


def ezilaires(lst):
    result = []
    for i in lst:
        c = {}
        c['ip'] = i['ip_addr']['ip']
        if 'host' in i['ip_addr'].keys():
            c['host'] = i['ip_addr']['host']
        else:
            c['host'] = ''
        c['country'] = i['country']
        c['quality'] = i['quality']
        c['info']    = i['vpn_conn_info'].replace('.','')
        c['perfor']  = i['performance']
        c['ssl5pn']  = i['conn_supported']
        c['open5pn'] = i['openvpn_config']
        result.append(c)
    return result


def push_sae(lst):
    if not lst:
        return
    headers = {}
    headers['Content-Type'] = 'application/json'
    jdata = json.dumps(ezilaires(lst))
    r = requests.post(
        'http://1.iterator.sinaapp.com/upload', data=jdata, headers=headers)
    print r.text


if __name__ == '__main__':
    links = mail_main()
    for link in links:
        push_sae(parser_url(link))
