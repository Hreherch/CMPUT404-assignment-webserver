#  coding: utf-8 
import socketserver

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

responseCodeInfo = {
    200: "OK",
    403: "FORBIDDEN",
    404: "NOT FOUND",
    500: "INTERNAL SERVER ERROR"
}

responseTemplate = ""
responseTemplate += "HTTP/1.1 {STATUS} {STATUS_DESC}\r\n"
responseTemplate += "Connection: close\r\n"
responseTemplate += "\r\n"
responseTemplate += "{CONTENT}"

class MyWebServer(socketserver.BaseRequestHandler):
    def doResponse(self, status, content):
        # protect from explosions
        if status not in responseCodeInfo:
            content = "Error: Attempted to use a status code not in the response dictionary ({STATUS}).".format(STATUS=status)
            status = 500

        response = responseTemplate.format(
            STATUS=status,
            STATUS_DESC=responseCodeInfo[status],
            CONTENT=content
        )

        self.request.sendall(bytearray(response, "utf-8"))
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        decoded_string = self.data.decode()
        print("RECEIVED:\n***")
        print(decoded_string)
        print("***")
        # split_decode = decoded_string.split()
        # method = split_decode[0]
        # location = split_decode[1]

        # f = open("www/index.html", "r")
        # lines = f.read()
        # f.close()
        # lines = lines.encode("utf-8")
        # print("SENDING:\n***")
        # print(lines)
        # print("***")

        # if (method != "GET"):
        #     pass
        self.doResponse(220, "Hello World!")

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
