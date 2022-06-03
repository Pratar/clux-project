from http.server import BaseHTTPRequestHandler, HTTPServer
from apscheduler.schedulers.background import BackgroundScheduler as scheduler
import requests
import os
import logging
from urllib.parse import urlencode


def build_url(host, port):
    return f"http://{host}:{port}/ping"

def probe_request(url):

    headers = { 'Content-Type': 'text/html' }

    wait = os.environ[ 'WEB_ERROR_TIMEOUT' ]

    try:
        request = requests.get(url, headers = headers, timeout=int(wait) )
    except (requests.Timeout, requests.ConnectionError, requests.HTTPError) as err:
        logging.info("Error while trying to GET requiest")
        logging.debug(err)
        return False

    return True


def probe_job():
    logging.info('Check probe')

    host_list = [i.split(":") for i in os.environ.get("WEB_HOST_LIST").split(" ")]

    for h, p in host_list:
      logging.info( 'Check host ' + h + ' port ' + p )
      if probe_request(build_url(h, p)) != True:
         logging.info('Fail!')
         pass
      else:
         logging.info('Ok')


class WebServer(BaseHTTPRequestHandler):
    def do_GET(self):
       if self.path == '/ping':
          self.send_response(200)
          self.send_header("Content-type", "text/html")
          self.end_headers()
          self.wfile.write(bytes("pong\n", "utf-8"))


if __name__ == "__main__":

    host    = os.environ[ 'WEB_HOST' ]
    port    = os.environ[ 'WEB_PORT' ]
    timeout = os.environ[ 'WEB_CHECK_TIMEOUT' ]

    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    sch = scheduler()
    sch.add_job(probe_job, 'interval', seconds=int(timeout))
    sch.start()

    webServer = HTTPServer(( host, int(port)), WebServer)
    logging.info("Web server started " + host + " at port: " + port)
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    if sch.state:
       sch.shutdown()
       logging.info("Job probe stopped.")

    webServer.server_close()
    logging.info("Web server stopped.")
