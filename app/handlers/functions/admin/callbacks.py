from typing import List, Tuple
from aiogram import Bot, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


from app.utils.info import (
    get_about_quiz,
    get_faq,
    get_news_admin,
    get_news_one,
    get_news_user,
    get_quizzes_admin,
    del_quiz,
    get_quiz,
    del_news,
    get_quizzes_user,
    get_rules,
)
from app.utils.ranks import (
    del_moder,
    del_subadmin,
    get_full_moders,
    get_full_subadmins,
    get_moder_username,
    get_subadmin_username,
    reset_chat,
    get_chat_link,
)
from app.database.actions import get_all_confirms, get_confirm, end_confirm

from app.states.admin import Admin

from app.keyboards.admin import (
    get_add_confirm_kb,
    get_add_moder_kb,
    get_add_news_kb,
    get_add_quiz_kb,
    get_admin_kb,
    get_back_kb,
    get_chat_kb,
    get_confirm_kb,
    get_del_chat_kb,
    get_del_moder_kb,
    get_del_news_kb,
    get_del_quiz_kb,
    get_edit_news_kb,
    get_edit_quiz_kb,
    get_end_confirm_kb,
    get_mailing_kb,
    get_moders_kb,
    get_moder_kb,
    get_confirms_kb,
    get_news_kb,
    get_news_one_kb,
    get_quiz_kb,
    get_quizzes_kb,
    get_add_subadmin_kb,
    get_del_subadmin_kb,
    get_subadmin_kb,
    get_subadmins_kb,
    get_user_kb,
    get_back_user_kb,  # TODO
)

router = Router(name="admin_callbacks")


async def user_mode_callback(callback: CallbackQuery) -> None:
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
        f"Добро пожаловать, @{callback.from_user.username}!", reply_markup=get_user_kb()
    )


async def about_quiz_user_callback(callback: CallbackQuery) -> None:
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
            "Информация о викторине не найдена", reply_markup=get_back_user_kb()
        )
        return

    await callback.message.edit_text(about_quiz, reply_markup=get_back_user_kb())


async def faq_user_callback(callback: CallbackQuery) -> None:
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
            "Информация о частых вопросах не найдена", reply_markup=get_back_user_kb()
        )
        return

    await callback.message.edit_text(faq, reply_markup=get_back_user_kb())


async def quizzes_user_callback(callback: CallbackQuery) -> None:
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
            "Нет предстоящих викторин", reply_markup=get_back_user_kb()
        )
        return

    text = "\n".join(quizzes)

    await callback.message.edit_text(text, reply_markup=get_back_user_kb())


async def news_user_callback(callback: CallbackQuery) -> None:
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
        await callback.message.edit_text(
            "Нет новостей", reply_markup=get_back_user_kb()
        )
        return

    text = "\n".join(news)

    await callback.message.edit_text(text, reply_markup=get_back_user_kb())


async def rules_user_callback(callback: CallbackQuery) -> None:
    """
    Обрабатывает callback-запрос для просмотра правил.
    Она очищает текущее состояние, получает текст правил из базы данных
    и отправляет сообщение с его данными.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :return: None

    Внутренний процесс:
    1. Получаем текст правил из базы данных с помощью функции get_rules().
    2. Если текст правил не найден, отправляем сообщение о том, что правил не найдены.
    3. Если правила найдены, отправляем сообщение с данными правил.
    """
    rules = await get_rules()

    if not rules:
        await callback.message.edit_text(
            "Правила не выставлены", reply_markup=get_back_user_kb()
        )
        return

    await callback.message.edit_text(rules, reply_markup=get_back_user_kb())


