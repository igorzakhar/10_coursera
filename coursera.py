import random
import xml.etree.ElementTree as etree
from collections import namedtuple

import requests
from bs4 import BeautifulSoup


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


def get_course_info(course_slug):
    soup = BeautifulSoup(course_slug, 'lxml')
    length_course = None
    user_rating = None
    course_name = soup.find('h1', {'class': 'title'}).text
    start_date = soup.find('div', {'class': 'startdate'}).text
    language = soup.find('div', {'class':'rc-Language'}).text
    #length_course = soup.find('div', {'class':'rc-WeekView'})
    #user_rating = soup.find('div', {'class': 'ratings-text'})

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

    CourseInfo = namedtuple('CourseInfo', ('course_name', 'start_date',
                                           'language', 'length_course',
                                           'user_rating'))
    course_info = CourseInfo(course_name=course_name, start_date=start_date,
                             language=language, length_course=length_course,
                             user_rating=user_rating)
    print('-' * 20)
    print(course_name)
    print(start_date)
    print(language)
    print(length_course)
    print(user_rating)
    return course_info


def get_course(url):
    try:
        response = requests.get(url, headers=headers)
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        return get_course_info(response.content)
    #rating = re.search(r'[0-9.]+',soup.find('div', {'class': 'ratings-text'}).text)
    #rating.group()

def output_courses_info_to_xlsx(filepath):
    pass


if __name__ == '__main__':
    urls = get_courses_list()
    print(urls)
    for url in urls:
        course_info = get_course(url)
        print(course_info)
