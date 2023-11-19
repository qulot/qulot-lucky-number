
import typing


def bits_length(obj: typing.Union[int, typing.Any]) -> int:
    """get bits length of obj

    Args:
        obj (typing.Union[int, typing.Any]): obj to get bits length

    Returns:
        int: bits length of obj input
    """
    if isinstance(obj, int):
        return obj.bit_length()

    raise NotImplementedError(f'check {type(obj)} not implemented!')


def bits_to_int(bits: str):
    """convert bits string to integer

    Args:
        bits (str): bits list as string

    Returns:
        _type_: integer number
    """
    return int(bits, 2)
