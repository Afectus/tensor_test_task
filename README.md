### ОБЩАЯ СТРУКТУРА ПРОЕКТА

> Представление общей структуры проекта

```bash
├── json_data.json # Данные для загрузки в базу, в формате json
├── main_class.py # Базовые классы для работы с базой
├── README.md 
├── requirements.txt # Необходимые библиотеки
├── run.py # Запуск утилиты
├── settings.py # Настройки для подключения к базе
```
### FAQ
```bash
Для запуска необходимо использовать run.py
Примеры использования:
	python run.py --create_table создание таблицы для персонала
	python run.py --load_json_data загрузка данных из json файла
	python run.py --show_persons_in_city вывод всех сотрудников работающих в городе.
				  --show_persons_in_city [id] работника
```