import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from api_client import APIClient


request_count = 0


class TestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global request_count

        request_count += 1

        print(f"Server received request #{request_count}")

        self.send_response(503)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(
            b'{"error": "Service unavailable"}'
        )

    def log_message(self, format, *args):
        pass


server = HTTPServer(("localhost", 8000), TestHandler)

server_thread = threading.Thread(
    target=server.serve_forever,
    daemon=True,
)

server_thread.start()


try:
    with APIClient() as client:
        client.get(
            "/test"
        )

except Exception as e:
    print(f"Final exception: {type(e).__name__}")
    print(f"Total requests: {request_count}")

finally:
    server.shutdown()