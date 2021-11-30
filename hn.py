from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import urllib.request
import json

# simple Python HTTP server that grabs the top 10 new Hacker News stories and returns them
# as a json document
class HNServer(BaseHTTPRequestHandler):
    def do_GET(self):
        resp = urllib.request.urlopen('https://hacker-news.firebaseio.com/v0/newstories.json')
        self.send_response(resp.code)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        articles = resp.read()
        # convert into an array of strings
        articles_string = articles.decode('utf-8')
        articles_string = articles_string.replace('[','')
        articles_string = articles_string.replace(']','')
        articles_list = articles_string.split(',')

        # send back the titles as a JSON array

        # request the title of each article up to 10
        ret = {}
        for index, id in zip(range(10), articles_list):
            article_req = urllib.request.urlopen('https://hacker-news.firebaseio.com/v0/item/' + str(id) + '.json')
            dict = json.loads(article_req.read())
            ret[str(index)] = dict['title']

        self.wfile.write(bytes(json.dumps(ret, indent=4), 'utf-8'))

if __name__ == "__main__":
    host = "localhost"
    port = 8080

    webServer = HTTPServer((host, port), HNServer)
    print("HTTP Server started at http://%s:%s" % (host, port))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("HTTP Server finished.")