import requests
import http.server
import socketserver

Handler = "http://deta224.cs.uky.edu"
PORT = 9000

with socketserver.TCPServer(("", PORT), Handler) as http:
    print("serving at port", PORT)
    http.serve_forever()
