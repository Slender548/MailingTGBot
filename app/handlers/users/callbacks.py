from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from app.keyboards.user import get_user_kb, get_back_kb
from app.utils.info import get_about_quiz, get_faq, get_news_user, get_quizzes_user
from app.states.user import User


router = Router(name="user_callbacks")


@router.callback_query(F.data == "start")
async def start_callback(callback: CallbackQuery) -> None:
    """
    Обрабатывает callback-запрос на старт.
    Эта функция изменяет текст сообщения на инструкцию
    и отправляет сообщение с клавиатурой для выбора действия.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :return: None

    Внутренний процесс:
    1. Изменяем текст сообщения на инструкцию.
    2. Отправляем сообщение с клавиатурой.
    """
    await callback.message.edit_text(
        "Здравствуйте!\nВыберите действие", reply_markup=get_user_kb()
    )


@router.callback_query(F.data == "about_quiz")
async def about_quiz_callback(callback: CallbackQuery) -> None:
    """
    Обрабатывает callback-запрос для просмотра информации о викторине.
    Она очищает текущее состояние, получает информацию о викторине из базы данных
    и отправляет сообщение с ее данными.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :return: None

    Внутренний процесс:
    1. Получаем информацию о викторине из базы данных с помощью функции get_about_quiz().
    2. Если информация не найдена, отправляем сообщение о том, что информация не найдена.
    3. Если информация найдена, формируем текст сообщения с ее данными.
    4. Отправляем сообщение с данными викторины и клавиатурой с возможными действиями.
    """
    about_quiz = await get_about_quiz()

    if not about_quiz:
        await callback.message.edit_text(
            "Информация о викторине не найдена", reply_markup=get_back_kb()
        )
        return

    await callback.message.edit_text(
        f"О викторине:\n\n{about_quiz}", reply_markup=get_back_kb()
    )


@router.callback_query(F.data == "faq")
async def faq_callback(callback: CallbackQuery) -> None:
    """
    Обрабатывает callback-запрос для просмотра информации о частых вопросах.
    Она очищает текущее состояние, получает информацию о частых вопросах из базы данных
    и отправляет сообщение с ее данными.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :return: None

    Внутренний процесс:
    1. Получаем информацию о частых вопросах из базы данных с помощью функции get_faq().
    2. Если информация не найдена, отправляем сообщение о том, что информация не найдена.
    3. Если информация найдена, формируем текст сообщения с ее данными.
    4. Отправляем сообщение с данными частых вопросов и клавиатурой с возможными действиями.
    """
    faq = await get_faq()

    if not faq:
        await callback.message.edit_text(
            "Информация о частых вопросах не найдена", reply_markup=get_back_kb()
        )
        return

    await callback.message.edit_text(
        f"Частые вопросы:\n\n{faq}", reply_markup=get_back_kb()
    )


@router.callback_query(F.data == "quizzes")
async def quizzes_callback(callback: CallbackQuery) -> None:
    """
    Обрабатывает callback-запрос для просмотра предстоящих викторин.
    Она очищает текущее состояние, получает список предстоящих викторин из базы данных
    и отправляет сообщение с ее данными.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :return: None

    Внутренний процесс:
    1. Получаем список предстоящих викторин из базы данных с помощью функции get_quizzes_user().
    2. Если список викторин пуст, отправляем сообщение о том, что викторин нет.
    3. Если викторины найдены, формируем текст сообщения с их ID и текстом.
    4. Отправляем сообщение с данными викторин.
    """
    quizzes = await get_quizzes_user()

    if not quizzes:
        await callback.message.edit_text(
            "Нет предстоящих викторин", reply_markup=get_back_kb()
        )
        return

    text = "Предстоящие викторины:\n\n"
    text += "\n".join(quizzes)

    await callback.message.edit_text(text, reply_markup=get_back_kb())


@router.callback_query(F.data == "news")
async def news_callback(callback: CallbackQuery) -> None:
    """
    Обрабатывает callback-запрос для просмотра новостей.
    Она очищает текущее состояние, получает список новостей из базы данных
    и отправляет сообщение с ее данными.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :return: None

    Внутренний процесс:
    1. Получаем список новостей из базы данных с помощью функции get_news_user().
    2. Если список новостей пуст, отправляем сообщение о том, что новостей нет.
    3. Если новости найдены, формируем текст сообщения с ними.
    4. Отправляем сообщение с данными новостей.
    """
    news = await get_news_user()

    if not news:
        await callback.message.edit_text("Нет новостей", reply_markup=get_back_kb())
        return

    text = "Новости:\n\n"
    text += "\n".join(news)

    await callback.message.edit_text(text, reply_markup=get_back_kb())


@router.callback_query(F.data == "change_email")
async def change_email_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает callback-запрос для смены почты.
    Она очищает текущее состояние, изменяет состояние машины состояний на
    User.change_email и отправляет сообщение с инструкцией для смены почты.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Очищаем текущее состояние.
    2. Изменяем состояние машины состояний на User.change_email.
    3. Отправляем сообщение с инструкцией для смены почты.
    """
    await state.clear()
    await callback.message.edit_text(
        "Напишите вашу новую почту", reply_markup=get_back_kb()
    )

    await state.set_state(User.change_email)


@router.callback_query(F.data == "get_id")
async def get_id_callback(callback: CallbackQuery) -> None:
    """
    Обрабатывает callback-запрос для получения ID.
    Она отправляет сообщение с ID пользователя.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :return: None

    Внутренний процесс:
    1. Получаем ID пользователя.
    2. Формируем текст сообщения с ID.
    3. Отправляем сообщение с ID.
    """
    await callback.message.edit_text(
        f"Ваш ID: {callback.from_user.id}", reply_markup=get_back_kb()
    )


@router.callback_query(F.data == "ask_question")
async def ask_question_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает callback-запрос для отправки вопроса.
    Она очищает текущее состояние, изменяет состояние машины состояний на
    User.ask_question и отправляет сообщение с инструкцией для отправки вопроса.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Очищаем текущее состояние.
    2. Изменяем состояние машины состояний на User.ask_question.
    3. Отправляем сообщение с инструкцией для отправки вопроса.
    """
    await state.clear()
    await callback.message.edit_text("Напишите ваш вопрос", reply_markup=get_back_kb())

    await state.set_state(User.ask_question)
