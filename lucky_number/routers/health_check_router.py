from fastapi import APIRouter, status

HealthCheckRouter = APIRouter(
    prefix="/health", tags=["health"]
)

@HealthCheckRouter.get("/")
def index():
    return status.HTTP_200_OK
