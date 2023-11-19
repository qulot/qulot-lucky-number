from lucky_number.random.quantum_random_generator import QuantumRandomGenerator
from lucky_number.random.local_random_generator import LocalRandomGenerator
from lucky_number.random.random_generator import RandomGenerator
import typing
import logging

logger = logging.getLogger(__name__)


def get_generators() -> typing.List[RandomGenerator]:
    generators = [QuantumRandomGenerator(), LocalRandomGenerator()]
    return generators


def bulk_random_range(
    generators: typing.List[RandomGenerator],
    number_of_items: int,
    max_value_per_item: int,
    min_value_per_item: int
) -> typing.Tuple[bool, str, typing.List[int], Exception]:
    
    error: Exception = None
    for generator in generators:
        try:
            numbers = generator.bulk_random_range(
                number_of_items, max_value_per_item, min_value_per_item)
            return (True, generator.__str__(), numbers, None)
        except Exception as e:
            error = e
            logger.error(
                f"[random][bulk_random_range] generator: {generator.__str__()} error: {e}")
            continue

    return (False, None, [], error)
