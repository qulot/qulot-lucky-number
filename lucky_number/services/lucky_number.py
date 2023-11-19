from lucky_number.core.service import Service
from lucky_number.dto.lucky_number import BulkRandomRangeRequest, BulkRandomRangeResult
from lucky_number.random import get_generators, bulk_random_range


class LuckyNumberService(Service):

    def __init__(self) -> None:
        super().__init__()
        self.generators = get_generators()

    def GetLuckyNumbers(self, request: BulkRandomRangeRequest):
        (success, generator, numbers, _) = bulk_random_range(
            self.generators, request.bulk, request.min, request.max)

        return BulkRandomRangeResult(generator=generator, numbers=numbers, success=success)
