from fastapi import APIRouter
from src.api.contacts import router as contacts_router

router = APIRouter(prefix='/v1')

router.include_router(contacts_router)
