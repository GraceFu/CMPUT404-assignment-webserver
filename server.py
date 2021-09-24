#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        # print ("Got a request of: %s\n" % self.data)
        # self.request.sendall(bytearray("OK",'utf-8'))

        request_data = self.data.decode('utf-8')
        request_method = request_data.split()[0]
        request_uri = request_data.split()[1]

        response = self.handle_response(request_method, request_uri)
        self.request.sendall(bytearray(response,'utf-8'))

    def handle_response(self, method, uri):
        path = "./www" + uri
        # 1. Methods we cant handle
        if method != "GET":
            return self.code_405()
        # 2. Wrong path ending
        elif path[-1] != "/":
            if os.path.isdir(path):
                path += "/"
                return self.code_301(path)
            else:
                return self.code_404()
        # 3. Correct path
        else:
            path += "index.html"
            content = self.get_content(path)
            if content == None:
                return self.code_404()
            else:
                return self.code_200(path, content)

    def code_200(self, uri, body):
        header = "HTTP/1.1 200 OK\r\n"
        response = header + body
        return response

    def code_301(self, uri):
        header = "HTTP/1.1 301 Moved Permanently\r\n"
        body = "Location: " + uri
        response = header + body
        return response

    def code_404(self):
        header = "HTTP/1.1 404 Not Found\r\n"
        body = "404 Not Found\r\n"
        response = header + body
        return response

    def code_405(self):
        header = "HTTP/1.1 405 Method Not Allowed\r\n"
        body = "Method Not Allowed\r\n"
        response = header + body
        return response

    def get_content(self, path):
        try:
            file = open(path, "r")
            content = file.read()
            return content
        except:
            return


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
