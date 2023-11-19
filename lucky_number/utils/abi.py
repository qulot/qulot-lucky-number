from eth_abi import encode
import typing


def abi_encode(types: typing.List[str], args: typing.List[typing.Any]) -> str:
    """Return hex string of args data

    Args:
        types (typing.List[str]): Solidity data types
        args (typing.List[typing.Any]): List data want abi encode

    Returns:
        str: Hex string start with 0x
    """
    bytes = encode(types, args)
    return f'0x{bytes.hex()}'
