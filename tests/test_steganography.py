"""Round-trip and server tests that pin down what the project must keep doing."""

import random

import pytest

from steganography import SAMPLES_DIR
from steganography.bits import bits_to_text, text_to_bits
from steganography.decoder import decode_image
from steganography.encoder import encode_file, random_carrier_path
from steganography.server import handle_request

SAMPLE_FILES = sorted(SAMPLES_DIR.glob("file*.txt"))


@pytest.mark.parametrize(
    "text",
    ["Hello, World!", "a", "The quick brown fox 12345 ~!@#", "line1\nline2\n"],
)
def test_bits_round_trip(text):
    assert bits_to_text(text_to_bits(text)) == text


@pytest.mark.parametrize("sample", SAMPLE_FILES, ids=lambda p: p.name)
def test_encode_then_decode_recovers_the_file(sample, tmp_path):
    random.seed(42)
    output = tmp_path / "encoded.png"
    encode_file(sample, output)
    assert decode_image(output) == sample.read_text()


def test_carrier_choice_stays_in_range():
    random.seed(0)
    for _ in range(50):
        assert random_carrier_path().name in {f"{n}.png" for n in range(1, 6)}


def test_bad_request_for_unparseable_path():
    response = handle_request("GET / HTTP/1.1\r\n\r\n")
    assert response.startswith(b"HTTP/1.1 400 Bad request\nContent-type: text/html\n\n")


def test_not_found_for_missing_sample():
    response = handle_request("GET /file50.txt HTTP/1.1\r\n\r\n")
    assert response.startswith(b"HTTP/1.1 404 Not Found\nContent-type: text/html\n\n")


def test_ok_returns_png_payload(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # keep the runtime "Nmodified.png" out of the repo
    response = handle_request("GET /file2.txt HTTP/1.1\r\n\r\n")
    assert response.startswith(b"HTTP/1.1 200 OK\nContent-type: image/png\n\n")
    body = response.split(b"\n\n", 1)[1]
    assert body[:8] == b"\x89PNG\r\n\x1a\n"  # PNG magic number
