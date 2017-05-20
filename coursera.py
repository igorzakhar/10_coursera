import random
import xml.etree.ElementTree as etree
from collections import namedtuple

import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook


CourseInfo = namedtuple('CourseInfo', ('course_name', 'start_date',
                                       'language', 'length_course',
                                       'user_rating'))

headers = {'User-Agent':
               'Mozilla/5.0 (X11; Linux x86_64)AppleWebKit/537.36 \
               (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
           'Accept':
               'text/html,application/xhtml+xml,application/xml;\
               q=0.9,image/webp,*/*;q=0.8'}

def get_courses_list():
    url = 'https://www.coursera.org/sitemap~www~courses.xml'
    response = requests.get(url, headers=headers)
    root = etree.fromstring(response.content)
    url_list = [child[0].text for child in root]
    random_urls = random.sample(url_list, 50)
    return random_urls


def parser_course_page(course_slug):
    length_course = None
    user_rating = None
    soup = BeautifulSoup(course_slug, 'lxml')
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


def get_courses_info(urls_list):
    course_info_list = []
    for url in  urls_list:
        try:
            response = requests.get(url, headers=headers)
        except requests.exceptions.HTTPError as err:
            print(err)
        else:
            course_info = parser_course_page(response.content)
            course_info_list.append(course_info)
    return course_info_list


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
    workbook.save(filepath)

if __name__ == '__main__':
    urls_list = get_courses_list()
    course_info_list = get_courses_info(urls_list)
    output_courses_info_to_xlsx(course_info_list, 'sample.xlsx')
    