"""A tiny socket HTTP server that hides a requested text file inside a PNG.

A client asks for ``/fileN.txt``; I encode that sample file into a randomly
chosen carrier image and hand back the resulting PNG. Anything I can't parse
gets a 400, and a request for a file I don't have gets a 404. I write the HTTP
responses by hand on purpose -- rolling the protocol myself was the whole point
of the exercise.
"""

from __future__ import annotations

import os
import re
import socket

from steganography import SAMPLES_DIR
from steganography.encoder import encode_file

HOST = "localhost"
PORT = 55555
MAX_CONNECTIONS = 10  # backlog of pending connections to accept
REQUEST_PATTERN = re.compile(r"file(\d+).txt")

BAD_REQUEST = (
    "HTTP/1.1 400 Bad request\nContent-type: text/html\n\n"
    "<html><head><title>400 Bad request</title></head><body>"
    "<p>Sorry, your request is invalid.</p></body><html>"
)
NOT_FOUND = (
    "HTTP/1.1 404 Not Found\nContent-type: text/html\n\n"
    "<html><head><title>404 Not Found</title></head><body>"
    "<p>Sorry, the object you requested was not found.</p></body><html>"
)
OK_HEADER = "HTTP/1.1 200 OK\nContent-type: image/png\n\n"


def load_bytes(path) -> bytes:
    """Read a file in binary mode."""
    with open(path, "rb") as handle:
        return handle.read()


def handle_request(request: str) -> bytes:
    """Turn a raw HTTP request into the bytes I should send back."""
    match = REQUEST_PATTERN.search(request)
    if match is None:
        return BAD_REQUEST.encode("utf-8")

    file_name = match.group(0)  # e.g. "file1.txt"
    number = match.group(1)  # e.g. "1"
    sample_path = SAMPLES_DIR / file_name
    if not os.path.isfile(sample_path):
        return NOT_FOUND.encode("utf-8")

    # Encode the sample into a fresh PNG, then stream that PNG back to the client.
    output_path = f"{number}modified.png"
    encode_file(sample_path, output_path)
    return OK_HEADER.encode("utf-8") + load_bytes(output_path)


def main() -> None:
    server = socket.socket()
    server.bind((HOST, PORT))
    server.listen(MAX_CONNECTIONS)
    while True:
        client, address = server.accept()
        print("Got connection from", address)
        request = client.recv(4096).decode("utf-8")
        client.send(handle_request(request))
        client.close()


if __name__ == "__main__":
    main()
