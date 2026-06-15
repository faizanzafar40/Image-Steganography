"""Recover text hidden in a PNG by :mod:`steganography.encoder`."""

from __future__ import annotations

import argparse

from PIL import Image

from steganography.bits import bits_to_text

# The encoder ends the message with a 1 and a long run of zeros; once I have
# seen this many zero bits in a row I know the payload is over.
ZERO_RUN_TO_STOP = 35


def decode_image(image_path) -> str:
    """Read the hidden message out of ``image_path`` and return it as text.

    I read one bit from the LSB of each colour channel, in the same pixel order
    the encoder used, counting consecutive zeros. The moment that run reaches
    the end-of-message length I stop.
    """
    image = Image.open(image_path)
    width, height = image.size
    pixels = image.load()

    bits = []
    zero_run = 0
    stop = False
    for row in range(height - 1):
        if stop:
            break
        for col in range(width - 1):
            r, g, b = pixels[col, row]
            for channel in (r, g, b):
                if zero_run == ZERO_RUN_TO_STOP:
                    stop = True
                    break
                bit = channel & 1
                bits.append(str(bit))
                zero_run = zero_run + 1 if bit == 0 else 0
            if stop:
                break

    payload = "".join(bits)
    # Strip the end-of-message marker: the run of zeros I just counted plus the
    # single 1 that precedes it.
    payload = payload[: len(payload) - zero_run - 1]
    return bits_to_text(payload)


def main() -> None:
    parser = argparse.ArgumentParser(description="Decode text hidden in a PNG image.")
    parser.add_argument("image", help="path to the encoded PNG image")
    args = parser.parse_args()
    print(decode_image(args.image))


if __name__ == "__main__":
    main()
