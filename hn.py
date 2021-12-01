#!/usr/bin/env python3

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request
import socks
import socket
import json

# simple Python HTTP server that grabs the top 10 new Hacker News stories and returns them
# as a json document
class HNServer(BaseHTTPRequestHandler):
    def do_GET(self):
        # set socks proxies to allow CLI to capture traffic
        # NOTE: this is unnecessary with other Python libs or other languages like Go, Java, etc
        #   We'll use urllib to give a complex example, however.
        socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 4140)
        socket.socket = socks.socksocket

        # retrieve list of Hackernews stories by IDs
        resp = urllib.request.urlopen('https://hacker-news.firebaseio.com/v0/newstories.json')
        self.send_response(resp.code)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        articles = resp.read()

        # convert id bytes into an array of strings
        articles_string = articles.decode('utf-8')
        articles_string = articles_string.replace('[','')
        articles_string = articles_string.replace(']','')
        articles_list = articles_string.split(',')

        # request the title of each article up to 10
        ret = {}
        for index, id in zip(range(10), articles_list):
            article_req = urllib.request.urlopen('https://hacker-news.firebaseio.com/v0/item/' + str(id) + '.json')
            dict = json.loads(article_req.read())
            ret[str(index)] = dict['title']

        # send back the titles as a JSON array
        self.wfile.write(json.dumps(ret, indent=4).encode("utf-8"))

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8080

    webServer = HTTPServer((host, port), HNServer)
    print("HTTP Server started at http://%s:%s" % (host, port))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("HTTP Server finished.")
