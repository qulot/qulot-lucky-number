import logging
import random
import typing
from lucky_number.random.random_generator import RandomGenerator

logger = logging.getLogger(__name__)


def is_valid(min: int, max: int, number: int):
    return min <= number <= max


class LocalRandomGenerator(RandomGenerator):

    def random_range(self, min: int, max: int):
        logger.info(f"[random_range] input min: {min}, max: {max}")
        random_number = random.randint(min, max)
        logger.info(f"[random_range] output: {random_number}")
        return random_number

    def bulk_random_range(
        self,
        bulk: int,
        min: int,
        max: int
    ) -> typing.List[int]:
        logger.info(
            f"[bulk_random_range] input bulk: {bulk}, min: {min}, max: {max}")
        numbers = []
        while len(numbers) < bulk:
            number = random.randint(min, max)
            logger.info(f"[bulk_random_range] random range, min: {min}, max: {max}, result: {number}")
            if number in numbers:
                logger.warn(f"[bulk_random_range] exists the number in the result, continute")
                continue
            numbers.append(number)
        numbers = sorted(numbers)
        logger.info(
            f"[bulk_random_range] output number_of_items: {numbers}")
        return numbers

    def __str__(self):
        return type(self).__name__
