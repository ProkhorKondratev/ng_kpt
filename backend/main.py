from fastapi import FastAPI, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.middleware.cors import CORSMiddleware
from fastapi_profiler import PyInstrumentProfilerMiddleware
from contextlib import asynccontextmanager
from routing import processing_router, data_router
from db import create_tables, drop_tables
from services import Handler
import asyncio
import aiofiles.os as aos


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    await check_folders()
    await create_tables()
    await Handler.restart_working_tasks()
    yield
    # await drop_tables()


app = FastAPI(lifespan=app_lifespan, title="NGW-KPT", version="0.1.0", docs_url=None, redoc_url=None)

app.include_router(processing_router, prefix="/processing", tags=["processing"])
app.include_router(data_router, prefix="/data", tags=["data"])

origins = [
    "http://127.0.0.1:8785",
    "http://localhost:8785",
    "http://kadastr.lan",
    "http://kpt.nextgis.lan",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.add_middleware(
#     PyInstrumentProfilerMiddleware,
#     server_app=app,
#     profiler_output_type="html",
#     is_print_each_request=True,
#     open_in_browser=False,
#     html_file_name="./fastapi-profiler.html",
# )


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui.css",
    )


async def check_folders():
    print("Проверка папок")

    folders = [
        'data',
        'data/uploaded',
        'data/results',
        'data/database',
        'data/logs',
        'data/tmp',
    ]

    await asyncio.gather(*[aos.makedirs(folder, exist_ok=True) for folder in folders])
