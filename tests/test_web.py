import json
import threading
import time
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer

from pulse_prediction.web import PulseWebHandler


def _start_test_server() -> tuple[ThreadingHTTPServer, int]:
    server = ThreadingHTTPServer(("127.0.0.1", 0), PulseWebHandler)
    port = server.server_port
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.05)
    return server, port


def test_home_page_loads() -> None:
    server, port = _start_test_server()
    conn = HTTPConnection("127.0.0.1", port)
    conn.request("GET", "/")
    response = conn.getresponse()
    body = response.read().decode("utf-8")
    server.shutdown()

    assert response.status == 200
    assert "Pulse Prediction System" in body


def test_assess_endpoint_returns_assessment() -> None:
    server, port = _start_test_server()
    conn = HTTPConnection("127.0.0.1", port)
    payload = json.dumps({"heart_rate": 112, "systolic_bp": 168, "diastolic_bp": 104})

    conn.request("POST", "/api/assess", body=payload, headers={"Content-Type": "application/json"})
    response = conn.getresponse()
    body = json.loads(response.read().decode("utf-8"))
    server.shutdown()

    assert response.status == 200
    assert body["risk_level"] == "high"
    assert body["risk_score"] >= 5


def test_assess_endpoint_rejects_bad_input() -> None:
    server, port = _start_test_server()
    conn = HTTPConnection("127.0.0.1", port)
    payload = json.dumps({"heart_rate": "abc", "systolic_bp": 120, "diastolic_bp": 80})

    conn.request("POST", "/api/assess", body=payload, headers={"Content-Type": "application/json"})
    response = conn.getresponse()
    body = json.loads(response.read().decode("utf-8"))
    server.shutdown()

    assert response.status == 400
    assert "must be integers" in body["error"]
