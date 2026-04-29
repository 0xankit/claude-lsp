#!/usr/bin/env python3
"""
Null LSP server used for disabled languages.

Responds to `initialize` with empty capabilities so Claude Code considers the
server started successfully. Responds to `shutdown` then exits cleanly.
All other requests get a method-not-found error, which is spec-compliant for
a server that exposes no capabilities.
"""
import sys
import json


def read_message(stream):
    headers = {}
    while True:
        line = stream.readline()
        if not line or line in (b"\r\n", b"\n"):
            break
        if b":" in line:
            key, _, val = line.partition(b":")
            headers[key.strip().lower()] = val.strip()
    length = int(headers.get(b"content-length", 0))
    if length > 0:
        return json.loads(stream.read(length))
    return None


def write_message(stream, msg):
    body = json.dumps(msg).encode()
    stream.write(b"Content-Length: " + str(len(body)).encode() + b"\r\n\r\n" + body)
    stream.flush()


def main():
    stdin = sys.stdin.buffer
    stdout = sys.stdout.buffer

    while True:
        try:
            msg = read_message(stdin)
        except Exception:
            break
        if msg is None:
            break

        method = msg.get("method", "")
        msg_id = msg.get("id")

        # Notifications have no id — skip silently
        if msg_id is None:
            continue

        if method == "initialize":
            write_message(stdout, {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "capabilities": {},
                    "serverInfo": {"name": "null-lsp (language disabled)", "version": "0.0.0"},
                },
            })
        elif method == "shutdown":
            write_message(stdout, {"jsonrpc": "2.0", "id": msg_id, "result": None})
            break
        else:
            write_message(stdout, {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32601, "message": "Method not found"},
            })


if __name__ == "__main__":
    main()
