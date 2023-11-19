from fastapi import APIRouter, Depends
from lucky_number.services.lucky_number import LuckyNumberService
from lucky_number.dto.lucky_number import BulkRandomRangeResult, BulkRandomRangeRequest
from lucky_number.core.security import api_key_auth
from lucky_number.utils.abi import abi_encode

RandomRouter = APIRouter(
    prefix="/v1/random", tags=["random"]
)


@RandomRouter.get("/bulk", response_model=BulkRandomRangeResult)
def bulk_random(
    bulk: int,
    min: int,
    max: int,
    lucky_number_service: LuckyNumberService = Depends(),
    api_key: str = Depends(api_key_auth)
):
    result = lucky_number_service.GetLuckyNumbers(
        BulkRandomRangeRequest(bulk=bulk, min=min, max=max))
    return result


@RandomRouter.get("/bulk-bytes")
def bulk_random_bytes(
    bulk: int,
    min: int,
    max: int,
    lucky_number_service: LuckyNumberService = Depends(),
    api_key: str = Depends(api_key_auth)
):
    result = lucky_number_service.GetLuckyNumbers(
        BulkRandomRangeRequest(bulk=bulk, min=min, max=max))
    bytes = abi_encode(['bool', 'string', 'uint32[]'], [
        result.success, result.generator, result.numbers])
    return {'data_bytes': bytes}
