# Данные о курсах на Курсере

Программа собирает информацию о курсах c образовательного ресурса [Coursera](https://www.coursera.org) и сохраняет в файл excel.  По умолчанию выбираются 20 курсов в произвольном порядке и со страницы каждого курса извлекается следующая информация:
- Название курса;
- Язык;
- Дата начала;
- Продолжительность курса (в неделях);
- Пользовательский рейтинг.

# Установка

Для запуска программы требуется установленный Python 3.5.  
В программе используются следующие сторонние библиотеки:  
- [aiohttp](https://aiohttp.readthedocs.io/en/stable/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [lxml](http://lxml.de/)
- [openpyxl](https://openpyxl.readthedocs.io/en/default/)

Используйте команду pip для установки сторонних библиотек из файла зависимостей (или pip3 если есть конфликт с предустановленным Python 2):
```
pip install -r requirements.txt # В качестве альтернативы используйте pip3
```
Рекомендуется устанавливать зависимости в виртуальном окружении, используя [virtualenv](https://github.com/pypa/virtualenv), [virtualenvwrapper](https://pypi.python.org/pypi/virtualenvwrapper) или [venv](https://docs.python.org/3/library/venv.html).

# Использование

### Аргументы командной строки:
- ```-n``` - количество ссылок для парсинга (значение по умолчанию = 20).
- ```-a, --all``` - обрабатывать все ссылки.  

Пример запуска в Linux(Debian), Python 3.5.2:

```
$ python coursera.py 
File 'coursera.xlsx' has been saved
```
Excel файл сохраняется в текущую дерикторию.

# Цели проекта

Код написан для образовательных целей. Учебный курс для веб-разработчиков - [DEVMAN.org](https://devman.org)
