from fastapi import APIRouter

from koyarwa.features.health.router import router as health_router

api_router = APIRouter()
api_router.include_router(health_router)

# Nouvelle feature = un router dans `features/<nom>/router.py`, inclus ici :
# from koyarwa.features.<nom>.router import router as <nom>_router
# api_router.include_router(<nom>_router)
