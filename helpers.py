from collections.abc import (Sequence, Collection)


def _col_but_not_str(obj):
    return isinstance(obj, Collection) and not isinstance(obj, (str, bytes, bytearray))


def _seq_but_not_str(obj):
    return isinstance(obj, Sequence) and not isinstance(obj, (str, bytes, bytearray))
