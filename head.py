from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import random
import json
import os

# TODO: Рекомендуется хранить токен в переменных окружения или конфигурационном файле
TOKEN = "7547968978:AAF5TSlOiS4Kcj9X091wUNvjsdx6QisC5hw"

# База данных с вопросами (50 вопросов)
cards = {
    "Что такое Python?": ["Язык программирования", "Змея", "Философия", "Библиотека"],
    "Что такое функция?": ["Блок кода", "Математическая формула", "График", "Переменная"],
    "Как объявить список?": ["lst = []", "lst = {}", "list()", "array[]"],
    "Что выведет print(2+2*2)?": ["6", "8", "4", "Ошибку"],
    "Какой тип у 3.14?": ["float", "int", "str", "bool"],
    "Что делает метод append()?": ["Добавляет элемент", "Удаляет элемент", "Сортирует список", "Копирует список"],
    "Как создать кортеж?": ["t = (1, 2)", "t = [1, 2]", "t = {1, 2}", "t = '1, 2'"],
    "Что такое PEP8?": ["Стандарт оформления кода", "Библиотека", "Язык программирования", "Фреймворк"],
    "Как получить длину списка?": ["len(lst)", "lst.length", "lst.size", "length(lst)"],
    "Что такое Git?": ["Система контроля версий", "Язык программирования", "База данных", "Фреймворк"],
    "Как импортировать модуль?": ["import module", "require module", "include module", "use module"],
    "Что делает break в цикле?": ["Прерывает цикл", "Продолжает цикл", "Возвращает значение", "Вызывает ошибку"],
    "Как объявить словарь?": ["d = {}", "d = []", "d = ()", "d = ''"],
    "Что такое ООП?": ["Объектно-ориентированное программирование", "Операционная система", "База данных", "Язык запросов"],
    "Как создать класс?": ["class MyClass:", "def MyClass:", "new MyClass:", "create MyClass"],
    "Что такое self в Python?": ["Ссылка на экземпляр класса", "Зарезервированное слово", "Модуль", "Функция"],
    "Как работает наследование?": ["Класс-потомок получает методы родителя", "Копирует код", "Создает новый модуль", "Импортирует функции"],
    "Что такое Django?": ["Веб-фреймворк", "База данных", "Язык программирования", "Графическая библиотека"],
    "Как открыть файл для чтения?": ["open('file.txt', 'r')", "open('file.txt', 'w')", "read('file.txt')", "file.open('file.txt')"],
    "Что такое API?": ["Интерфейс программирования приложений", "Язык программирования", "База данных", "Фреймворк"],
    "Что такое lambda-функция?": ["Анонимная функция", "Именованная функция", "Главная функция", "Вложенная функция"],
    "Как работает list comprehension?": ["Генерация списка", "Фильтрация списка", "Сортировка списка", "Удаление элементов"],
    "Что такое декоратор?": ["Функция для модификации других функций", "Стиль оформления кода", "Тип данных", "Модуль"],
    "Как создать множество?": ["s = set()", "s = {}", "s = []", "s = ()"],
    "Что делает метод strip()?": ["Удаляет пробелы", "Добавляет пробелы", "Разделяет строку", "Объединяет строки"],
    "Как преобразовать строку в число?": ["int('123')", "str(123)", "float('123')", "num('123')"],
    "Что такое итератор?": ["Объект для перебора элементов", "Функция", "Модуль", "Тип данных"],
    "Как работает оператор in?": ["Проверяет наличие элемента", "Добавляет элемент", "Удаляет элемент", "Сортирует элементы"],
    "Что такое генератор?": ["Функция с yield", "Функция с return", "Цикл", "Условие"],
    "Как получить текущую дату и время?": ["datetime.now()", "time.now()", "date.current()", "now()"],
    "Что делает метод split()?": ["Разделяет строку", "Объединяет строки", "Удаляет пробелы", "Заменяет подстроки"],
    "Как объявить глобальную переменную?": ["global x", "glob x", "var x", "x = global"],
    "Что такое виртуальное окружение?": ["Изолированная среда для Python", "Облачное хранилище", "Графическая среда", "База данных"],
    "Как работает try-except?": ["Обработка исключений", "Условие", "Цикл", "Функция"],
    "Что такое модуль collections?": ["Специальные структуры данных", "Коллекции картинок", "База данных", "Фреймворк"],
    "Как создать асинхронную функцию?": ["async def", "async function", "def async", "function async"],
    "Что такое @staticmethod?": ["Декоратор для статического метода", "Декоратор для класса", "Декоратор для свойства", "Декоратор для функции"],
    "Как работает enumerate()?": ["Возвращает индекс и значение", "Сортирует элементы", "Фильтрует элементы", "Преобразует типы"],
    "Что такое pickle?": ["Модуль для сериализации", "Модуль для работы с файлами", "Модуль для математики", "Модуль для сетей"],
    "Как работает zip()?": ["Объединяет последовательности", "Разделяет последовательности", "Сортирует последовательности", "Фильтрует последовательности"],
    "Что такое init?": ["Конструктор класса", "Деструктор класса", "Метод класса", "Свойство класса"],
    "Как работает with?": ["Контекстный менеджер", "Цикл", "Условие", "Функция"],
    "Что такое NumPy?": ["Библиотека для научных вычислений", "Фреймворк для веба", "База данных", "Графическая библиотека"],
    "Как создать пакет в Python?": ["Папка с init.py", "Файл .py", "Файл .txt", "Файл .json"],
    "Что такое pandas?": ["Библиотека для анализа данных", "База данных", "Фреймворк для веба", "Графическая библиотека"],
    "Как работает map()?": ["Применяет функцию к последовательности", "Создает карту", "Фильтрует последовательность", "Сортирует последовательность"],
    "Что такое Flask?": ["Микро-фреймворк для веба", "Полноценный фреймворк", "База данных", "Графическая библиотека"],
    "Как работает filter()?": ["Фильтрует последовательность", "Сортирует последовательность", "Преобразует последовательность", "Объединяет последовательности"],
    "Что такое name?": ["Специальная переменная", "Функция", "Модуль", "Класс"],
    "Как работает any()?": ["Возвращает True если хотя бы один элемент True", "Возвращает True если все элементы True", "Возвращает False", "Фильтрует последовательность"],
}

