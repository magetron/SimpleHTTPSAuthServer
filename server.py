import os
import ssl
import logging
import http.server
from base64 import b64decode

# Logging Setup
logging.basicConfig(filename='server.log', level=logging.DEBUG)
logger = logging.getLogger()


class BasicAuthHandler(http.server.SimpleHTTPRequestHandler):

    # base64 encoded username:password
    key = 'dXNlcm5hbWU6cGFzc3dvcmQ='

    def do_HEAD(self):
        '''Send Headers'''
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        '''Send Basic Auth Headers'''
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        '''Handle GET Request'''
        try:
            if self.headers.get('Authorization') is None:
                # Send Auth Headers
                self.do_AUTHHEAD()
                logger.debug('Auth Header Not Found')
                self.wfile.write(bytes('Unauthorized', 'utf8'))
            elif self.headers.get('Authorization') == 'Basic ' + self.key:
                # Successful Auth
                http.server.SimpleHTTPRequestHandler.do_GET(self)
            else:
                print(self.headers.get('Authorization'))
                # Bad Credentials Supplied
                self.do_AUTHHEAD()
                auth_header = self.headers.get('Authorization')
                # Log Bad Credentials
                if len(auth_header.split(' ')) > 1:
                    logger.debug(auth_header.split(' ')[1])
                    logger.debug(b64decode(auth_header.split(' ')[1]))
                logger.debug('Bad Creds')
                self.wfile.write(bytes('Unauthorized', 'utf8'))
        except Exception:
            logger.error("Error in GET Functionality", exc_info=True)

    def date_time_string(self, time_fmt='%s'):
        return ''

    def log_message(self, format, *args):
        '''Requests Logging'''
        logger.debug("%s - - [%s] %s" % (
            self.client_address[0],
            self.log_date_time_string(),
            format % args))


if __name__ == '__main__':

    # Create Handler Instance
    handler = BasicAuthHandler

    # Server Header 
    handler.server_version = ' '
    handler.sys_version = ''

    # SimpleHTTPServer Setup
    httpd = http.server.HTTPServer(('', 443), handler)
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile='site.crt', keyfile='site.key', server_side=True)
    try:
        if not os.path.isdir('./files'):
            os.makedirs('./files')
        os.chdir('./files')
        httpd.serve_forever()
    except Exception:
        logger.error("Fatal error in main loop", exc_info=True)

