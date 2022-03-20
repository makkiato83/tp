import sys
import signal

def catch_the_signal(signal, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, catch_the_signal)

import os
import logging
import socket
from threading import Thread
from contextlib import closing
from http.server import BaseHTTPRequestHandler, HTTPServer
from stem.control import Controller as Controller
from stem import SocketError as StemSocketError
from stem import process
import click



# Handler for Http requests.
# It tries to understand if the content is text/html (UTF-8) or binary, and sends appropriate headers.
class MyHandler(BaseHTTPRequestHandler):
    data_to_send = None
    def do_GET(self):
        is_unicode = True
        try:
            self.data_to_send.decode('utf-8')
        except UnicodeDecodeError:
            is_unicode = False

        self.send_response(200)
        if is_unicode:
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(self.data_to_send)
        else:
            self.send_header("Content-type", "application/octet-stream")
            self.end_headers()
            self.wfile.write(self.data_to_send)

# Minimal HTTP server
class Httpd():
    def __init__(self, data,  logger, port = 5050):
        server_address = ('localhost', port)
        MyHandler.data_to_send = data
        self.logger = logger
        self.server = HTTPServer(server_address, MyHandler)
        self.server.handle_request()


class MainThread(Thread):
    def __init__(self, data_to_send, logger, wait, port):
        Thread.__init__(self)
        self.data_to_send = data_to_send
        self.controller = None
        self.service = None
        self.logger = logger
        self.wait = wait
        self.port = port

    @staticmethod
    def find_free_port():   # Asks the OS for a port number available for listening.
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            s.bind(('localhost', 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return s.getsockname()[1]

    def run(self):
        # Handle CTRL-C with dedicated procedure
        signal.signal(signal.SIGINT, self.handle_keyboardInterrupt)

        # Get a port available for listening.
        local_port = self.find_free_port()

        # create TOR controller
        self.controller = Controller.from_port()
        self.controller.authenticate()

        # Create Hidden Service
        self.service = self.controller.create_ephemeral_hidden_service({80: local_port}, await_publication=False)

        # Print out Onion address.
        print(self.service.service_id + f'.onion')

        self.logger.info(f'Successfully created Hidden service: {self.service.service_id + f".onion"}, listening on localhost:{local_port}.')

        if not self.wait:
            n = os.fork()
            # n greater than 0  means parent process
            if n > 0:
                sys.exit()

        # Start HTTP server on localhost:local_port
        server = Httpd(self.data_to_send, port=local_port, logger = self.logger)

        # Once the page has been served, remove the hidden service and terminate
        self.controller.remove_ephemeral_hidden_service(self.service.service_id)
        self.logger.info(f'Hidden service {self.service.service_id}.onion properly terminated.')
        sys.exit()

    def handle_keyboardInterrupt(self, signal, frame):
        try:
            self.controller.remove_ephemeral_hidden_service(self.service.service_id)
            self.logger.info(f'Hidden service {self.service.service_id}.onion properly terminated.')
            self.logger.info('Exiting (CTRL-C).')
            sys.exit()
        except Exception as e:
            self.logger.error(f'Error while exiting (CTRL-C): {e}')
            sys.exit()


# create logger
logger = logging.getLogger("TP")
logger.setLevel(logging.ERROR)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter('%(levelname)s : %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)


@click.command()
@click.option('--blocking', '-b', is_flag=True, default=False, help='Returns only after the content is fully delivered. [Default = False]')
@click.option('--port', '-p', default=9151, help='Tor Socks port. Usually set in the torrc file. [Default = 9151]')
def cli(blocking, port):
    """
    Documentation
    """
    try:
        data_input = sys.stdin.buffer.read()
        thread = MainThread(data_to_send=data_input, logger=logger, wait = blocking, port = port)
        thread.run()
    except StemSocketError:
        logger.critical('Could not connect to the Tor socks. Is Tor Running?')
        sys.exit()








