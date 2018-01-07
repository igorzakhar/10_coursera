import asyncio
import random
import xml.etree.ElementTree as etree

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from openpyxl import Workbook


async def fetch_response(url, session):
    async with session.get(url) as response:
        return await response.text(encoding='utf-8')


async def fetch_xml(session):
    xml = 'https://www.coursera.org/sitemap~www~courses.xml'
    body = await fetch_response(xml, session)
    return body


def get_random_urls(body):
    number_links = 20
    root = etree.fromstring(body)
    url_list = [child[0].text for child in root]
    random_urls = random.sample(url_list, number_links)
    return random_urls


async def fetch_courses_html():
    async with ClientSession() as session:
        body = await fetch_xml(session)
        urls = get_random_urls(body)
        tasks = [
            asyncio.ensure_future(fetch_response(url, session))
            for url in urls
        ]
        courses_html = await asyncio.gather(*tasks)
    return courses_html


def parse_course_info(html):
    soup = BeautifulSoup(html, 'lxml')
    course_name = soup.find('h1', {'class': 'title'}).text
    start_date = soup.find('div', {'class': 'startdate'}).text
    language = soup.find('div', {'class': 'rc-Language'}).text

    if soup.find('div', {'class': 'rc-WeekView'}):
        length_course = soup.find('div', {'class': 'rc-WeekView'})
        length_course = str(len(length_course)) + ' week(s)'
    elif soup.find('i', {'class': 'cif-clock'}):
        length_course = soup.find('i', {'class': 'cif-clock'})
        length_course = length_course.parent.next_sibling.text
    else:
        length_course = None

    if soup.find('div', {'class': 'ratings-text'}):
        user_rating = soup.find('div', {'class': 'ratings-text'}).text
    else:
        user_rating = None

    return {
        'course_name': course_name,
        'start_date': start_date,
        'language': language,
        'length_course': length_course,
        'user_rating': user_rating
    }


def fill_xlsx(courses_info):
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.append([
        'Course name',
        'Start date',
        'Language',
        'Length of the course',
        'User rating'
    ])

    for course in courses_info:
        if not course['user_rating']:
            course['user_rating'] = 'Not yet rating'
        worksheet.append([
            course['course_name'],
            course['start_date'],
            course['language'],
            course['length_course'],
            course['user_rating']
        ])

    for column_cells in worksheet.columns:
        length = (max(len(str(cell.value)) for cell in column_cells))
        worksheet.column_dimensions[column_cells[0].column].width = length

    return workbook


def save_workbook(workbook, filename):
    try:
        workbook.save(filename)
    except OSError as error:
        return error


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    courses_html = loop.run_until_complete(fetch_courses_html())
    courses_info = [parse_course_info(html) for html in courses_html]
    workbook = fill_xlsx(courses_info)
    filepath = 'couesera.xlsx'
    error = save_workbook(workbook, filepath)
    if not error:
        print('File \'{}\' has been saved'.format(filepath))
    else:
        print(error)
    loop.close()
