from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from alloba import __version__
from alloba.config import settings
from alloba.proxy import proxy_to_backend
from alloba.routers.gateway import router as gateway_router
from alloba.routers.sourcing import router as sourcing_router

app = FastAPI(
    title="Alloba API Gateway",
    description=(
        "Single standalone entry point for the ispaces Commerce platform: "
        "aggregates the platform API, the ethical AI compliance knowledge "
        "engine (safe FAISS RAG), and the agentic sourcing service."
    ),
    version=__version__,
    docs_url="/v1/docs",
    redoc_url="/v1/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root info route (registered before the catch-all so it is not shadowed).
@app.get("/", include_in_schema=False)
async def root() -> dict:
    return {"service": "alloba", "version": __version__, "docs": "/v1/docs"}


# Gateway-owned endpoints (registered first so they win over the catch-all).
app.include_router(gateway_router)
app.include_router(sourcing_router)


@app.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    include_in_schema=False,
)
async def catch_all_proxy(request: Request, path: str):
    """Everything else is transparently forwarded to the platform backend."""
    if path in {"", "favicon.ico"}:
        return JSONResponse(status_code=404, content={"detail": "Not found"})
    return await proxy_to_backend(request, path)



