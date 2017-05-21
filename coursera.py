import asyncio
import random
from collections import namedtuple
import xml.etree.ElementTree as etree

import tqdm
from bs4 import BeautifulSoup
from openpyxl import Workbook
from aiohttp import ClientSession


CourseInfo = namedtuple('CourseInfo', ('course_name', 'start_date',
                                       'language', 'length_course',
                                       'user_rating'))


async def get_response_data(url, session):
    async with session.get(url) as response:
        return await response.read()


async def get_courses_urls(session):
    url = 'https://www.coursera.org/sitemap~www~courses.xml'
    response = await get_response_data(url, session)
    response = response.decode('utf-8')
    root = etree.fromstring(response)
    url_list = [child[0].text for child in root]
    random_urls = random.sample(url_list, 20)
    return random_urls


async def get_course_pages():
    results = []
    async with ClientSession() as session:
        random_links = await get_courses_urls(session)
        tasks=[asyncio.ensure_future(
            get_response_data(url, session)) for url in random_links]
        to_do_iter = asyncio.as_completed(tasks)
        progress_meter_wrap = tqdm.tqdm(to_do_iter, total=len(random_links))
        for future in progress_meter_wrap:
            res = await future
            results.append(res.decode('utf-8'))
    return results


def parse_course_info(page):
    length_course = None
    user_rating = None
    soup = BeautifulSoup(page, 'lxml')
    course_name = soup.find('h1', {'class': 'title'}).text
    start_date = soup.find('div', {'class': 'startdate'}).text
    language = soup.find('div', {'class':'rc-Language'}).text

    if soup.find('div', {'class':'rc-WeekView'}):
        length_course = soup.find('div', {'class':'rc-WeekView'})
        length_course = str(len(length_course)) + ' week(s)'
    elif soup.find('i', {'class':'cif-clock'}):
        length_course = soup.find('i', {'class':'cif-clock'}).parent.next_sibling.text
    else:
        length_course = 'No data'

    if soup.find('div', {'class': 'ratings-text'}):
        user_rating = soup.find('div', {'class': 'ratings-text'}).text
    else:
        user_rating = 'No data'

    course_info = CourseInfo(course_name=course_name, start_date=start_date,
                             language=language, length_course=length_course,
                             user_rating=user_rating)
    return course_info


def get_courses_info(pages):
    courses_info = []
    for page in pages:
        course_info = parse_course_info(page)
        courses_info.append(course_info)
    return courses_info


def output_courses_info_to_xlsx(courses_info_list, filepath):
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.append(['Course name', 'Start date', 
                      'Language', 'Length of the course', 'User rating'])
    for course in courses_info_list:
        worksheet.append([course.course_name,
                          course.start_date,
                          course.language,
                          course.length_course,
                          course.user_rating])
    
    for column_cells in worksheet.columns:
        length = (max(len(str(cell.value)) for cell in column_cells))
        worksheet.column_dimensions[column_cells[0].column].width = length
        
    workbook.save(filepath)
    print('File \'{}\' has been saved'.format(filepath))


if __name__ == '__main__':

    loop=asyncio.get_event_loop()
    courses_page = loop.run_until_complete(get_course_pages())
    courses_info_list = get_courses_info(courses_page)
    output_courses_info_to_xlsx(courses_info_list, 'couesera.xlsx')