correct_answers = {
    "Что такое Python?": 0,
    "Что такое функция?": 0,
    "Как объявить список?": 0,
    "Что выведет print(2+2*2)?": 0,
    "Какой тип у 3.14?": 0,
    "Что делает метод append()?": 0,
    "Как создать кортеж?": 0,
    "Что такое PEP8?": 0,
    "Как получить длину списка?": 0,
    "Что такое Git?": 0,
    "Как импортировать модуль?": 0,
    "Что делает break в цикле?": 0,
    "Как объявить словарь?": 0,
    "Что такое ООП?": 0,
    "Как создать класс?": 0,
    "Что такое self в Python?": 0,
    "Как работает наследование?": 0,
    "Что такое Django?": 0,
    "Как открыть файл для чтения?": 0,
    "Что такое API?": 0,
    "Что такое lambda-функция?": 0,
    "Как работает list comprehension?": 0,
    "Что такое декоратор?": 0,
    "Как создать множество?": 0,
    "Что делает метод strip()?": 0,
    "Как преобразовать строку в число?": 0,
    "Что такое итератор?": 0,
    "Как работает оператор in?": 0,
    "Что такое генератор?": 0,
    "Как получить текущую дату и время?": 0,
    "Что делает метод split()?": 0,
    "Как объявить глобальную переменную?": 0,
    "Что такое виртуальное окружение?": 0,
    "Как работает try-except?": 0,
    "Что такое модуль collections?": 0,
    "Как создать асинхронную функцию?": 0,
    "Что такое @staticmethod?": 0,
    "Как работает enumerate()?": 0,
    "Что такое pickle?": 0,
    "Как работает zip()?": 0,
    "Что такое init?": 0,
    "Как работает with?": 0,
    "Что такое NumPy?": 0,
    "Как создать пакет в Python?": 0,
    "Что такое pandas?": 0,
    "Как работает map()?": 0,
    "Что такое Flask?": 0,
    "Как работает filter()?": 0,
    "Что такое name?": 0,
    "Как работает any()?": 0,
}

# Для хранения конспектов
notes_file = "user_notes.json"
user_notes = {}
if os.path.exists(notes_file):
    try:
        with open(notes_file, 'r', encoding='utf-8') as f:
            user_notes = json.load(f)
    except json.JSONDecodeError:
        print(f"Ошибка: не удалось декодировать {notes_file}. Начинаем с пустыми конспектами.")
        user_notes = {} # Инициализация пустым словарем в случае ошибки
    except Exception as e:
        print(f"Произошла непредвиденная ошибка при загрузке {notes_file}: {e}. Начинаем с пустыми конспектами.")
        user_notes = {}
else:
    user_notes = {}

