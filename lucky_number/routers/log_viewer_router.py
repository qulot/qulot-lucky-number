import asyncio
from typing import List
from fastapi import APIRouter, Request, WebSocket, Response, Query
from fastapi.templating import Jinja2Templates
from lucky_number.core import settings

LogViewerRouter = APIRouter(
    prefix="/log", tags=["log"]
)


async def log_reader(n=5) -> List[str]:
    log_lines = []
    with open(settings.get("LOGGING_FILE_NAME"), "r") as file:
        for line in file.readlines()[-n:]:
            log_lines.append(line)
        return log_lines


@LogViewerRouter.websocket("/stream-ws")
async def websocket_endpoint_log(websocket: WebSocket, tail: int = Query(10, lte=1, gte=100)):
    await websocket.accept()

    try:
        while True:
            await asyncio.sleep(1)
            log_lines = await log_reader(tail)
            await websocket.send_json(log_lines)
    except Exception as e:
        print(e)
    finally:
        await websocket.close()


@LogViewerRouter.get("/viewer")
async def get(request: Request) -> Response:
    """Log file viewer

    Args:
        request (Request): Default web request.

    Returns:
        TemplateResponse: Jinja template with context data.
    """
    context = {
        "title": "Qulot Lucky Number Api Stream Log Viewer",
        "log_file": settings.get("LOGGING_FILE_NAME")
    }
    templates = Jinja2Templates(directory=settings.get("TEMPLATE_DIR", "templates"))
    return templates.TemplateResponse("index.html", {"request": request, "context": context})
