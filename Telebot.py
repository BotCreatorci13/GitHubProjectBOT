import requests
import asyncio
from bs4 import BeautifulSoup
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters, CallbackQueryHandler, Updater

# Функция для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Текст приветствия
    welcome_text = (
        "Здравствуйте, вас приветствует информационный телеграмм-бот средней школы №13🎓.\n\n"
        "Пожалуйста, выберите пользователя или используйте следующие команды для навигации:\n\n"
        "  /news — для показа новостей\n"
        "  /Info — для получения информации о школе\n"
        "  /schedule — для получения расписания\n"
        "  /help — для получения большей информации о боте и его функционале"
    )

    # Создание inline-кнопок для выбора пользователя
    inline_keyboard = [
        [
            InlineKeyboardButton("Родитель", callback_data='parent'),
            InlineKeyboardButton("Учитель", callback_data='teacher'),
            InlineKeyboardButton("Ученик", callback_data='student')
        ]
    ]

    # Создание разметки для inline-кнопок
    inline_markup = InlineKeyboardMarkup(inline_keyboard)

    # Создание reply-клавиатуры, которая будет отображаться под полем ввода
    reply_keyboard = [
        [
            KeyboardButton("Новости"),
            KeyboardButton("Расписание"),
            KeyboardButton("Инфо")
        ],
        [
            KeyboardButton("Помощь")
        ],
        [
            KeyboardButton("Начало")
        ]
    ]

    # Разметка для reply-клавиатуры
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=False)

    # Отправка сообщения с inline-кнопками и reply-клавиатурой
    if update.message:
        # Отправка с обеими клавишами
        await update.message.reply_text(welcome_text, reply_markup=inline_markup, parse_mode="Markdown")
        await update.message.reply_text(text="Кнопки активны", reply_markup=reply_markup)
    elif update.callback_query:
        # Для обработки callback_query (например, при нажатии на inline-кнопки)
        await update.callback_query.edit_message_text(welcome_text, reply_markup=inline_markup, parse_mode="Markdown")
        await update.callback_query.message.reply_text(text="Кнопки активны", reply_markup=reply_markup)
