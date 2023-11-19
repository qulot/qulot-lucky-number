from fastapi import FastAPI

from lucky_number.core import settings, logging
from lucky_number.routers.v1.random_router import RandomRouter
from lucky_number.routers.health_check_router import HealthCheckRouter
from lucky_number.routers.log_viewer_router import LogViewerRouter

# load settings
settings.load_settings()

# setup logging
logging.setup_logging()


# Core Application Instance
app = FastAPI(
    title="Qulot lucky number by quantum random number generator",
    version="1.0.0",
)

# Add Routers
app.include_router(RandomRouter)
app.include_router(HealthCheckRouter)
app.include_router(LogViewerRouter)