import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from m01_qr import StrictJsonPostTransport, TransportError


class Handler(BaseHTTPRequestHandler):
    calls = []
    response_body = {"status": "Success"}

    def do_POST(self):
        size = int(self.headers.get("Content-Length", "0"))
        body = json.loads(self.rfile.read(size))
        type(self).calls.append((self.path, body, self.headers.get("Content-Type")))
        encoded = json.dumps(type(self).response_body).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, _format, *_args):
        pass


class M01HTTPTransportTests(unittest.TestCase):
    def setUp(self):
        Handler.calls = []
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def test_posts_exact_json_once_to_explicit_loopback_target(self):
        transport = StrictJsonPostTransport(timeout_seconds=1.0)
        port = self.server.server_address[1]
        response = transport(
            f"http://127.0.0.1:{port}/api/led",
            {"red": 255, "green": 105, "blue": 180},
        )
        self.assertEqual(response, {"status": "Success"})
        self.assertEqual(
            Handler.calls,
            [("/api/led", {"red": 255, "green": 105, "blue": 180}, "application/json")],
        )

    def test_rejects_unsafe_configuration_without_network(self):
        for timeout in (0, -1, 5.1):
            with self.assertRaises(TransportError):
                StrictJsonPostTransport(timeout_seconds=timeout)
        transport = StrictJsonPostTransport()
        with self.assertRaises(TransportError):
            transport("file:///tmp/not-network", {"red": 1, "green": 2, "blue": 3})


if __name__ == "__main__":
    unittest.main()
