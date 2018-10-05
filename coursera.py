import argparse
import asyncio
import os
import random
import xml.etree.ElementTree as etree

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from openpyxl import Workbook


def process_args():
    parser = argparse.ArgumentParser(
        description="Get courses info from Coursera"
    )
    parser.add_argument(
        '-n',
        type=int,
        dest='num',
        default=20,
        help='Number of links'
    )
    parser.add_argument(
        '-a',
        '--all',
        action='store_true',
        help='Get all links from xml feed'
    )
    parser.add_argument(
        '-p',
        '--path',
        type=str,
        default='coursera.xlsx',
        help='Set a path for saving file'
    )
    return parser.parse_args()


async def fetch_response(url, session):
    async with session.get(url) as response:
        return await response.text(encoding='utf-8')


async def fetch_xml(session):
    xml_feed = 'https://www.coursera.org/sitemap~www~courses.xml'
    body = await fetch_response(xml_feed, session)
    return body


def get_random_urls(body, number_links):
    root = etree.fromstring(body)
    url_list = [child[0].text for child in root]
    if number_links:
        url_list = random.sample(url_list, number_links)
    return url_list


async def fetch_courses_html(urls, session):
    tasks = [
        fetch_response(url, session)
        for url in urls
    ]
    courses_html = await asyncio.gather(*tasks)
    return courses_html


async def get_courses_pages(loop, number_links):
    async with ClientSession(loop=loop) as session:
        body = await fetch_xml(session)
        urls = get_random_urls(body, number_links)
        courses_html = await fetch_courses_html(urls, session)
    return courses_html


def parse_course_info(html):
    soup = BeautifulSoup(html, 'lxml')
    course_name = soup.find('h1', {'class': 'title'}).text
    start_date = soup.find('div', {'class': 'startdate'}).text
    language = soup.find('div', {'class': 'rc-Language'}).text

    duration_course = soup.findAll('div', {'class': 'week'})
    if duration_course:
        duration_course = str(len(duration_course)) + ' week(s)'
    else:
        duration_course = None

    user_rating = soup.find('div', {'class': 'ratings-text'})
    if user_rating:
        user_rating = user_rating.text
    else:
        user_rating = None

    return {
        'course_name': course_name,
        'start_date': start_date,
        'language': language,
        'duration_course': duration_course,
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
            course['duration_course'],
            course['user_rating']
        ])

    for column_cells in worksheet.columns:
        length = (max(len(str(cell.value)) for cell in column_cells))
        worksheet.column_dimensions[column_cells[0].column].width = length

    return workbook


def save_workbook(workbook, filename):
    path_to_save = os.path.abspath(filename)
    try:
        workbook.save(path_to_save)
    except OSError as error:
        return error


if __name__ == '__main__':
    args = process_args()
    if args.all:
        args.num = 0
    loop = asyncio.get_event_loop()
    courses_html = loop.run_until_complete(
        get_courses_pages(loop, args.num)
    )
    courses_info = [parse_course_info(html) for html in courses_html]
    workbook = fill_xlsx(courses_info)
    error = save_workbook(workbook, args.path)
    if not error:
        print('File \'{}\' has been saved'.format(args.path))
    else:
        print(error)
    loop.close()
