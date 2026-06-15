"""Hide the contents of a text file inside a PNG using LSB steganography."""

from __future__ import annotations

import random
from pathlib import Path

from PIL import Image

from steganography import CARRIERS_DIR
from steganography.bits import clear_last_bit, set_last_bit, text_to_bits

# A 1 followed by 40 zeros marks the end of the hidden message. The decoder
# stops once it sees a run of 35 zero bits, so I lead with a 1 (the run can
# never start early inside real data) and pad with far more zeros than the
# decoder needs -- the extra margin means the marker survives even though the
# final, partially filled pixel is intentionally left unwritten below.
END_OF_MESSAGE = "1" + "0" * 40

CARRIER_COUNT = 5  # carriers are named 1.png .. 5.png


def random_carrier_path(carriers_dir: Path = CARRIERS_DIR) -> Path:
    """Pick one of the carrier images at random."""
    return carriers_dir / f"{random.randrange(1, CARRIER_COUNT + 1)}.png"


def encode_text(text: str, carrier_path: Path) -> Image.Image:
    """Embed ``text`` into the carrier at ``carrier_path`` and return the image.

    I walk the pixels left to right, top to bottom and write one message bit
    into the LSB of each colour channel. A pixel is only saved once all three
    of its channels have taken a bit, so a trailing partial pixel is dropped --
    which is exactly why END_OF_MESSAGE carries so many spare zeros.
    """
    bits = text_to_bits(text) + END_OF_MESSAGE
    total_bits = len(bits)

    image = Image.open(carrier_path)
    width, height = image.size
    pixels = image.load()

    index = 0
    for row in range(height - 1):
        for col in range(width - 1):
            channels = list(pixels[col, row])
            for channel in range(3):
                if index >= total_bits:
                    return image
                channels[channel] = (
                    set_last_bit(channels[channel])
                    if bits[index] == "1"
                    else clear_last_bit(channels[channel])
                )
                index += 1
            pixels[col, row] = tuple(channels)
    return image


def encode_file(text_path, output_path, carrier_path: Path | None = None) -> Path:
    """Read ``text_path``, hide it in a carrier image, and save to ``output_path``.

    When no carrier is given I pick one at random, mirroring how the server
    serves a different-looking image on each request.
    """
    with open(text_path) as handle:
        text = handle.read()
    if carrier_path is None:
        carrier_path = random_carrier_path()
    image = encode_text(text, carrier_path)
    image.save(output_path, "PNG")
    return Path(output_path)
