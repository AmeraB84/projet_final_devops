import http.server

port = 80
server_address = ("", port)

server = http.server.HTTPServer
handler = http.server.CGIHTTPRequestHandler
handler.cgi_directories = [""]

httpd = server(server_address, handler)
httpd.serve_forever()
