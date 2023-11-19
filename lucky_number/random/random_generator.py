import abc
import typing


class RandomGenerator(metaclass=abc.ABCMeta):

    def __init__(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def random_range(self, min: int, max: int) -> int:
        pass

    @abc.abstractmethod
    def bulk_random_range(
        self,
        bulk: int,
        min: int,
        max: int
    ) -> typing.List[int]:
        """Returns the set of random numbers

        Args:
            bulk (int): Number of sets
            min (int): Maximum value of each item
            max (int): Minimum value of each item

        Returns:
            typing.List[int]: List of random numbers
        """
        pass