user_state = {} # Для хранения состояния теста для каждого пользователя

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("/test"), KeyboardButton("/notes")],
        [KeyboardButton("/help")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Привет! Это учебный бот с тестами и конспектами.\n"
        "Выбери действие:",
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = ("Доступные команды:\n"
        "/start - главное меню\n"
        "/test - начать тест\n"
        "/end_test - завершить тест досрочно\n"
        "/notes - работа с конспектами\n"
        "/add_note - добавить конспект\n"
        "/find_note - найти конспект\n"
        "/shuffle - перемешать вопросы (для следующего теста)\n"
        "/reset - сбросить прогресс текущего теста\n"
        "/cancel - отменить текущее действие (например, добавление конспекта)"
    )
    await update.message.reply_text(help_text)

async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    questions = list(cards.keys())
    random.shuffle(questions) # Перемешиваем вопросы для каждого нового теста

    user_state[chat_id] = {
        "mode": "test",
        "score": 0,
        "questions": questions,
        "current_question": 0,
        "total_questions": len(questions)
    }
    await ask_question(update, chat_id)

async def ask_question(update: Update, chat_id: int):
    state = user_state.get(chat_id, {})
    if not state or state.get("mode") != "test":
        # Если по какой-то причине состояние не теста, выходим или возвращаем в меню
        await update.message.reply_text("Ошибка: режим теста не активен. Пожалуйста, начните заново.",
                                        reply_markup=ReplyKeyboardMarkup([["/start"]], resize_keyboard=True))
        if chat_id in user_state:
             del user_state[chat_id] # Очищаем некорректное состояние
        return

    if state["current_question"] >= len(state["questions"]):
        await end_test(update, chat_id)
        return

    question = state["questions"][state["current_question"]]
    options = cards[question]

    # Создаем кнопки для вариантов ответа
    option_buttons = [[KeyboardButton(option)] for option in options]
    # Добавляем кнопку для досрочного завершения
    option_buttons.append([KeyboardButton("/end_test")])
    markup = ReplyKeyboardMarkup(option_buttons, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text(
        f"Вопрос {state['current_question']+1}/{state['total_questions']}\n"
        f"❓ {question}",
        reply_markup=markup
    )

async def handle_test_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    state = user_state.get(chat_id, {})

    # Если не в режиме теста или нет текущего вопроса - пропускаем
    if not state or state.get("mode") != "test":
        return

    # Если вопросы закончились
    if state["current_question"] >= len(state["questions"]):
        await end_test(update, chat_id)
        return

    text = update.message.text
    if text == "/end_test": # Команда для досрочного завершения
        await end_test(update, chat_id)
        return

    current_question_text = state["questions"][state["current_question"]]
    correct_idx = correct_answers[current_question_text]
    correct_option_text = cards[current_question_text][correct_idx]

    if text == correct_option_text:
        state["score"] += 1
        await update.message.reply_text("✅ Верно!")
    else:
        await update.message.reply_text(f"❌ Неверно! Правильный ответ: {correct_option_text}")

    state["current_question"] += 1
    await ask_question(update, chat_id)


async def end_test(update: Update, chat_id: int):
    state = user_state.get(chat_id, {})
    if not state or state.get("mode") != "test":
        await update.message.reply_text("Тест не был начат или уже завершен.",
                                        reply_markup=ReplyKeyboardMarkup([["/start"]], resize_keyboard=True))
        return

    score = state["score"]
    total = state["total_questions"]
    percentage = int(score/total*100) if total > 0 else 0

    await update.message.reply_text(
        f"Тест завершен!\n"
        f"Правильных ответов: {score}/{total}\n"
        f"Процент правильных: {percentage}%\n"
        "Напишите /test чтобы начать заново или /start для возврата в меню.",
        reply_markup=ReplyKeyboardMarkup([["/test"], ["/start"]], resize_keyboard=True)
    )

    if chat_id in user_state:
        del user_state[chat_id] # Удаляем состояние теста

async def end_test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await end_test(update, update.message.chat.id)


# --- Система конспектов ---
async def notes_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("/add_note"), KeyboardButton("/find_note")],
        [KeyboardButton("/start")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Работа с конспектами:\n"
        "/add_note - добавить новый конспект\n"
        "/find_note - найти существующий конспект",
        reply_markup=reply_markup
    )

ADD_NOTE_TITLE, ADD_NOTE_CONTENT = range(2)

async def add_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Введите название для вашего нового конспекта:",
        reply_markup=ReplyKeyboardMarkup([["/cancel"]], resize_keyboard=True)
    )
    return ADD_NOTE_TITLE