results=[]
async def start_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Если нажата кнопка "Назад" (Sback), перенаправляем на блок обработки student
    if query.data == "Sback":
        query_data = "student"
    elif query.data == "Tback":
        query_data="teacher"
    elif query.data == "Pback":
        query_data = "parent"
    else:
        query_data = query.data

    # Устанавливаем сообщения и клавиатуры для каждого сценария
    if query_data == "parent":
        message = ("Здравствуйте Родитель! Вас приветствует информационный телеграмм-бот средней школы №13🎓.\n\n"
                   "Пожалуйста, выберите интересующую вас категорию или используйте следующие команды для навигации:\n\n"
                   "  /news — для показа новостей\n"
                   "  /Info — для получения информации о школе\n"
                   "  /schedule — для получения расписания\n"
                   "  /help — для получения большей информации о боте и его функционале")
        keyboard = [
            [InlineKeyboardButton("Родительский комитет", callback_data='Pbutton1'),
             InlineKeyboardButton("Попечительский совет", callback_data='Pbutton2'),
             InlineKeyboardButton("СППС", callback_data='Pbutton3')],
            [InlineKeyboardButton("На главную", callback_data='back')]
        ]
    elif query_data == "Pbutton1":
        url="https://sch13.oktobrgrodno.gov.by/%D1%80%D0%BE%D0%B4%D0%B8%D1%82%D0%B5%D0%BB%D1%8F%D0%BC/%D1%80%D0%BE%D0%B4%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D1%81%D0%BA%D0%B8%D0%B9-%D0%BA%D0%BE%D0%BC%D0%B8%D1%82%D0%B5%D1%82"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Проверяем статус ответа

            soup = BeautifulSoup(response.text, "html.parser")
            items = soup.find("table").find("tbody").find_all("tr")[1:]  # Пропускаем заголовок таблицы

            # Инициализация переменной для сообщения
            message = (f"📋 Состав родительского комитета:\n\n"
                       )

            for item in items:
                cells = item.find_all("td")  # Используем find_all для всех ячеек
                if len(cells) >= 2:  # Проверяем, что в строке есть хотя бы две ячейки
                    FIo = cells[0].get_text(strip=True)  # ФИО
                    klass = cells[1].get_text(strip=True)  # Класс
                    message += f"• **{FIo}**, класс: `{klass}`\n"  # Добавляем строку в сообщение
            message+=(f"\n\nC планом работы родителского комитета можно ознакомиться [здесь]({url})\n\n")
            # Если message пустой после цикла
            if not message:
                message = "Данные не найдены на сайте."

        except requests.RequestException as e:
            message = f"Ошибка при получении данных с сайта: {e}"
        except Exception as e:
            message = f"Произошла ошибка: {e}"

        keyboard=[
            [InlineKeyboardButton("Попечительский совет",callback_data="Pbutton2"),
             InlineKeyboardButton("СППС",callback_data="Pbutton3")],
            [InlineKeyboardButton("Назад", callback_data="Pback")]
        ]
    elif query_data == "Pbutton2":
        message=("📋 Попечительский совет\n\n"
                 "`Работа попечительского совета осуществляется согласно ст.25 Кодекса Республики Беларусь об образовании. "
                 "Деятельность попечительских советов осуществляется в соответствии "
                 "с Положением о попечительском совете учреждения образования, утвержденным "
                 "постановлением Министерства образования РБ от 25 июля 2011 г. №146 (в ред. от 16.08.2022 №266).`"
                 "\n\n •Телефон горячей линии: 8 (0152) 71 22 44\n\n"
                 "C **составом** и **отчетом** по работе можно ознакомиться ниже")

        keyboard=[
            [InlineKeyboardButton("Состав",callback_data="sostav"),InlineKeyboardButton("Отчет",callback_data="otchet")],
            [InlineKeyboardButton("Родительский комитет",callback_data="Pbutton1"),
             InlineKeyboardButton("СППС",callback_data="Pbutton3")],
            [InlineKeyboardButton("Назад", callback_data="Pback")]
        ]
    elif query_data=="sostav":
        url="https://sch13.oktobrgrodno.gov.by/%D1%80%D0%BE%D0%B4%D0%B8%D1%82%D0%B5%D0%BB%D1%8F%D0%BC/%D0%BF%D0%BE%D0%BF%D0%B5%D1%87%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D1%81%D0%BA%D0%B8%D0%B9-%D1%81%D0%BE%D0%B2%D0%B5%D1%82"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Проверяем статус ответа

            soup = BeautifulSoup(response.text, "html.parser")
            items = soup.find("table").find_all("tr")[1:]

            # Инициализация переменной для сообщения
            message = (f"📋 Состав попечительского совета:\n\n")

            for item in items:
                cells = item.find_all("td")  # Используем find_all для всех ячеек
                if len(cells) >= 2:  # Проверяем, что в строке есть хотя бы две ячейки
                    FIo = cells[0].get_text(strip=True)  # ФИО
                    klass = cells[1].get_text(strip=True)  # Класс
                    message += f"• **{FIo}**,   Должность: `{klass}`\n"  # Добавляем строку в сообщение

            # Если message пустой после цикла
            if not message:
                message = "Данные не найдены на сайте."

        except requests.RequestException as e:
            message = f"Ошибка при получении данных с сайта: {e}"
        except Exception as e:
            message = f"Произошла ошибка: {e}"

        keyboard=[[InlineKeyboardButton("Назад", callback_data="Pbutton2")]]
    elif query_data == "otchet":
        url = "https://sch13.oktobrgrodno.gov.by/%D1%80%D0%BE%D0%B4%D0%B8%D1%82%D0%B5%D0%BB%D1%8F%D0%BC/%D0%BF%D0%BE%D0%BF%D0%B5%D1%87%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D1%81%D0%BA%D0%B8%D0%B9-%D1%81%D0%BE%D0%B2%D0%B5%D1%82"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Проверяем статус ответа

            soup = BeautifulSoup(response.text, "html.parser")
            # Находим вкладку с id="tab4"
            items = soup.find("div", id="tab4")

            # Извлекаем заголовок, период и описание
            title = items.find("span", style="text-decoration: none;").get_text(strip=True)
            period = items.find_all("span", style="text-decoration: none;")[2].get_text(strip=True)

            # Формируем сообщение
            message = (
                f"📋 *Отчет попечительского совета*\n\n"
                f"**{title}**\n"
                f"📅 Период: {period}\n\n"
            )
            description = items.find_all("p", style="text-align: justify;")
            for desc in description:
                des=desc.get_text(strip=True)
                message +=(f"{des}\n\n")

            message +=(f"📚 С планом работы попечительского совета можно ознакомиться [здесь]({url})")
        except requests.RequestException as e:
            message = f"Ошибка при получении данных с сайта: {e}"
        except Exception as e:
            message = f"Произошла ошибка: {e}"

        # Клавиатура с кнопкой назад
        keyboard = [[InlineKeyboardButton("Назад", callback_data="Pbutton2")]]
    elif query_data == "Pbutton3":
        url1="https://sch13.oktobrgrodno.gov.by/%D1%81%D0%BF%D0%BF%D1%81/%D1%81%D0%BE%D1%86%D0%B8%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE-%D0%BF%D0%B5%D0%B4%D0%B0%D0%B3%D0%BE%D0%B3%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F-%D0%B8-%D0%BF%D1%81%D0%B8%D1%85%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F-%D1%81%D0%BB%D1%83%D0%B6%D0%B1%D0%B0"
        url2="https://sch13.oktobrgrodno.gov.by/%D1%81%D0%BF%D0%BF%D1%81/%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D1%8F-%D0%B4%D0%BB%D1%8F-%D1%80%D0%BE%D0%B4%D0%B8%D1%82%D0%B5%D0%BB%D0%B5%D0%B9"
        message=("📚 Социально-педагогическая и психологическая служба\n\n"
                 f"Ознкомиться с общей информацией о СППС школы можно [здесь]({url1})\n\n"
                 f"Вот [СППС]({url2}) специально для родителй")
        keyboard=[
            [InlineKeyboardButton("Попечительский совет",callback_data="Pbutton2"),
             InlineKeyboardButton("Родительский комитет",callback_data="Pbutton1")],
            [InlineKeyboardButton("Назад", callback_data="Pback")]
        ]
    elif query_data == "teacher":
        message = ("Здравствуйте Учитель! Вас приветствует информационный телеграмм-бот средней школы №13🎓.\n\n"
                   "Пожалуйста, выберите интересующую вас категорию или используйте следующие команды для навигации:\n\n"
                   "  /news — для показа новостей\n"
                   "  /Info — для получения информации о школе\n"
                   "  /schedule — для получения расписания\n"
                   "  /help — для получения большей информации о боте и его функционале")
        keyboard = [
            [InlineKeyboardButton("ШАГ", callback_data='Tbutton1'),
             InlineKeyboardButton("Норм. Документы", callback_data='Tbutton2'),
             InlineKeyboardButton("СППС", callback_data='Tbutton3')],
            [InlineKeyboardButton("На главную", callback_data='back')]
        ]
    elif query_data == "Tbutton1":
        global results
        url="https://sch13.oktobrgrodno.gov.by/%D0%B2%D0%BE%D1%81%D0%BF%D0%B8%D1%82%D0%B0%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F-%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0/%D1%88%D0%BA%D0%BE%D0%BB%D0%B0-%D0%B0%D0%BA%D1%82%D0%B8%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE-%D0%B3%D1%80%D0%B0%D0%B6%D0%B4%D0%B0%D0%BD%D0%B8%D0%BD%D0%B0"
        message=("*📚 Школа Активного Гражданина*\n\n"
                 "")
        results.clear()
        try:
            response = requests.get(url)
            response.raise_for_status()  # Проверяем статус ответа

            soup = BeautifulSoup(response.text, "html.parser")
            containers = soup.find_all("div", class_="spoiler item entry", limit=9)


            for container in containers:
                theme_tag = container.find("h3")
                date_tag = container.find("span", class_="date")

                # Проверяем наличие тегов и их содержимого
                if theme_tag:
                    theme = theme_tag.find_next(string=True).strip() if theme_tag.find_next(string=True) else "Тема не найдена"
                else:
                    theme = "Тема не найдена"

                if date_tag and date_tag.string:
                    date = date_tag.string.strip()
                else:
                    date = "Дата не найдена"

                results.append({"Тема": theme, "Дата": date})

            # Формируем сообщение для бота
            for i, result in enumerate(results, start=1):
                message += f"*{i}.* _Тема:_ {result['Тема']}\n"
                message += f"   📆 *Дата:* {result['Дата']}\n\n"
            message+=f"Ознакомиться с полным перечнем можно [здесь]({url})"
        except requests.RequestException as e:
            message = f"Ошибка при получении данных с сайта: {e}"
        except Exception as e:
            message = f"Произошла ошибка: {e}"

        keyboard = [[InlineKeyboardButton("Поиск по дате 🔍",callback_data="search_date"),
                     InlineKeyboardButton("Поиск по теме 🔍",callback_data="search_theme")],
        [InlineKeyboardButton("Норм. Документы", callback_data='Tbutton2'),
         InlineKeyboardButton("СППС", callback_data='Tbutton3')],
        [InlineKeyboardButton("Назад", callback_data='Tback')]
    ]
    elif query_data == "search_date":
        message=("🔍 Введите дату для поиска (например, 27.11.2024):")
        keyboard =[[(InlineKeyboardButton("Назад",callback_data="Tbutton1"))]]
        context.user_data['search_type'] = 'date'

    elif query_data == "search_theme":
        message=("🔍 Введите ключевое слово для поиска по теме:")
        keyboard =[[(InlineKeyboardButton("Назад",callback_data="Tbutton1"))]]
        context.user_data['search_type'] = 'theme'


    elif query_data == "Tbutton2":
        url="https://sch13.oktobrgrodno.gov.by/%D1%83%D1%87%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D1%81%D0%BA%D0%B0%D1%8F/%D0%BD%D0%BE%D1%80%D0%BC%D0%B0%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B5-%D0%BF%D1%80%D0%B0%D0%B2%D0%BE%D0%B2%D1%8B%D0%B5-%D0%B4%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D1%8B"
        url1 = "https://sch13.oktobrgrodno.gov.by/%D1%83%D1%87%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D1%81%D0%BA%D0%B0%D1%8F/%D0%BD%D0%BE%D1%80%D0%BC%D0%B0%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B5-%D0%BF%D1%80%D0%B0%D0%B2%D0%BE%D0%B2%D1%8B%D0%B5-%D0%B4%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D1%8B"
        Url_Base1="https://drive.google.com/file/d/1VXrVd-WmhS4jLipUtIGxiYDs6OvyqoHw/view"
        Url_Base2="https://drive.google.com/file/d/1Vm8cxoIY_5TkHUu9Qed0uG4tICbnufhu/view"
        message = ("")
        try:
            response = requests.get(url)
            response.raise_for_status()  # Проверяем статус ответа

            soup = BeautifulSoup(response.text, "html.parser")
            articles = soup.find_all('div', class_='col-sm-8 col-lg-9 article')
            for article in articles:
                # Заголовок основного раздела
                title = article.find('h1').get_text(strip=True)
                message += f"📂 {title}\n\n"
                message += f"   🔗 [Кодекс Республики Беларусь]({Url_Base1}\n)"
                message += f"\n   🔗 [ДЕКРЕТ ПРЕЗИДЕНТА РЕСПУБЛИКИ БЕЛАРУСЬ 24 ноября 2006 г. No 18 О дополнительных мерах по государственной защите детей в неблагополучных семьях]({Url_Base2})\n\n"
                # Обработка всех `div.content` внутри статьи
                contents = article.find_all('div', class_='content')[:3]
                for content in contents:
                    # Поиск подзаголовков (h2)
                    subtitles = content.find_all('h2')
                    if subtitles:
                        for subtitle in subtitles:
                            subtitle_text = subtitle.get_text(strip=True)
                            message += f"📌 {subtitle_text}\n"

                            # Ищем все ссылки после подзаголовка
                            sibling = subtitle.find_next_sibling()
                            while sibling:
                                links = sibling.find_all('a', href=True)
                                for link in links:
                                    text = link.get_text(strip=True)
                                    url = link['href']
                                    if text:
                                        message += f"   🔗 [{text}]({url})\n"
                                    else:
                                        message += f"   🔗 {url}\n"
                                sibling = sibling.find_next_sibling()
                            message += "\n"
                    else:
                        # Если подзаголовков нет, ищем ссылки в общем контенте
                        links = content.find_all('a', href=True)
                        for link in links:
                            text = link.get_text(strip=True)
                            url = link['href']
                            if text:
                                message += f"🔗 [{text}]({url})\n"
                            else:
                                message += f"🔗 {url}\n"
                        message += "\n"
            message +=(f"\n📚 C более подробной информацие можно ознакомиться [здесь]({url1})")
        except requests.RequestException as e:
            message = f"Ошибка при получении данных с сайта: {e}"
        except Exception as e:
            message = f"Произошла ошибка: {e}"

        keyboard = [
            [InlineKeyboardButton("ШАГ", callback_data='Tbutton1'),
             InlineKeyboardButton("СППС", callback_data='Tbutton3')],
            [InlineKeyboardButton("На главную", callback_data='back')]
        ]
    elif query_data == "Tbutton3":
        url = "https://sch13.oktobrgrodno.gov.by/%D1%81%D0%BF%D0%BF%D1%81/%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D1%8F-%D0%B4%D0%BB%D1%8F-%D0%BF%D0%B5%D0%B4%D0%B0%D0%B3%D0%BE%D0%B3%D0%BE%D0%B2"
        url1 = "https://sch13.oktobrgrodno.gov.by/%D1%81%D0%BF%D0%BF%D1%81/%D1%81%D0%BE%D1%86%D0%B8%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE-%D0%BF%D0%B5%D0%B4%D0%B0%D0%B3%D0%BE%D0%B3%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F-%D0%B8-%D0%BF%D1%81%D0%B8%D1%85%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F-%D1%81%D0%BB%D1%83%D0%B6%D0%B1%D0%B0"
        message = ("📢**Информация для Учителей:**\n")
        try:
            response = requests.get(url)
            response.raise_for_status()  # Проверяем статус ответа

            soup = BeautifulSoup(response.text, "html.parser")
            # Находим вкладку с id="tab4"
            items1 = soup.find("div", class_="col-sm-8 col-lg-9 article")
            items = items1.find_all("h3")
            # Извлекаем заголовок, период и описание
            for item in items:
                temp = item.get_text(strip=True)
                message += f"\n✅{temp}\n [Подробнее]({url})"
            # Формируем сообщение
            message += (f"\n\n📞Горячая линия помощи для учащихся: `170`")
            message += (f"\n\n❓ Если у вас есть вопросы или вам нужна помощь обратитесь 💬[Сюда]({url1} \n ")

        except requests.RequestException as e:
            message = f"Ошибка при получении данных с сайта: {e}"
        except Exception as e:
            message = f"Произошла ошибка: {e}"
        keyboard = [
            [InlineKeyboardButton("Норм. Документы", callback_data='Tbutton2'),
             InlineKeyboardButton("ШАГ", callback_data='Tbutton1')],
            [InlineKeyboardButton("На главную", callback_data='back')]
        ]
    elif query_data == "student":
        message = ("Здравствуйте Ученик! Вас приветствует информационный телеграмм-бот средней школы №13🎓.\n\n"
                   "Пожалуйста, выберите интересующую вас категорию или используйте следующие команды для навигации:\n\n"
                   "  /news — для показа новостей\n"
                   "  /Info — для получения информации о школе\n"
                   "  /schedule — для получения расписания\n"
                   "  /help — для получения большей информации о боте и его функционале")
        keyboard = [
            [InlineKeyboardButton("Профориентация", callback_data='Sbutton1'),
             InlineKeyboardButton("СППС", callback_data='Sbutton2'),
             InlineKeyboardButton("Выпускнику", callback_data='Sbutton3')],
            [InlineKeyboardButton("На главную", callback_data='back')]
        ]
    elif query_data == "Sbutton1":
        url="https://docs.google.com/presentation/d/1N5-rN4vbGvJ-wWfWU8ID7ZK52F7uZpFma1JkHltbFHg/edit?usp=sharing"
        url1="https://sch13.oktobrgrodno.gov.by/%D0%BE%D0%B1%D1%83%D1%87%D0%B0%D1%8E%D1%89%D0%B8%D0%BC%D1%81%D1%8F/%D0%BF%D1%80%D0%BE%D1%84%D0%BE%D1%80%D0%B8%D0%B5%D0%BD%D1%82%D0%B0%D1%86%D0%B8%D1%8F"
        message = (
            "🎓 *Профориентация для учащихся*\n\n"
            "Для учащихся *9-х классов* вопрос о выборе профориентации остается актуальным. "
            "Чтобы помочь школьникам определиться с выбором и устранить сомнения, была подготовлена специальная:\n\n"
            f"📑 **[ПРЕЗЕНТАЦИЯ]({url})**\n"
            "✨ Дополнительно ознакомиться с информацией можно по ссылке:\n"
            f"🔗 **[Подробнее здесь]({url1})**\n\n"
            f"Мы надеемся, что эти материалы помогут вам в выборе будущей профессии!🚀\n\n {url1}"
        )

        keyboard = [
            [InlineKeyboardButton("СППС", callback_data="Sbutton2"),
             InlineKeyboardButton("Выпускнику", callback_data="Sbutton3")],
             [InlineKeyboardButton("Назад", callback_data="Sback")]
        ]
    elif query_data == "Sbutton2":
        url="https://sch13.oktobrgrodno.gov.by/%D1%81%D0%BF%D0%BF%D1%81/%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D1%8F-%D0%B4%D0%BB%D1%8F-%D1%83%D1%87%D0%B0%D1%89%D0%B8%D1%85%D1%81%D1%8F"
        url1="https://sch13.oktobrgrodno.gov.by/%D1%81%D0%BF%D0%BF%D1%81/%D1%81%D0%BE%D1%86%D0%B8%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE-%D0%BF%D0%B5%D0%B4%D0%B0%D0%B3%D0%BE%D0%B3%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F-%D0%B8-%D0%BF%D1%81%D0%B8%D1%85%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F-%D1%81%D0%BB%D1%83%D0%B6%D0%B1%D0%B0"
        message=("📢**Информация для учащихся**\n"
                 "📌Актуальные темы для учащихся:\n")
        try:
            response = requests.get(url)
            response.raise_for_status()  # Проверяем статус ответа

            soup = BeautifulSoup(response.text, "html.parser")
            # Находим вкладку с id="tab4"
            items1 = soup.find("div", class_="col-sm-8 col-lg-9 article")
            items=items1.find_all("h3")
            # Извлекаем заголовок, период и описание
            for item in items:
                temp=item.get_text(strip=True)
                message+=f"\n✅{temp}\n [Подробнее]({url})"
            # Формируем сообщение
            message += (f"\n\n📞Горячая линия помощи: `170`")
            message+=(f"\n\n❓ Если у вас есть вопросы или вам нужна помощь обратитесь 💬[Сюда]({url1} \n ")

        except requests.RequestException as e:
            message = f"Ошибка при получении данных с сайта: {e}"
        except Exception as e:
            message = f"Произошла ошибка: {e}"

        keyboard = [
            [InlineKeyboardButton("Профориентация", callback_data="Sbutton1"),
             InlineKeyboardButton("Выпускнику", callback_data="Sbutton3")],
             [InlineKeyboardButton("Назад", callback_data="Sback")]
        ]
    elif query_data == "Sbutton3":
        url="https://sch13.oktobrgrodno.gov.by/%D0%BE%D0%B1%D1%83%D1%87%D0%B0%D1%8E%D1%89%D0%B8%D0%BC%D1%81%D1%8F/%D0%B2%D1%8B%D0%BF%D1%83%D1%81%D0%BA%D0%BD%D0%B8%D0%BA%D1%83"
        message = (
            "🎓 *Информация для выпускников*\n\n"
            "В этом разделе собрана основная информация, которая поможет вам успешно пройти этапы поступления и подготовки.\n\n"
            f"📌 Полный перечень материалов доступен [здесь]({url}).\n"
            "Мы желаем вам удачи на пути к новым достижениям и успехам! 🚀"
        )

        keyboard = [
            [InlineKeyboardButton("Поступления в УВО", callback_data="UVO"),
             InlineKeyboardButton("Поступления в УССО", callback_data="USSO"),
             InlineKeyboardButton("Календарь выпускника", callback_data="Kalend")],
            [InlineKeyboardButton("СППС", callback_data="Sbutton2"),
             InlineKeyboardButton("Профориентация", callback_data="Sbutton1")],
             [InlineKeyboardButton("Назад", callback_data="Sback")]
        ]

    elif query_data=="UVO":
        url="https://sch13.oktobrgrodno.gov.by/%D0%BE%D0%B1%D1%83%D1%87%D0%B0%D1%8E%D1%89%D0%B8%D0%BC%D1%81%D1%8F/%D0%B2%D1%8B%D0%BF%D1%83%D1%81%D0%BA%D0%BD%D0%B8%D0%BA%D1%83"
        message=("📋 *Информация для выпускников:*\n\n")
        try:
            response = requests.get(url)
            response.raise_for_status()  # Проверяем статус ответа

            soup = BeautifulSoup(response.text, "html.parser")
            # Находим вкладку с id="t"
            items = soup.find("div", id="tab2")
            # Извлекаем заголовок, период и описание
            paragraphs = items.find_all("p")[1:]
            list_items = items.find_all("li")

            # Индексы для списков
            din = 0  # Для paragraphs
            bin = 0  # Для list_items

            # Выводим один блок <p> и два блока <li>
            for i in range(min(len(paragraphs), 2)):
                # Выводим один элемент из paragraphs
                paragraph_text = paragraphs[i].get_text(strip=True)
                if paragraph_text:
                    message += f"📌 {paragraph_text}\n\n"

                # Выводим три элемента из list_items
                for j in range(i * 3, i * 3 + 3):
                    if j < len(list_items):
                        item_text = list_items[j].get_text(strip=True)
                        if item_text:
                            message += f"🔹 {item_text}\n\n"

            message += (f"\n📖 Вся информация доступна [здесь]({url}) в разделе \"Сроки поступления в УССО\".")
        except requests.RequestException as e:
            message = f"Ошибка при получении данных с сайта: {e}"
        except Exception as e:
            message = f"Произошла ошибка: {e}"

        keyboard =[[(InlineKeyboardButton("Назад",callback_data="Sbutton3"))]]

    elif query_data=="USSO":
        url = "https://sch13.oktobrgrodno.gov.by/%D0%BE%D0%B1%D1%83%D1%87%D0%B0%D1%8E%D1%89%D0%B8%D0%BC%D1%81%D1%8F/%D0%B2%D1%8B%D0%BF%D1%83%D1%81%D0%BA%D0%BD%D0%B8%D0%BA%D1%83"
        message=("📋 *Информация для выпускников:*\n\n")
        try:
            response = requests.get(url)
            response.raise_for_status()  # Проверяем статус ответа

            soup = BeautifulSoup(response.text, "html.parser")
            # Находим вкладку с id="tab3"
            items = soup.find("div", id="tab3")
            # Извлекаем заголовки <p> и списки <li>
            paragraphs = items.find_all("p")[1:]
            list_items = items.find_all("li")

            for i in range(min(len(paragraphs), 2)):
                # Выводим один элемент из paragraphs
                paragraph_text = paragraphs[i].get_text(strip=True)
                if paragraph_text:
                    message += f"📌 {paragraph_text}\n\n"

                # Выводим три элемента из list_items
                for j in range(i * 4, i * 4 + 4):
                    if j < len(list_items):
                        item_text = list_items[j].get_text(strip=True)
                        if item_text:
                            message += f"🔹 {item_text}\n\n"

            message += (f"\n📖 Вся информация доступна [здесь]({url}) в разделе \"Сроки поступления в УССО\".")
        except requests.RequestException as e:
            message = f"Ошибка при получении данных с сайта: {e}"
        except Exception as e:
            message = f"Произошла ошибка: {e}"


        keyboard =[[(InlineKeyboardButton("Назад",callback_data="Sbutton3"))]]

    elif query_data=="Kalend":
        url = "https://sch13.oktobrgrodno.gov.by/%D0%BE%D0%B1%D1%83%D1%87%D0%B0%D1%8E%D1%89%D0%B8%D0%BC%D1%81%D1%8F/%D0%B2%D1%8B%D0%BF%D1%83%D1%81%D0%BA%D0%BD%D0%B8%D0%BA%D1%83"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Проверяем успешность запроса

            soup = BeautifulSoup(response.text, "html.parser")

            # Находим основной контейнер с календарем
            items = soup.find("div", id="tab1")

            # Ищем все параграфы
            paragraphs = items.find_all("p")

            events = []

            # Перебираем все параграфы
            for paragraph in paragraphs:
                # Ищем элементы, которые могут быть месяцем или событием
                month_span = paragraph.find("span", style="color: red;")  # Месяц
                event_spans_120 = paragraph.find_all("span",
                                                     style="color: black; font-size: 120%;")  # События с font-size 120%
                event_spans = paragraph.find_all("span", style="color: black;")  # События без font-size 120%

                # Извлекаем текст месяца
                month = month_span.get_text(strip=True) if month_span else None

                # Извлекаем все события и объединяем их в одну строку
                all_event_text = []

                # Сначала добавляем события с font-size 120%
                for event in event_spans_120:
                    event_text = event.get_text(strip=True)
                    if event_text:  # Проверка на пустое событие
                        all_event_text.append(event_text)

                # Затем добавляем все остальные события
                for event in event_spans:
                    event_text = event.get_text(strip=True)
                    if event_text:  # Проверка на пустое событие
                        all_event_text.append(event_text)

                # Если месяц или события найдены, добавляем их в список
                if month or all_event_text:
                    # Убираем лишние пробелы и пустые строки
                    events.append({"month": month, "events": ' '.join(all_event_text).strip()})

            # Формируем сообщение
            message = "📅 *Календарь выпускника*\n\n"
            for event in events:
                if event["month"]:
                    message += f"🔸 *{event['month']}*\n"
                if event["events"]:  # Если есть события
                    message += f"  - {event['events']}\n"
                message += "\n"


        except requests.RequestException as e:
            message = f"Ошибка при получении данных с сайта: {e}"
        except Exception as e:
            message = f"Произошла ошибка: {e}"

        keyboard = [[(InlineKeyboardButton("Назад", callback_data="Sbutton3"))]]


    elif query_data == "back":
        await start(update, context)
        return
    else:
        return

    # Создание разметки для новых кнопок
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Обновление сообщения с новым текстом и кнопками
    await query.edit_message_text(text=message, reply_markup=reply_markup, parse_mode="Markdown")

