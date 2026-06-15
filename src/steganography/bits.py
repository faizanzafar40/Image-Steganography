"""Low-level bit helpers for hiding data in the least significant bit (LSB).

Every colour channel of every pixel carries exactly one bit of the message:
I flip only the LSB, which changes a value by at most 1 and is invisible to the
eye. These helpers are the smallest building blocks the encoder and decoder
share.
"""


def set_last_bit(value: int) -> int:
    """Force the least significant bit of ``value`` to 1."""
    return value | 1


def clear_last_bit(value: int) -> int:
    """Force the least significant bit of ``value`` to 0."""
    return value & ~1


def text_to_bits(text: str) -> str:
    """Turn a string into its binary digits.

    I treat the whole UTF-8 encoded string as one big integer and read its
    binary representation. ``bin()`` drops leading zeros, so the first byte may
    contribute fewer than 8 bits; :func:`bits_to_text` reverses this exactly by
    rebuilding the same integer, so nothing is lost on the round trip.
    """
    as_int = int.from_bytes(text.encode(), "big")
    return bin(as_int)[2:]


def bits_to_text(bits: str) -> str:
    """Rebuild the original string from its binary digits."""
    as_int = int("0b" + bits, 2)
    byte_count = (as_int.bit_length() + 7) // 8
    return as_int.to_bytes(byte_count, "big").decode()
