# Coursera Dump

Программа собирает информацию о курсах c образовательного ресурса [Coursera](https://www.coursera.org) и сохраняет в файл excel.  По умолчанию выбираются 20 курсов в произвольном порядке и со страницы каждого курса извлекается следующая информация:
- Название курса;
- Язык;
- Дата начала;
- Продолжительность курса (в неделях);
- Пользовательский рейтинг.

# Установка

Для запуска программы требуется установленный Python 3.  
Используйте команду pip для установки сторонних библиотек из файла зависимостей (или pip3 если есть конфликт с предустановленным Python 2):
```bash
pip install -r requirements.txt # В качестве альтернативы используйте pip3
```
Рекомендуется устанавливать зависимости в виртуальном окружении, используя [virtualenv](https://github.com/pypa/virtualenv), [virtualenvwrapper](https://pypi.python.org/pypi/virtualenvwrapper) или [venv](https://docs.python.org/3/library/venv.html).

# Использование

Пример запуска в Linux, Python 3.5.2:

```
$ python coursera.py 
100%|██████████████████████████████████████████████████████████████| 20/20 [00:02<00:00,8.25it/s]
File 'coursera.xlsx' has been saved
```
Excel файл сохраняется в текущую папку.

# Цели проекта

Код написан для образовательных целей. Учебный курс для веб-разработчиков - [DEVMAN.org](https://devman.org)
