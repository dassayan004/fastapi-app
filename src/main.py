from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, status
from pydantic import BaseModel
from core.config import appSetting
from auth.routes import router as auth_router
from database.dbSession import lifespan


app = FastAPI(title=appSetting.app_name, lifespan=lifespan)

# ✅ Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=appSetting.BACKEND_CORS_ORIGINS,  # ✅ Read from env
    allow_credentials=True,
    allow_methods=["*"],  # ✅ Allow all methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # ✅ Allow all headers
)


class HealthCheck(BaseModel):
    """Response model to validate and return when performing a health check."""

    status: str = "OK"


# ✅ Health Check Route


@app.get(
    "/health",
    tags=["Health"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
def get_health() -> HealthCheck:
    """
    ## Perform a Health Check
    Endpoint to perform a healthcheck on. This endpoint can primarily be used Docker
    to ensure a robust container orchestration and management is in place. Other
    services which rely on proper functioning of the API service will not deploy if this
    endpoint returns any other HTTP status code except 200 (OK).
    Returns:
        HealthCheck: Returns a JSON response with the health status
    """
    return HealthCheck(status="OK")


app.include_router(auth_router)
