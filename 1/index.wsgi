import sae
import app

import json
from django.http import *


def appr(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/html; charset=utf-8')]
    start_response(status, response_headers)
    return ['<strong>Welcome to SAE!</strong>']

def getin(environ,start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/json; charset=utf-8')]
    start_response(status, response_headers)
   
    content = []
    
    for k,v in environ.items():
    	content.append('%s : %s' % (k, v))

    
    #req = HttpRequest()
    #cont = environ.get('QUERY_STRING').split('=')[1]
   	
    return json.dumps(content)
    

application = sae.create_wsgi_app(app.app)
