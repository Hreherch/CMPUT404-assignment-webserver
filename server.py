#  coding: utf-8 
import socketserver
from os import path

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

class MyWebServer(socketserver.BaseRequestHandler):
    def do404(self):
        return self.doResponse("<h1>Error 404: Page Not Found</h1>", status=404)

    def doResponse(self, content, status=200, headers={}):
        # protect from explosions
        if status not in responseCodeInfo:
            content = "Error: Attempted to use a status code not in the response dictionary ({STATUS}).".format(STATUS=status)
            status = 500

        responseTemplate = ""
        responseTemplate += "HTTP/1.1 {STATUS} {STATUS_DESC}\r\n".format(
            STATUS=status,
            STATUS_DESC=responseCodeInfo[status]
        )
        responseTemplate += "Connection: close\r\n"
        # add headers
        for key in headers:
            if len(key) and len(headers[key]):
                responseTemplate += "{KEY}: {VALUE}\r\n".format(
                    KEY=key,
                    VALUE=headers[key]
                )
        responseTemplate += "\r\n"
        responseTemplate += "{CONTENT}".format(
            CONTENT=content
        )

        self.request.sendall(bytearray(responseTemplate, "utf-8"))
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        decoded_string = self.data.decode()
        split_string = decoded_string.split()
        # print("RECEIVED:\n***")
        # print(decoded_string)
        # print("***")
        method = split_string[0]
        dest = split_string[1]

        if (method != "GET"):
            return self.doResponse("Error: You may only use GET with this webserver.")
        #print("TO ACCESS WITH", method, "\b:", dest)
        dest = "./www" + dest

        if not path.isfile(dest):
            #print(dest, "is not file!")
            if not path.isdir(dest):
                #print(dest, "is not dir!")
                return self.do404()
            else:
                if dest[-1] != "/":
                    dest += "/"
                dest += "index.html"
                if not path.isfile(dest):
                    #print(dest, "still not file!")
                    return self.do404()

        if "www/" not in path.abspath(dest):
            return self.do404()
        
        f = open(dest, "r")
        fileData = f.read()
        f.close()
        contentType = "text/" + dest.split(".")[-1]
        headers = {"Content-Type": contentType}
        self.doResponse(fileData, headers=headers)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
