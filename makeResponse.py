import os
from time import strftime, gmtime
import urllib

CONTENT_TYPE = {
    'txt': 'text/html',
    'html': 'text/html',
    'css': 'text/css',
    'js': 'application/javascript',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
    'swf': 'application/x-shockwave-flash',
}
SERVER = 'Server: MyServer \r\n'
CONNECTION = 'Connection: keep-alive \r\n'


def parse_request(request):
    try:
        print request
        data = request.split('\r\n')[0].split(' ')
        method = data[0]
        uri = data[1]
        uri = urllib.unquote(uri).decode('utf8')
        if '?' in uri:
            uri = uri.split('?')[0]
        httpv = data[2]
        return method, uri, httpv
    except:
        return 'NOTGETorHEAD', 'not important', 'HTTP/1.1'


def make_response(request, root):
    method, uri, httpv = parse_request(request)
    date = 'Date: ' + strftime("%a, %d %b %Y %H:%M:%S ", gmtime()) + '\r\n'
    content_type = ''
    content_length = ''
    if method in ['GET', 'HEAD']:
        if ('..' in uri) and (uri.split('.')[-1] not in CONTENT_TYPE.keys()):
            code = '400 '
            reason = ' Bad Request \r\n'
            body = False
        elif '.' in uri:
            if os.path.isfile(root+uri):
                code = '200'
                reason = ' OK\r\n'
                content_type = 'Content-Type: ' + CONTENT_TYPE[(uri.split('.')[-1]).lower()] + '\r\n\r\n'
                content_length = 'Content-Length: ' + str(os.stat(root+uri).st_size) + '\r\n'
                print root+uri
                if method == 'GET':
                    body = open(root+uri, 'rb')
                else:
                    body = False
            else:
                code = '404'
                reason = ' FILE NOT FOUND \r\n'
                body = False
                print root+uri + reason
        elif os.path.isfile(root+uri+'index.html'):
            code = '200'
            reason = ' OK\r\n'
            content_type = 'Content-Type: ' + CONTENT_TYPE['html'] + '\r\n\r\n'
            content_length = 'Content-Length: ' + str(os.stat(root+uri+'index.html').st_size) + '\r\n'
            print root+uri+'index.html'
            if method == 'GET':
                body = open(root+uri+'index.html', 'rb')
            else:
                body = False
        else:
            code = '403'
            reason = ' INDEX NOT FOUND \r\n'
            body = False
            print root+uri+'index.html' + reason

    else:
        code = '405'
        reason = ' BAD METHOD \r\n'
        body = False

    response = httpv + ' ' + code + reason + SERVER + date + CONNECTION + content_length + content_type
    return response, body


def do_response(connection, root):
    request = connection.recv(1024)
    response, body = make_response(request, root)
    connection.send(response)
    if body:
        chunk = body.read(1024)
        while (chunk):
                connection.send(chunk)
                chunk = body.read(1024)
        body.close()

