import typing


def split_chunks(l: typing.Union[typing.List[typing.Any], str], n: int):
    """Split list or array to chunks

    Args:
        l (typing.Union[typing.List[typing.Any], str]): list or string want split
        n (int): chunk size

    Raises:
        ArgumentError: l must be list or string

    Yields:
        _type_: chunk item
    """

    if type(l) is not str and not list:
        raise ValueError('l must be list or string')

    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]