from aiogram import Router

from app.filters.subadmin import IsSubAdminMessage, IsSubAdminCallback

from .callbacks import router as callbacks_router
from .commands import router as commands_router
from .states import router as states_router


def get_subadmin_router() -> Router:
    """
    Функция, которая возвращает роутер субадминистратора.
    """
    router = Router(name="admin")

    # Добавляем роутеры для обработки сообщений, callback-запросов и состояний
    router.include_router(states_router)
    router.include_router(callbacks_router)
    router.include_router(commands_router)

    # Добавляем фильтры для роутера
    router.message.filter(IsSubAdminMessage())
    router.callback_query.filter(IsSubAdminCallback())

    return router
