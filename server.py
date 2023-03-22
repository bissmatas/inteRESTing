try:
    import http.server as server
except ImportError:
    # Handle Python 2.x
    import SimpleHTTPServer as server

def diff_get_flag(httpd):
    return httpd.path == "/flag"

def diff_get_with_header(httpd):
    return httpd.path == "/flag" and httpd.headers.get("Is-Matas", "") == "True"

DEFAULT_GET_DIFFICULTY = diff_get_with_header
GET_DIFFICULTY = {'127.0.0.1': diff_get_with_header}
POST_FLAG = "' is a POST trophy"

GET_FLAG = "tarGET"

def parse_post_from_httpd(httpd):
    content_length = int(httpd.headers['Content-Length'])
    post_data = str(httpd.rfile.read(content_length), "ascii")
    var_vals = post_data.split("&")
    post_dict = {vv.split("=")[0]: vv.split("=")[1] for vv in var_vals}
    return post_dict


def post_diff_name_and_pass(httpd):
    try:
        post_dict = parse_post_from_httpd(httpd)
        return "name" in post_dict and post_dict.get("password", "") == "matas"
    except:
        return False

DEFAULT_POST_DIFFICULTY = post_diff_name_and_pass
POST_DIFFICULTY = {'127.0.0.1': post_diff_name_and_pass}
POST_FLAG = "' is a POST trophy"

FAIL_FLAG = "failed!"

class HTTPRequestHandler(server.BaseHTTPRequestHandler):
    """
    HTTPServer with custom responses
    """

    def do_POST(self):
        print("Received POST request from hanich at", self.client_address[0])
        if POST_DIFFICULTY.get(self.client_address[0], DEFAULT_POST_DIFFICULTY)(self): 
            print("POST challange solved by hanich at", self.client_address[0])
            self.send_response(server.HTTPStatus.OK)
            self.wfile.write(bytes(POST_FLAG + '\n', "ascii"))
        else:
            print("POST challange failed by hanich at", self.client_address[0])
            self.send_response(server.HTTPStatus.BAD_REQUEST)
            self.wfile.write(bytes(FAIL_FLAG + '\n', "ascii"))

    def do_GET(self):
        print("Received GET request from hanich at", self.client_address[0])
        if GET_DIFFICULTY.get(self.client_address[0], DEFAULT_GET_DIFFICULTY)(self): 
            print("GET challange solved by hanich at", self.client_address[0])
            self.send_response(server.HTTPStatus.OK)
            self.wfile.write(bytes(GET_FLAG + '\n', "ascii"))
        else:
            print("GET challange failed by hanich at", self.client_address[0])
            self.send_response(server.HTTPStatus.BAD_REQUEST)
            self.wfile.write(bytes(FAIL_FLAG + '\n', "ascii"))

PORT = 8080
Handler = HTTPRequestHandler

with server.HTTPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()

