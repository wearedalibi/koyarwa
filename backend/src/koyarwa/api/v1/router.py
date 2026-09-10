from fastapi import APIRouter, Depends

from koyarwa.api.auth import require_api_token
from koyarwa.features.announcements.router import router as announcements_router
from koyarwa.features.health.router import router as health_router

api_router = APIRouter()

# `health` reste public (sondes de disponibilité). Les routes de données sont
# protégées par le jeton de service (require_api_token).
api_router.include_router(health_router)
api_router.include_router(announcements_router, dependencies=[Depends(require_api_token)])

# Nouvelle feature = un router dans `features/<nom>/router.py`, inclus ici AVEC
# la garde de jeton :
# from koyarwa.features.<nom>.router import router as <nom>_router
# api_router.include_router(<nom>_router, dependencies=[Depends(require_api_token)])
