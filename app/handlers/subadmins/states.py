from aiogram import Bot, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.database.actions import add_confirm, end_confirm

from app.states.admin import Admin
from app.utils.info import (
    add_news,
    add_quiz,
    edit_about_quiz,
    edit_faq,
    edit_news,
    edit_quiz,
)
from app.utils.mailing import make_mailing
from app.utils.ranks import add_moder, del_moder
from app.keyboards.admin import get_back_kb


router = Router(name="admin_states")


@router.message(Admin.add_moderator)
async def add_moder_state(message: Message, state: FSMContext) -> None:
    """
    Функция, которая обрабатывает сообщение, отправленное администратором,
    для добавления модератора. Она очищает текущее состояние, получает
    информацию о пользователе, пытается добавить модератора, используя
    функцию add_moder(), и отправляет сообщение с результатом.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Очищаем текущее состояние машины состояний.
    2. Получаем аргументы сообщения.
    3. Если аргументы неправильны, отправляем сообщение с инструкциями.
    4. Если аргументы правильны, пытаемся добавить модератора.
    5. Если модератор успешно добавлен, отправляем сообщение об успешном
    добавлении.
    6. Если пользователь уже является модератором, отправляем соответствующее
    сообщение.
    7. Если возникла ошибка, отправляем сообщение об ошибке.
    """
    args = message.text.split(" ")

    if len(args) != 2 or not args[0].isdigit():
        await message.answer(
            "Неверный формат. Введите <id> <username> с пробелом между ними. Пример: 123 @username или 123 username",
            reply_markup=get_back_kb(),
        )
        return

    id, username = args

    username = username.replace("@", "")

    try:
        result = await add_moder(id, username)

        if result:
            await message.answer(
                "Пользователь назначен модератором", reply_markup=get_back_kb()
            )
        else:
            await message.answer(
                "Пользователь уже модератор", reply_markup=get_back_kb()
            )

    except Exception:
        await message.answer(
            "Пользователь не назначен модератором. Произошла ошибка",
            reply_markup=get_back_kb(),
        )

    await state.clear()