async def handle_note_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['note_title'] = update.message.text
    await update.message.reply_text("Отлично! Теперь введите содержание вашего конспекта:")
    return ADD_NOTE_CONTENT

async def handle_note_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id_str = str(update.message.chat.id)
    title = context.user_data.pop('note_title', 'Без названия') # Удаляем из user_data после использования
    content = update.message.text

    if chat_id_str not in user_notes:
        user_notes[chat_id_str] = {}

    user_notes[chat_id_str][title] = content

    try:
        with open(notes_file, 'w', encoding='utf-8') as f:
            json.dump(user_notes, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Ошибка при сохранении конспекта в файл: {e}")
        await update.message.reply_text("Произошла ошибка при сохранении конспекта. Попробуйте позже.")
        return ConversationHandler.END

    await update.message.reply_text(
        f"Конспект '{title}' успешно сохранен!",
        reply_markup=ReplyKeyboardMarkup([["/add_note", "/find_note"], ["/start"]], resize_keyboard=True)
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Если пользователь был в процессе добавления конспекта, очищаем временные данные
    if 'note_title' in context.user_data:
        context.user_data.pop('note_title', None)

    await update.message.reply_text(
        "Действие отменено.",
        reply_markup=ReplyKeyboardMarkup([["/start"]], resize_keyboard=True)
    )
    return ConversationHandler.END

# Обработчик добавления конспекта
conv_handler_add_note = ConversationHandler(
    entry_points=[CommandHandler('add_note', add_note)],
    states={
        ADD_NOTE_TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_note_title)],
        ADD_NOTE_CONTENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_note_content)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

# Обработчик поиска конспекта
FIND_NOTE = range(1)

async def find_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔍 Введите название или часть названия конспекта для поиска:",
        reply_markup=ReplyKeyboardMarkup([["/cancel"]], resize_keyboard=True)
    )
    return FIND_NOTE

async def handle_find_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id_str = str(update.message.chat.id)
    search_term = update.message.text.lower().strip()

    if not search_term:
        await update.message.reply_text("Пожалуйста, введите непустой запрос для поиска.")
        return FIND_NOTE

    user_personal_notes = user_notes.get(chat_id_str, {})
    found_notes_messages = []

    for title, content in user_personal_notes.items():
        if search_term in title.lower():
            found_notes_messages.append(f"📝 <b>{title}</b>:\n{content}")
        elif search_term in content.lower():
            found_notes_messages.append(f"📝 <b>{title}</b> (найдено в содержании):\n{content}")

    if found_notes_messages:
        response_message = "\n\n---\n\n".join(found_notes_messages)
        if len(response_message) > 4096:
            response_message = response_message[:4090] + "\n[...]"
        await update.message.reply_text(response_message, parse_mode='HTML')
    else:
        await update.message.reply_text("Конспекты по вашему запросу не найдены.")

    keyboard = [
        [KeyboardButton("/add_note"), KeyboardButton("/find_note")],
        [KeyboardButton("/start")]
    ]
    await update.message.reply_text(
        "Поиск завершен. Выберите действие:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    return ConversationHandler.END

# Правильный синтаксис для ConversationHandler
conv_handler_find_note = ConversationHandler(
    entry_points=[CommandHandler('find_note', find_note)],
    states={
        FIND_NOTE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_find_note)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

async def shuffle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Вопросы для тестов будут перемешаны при следующем запуске /test.")

async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    if chat_id in user_state and user_state[chat_id].get("mode") == "test":
        del user_state[chat_id]
        await update.message.reply_text("Прогресс текущего теста сброшен! Можете начать новый /test.",
                                        reply_markup=ReplyKeyboardMarkup([["/test"],["/start"]], resize_keyboard=True))
    else:
        await update.message.reply_text("Активный тест для сброса не найден.",
                                         reply_markup=ReplyKeyboardMarkup([["/start"]], resize_keyboard=True))

def main():
    app = Application.builder().token(TOKEN).build()

    # Обработчики конспектов
    app.add_handler(conv_handler_add_note)
    app.add_handler(conv_handler_find_note)

    # Обработчики команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("test", test_command))
    app.add_handler(CommandHandler("end_test", end_test_command))
    app.add_handler(CommandHandler("notes", notes_command))
    app.add_handler(CommandHandler("shuffle", shuffle_command))
    app.add_handler(CommandHandler("reset", reset_command))
    app.add_handler(CommandHandler("cancel", cancel))

    # Обработчики текстовых сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_test_answer))

    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()