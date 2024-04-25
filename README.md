На сайте codeforces есть большая подборка задач.
В данном проекте представлен парсер задач и их свойств:
1. Тема("математика" , "перебор", "графы" ...)
2. Количество решений задач
3. Название + номер
4. Сложность задачи
Парсер парсит и сохраняет в базу данных postgresql с периодичностью 1 час.
Выбрать тему и сложность и получить выборку из 10 задач можно через телеграм бота,
а также получить детали конкретной задачи по ее имени и номеру.

Чтоб запустить проект необходимо запустить файл main.py. Также в отдельных
терминалах ввести команду для запуска worker celery
celery -A main worker --loglevel=info
а также beat celery в другом терминале
celery -A main beat --loglevel=info

Также предварительно необходимо создать телеграм бота через чат BotFather,
выполнив команду /newbot. Далее ввести название и юзернэйм бота. Получив
токен вставьте его в файл зависимостей. Далее нажав команду /start бот начнет диалог.
Нажав кнопку /Task_parser бот предложит варианты тематик задач. Следующим вопросом
будет сложность задач. Также бот предложит рассмотреть детали задачи по имени и номеру.