@router.message(Admin.make_mailing)
async def make_mailing_state(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Эта функция обрабатывает сообщение, отправленное администратором,
    для запуска рассылки. Она получает текст сообщения, передает его
    на функцию make_mailing() для отправки и оповещает пользователя
    о результате.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :param bot: Объект Bot, представляющий бота, который отправляет сообщение.
    :return: None

    Внутренний процесс:
    1. Получаем текст сообщения.
    2. Пытаемся отправить рассылку, используя функцию make_mailing().
    3. Если рассылка успешно отправлена, отправляем сообщение об успешной
    отправке.
    4. Если рассылка не отправлена, отправляем сообщение о неудаче.
    5. В случае ошибки отправляем сообщение об ошибке.
    6. Очищаем текущее состояние машины состояний.
    """
    text = message.text

    try:
        result = await make_mailing(text, bot)

        if result:
            await message.answer("Рассылка запущена", reply_markup=get_back_kb())
        else:
            await message.answer("Рассылка не запущена", reply_markup=get_back_kb())

    except Exception:
        await message.answer(
            "Рассылка не запущена. Произошла ошибка", reply_markup=get_back_kb()
        )

    await state.clear()


@router.message(Admin.add_news)
async def add_news_state(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает сообщение, отправленное администратором,
    для добавления новостей. Она получает текст сообщения,
    передает его на функцию add_news() для добавления
    и оповещает пользователя о результате.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Получаем текст сообщения.
    2. Пытаемся добавить новость, используя функцию add_news().
    3. Если новость была успешно добавлена, отправляем сообщение об успешном
    добавлении.
    4. Если новость не была добавлена, отправляем сообщение о неудаче.
    5. В случае ошибки отправляем сообщение об ошибке.
    6. Очищаем текущее состояние машины состояний.
    """
    text = message.text

    try:
        result = await add_news(text)

        if result:
            await message.answer("Новости добавлены", reply_markup=get_back_kb())
        else:
            await message.answer("Новости не добавлены", reply_markup=get_back_kb())

    except Exception:
        await message.answer(
            "Новости не добавлены. Произошла ошибка", reply_markup=get_back_kb()
        )

    await state.clear()


@router.message(Admin.add_quiz)
async def add_quiz_state(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает сообщение, отправленное администратором,
    для добавления викторины. Она получает текст сообщения,
    передает его на функцию add_quiz() для добавления
    и оповещает пользователя о результате.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Получаем текст сообщения.
    2. Пытаемся добавить викторину, используя функцию add_quiz().
    3. Если викторина была успешно добавлена, отправляем сообщение об успешном
    добавлении.
    4. Если викторина не была добавлена, отправляем сообщение о неудаче.
    5. В случае ошибки отправляем сообщение об ошибке.
    6. Очищаем текущее состояние машины состояний.
    """
    text = message.text

    try:
        result = await add_quiz(text)

        if result:
            await message.answer("Викторина добавлена", reply_markup=get_back_kb())
        else:
            await message.answer("Викторина не добавлена", reply_markup=get_back_kb())

    except Exception:
        await message.answer(
            "Викторина не добавлена. Произошла ошибка", reply_markup=get_back_kb()
        )

    await state.clear()


@router.message(Admin.add_confirm)
async def add_confirm_state(message: Message, state: FSMContext) -> None:
    """
    Эта функция обрабатывает сообщение, отправленное администратором,
    для добавления рассылки с подтверждением. Она получает текст сообщения,
    передает его на функцию add_confirm() для добавления и оповещает
    пользователя о результате.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Получаем текст сообщения.
    2. Пытаемся добавить рассылку с подтверждением, используя функцию add_confirm().
    3. Если рассылка успешно добавлена, отправляем сообщение об успешном
       добавлении.
    4. Если рассылка не была добавлена, отправляем сообщение о неудаче.
    5. В случае ошибки отправляем сообщение об ошибке.
    6. Очищаем текущее состояние машины состояний.
    """
    text = message.text

    try:
        result = add_confirm(text)

        if result:
            await message.answer(
                "Рассылка с подтверждением выполнена", reply_markup=get_back_kb()
            )
        else:
            await message.answer(
                "Рассылка с подтверждением не выполнена", reply_markup=get_back_kb()
            )

    except Exception:
        await message.answer(
            "Рассылка с подтверждением не выполнена. Произошла ошибка",
            reply_markup=get_back_kb(),
        )

    await state.clear()


@router.message(Admin.edit_about_quiz)
async def edit_about_quiz_state(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает сообщение для редактирования информации о викторине.
    Получает текст сообщения от пользователя и пытается обновить
    информацию в базе данных.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Извлекаем текст из сообщения пользователя.
    2. Вызываем функцию edit_about_quiz() для обновления текста в базе данных.
    3. Проверяем результат выполнения функции:
       - Если обновление успешно, отправляем сообщение об успешном изменении.
       - Если обновление не удалось, отправляем сообщение о неудаче.
    4. Обрабатываем исключения и отправляем сообщение об ошибке в случае сбоя.
    5. Очищаем текущее состояние машины состояний.
    """
    text = message.text

    try:
        result = await edit_about_quiz(text)

        if result:
            await message.answer("О викторине изменено", reply_markup=get_back_kb())
        else:
            await message.answer("О викторине не изменено", reply_markup=get_back_kb())

    except Exception:
        await message.answer(
            "О викторине не изменено. Произошла ошибка", reply_markup=get_back_kb()
        )

    await state.clear()


@router.message(Admin.edit_faq)
async def edit_faq_state(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает сообщение для редактирования информации о часто задаваемых вопросах (FAQ).
    Получает текст сообщения от пользователя и пытается обновить информацию в базе данных.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Извлекаем текст из сообщения пользователя.
    2. Вызываем функцию edit_faq() для обновления текста в базе данных.
    3. Проверяем результат выполнения функции:
       - Если обновление успешно, отправляем сообщение об успешном изменении.
       - Если обновление не удалось, отправляем сообщение о неудаче.
    4. Обрабатываем исключения и отправляем сообщение об ошибке в случае сбоя.
    5. Очищаем текущее состояние машины состояний.
    """
    text = message.text

    try:
        result = await edit_faq(text)

        if result:
            await message.answer("Частые вопросы изменены", reply_markup=get_back_kb())
        else:
            await message.answer(
                "Частые вопросы не изменены", reply_markup=get_back_kb()
            )

    except Exception:
        await message.answer(
            "Частые вопросы не изменены. Произошла ошибка", reply_markup=get_back_kb()
        )

    await state.clear()


@router.message(Admin.edit_news)
async def edit_news_state(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает сообщение для редактирования новости.
    Функция извлекает текст новости из сообщения пользователя и обновляет
    соответствующую запись в базе данных.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Извлекаем текст новости из сообщения пользователя.
    2. Получаем данные состояния, чтобы извлечь ID новости для редактирования.
    3. Пытаемся обновить новость в базе данных, вызывая функцию edit_news().
    4. Проверяем результат выполнения функции:
       - Если обновление успешно, отправляем сообщение об успешном изменении.
       - Если обновление не удалось, отправляем сообщение о неудаче.
    5. Обрабатываем исключения и отправляем сообщение об ошибке в случае сбоя.
    6. Очищаем текущее состояние машины состояний.
    """
    text = message.text

    data = await state.get_data()

    id = data.get("id", None)

    try:
        result = await edit_news(id, text)

        if result:
            await message.answer("Новости изменены", reply_markup=get_back_kb())
        else:
            await message.answer("Новости не изменены", reply_markup=get_back_kb())

    except Exception:
        await message.answer(
            "Новости не изменены. Произошла ошибка", reply_markup=get_back_kb()
        )

    await state.clear()


@router.message(Admin.edit_quiz)
async def edit_quiz_state(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает текст, отправленный администратором, и обновляет
    текст викторины с соответствующим ID.

    :param message: Объект Message, представляющий отправленное сообщение.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Извлекаем текст викторины из сообщения администратора.
    2. Получаем данные состояния, чтобы извлечь ID викторины для редактирования.
    3. Пытаемся обновить викторину в базе данных, вызывая функцию edit_quiz().
    4. Проверяем результат выполнения функции:
       - Если обновление успешно, отправляем сообщение об успешном изменении.
       - Если обновление не удалось, отправляем сообщение о неудаче.
    5. Обрабатываем исключения и отправляем сообщение об ошибке в случае сбоя.
    6. Очищаем текущее состояние машины состояний.
    """
    text = message.text

    data = await state.get_data()

    id = data.get("id", None)

    try:
        result = await edit_quiz(id, text)

        if result:
            await message.answer("Викторина изменена", reply_markup=get_back_kb())
        else:
            await message.answer("Викторина не изменена", reply_markup=get_back_kb())

    except Exception:
        await message.answer(
            "Викторина не изменена. Произошла ошибка", reply_markup=get_back_kb()
        )

    await state.clear()
