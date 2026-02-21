"""Simple full-stack web server for pulse and BP risk assessment (no external deps)."""

from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .model import assess_cardiovascular_risk

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"


class PulseWebHandler(BaseHTTPRequestHandler):
    """HTTP handler that serves UI and JSON API endpoints."""

    def _send_text(self, body: str, status: int = 200, content_type: str = "text/html") -> None:
        encoded = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def _send_json(self, payload: dict, status: int = 200) -> None:
        self._send_text(json.dumps(payload), status=status, content_type="application/json")

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/":
            return self._send_text((TEMPLATES_DIR / "index.html").read_text(encoding="utf-8"))

        if self.path == "/api/health":
            return self._send_json({"status": "ok"})

        if self.path == "/static/styles.css":
            return self._send_text(
                (STATIC_DIR / "styles.css").read_text(encoding="utf-8"),
                content_type="text/css",
            )

        if self.path == "/static/app.js":
            return self._send_text(
                (STATIC_DIR / "app.js").read_text(encoding="utf-8"),
                content_type="text/javascript",
            )

        return self._send_json({"error": "Not found"}, status=HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/api/assess":
            return self._send_json({"error": "Not found"}, status=HTTPStatus.NOT_FOUND)

        content_length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(content_length).decode("utf-8")

        try:
            data = json.loads(raw)
            heart_rate = int(data.get("heart_rate"))
            systolic_bp = int(data.get("systolic_bp"))
            diastolic_bp = int(data.get("diastolic_bp"))
        except (ValueError, TypeError, json.JSONDecodeError):
            return self._send_json(
                {"error": "heart_rate, systolic_bp, and diastolic_bp must be integers"},
                status=HTTPStatus.BAD_REQUEST,
            )

        try:
            result = assess_cardiovascular_risk(heart_rate, systolic_bp, diastolic_bp)
        except ValueError as exc:
            return self._send_json({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)

        return self._send_json(
            {
                "risk_level": result.risk_level,
                "risk_score": result.risk_score,
                "reasons": result.reasons,
            }
        )


def run(host: str = "0.0.0.0", port: int = 5000) -> None:
    """Run the web server."""
    server = ThreadingHTTPServer((host, port), PulseWebHandler)
    print(f"Serving Pulse Prediction System on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
