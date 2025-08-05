#!/usr/bin/env python3
# -*- coding: utf-8

import os
import sys
import time
import logging
import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import threading
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('einsteindb_server.log')
    ]
)
logger = logging.getLogger('EinsteinDBServer')

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    daemon_threads = True

class EinsteinDBRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests."""
        try:
            if self.path == '/status':
                self._set_headers()
                response = {
                    'status': 'running',
                    'version': '1.0.0',
                    'timestamp': time.time()
                }
                self.wfile.write(json.dumps(response).encode('utf-8'))
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({'error': 'Not found'}).encode('utf-8'))
        except Exception as e:
            logger.error(f"Error handling GET request: {str(e)}")
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': 'Internal server error'}).encode('utf-8'))
    
    def do_POST(self):
        """Handle POST requests."""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            logger.info(f"Received data: {data}")
            
            # Process the request here
            response = {
                'status': 'success',
                'message': 'Request processed',
                'data': data
            }
            
            self._set_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except json.JSONDecodeError:
            self._set_headers(400)
            self.wfile.write(json.dumps({'error': 'Invalid JSON'}).encode('utf-8'))
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': 'Internal server error'}).encode('utf-8'))

def run_server(port=8000):
    """Run the HTTP server."""
    server_address = ('', port)
    httpd = ThreadedHTTPServer(server_address, EinsteinDBRequestHandler)
    logger.info(f"Starting EinsteinDB server on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='EinsteinDB Server')
    parser.add_argument('--port', type=int, default=8000, help='Port to run the server on')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    
    args = parser.parse_args()
    
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")
    
    try:
        run_server(args.port)
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        sys.exit(1)