#Новости + ссылка на них
async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://sch13.oktobrgrodno.gov.by/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/%D0%B0%D1%80%D1%85%D0%B8%D0%B2-%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D0%B5%D0%B9"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('div', class_='item')

        if items:
            news_text = "📢 Последние новости за этот месяц:\n\n"
            for item in items[:10]:  # Ограничим вывод 10 новостями
                # Извлекаем ссылку на новость
                link = item.find('a', class_='preview')['href'] if item.find('a', class_='preview') else None

                # Если ссылка относительная, добавляем базовый URL
                full_link = link if link else "Ссылка недоступна"
                if not full_link.startswith("http"):
                    full_link = "https://sch13.oktobrgrodno.gov.by" + link  # Добавить базовый URL

                # Извлекаем дату
                date = item.find('span', class_='date').get_text() if item.find('span', class_='date') else "Дата не указана"

                # Извлекаем заголовок новости
                title = item.find('h3').get_text() if item.find('h3') else "Без заголовка"

                # Формируем строку для новости с кликабельной ссылкой
                news_text += f"**{title}**\n📅 Дата: {date}\n [Читать далее]({full_link})\n\n"

            # Отправляем сообщение с новостями
            await update.message.reply_text(news_text, parse_mode='Markdown')
        else:
            await update.message.reply_text("Не удалось найти новости.")
    else:
        await update.message.reply_text("Ошибка при получении данных с сайта.")

 #Функция для обработки команды /info
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Ссылки на классы
    link1 = "https://sch13.oktobrgrodno.gov.by/%D0%BE%D0%B1-%D1%83%D1%87%D1%80%D0%B5%D0%B6%D0%B4%D0%B5%D0%BD%D0%B8%D0%B8/%D0%BA%D0%BB%D0%B0%D1%81%D1%81%D1%8B-%D0%BF%D1%80%D0%BE%D1%84%D0%B5%D1%81%D1%81%D0%B8%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B9-%D0%BD%D0%B0%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D0%B8/%D1%82%D0%B0%D0%BC%D0%BE%D0%B6%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9-%D0%BA%D0%BB%D0%B0%D1%81%D1%81"
    link2 = "https://sch13.oktobrgrodno.gov.by/%D0%BE%D0%B1-%D1%83%D1%87%D1%80%D0%B5%D0%B6%D0%B4%D0%B5%D0%BD%D0%B8%D0%B8/%D0%BA%D0%BB%D0%B0%D1%81%D1%81%D1%8B-%D0%BF%D1%80%D0%BE%D1%84%D0%B5%D1%81%D1%81%D0%B8%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B9-%D0%BD%D0%B0%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D0%B8/%D0%BF%D1%80%D0%B0%D0%B2%D0%BE%D0%B2%D0%BE%D0%B9-%D0%BA%D0%BB%D0%B0%D1%81%D1%81"
    link3 = "https://sch13.oktobrgrodno.gov.by/%D0%BE%D0%B1-%D1%83%D1%87%D1%80%D0%B5%D0%B6%D0%B4%D0%B5%D0%BD%D0%B8%D0%B8/%D0%BA%D0%BB%D0%B0%D1%81%D1%81%D1%8B-%D0%BF%D1%80%D0%BE%D1%84%D0%B5%D1%81%D1%81%D0%B8%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B9-%D0%BD%D0%B0%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D0%B8/%D0%BD%D0%B0%D0%BB%D0%BE%D0%B3%D0%BE%D0%B2%D0%BE%D0%B9-%D0%BA%D0%BB%D0%B0%D1%81%D1%81"

    # Текст приветствия
    welcome_text = (
        f"🎓*СРЕДНЯЯ ШКОЛА №13 имени В.Т.Цабо*\n\n"
        "Предметом деятельности школы является осуществление образовательной деятельности, "
        "включающей обучение и воспитание в соответствии с законодательством Республики Беларусь.\n\n"
        "*Основная цель:* формирование интеллектуальной, образованной, нравственно зрелой, "
        "разносторонне развитой личности, способной реализовать творческий потенциал "
        "в динамических социально-экономических условиях.\n\n"
        "*Особенности школы:* \n "
        "• Классы профессиональной направленности:\n"
        f"[Таможенный класс]({link1}), [Правовой класс]({link2}), [Налоговый класс]({link3});\n"
        f"• Уникальная школьная форма отличающаяся в зависимости от проф. класса.\n\n"
        f"Для получения мини-истории о названии школы напишите 📖'*История*'\n\n"
        f"Для получения доп информации воспользуйтесь командами\n"
        f"Или выберите раздел ниже:"
    )

    # Кнопки выбора
    # Кнопки выбора
    keyboard = [
        [
            InlineKeyboardButton("Контактная информация", callback_data='kinfo'),
            InlineKeyboardButton("Руководство школы", callback_data='pkol'),
            InlineKeyboardButton("Ссылки на веб ресурсы", callback_data='veb')
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправка сообщения
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")
    elif update.callback_query:
        await update.callback_query.edit_message_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

#мини история
async def story(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message
    if user_message:
        await user_message.delete()
    story_text = (
        "🎓СРЕДНЯЯ ШКОЛА №13 имени В.Т.Цабо.🎓\n\n"
        "•Мини-история названия:\n"
        "Школа названа в честь имени Владимира Тихоновича Цабо. Цабо, одного из командиров "
        "диверсионной бригады, являющейся самым мощным диверсионным подразделением бригады Ворошилова."
        "В ходе одного из налетов Владимир Тихонович был ранен в обе ноги, одну из них позже он потерял."
        "В последствии чего был доставлен в тыл и получил Орден Отечественной войны I степени. "
        "В.Т. Цабо руководил Средней школой № 13 г. Гродно с 1957 по 1968 гг."
        "и за этот период сумел достичь немалых успехов. Он первым зародил школьные традиции "
        "проводить праздники, экскурсии, организовать горячие завтраки для учащихся.\n\n"
        "На сегодняшний день Школа представляет из себя учреждение где одновременно "
        "обучается более 500 учащихся в различных классах."
    )
    # Создаем кнопку для удаления сообщения
    keyboard = [
        [InlineKeyboardButton("🗑 Удалить сообщение", callback_data="delete_story")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем сообщение пользователю с кнопкой
    await update.message.reply_text(
        text=story_text,
        parse_mode="HTML",
        reply_markup=reply_markup
    )

async def delete_story(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Отвечаем на нажатие кнопки, чтобы избежать "часов"
    # Удаляем сообщение
    await query.message.delete()
    # Обработчик для кнопок в разделе информации
async def info_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Закрываем "загрузка" на кнопке

    # Создаем текст для каждой кнопки
    if query.data == 'kinfo':
        text = (
            "📞 Контактная информация:\n"
            "• Телефоны:\n"
            "  (0152) 71-22-44 Директор школы\n"
            "  (0152) 71-22-47 Приемная, факс\n"
            "  (0152) 71-22-45 Заместитель дирректора по учебно-метод. работе\n"
            "  (0152) 71-22-46 Медецинский кабинет\n"
            "• Адрес: г. Гродно, ул.Берёзовая, 2 \n"
            "• Электронная почта: sch13@oktobrgrodno.gov.by"
        )
    elif query.data == 'pkol':
        Url="https://sch13.oktobrgrodno.gov.by/%D0%BE%D0%B1-%D1%83%D1%87%D1%80%D0%B5%D0%B6%D0%B4%D0%B5%D0%BD%D0%B8%D0%B8/%D1%80%D1%83%D0%BA%D0%BE%D0%B2%D0%BE%D0%B4%D1%81%D1%82%D0%B2%D0%BE-%D1%88%D0%BA%D0%BE%D0%BB%D1%8B"
        linkTech="https://sch13.oktobrgrodno.gov.by/%D1%83%D1%87%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D1%81%D0%BA%D0%B0%D1%8F/%D0%BF%D0%B5%D0%B4%D0%B0%D0%B3%D0%BE%D0%B3%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9-%D0%BA%D0%BE%D0%BB%D0%BB%D0%B5%D0%BA%D1%82%D0%B8%D0%B2"
        response = requests.get(Url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.find_all('div', class_='item item_card')

            leadership = []
            for item in items:
                # Имя руководителя
                name_tag = item.find("h3")
                name = name_tag.text.strip() if name_tag else "Имя неизвестно"

                # Характеристики руководителя
                details_list = item.find("ul", class_="list-unstyled")
                details = []
                if details_list:
                    details = [li.text.strip() for li in details_list.find_all("li")]

                leadership.append({"name": name, "details": details})

            # Формирование текста для вывода
            if leadership:
                text = "👨‍💼 Руководство школы:\n\n"
                for leader in leadership:
                    text += f"• Имя: {leader['name']}\n"
                    text += "\n ".join(leader['details']) + "\n\n"
                text+=f"👩‍🏫 Так же можете ознакомиться с [Педагогическим коллективом]({linkTech})"
            else:
                text = "Данные о руководстве школы не найдены."
        else:
            text="Ошибка парсинга"

    elif query.data == 'veb':

        text = (
            "🌐 Ссылки на веб-ресурсы:\n"
            "• [Сайт школы](https://sch13.oktobrgrodno.gov.by)\n"
            "• [Электронный журнал](https://example.com)"
        )
    elif query.data == 'Iback':
        await info(update, context)  # Возвращаем пользователя в главное меню информации
        return
    else:
        return

    # Добавляем кнопки с возможностью "Назад"
    keyboard = [
        [
            InlineKeyboardButton("Контактная информация", callback_data='kinfo') if query.data != 'kinfo' else None,
            InlineKeyboardButton("Руководство школы", callback_data='pkol') if query.data != 'pkol' else None,
            InlineKeyboardButton("Ссылки на веб ресурсы", callback_data='veb') if query.data != 'veb' else None,
            InlineKeyboardButton("Назад", callback_data='Iback'),

        ]
    ]

    # Убираем `None` из списка кнопок
    keyboard = [list(filter(None, row)) for row in keyboard]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # Обновляем сообщение
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text=(
        "📅 <b>Расписание занятий</b>:\n\n"
        "<pre>"
        "|1 смена       | 2 смена       | \n"
        "|------------------------------| \n"
        "|8:00 – 8:45   | 14:00 – 14:45 | \n"
        "|8:55 – 9:40   | 15:00 – 15:45 | \n"
        "|9:55 – 10:40  | 16:00 – 16:45 | \n"
        "|10:55 – 11:40 | 16:55 – 17:40 | \n"
        "|12:00 – 12:45 | 17:50 – 18:35 | \n"
        "|12:55 – 13:40 | 18:45 – 19:30 | "
        "</pre>"
    )
    keyboard=[
        [
            InlineKeyboardButton("Расписание факультативных занятий",callback_data="fakult")],
            [InlineKeyboardButton("Календарь четвертей и каникул",callback_data="Kon")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        query = update.callback_query
        await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode="HTML")
    else:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="HTML")

async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Закрываем индикатор загрузки на кнопке

    # Проверяем, какая кнопка была нажата
    if query.data == "fakult":
        text = (
            "📚 <b>Расписание факультативных занятий</b>:\n\n"
            "<pre>"
            "День       | Время        | Предмет\n"
            "---------------------------------\n"
            "Понедельник| 14:00 - 15:00| Математика\n"
            "Вторник    | 15:00 - 16:00| Химия\n"
            "Среда      | 13:00 - 14:00| Физика\n"
            "Четверг    | 14:30 - 15:30| Биология\n"
            "Пятница    | 12:00 - 13:00| История\n"
            "</pre>"
        )
        keyboard = [
            [InlineKeyboardButton("Назад", callback_data="schedule")]
        ]
    elif query.data == "Kon":
        url = "https://sch13.oktobrgrodno.gov.by/%d0%be%d0%b1%d1%83%d1%87%d0%b0%d1%8e%d1%89%d0%b8%d0%bc%d1%81%d1%8f/%d0%be%d1%80%d0%b3%d0%b0%d0%bd%d0%b8%d0%b7%d0%b0%d1%86%d0%b8%d1%8f-%d0%be%d0%b1%d1%80%d0%b0%d0%b7%d0%be%d0%b2%d0%b0%d1%82%d0%b5%d0%bb%d1%8c%d0%bd%d0%be%d0%b3%d0%be-%d0%bf%d1%80%d0%be%d1%86%d0%b5%d1%81%d1%81%d0%b0"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Генерирует исключение, если статус код не 200

            soup = BeautifulSoup(response.text, "html.parser")
            items = soup.find_all("p", style=lambda value: value and "text-align: justify;" in value)

            # Сбор текста из подходящих элементов
            text_list = [item.get_text(strip=True) for item in items if item.get_text(strip=True)]
            text = "📜 <b>Календарь четвертей и каникул:</b>\n\n" + "\n\n".join(text_list[:10])
        except requests.RequestException as e:
            text = f"Ошибка при получении данных с сайта: {e}"
        except Exception as e:
            text = f"Произошла ошибка: {e}"

        keyboard = [
            [InlineKeyboardButton("Назад", callback_data="schedule")]
        ]
    elif query.data == "schedule":
        # Возврат к расписанию
        await schedule(update, context)
        return
    else:
        text = "❌ Неизвестная команда!"
        keyboard = [
            [InlineKeyboardButton("Назад", callback_data="schedule")]
        ]

    # Обновляем текст сообщения и кнопки
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=text, parse_mode="HTML", reply_markup=reply_markup)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text=(f"Справка по функционалу и возможностям бота:\n\n"
          f"📝Основные комманды:\n"
          f" /start - для получения основной информации\n"
          f" /news — для показа новостей\n"
          f" /Info — для получения информации о школе\n"
          f" /schedule — для получения расписания\n"
          f" /help — для получения большей информации о боте и его функционале\n"
          "💬 *Дополнительно:*\n"
          "   Не обязательно использовать команды, достаточно просто написать:\n"
          "   - _\"Новости\"_ для получения новостей\n"
          "   - _\"Расписание\"_ для получения расписания\n"
          "   _И.т.д_"
    )

    await update.message.reply_text(text=text, parse_mode="Markdown")
# Основная программа для запуска бота


# Обработчик ввода текста для поиска
async def handle_search_input(update, context):
    user_input = update.message.text.strip().lower()
    search_type = context.user_data.get('search_type')  # Получаем тип поиска из контекста
    url="https://sch13.oktobrgrodno.gov.by/%D0%B2%D0%BE%D1%81%D0%BF%D0%B8%D1%82%D0%B0%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F-%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0/%D1%88%D0%BA%D0%BE%D0%BB%D0%B0-%D0%B0%D0%BA%D1%82%D0%B8%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE-%D0%B3%D1%80%D0%B0%D0%B6%D0%B4%D0%B0%D0%BD%D0%B8%D0%BD%D0%B0"
    # Проверяем, есть ли активный поиск
    if not search_type:
        # Если поиска нет (то есть нет запроса на поиск), игнорируем ввод
        return

    filtered_results = []
    if search_type == 'date':
        # Поиск по дате
        filtered_results = [r for r in results if user_input in r['Дата'].lower()]
    elif search_type == 'theme':
        # Поиск по теме
        filtered_results = [r for r in results if user_input in r['Тема'].lower()]

    # Формируем ответ с результатами поиска
    message = "*🔍 Результаты поиска:*\n\n"
    if filtered_results:
        for i, result in enumerate(filtered_results, start=1):
            message += f"*{i}.* _Тема:_ {result['Тема']}\n"
            message += f"   📆 *Дата:* {result['Дата']}\n"
            message+=f"Ссылка на [информацию]({url})\n\n"
    else:
        message += ("❗ Ничего не найдено по вашему запросу."
                    "\n\n❗ Проаерьте корреектность запроса")


    # Создаем клавиатуру для возврата к основному меню
    keyboard = [[InlineKeyboardButton("Назад", callback_data="Tbutton1")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем новое сообщение с результатами поиска
    await update.message.reply_text(message, reply_markup=reply_markup, parse_mode="Markdown")
    context.user_data['search_type'] = None



if __name__ == '__main__':

    app = Application.builder().token("ТУТ ВАШ ТОКЕН БОТА!").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^(Начало|начало|глав|Глав|Главная|главная|Старт|старт|start)$"), start))
    app.add_handler(CallbackQueryHandler(start_button_callback,pattern="^(parent|Pbutton1|Pbutton2|sostav|otchet|Pbutton3|Pback|teacher|Tbutton1|search_date|search_theme|Tbutton2|Tbutton3|Tback|student|Sbutton1|Sbutton2|Sbutton3|UVO|USSO|Kalend|Sback|back)$"))
    app.add_handler(CommandHandler(["news"], news))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^(Новости|новости|news)$"), news))
    app.add_handler(CommandHandler(["info"], info))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^(Инфо|информация|info)$"), info))
    app.add_handler(CallbackQueryHandler(info_button_callback, pattern="^(kinfo|pkol|veb|Iback)$"))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^(История|история)$"), story))
    app.add_handler(CallbackQueryHandler(delete_story, pattern="delete_story"))
    app.add_handler(CommandHandler("schedule",schedule))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^(расп|рсапис|Распис|Расп|расписание|Расписание|schedule)$"), schedule))
    app.add_handler(CallbackQueryHandler(handle_button_click, pattern="^(fakult|Kon|schedule)$"))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^(памагы|помощь|Помощь|help)$"),help))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_search_input))

    # Запускаем бота
    print("Бот запущен!")
    app.run_polling()