async def ask_question_user_callback(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    Обрабатывает callback-запрос для отправки вопроса.
    Она очищает текущее состояние, изменяет состояние машины состояний на
    Admin.ask_question и отправляет сообщение с инструкцией для отправки вопроса.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Очищаем текущее состояние.
    2. Изменяем состояние машины состояний на Admin.ask_question.
    3. Отправляем сообщение с инструкцией для отправки вопроса.
    """
    await state.clear()
    await callback.message.edit_text(
        "Напишите ваш вопрос", reply_markup=get_back_user_kb()
    )

    await state.set_state(Admin.ask_question)


async def show_moders_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Эта функция обрабатывает callback-запрос для показа списка модераторов.
    Она очищает текущее состояние, получает список модераторов из базы данных
    и отправляет сообщение с их данными.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Очищаем текущее состояние машины состояний.
    2. Получаем список модераторов с помощью функции get_full_moders().
    3. Если список модераторов пуст, отправляем сообщение о том, что модераторов нет.
    4. Если модераторы найдены, формируем текст сообщения с их ID и именами.
    5. Отправляем сообщение с данными модераторов и клавиатурой с возможными действиями.
    """
    await state.clear()
    moders = await get_full_moders()

    if not moders:
        await callback.message.edit_text(
            "Нет модераторов", reply_markup=get_moders_kb()
        )
        return

    text = "Модераторы:\n\n"
    text += "\n".join([f"@{moder[1]}" for moder in moders])
    await callback.message.edit_text(
        text, reply_markup=get_moders_kb([moder[0] for moder in moders])
    )


async def show_moder_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Эта функция обрабатывает callback-запрос для показа информации о модераторе.
    Она очищает текущее состояние, получает информацию о модераторе из базы данных
    и отправляет сообщение с его данными.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Очищаем текущее состояние машины состояний.
    2. Получаем информацию о модераторе с помощью функции get_moder().
    3. Если модератор не найден, отправляем сообщение о том, что модератор не найден.
    4. Если модератор найден, формируем текст сообщения с его ID, именем
    5. Отправляем сообщение с данными модератора и клавиатурой с возможными действиями.
    """
    await state.clear()
    _, id = callback.data.split("_")

    username = await get_moder_username(id)
    if not username:
        await callback.message.edit_text(
            "Модератор не найден", reply_markup=get_moder_kb(id)
        )
        return

    await callback.message.answer(
        f"Модератор:\n\nID: {id}\n@{username}\n\nВыберите действие:",
        reply_markup=get_moder_kb(id),
    )


async def del_moder_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Эта функция обрабатывает callback-запрос для удаления модератора.
    Она очищает текущее состояние, пытается удалить модератора по ID и
    отправляет соответствующее сообщение в зависимости от результата.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Очищаем текущее состояние машины состояний.
    2. Извлекаем ID модератора из данных callback-запроса.
    3. Пытаемся удалить модератора, используя функцию del_moder().
    4. Если модератор успешно удален, отправляем сообщение об успешном удалении.
    5. Если пользователь не является модератором, отправляем соответствующее сообщение.
    6. В случае возникновения исключения, отправляем сообщение об ошибке.
    """
    await state.clear()
    _, _, id = callback.data.split("_")

    try:
        if await del_moder(id):
            await callback.message.edit_text(
                "Модератор удален", reply_markup=get_del_moder_kb()
            )
        else:
            await callback.message.edit_text(
                "Пользователь не модератор", reply_markup=get_del_moder_kb()
            )

    except Exception:
        await callback.message.edit_text(
            "Произошла ошибка", reply_markup=get_del_moder_kb()
        )


async def add_moderator_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Эта функция обрабатывает callback-запрос для добавления модератора.
    Она очищает текущее состояние, изменяет состояние машины состояний на
    Admin.add_moderator и отправляет сообщение с инструкциями для добавления
    модератора.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Очищаем текущее состояние машины состояний.
    2. Изменяем состояние машины состояний на Admin.add_moderator.
    3. Отправляем сообщение с инструкциями для добавления модератора.
    """
    await state.set_state(Admin.add_moderator)
    await callback.message.edit_text(
        "Отправьте никнейм пользователя, которого хотите добавить в модераторы\n\nПример: @username или username",
        reply_markup=get_add_moder_kb(),
    )


async def show_subadmins_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Эта функция обрабатывает callback-запрос для показа списка субадминистраторов.
    Она очищает текущее состояние, получает список субадминистраторов из базы данных
    и отправляет сообщение с их данными.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Очищаем текущее состояние машины состояний.
    2. Получаем список субадминистраторов с помощью функции get_subadmins().
    3. Если список субадминистраторов пуст, отправляем сообщение о том, что субадминистраторов нет.
    4. Если модераторы найдены, формируем текст сообщения с их ID и именами.
    5. Отправляем сообщение с данными субадминистраторов и клавиатурой с возможными действиями.
    """
    await state.clear()
    subadmins = await get_full_subadmins()

    if not subadmins:
        await callback.message.edit_text(
            "Нет субадминистраторов", reply_markup=get_subadmins_kb()
        )
        return

    text = "Субадминистраторы:\n\n"
    text += "\n".join([f"@{moder[1]}" for moder in subadmins])
    await callback.message.edit_text(
        text, reply_markup=get_subadmins_kb([moder[0] for moder in subadmins])
    )


async def show_subadmin_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Эта функция обрабатывает callback-запрос для показа информации о субадминистраторе.
    Она очищает текущее состояние, получает информацию о субадминистраторе из базы данных
    и отправляет сообщение с его данными.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Очищаем текущее состояние машины состояний.
    2. Получаем информацию о субадминистраторе с помощью функции get_subadmin().
    3. Если модератор не найден, отправляем сообщение о том, что модератор не найден.
    4. Если модератор найден, формируем текст сообщения с его ID, именем
    5. Отправляем сообщение с данными модератора и клавиатурой с возможными действиями.
    """
    await state.clear()
    _, id = callback.data.split("_")

    username = await get_subadmin_username(id)
    if not username:
        await callback.message.edit_text(
            "Субадминистратор не найден", reply_markup=get_subadmin_kb(id)
        )
        return

    await callback.message.answer(
        f"Субадминистратор:\n\nID: {id}\n@{username}\n\nВыберите действие:",
        reply_markup=get_subadmin_kb(id),
    )


async def del_subadmin_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Эта функция обрабатывает callback-запрос для удаления субадминистратора.
    Она очищает текущее состояние, пытается удалить субадминистратора по ID и
    отправляет соответствующее сообщение в зависимости от результата.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Очищаем текущее состояние машины состояний.
    2. Извлекаем ID субадминистратора из данных callback-запроса.
    3. Пытаемся удалить субадминистратора, используя функцию del_subadmin().
    4. Если модератор успешно удален, отправляем сообщение об успешном удалении.
    5. Если пользователь не является модератором, отправляем соответствующее сообщение.
    6. В случае возникновения исключения, отправляем сообщение об ошибке.
    """
    await state.clear()
    _, _, id = callback.data.split("_")

    try:
        if await del_subadmin(id):
            await callback.message.edit_text(
                "Субадминистратор удален", reply_markup=get_del_subadmin_kb()
            )
        else:
            await callback.message.edit_text(
                "Пользователь не субадминистратор", reply_markup=get_del_subadmin_kb()
            )

    except Exception:
        await callback.message.edit_text(
            "Произошла ошибка", reply_markup=get_del_subadmin_kb()
        )


async def add_subadmin_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Эта функция обрабатывает callback-запрос для добавления модератора.
    Она очищает текущее состояние, изменяет состояние машины состояний на
    Admin.add_subadmin и отправляет сообщение с инструкциями для добавления
    модератора.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Очищаем текущее состояние машины состояний.
    2. Изменяем состояние машины состояний на Admin.add_subadmin.
    3. Отправляем сообщение с инструкциями для добавления модератора.
    """
    await state.set_state(Admin.add_subadmin)
    await callback.message.edit_text(
        "Отправьте никнейм пользователя, которого хотите добавить в субадминистраторы\n\nПример: @username или username",
        reply_markup=get_add_subadmin_kb(),
    )


async def make_mailing_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Эта функция обрабатывает callback-запрос для отправки рассылки.
    Она очищает текущее состояние, изменяет состояние машины состояний на
    Admin.make_mailing и отправляет сообщение с инструкциями для отправки
    рассылки.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Очищаем текущее состояние машины состояний.
    2. Изменяем состояние машины состояний на Admin.make_mailing.
    3. Отправляем сообщение с инструкциями для отправки рассылки.
    """
    await state.set_state(Admin.make_mailing)
    await callback.message.edit_text(
        "Отправьте текст для рассылки",
        reply_markup=get_mailing_kb(),
    )


async def ask_del_chat_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Эта функция обрабатывает callback-запрос для сброса чата вопросов.
    Она очищает текущее состояние машины состояний и
    отправляет сообщение с вопросом о подтверждении сброса чата.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Очищаем текущее состояние машины состояний.
    2. Отправляем сообщение с вопросом о подтверждении сброса чата.
    """
    await state.clear()
    await callback.message.answer(
        "Вы уверены, что хотите сбросить чат вопросов?",
        reply_markup=get_del_chat_kb(True),
    )


async def del_chat_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Эта функция обрабатывает callback-запрос для сброса чата вопросов.
    Она очищает текущее состояние машины состояний и
    отправляет сообщение, подтверждающее сброс чата.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Очищаем текущее состояние машины состояний.
    2. Отправляем сообщение, подтверждающее сброс чата.
    """
    await state.clear()
    result = await reset_chat()

    if result:
        await callback.message.answer(
            "Чат сброшен.", reply_markup=get_del_chat_kb(False)
        )
    else:
        await callback.message.answer(
            "Чат не сброшен. Произошла ошибка", reply_markup=get_del_chat_kb(False)
        )


async def show_confirms_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает callback-запрос для просмотра рассылок с подтверждением.
    Она очищает текущее состояние машины состояний, получает из базы данных
    все рассылки с подтверждением и отправляет сообщение с текстом,
    содержащим информацию о рассылках.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Очищаем текущее состояние машины состояний.
    2. Получаем из базы данных все рассылки с подтверждением.
    3. Если рассылки с подтверждением не найдены, отправляем сообщение,
       информирующее о том, что рассылки не найдены.
    4. Если рассылки с подтверждением найдены, отправляем сообщение,
       содержащее информацию о рассылках.
    """
    await state.clear()
    confirms = get_all_confirms()

    if not confirms:
        await callback.message.edit_text(
            text="Нет рассылок с подтверждением", reply_markup=get_confirms_kb()
        )
        return

    text = "Рассылки с подтверждением:\n\n"
    text += "\n".join(f"ID: {id} - {text}" for id, text in confirms)

    await callback.message.edit_text(
        text, reply_markup=get_confirms_kb([id for id, _ in confirms])
    )


async def del_confirm_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает callback-запрос для отображения информации о рассылке с подтверждением.
    Она очищает текущее состояние, получает данные о рассылке из базы данных
    и отправляет сообщение с информацией о рассылке и пользователях.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Очищаем текущее состояние машины состояний.
    2. Извлекаем идентификатор рассылки из данных callback.
    3. Получаем данные о рассылке с подтверждением из базы данных.
    4. Если данные о рассылке не найдены, отправляем сообщение о том, что рассылка не найдена.
    5. Если данные о рассылке найдены, форматируем сообщение с текстом рассылки и списком пользователей.
    6. Отправляем сообщение с информацией о рассылке и клавиатурой с возможными действиями.
    """
    await state.clear()
    _, _, id = callback.data.split("_")

    data: Tuple[str, List[Tuple[str | int, str]]] = get_confirm(id)

    if not data:
        await callback.message.edit_text(
            "Рассылка с подтверждением не найдена", reply_markup=get_confirm_kb()
        )
        return

    text, users = data

    await callback.message.edit_text(
        f"Рассылка с подтверждением:\n\n{text}\n\nПользователи:\n\n{users}\n.Выберите действие:",
        reply_markup=get_confirm_kb(id),
    )


async def add_confirm_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Эта функция обрабатывает callback-запрос для добавления рассылки с подтверждением.
    Она изменяет состояние машины состояний на Admin.add_confirm и отправляет сообщение
    с инструкциями для добавления рассылки с подтверждением.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Изменяем состояние машины состояний на Admin.add_confirm.
    2. Отправляем сообщение с инструкциями для добавления рассылки с подтверждением.
    """
    await state.set_state(Admin.add_confirm)
    await callback.message.edit_text(
        "Отправьте текст для рассылки с подтверждением",
        reply_markup=get_add_confirm_kb(),
    )


async def del_confirm_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Эта функция обрабатывает callback-запрос для удаления рассылки с подтверждением.
    Она очищает текущее состояние, пытается удалить рассылку с подтверждением, используя функцию end_confirm()
    и отправляет соответствующее сообщение в зависимости от результата.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Очищаем текущее состояние машины состояний.
    2. Извлекаем ID рассылки с подтверждением из данных callback-запроса.
    3. Пытаемся удалить рассылку с подтверждением, используя функцию end_confirm().
    4. Если рассылка с подтверждением успешно удалена, отправляем сообщение об успешном удалении.
    5. Если пользователь не является модератором, отправляем соответствующее сообщение.
    6. В случае возникновения исключения, отправляем сообщение об ошибке.
    """
    await state.clear()
    _, _, id = callback.data.split("_")

    try:
        if end_confirm(id):
            await callback.message.edit_text(
                "Рассылка с подтверждением удалена",
                reply_markup=get_end_confirm_kb(),
            )
        else:
            await callback.message.edit_text(
                "Рассылка с подтверждением не удалена",
                reply_markup=get_end_confirm_kb(),
            )

    except Exception:
        await callback.message.edit_text(
            "Произошла ошибка",
            reply_markup=get_end_confirm_kb(),
        )


async def show_chat_callback(
    callback: CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    """
    Эта функция обрабатывает callback-запрос для показа ссылки на чат.
    Она очищает текущее состояние, получает ссылку на чат,
    используя функцию get_chat_link(), и отправляет сообщение
    с этой ссылкой.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :param bot: Объект Bot, представляющий бота.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Очищаем текущее состояние машины состояний.
    2. Получаем ссылку на чат.
    3. Если чат не инициализирован, отправляем сообщение об этом.
    4. Если чат инициализирован, отправляем сообщение с ссылкой на чат.
    """
    await state.clear()
    chat_link = await get_chat_link(bot)

    if not chat_link:
        await callback.message.edit_text(
            "Чат не инициализирован",
            reply_markup=get_chat_kb(None),
        )
        return

    await callback.message.edit_text(
        f"Ссылка на чат: {chat_link}",
        reply_markup=get_chat_kb(chat_link),
    )


async def edit_quiz_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Эта функция обрабатывает callback-запрос для редактирования информации о викторине.
    Она очищает текущее состояние, получает текст информации о викторине,
    используя функцию get_about_quiz(), и отправляет сообщение
    с текущим текстом и кнопкой для редактирования.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Изменяем состояние машины состояний на Admin.edit_about_quiz для редактирования О викторине.
    2. Получаем текст информации о викторине.
    3. Если текст не существует, отправляем сообщение об этом.
    4. Если текст существует, отправляем сообщение с текстом
    и кнопкой для редактирования.
    """
    await state.set_state(Admin.edit_about_quiz)
    about_quiz = await get_about_quiz()

    if not about_quiz:
        await callback.message.edit_text(
            "Отправьте текст для выставления в О викторине",
            reply_markup=get_back_kb(),
        )
        return

    await callback.message.edit_text(
        f"Текст о викторине:\n{about_quiz}\n\n",
        reply_markup=get_back_kb(),
    )


async def edit_faq_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Эта функция обрабатывает callback-запрос для редактирования часто задаваемых вопросов (FAQ).
    Она изменяет состояние машины состояний на Admin.edit_faq и отправляет сообщение
    с текущим текстом FAQ и инструкцией для редактирования.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Изменяем состояние машины состояний на Admin.edit_faq для редактирования FAQ.
    2. Получаем текущий текст FAQ из базы данных.
    3. Если текст FAQ не существует, отправляем сообщение с инструкцией для добавления текста.
    4. Если текст FAQ существует, отправляем сообщение с текущим текстом и инструкцией для редактирования.
    """
    await state.set_state(Admin.edit_faq)
    faq = await get_faq()

    if not faq:
        await callback.message.edit_text(
            "Отправьте текст для выставления в Частые вопросы",
            reply_markup=get_back_kb(),
        )
        return

    await callback.message.edit_text(
        f"Текст частых вопросов:\n{faq}\n\n",
        reply_markup=get_back_kb(),
    )


async def edit_rules_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Эта функция обрабатывает callback-запрос для редактирования правил.
    Она изменяет состояние машины состояний на Admin.edit_rules и отправляет сообщение
    с текущим текстом правил и инструкцией для редактирования.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Изменяем состояние машины состояний на Admin.edit_rules для редактирования правил.
    2. Получаем текущий текст правил из базы данных.
    3. Если текст правил не существует, отправляем сообщение с инструкцией для добавления текста.
    4. Если текст правил существует, отправляем сообщение с текущим текстом и инструкцией для редактирования.
    """
    await state.set_state(Admin.edit_rules)
    rules = await get_rules()

    if not rules:
        await callback.message.edit_text(
            "Отправьте текст для выставления в правилах",
            reply_markup=get_back_kb(),
        )
        return

    await callback.message.edit_text(
        f"Текст правил:\n{rules}\n\n",
        reply_markup=get_back_kb(),
    )


async def show_quizzes_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает callback-запрос для показа всех викторин администратору.
    Эта функция очищает текущее состояние, получает список викторин
    и отправляет сообщение с их данными.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Очищаем текущее состояние машины состояний.
    2. Получаем список викторин из базы данных с помощью функции get_quizzes_admin().
    3. Если список викторин пуст, отправляем сообщение о том, что викторин нет.
    4. Если викторины найдены, формируем текст сообщения с их ID и текстом.
    5. Отправляем сообщение с данными викторин и клавиатурой с возможными действиями.
    """
    await state.clear()
    quizzes = await get_quizzes_admin()

    if not quizzes:
        await callback.message.edit_text(
            "Нет викторин",
            reply_markup=get_quizzes_kb(),
        )
        return

    text = "Викторины:\n\n"
    text += "\n".join(f"ID: {quiz[0]} - {quiz[1]}" for quiz in quizzes)

    await callback.message.edit_text(
        text, reply_markup=get_quizzes_kb([quiz[0] for quiz in quizzes])
    )


async def show_quiz_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает callback-запрос для показа информации о викторине администратору.
    Она очищает текущее состояние, получает информацию о викторине из базы данных
    и отправляет сообщение с ее данными.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Очищаем текущее состояние машины состояний.
    2. Получаем информацию о викторине из базы данных с помощью функции get_quiz().
    3. Если викторина не найдена, отправляем сообщение о том, что викторина не найдена.
    4. Если викторина найдена, формируем текст сообщения с ее ID, текстом и ID.
    5. Отправляем сообщение с данными викторины и клавиатурой с возможными действиями.
    """
    await state.clear()
    _, _, id = callback.data.split("_")

    quiz = await get_quiz(id)

    if not quiz:
        await callback.message.edit_text(
            "Викторина не найдена",
            reply_markup=get_quiz_kb(),
        )
        return

    await callback.message.edit_text(
        f"Викторина:\n\n{quiz}\n\nВыберите действие:",
        reply_markup=get_quiz_kb(id),
    )


async def edit_quiz_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает callback-запрос для редактирования викторины администратором.
    Она очищает текущее состояние, изменяет состояние машины состояний на
    Admin.edit_quiz и отправляет сообщение с инструкциями для редактирования
    предстоящей викторины.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Изменяем состояние машины состояний на Admin.edit_quiz для редактирования конкретной викторины.
    2. Изменяем состояние машины состояний на Admin.edit_quiz.
    3. Отправляем сообщение с инструкциями для редактирования викторины.
    4. Добавляем id викторины в состояние машины состояний.
    """
    _, _, id = callback.data.split("_")
    await state.set_state(Admin.edit_quiz)
    await callback.message.edit_text(
        "Отправьте текст для редактирования предстоящей викторины",
        reply_markup=get_edit_quiz_kb(id),
    )

    await state.update_data(id=id)


async def del_quiz_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Эта функция обрабатывает callback-запрос для удаления викторины.
    Она очищает текущее состояние, извлекает ID викторины из данных callback-запроса
    и пытается удалить викторину, отправляя соответствующее сообщение в зависимости от результата.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Очищаем текущее состояние машины состояний.
    2. Извлекаем ID викторины из данных callback-запроса.
    3. Пытаемся удалить викторину, используя функцию del_quiz().
    4. Если викторина успешно удалена, отправляем сообщение об успешном удалении.
    5. Если викторина не была удалена, отправляем соответствующее сообщение.
    """
    await state.clear()
    _, _, id = callback.data.split("_")

    if await del_quiz(id):
        await callback.message.edit_text(
            "Викторина удалена",
            reply_markup=get_del_quiz_kb(),
        )
    else:
        await callback.message.edit_text(
            "Викторина не удалена",
            reply_markup=get_del_quiz_kb(),
        )


async def add_quiz_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Эта функция обрабатывает callback-запрос для добавления викторины.
    Она изменяет состояние машины состояний на
    Admin.add_quiz и отправляет сообщение с инструкциями
    для добавления викторины.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Изменяем состояние машины состояний на Admin.add_quiz.
    2. Отправляем сообщение с инструкциями для добавления викторины.
    """
    await state.set_state(Admin.add_quiz)
    await callback.message.edit_text(
        "Отправьте текст для добавления викторины",
        reply_markup=get_add_quiz_kb(),
    )


async def show_all_news_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает callback-запрос для просмотра всех новостей.
    Она очищает текущее состояние, получает из базы данных
    все новости и отправляет сообщение с текстом,
    содержащим информацию о рассылках.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Очищаем текущее состояние машины состояний.
    2. Получаем из базы данных все новости.
    3. Если новости не найдены, отправляем сообщение,
       информирующее о том, что новости не найдены.
    4. Если новости найдены, отправляем сообщение,
       содержащее информацию о рассылках.
    """
    await state.clear()
    news = await get_news_admin()

    if not news:
        await callback.message.edit_text(
            "Нет новостей",
            reply_markup=get_news_kb(),
        )
        return

    text = "Новости:\n\n"
    text += "\n".join(f"ID: {news[0]} - {news[1]}" for news in news)

    await callback.message.edit_text(
        text, reply_markup=get_news_kb([news[0] for news in news])
    )


async def show_one_news_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает callback-запрос для показа отдельной новости.
    Она очищает текущее состояние, извлекает ID новости из данных callback-запроса
    и отображает текст новости, если она найдена.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Очищаем текущее состояние машины состояний.
    2. Извлекаем ID новости из данных callback-запроса.
    3. Получаем текст новости из базы данных с помощью функции get_news_one().
    4. Если новость не найдена, отправляем сообщение о том, что новость не найдена.
    5. Если новость найдена, отправляем сообщение с ID и текстом новости, а также клавиатуру с возможными действиями.
    """
    await state.clear()
    _, _, _, id = callback.data.split("_")

    news = await get_news_one(int(id))

    if not news:
        await callback.message.edit_text(
            "Новость не найдена",
            reply_markup=get_news_kb(),
        )
        return

    id, description = news

    await callback.message.edit_text(
        f"Новость:\n\nID:{id} - {description}\n\nВыберите действие:",
        reply_markup=get_news_one_kb(id),
    )


async def add_news_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает callback-запрос для добавления новости.
    Она изменяет состояние машины состояний на Admin.add_news
    и отправляет сообщение с инструкциями для добавления новости.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Изменяем состояние машины состояний на Admin.add_news.
    2. Отправляем сообщение с инструкциями для добавления новости.
    """
    await state.set_state(Admin.add_news)
    await callback.message.edit_text(
        "Отправьте текст для добавления новости",
        reply_markup=get_add_news_kb(),
    )


async def edit_news_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает callback-запрос для редактирования новости.
    Она изменяет состояние машины состояний на Admin.edit_news
    и отправляет сообщение с инструкциями для редактирования новости.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Изменяем состояние машины состояний на Admin.edit_news.
    2. Отправляем сообщение с инструкциями для редактирования новости.
    """
    _, _, id = callback.data.split("_")
    await state.set_state(Admin.edit_news)
    await callback.message.edit_text(
        "Отправьте текст для редактирования предстоящей новости",
        reply_markup=get_edit_news_kb(id),
    )

    await state.update_data(id=id)


async def del_news_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает callback-запрос для удаления новости.
    Она очищает текущее состояние машины состояний,
    извлекает ID новости из данных callback-запроса,
    удаляет новость с помощью функции del_news()
    и отправляет соответствующее сообщение в зависимости от результата.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Очищаем текущее состояние машины состояний.
    2. Извлекаем ID новости из данных callback-запроса.
    3. Пытаемся удалить новость с помощью функции del_news().
    4. Если новость была успешно удалена, отправляем сообщение об успешном удалении.
    5. Если новость не была удалена, отправляем сообщение об ошибке.
    """
    await state.clear()
    _, _, id = callback.data.split("_")

    if await del_news(id):
        await callback.message.edit_text(
            "Новость удалена",
            reply_markup=get_del_news_kb(),
        )
    else:
        await callback.message.edit_text(
            "Новость не удалена",
            reply_markup=get_del_news_kb(),
        )


async def start_callback(
    callback: CallbackQuery, state: FSMContext, is_subadmin: bool
) -> None:
    """
    Обрабатывает callback-запрос для начала работы.
    Она очищает текущее состояние машины состояний,
    отправляет сообщение с приветствием и предлагает
    выбрать действие.

    :param callback: Объект CallbackQuery, представляющий callback-запрос.
    :param state: Объект FSMContext, представляющий состояние машины состояний.
    :return: None

    Внутренний процесс:
    1. Очищаем текущее состояние машины состояний.
    2. Отправляем сообщение с приветствием.
    """
    await state.clear()
    if is_subadmin:
        role = "субадминистратор"
    else:
        role = "администратор"
    await callback.message.edit_text(
        f"Здравствуйте, {role}!\nВыберите действие",
        reply_markup=get_admin_kb(is_subadmin),
    )
