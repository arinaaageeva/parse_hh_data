import sys
import time
import json
import requests

sys.path.append("src/python")

from tqdm import tqdm
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError, ConnectionError
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from parse.parse_utils import parse_num_pages, parse_resume_ids

SOFTWARE_NAMES = [SoftwareName.CHROME.value]
OPERATING_SYSTEMS = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
USER_AGENT = UserAgent(software_names=SOFTWARE_NAMES, operating_systems=OPERATING_SYSTEMS, limit=100)

RESUME_URL = "https://hh.ru/resume/{}"
VACANCY_URL = "https://api.hh.ru/vacancies/{}"
SPECIALIZATIONS_URL = "https://api.hh.ru/specializations"
RESUME_PAGE_URL = "https://hh.ru/search/resume?area={}&specialization={}&search_period={}&page={}"
VACANCY_PAGE_URL = "https://api.hh.ru/vacancies?area={}&specialization={}&period={}&page={}&per_page=100"


def repeat_request(url, requests_interval=10, max_requests_number=100, break_reasons=None):
    """
    :param str url: url for request
    :param int requests_interval: time interval between requests (sec.)
    :param int max_requests_number: maximum number of requests
    :param list break_reasons: list of reasons
    :return:str
    """
    if break_reasons is None:
        break_reasons = []
    break_reasons = set(break_reasons)

    for _ in range(max_requests_number):
        try:
            request = requests.get(url, headers={'User-Agent': USER_AGENT.get_random_user_agent()})
            request.raise_for_status()
        except ConnectionError as connection_error:
            print(f"Connection error occurred: {connection_error}", file=sys.stderr)
        except HTTPError as http_error:
            print(f"HTTP error occurred: {http_error}", file=sys.stderr)
            if request.reason in break_reasons:
                break
        else:
            return request.content

        print(f"A second request to the {url} will be sent in {requests_interval} seconds")
        time.sleep(requests_interval)

    raise HTTPError(f"Page on this {url} has not been downloaded")


def download_specializations(requests_interval=10, max_requests_number=100):
    """
    :param int requests_interval: time interval between requests (sec.)
    :param int max_requests_number: maximum number of requests
    :return: dict
    """
    url = SPECIALIZATIONS_URL
    page_content = repeat_request(url, requests_interval, max_requests_number)
    page_content = json.loads(page_content)

    return page_content


def download_resume_search_page(area_id, specialization_id, search_period, num_page,
                                requests_interval=10, max_requests_number=100):
    """
    :param str area_id: area identifier from https://api.hh.ru/areas
    :param str specialization_id: specialization identifier from https://api.hh.ru/specializations
    :param int search_period: the number of days for search,
                              available values: 0 - all period, 1 - day,
                              3 - three days, 7 - week, 30 - month, 365 - year,
                              all other values are equivalent 0
    :param int num_page: page number
    :param int requests_interval: time interval between requests (sec.)
    :param int max_requests_number: maximum number of requests
    :return: bs4.BeautifulSoup
    """
    url = RESUME_PAGE_URL.format(area_id, specialization_id, search_period, num_page)
    page_content = repeat_request(url, requests_interval, max_requests_number)
    page_content = BeautifulSoup(page_content, 'html.parser')

    return page_content


def download_vacancy_search_page(area_id, specialization_id, search_period, num_page,
                                 requests_interval=10, max_requests_number=100):
    """
    :param str area_id: area identifier from https://api.hh.ru/areas
    :param str specialization_id: specialization identifier from https://api.hh.ru/specializations
    :param int search_period: the number of days for search, max value 30
    :param int num_page: page number, max value 19
    :param int requests_interval: time interval between requests (sec.)
    :param int max_requests_number: maximum number of requests
    :return: dict
    """
    url = VACANCY_PAGE_URL.format(area_id, specialization_id, search_period, num_page)
    page_content = repeat_request(url, requests_interval, max_requests_number)
    page_content = json.loads(page_content)

    return page_content


def download_resume(identifier, requests_interval=10, max_requests_number=100, break_reasons={"Forbidden"}):
    """
    :param str identifier: resume identifier
    :param int requests_interval: time interval between requests (sec.)
    :param int max_requests_number: maximum number of requests
    :param list break_reasons: list of reasons
    :return: bs4.BeautifulSoup
    """
    url = RESUME_URL.format(identifier)
    page_content = repeat_request(url, requests_interval, max_requests_number, break_reasons)
    page_content = BeautifulSoup(page_content, 'html.parser')

    return page_content


def download_vacancy(identifier, requests_interval=10, max_requests_number=100):
    """
    :param str identifier: vacancy identifier
    :param int requests_interval: time interval between requests (sec.)
    :param int max_requests_number: maximum number of requests
    :return: dict
    """
    url = VACANCY_URL.format(identifier)
    page_content = repeat_request(url, requests_interval, max_requests_number)
    page_content = json.loads(page_content)

    return page_content


def download_specialization_resume_ids(area_id, specialization_id, search_period, num_pages,
                                       requests_interval=10, max_requests_number=100):
    """
    :param str area_id: area identifier from https://api.hh.ru/areas
    :param str specialization_id: specialization identifier from https://api.hh.ru/specializations
    :param int search_period: the number of days for search,
                              available values: 0 - all period, 1 - day,
                              3 - three days, 7 - week, 30 - month, 365 - year,
                              all other values are equivalent 0
    :param int num_pages: number of pages
    :param int requests_interval: time interval between requests (sec.)
    :param int max_requests_number: maximum number of requests
    :return: list
    """
    resume_ids = []

    try:
        page = download_resume_search_page(area_id, specialization_id, search_period, 0,
                                           requests_interval, max_requests_number)
        resume_ids.extend(parse_resume_ids(page))
        num_pages = parse_num_pages(page) if num_pages is None else min(num_pages, parse_num_pages(page))

        for num_page in tqdm(range(1, num_pages), file=sys.stdout):
            page = download_resume_search_page(area_id, specialization_id, search_period, num_page,
                                               requests_interval, max_requests_number)
            resume_ids.extend(parse_resume_ids(page))

    except HTTPError as http_error:
        print(f"HTTP error occurred: {http_error}", file=sys.stderr)

    return resume_ids


def download_resume_ids(area_id, specialization_ids, search_period, num_pages,
                        requests_interval=10, max_requests_number=100):
    """
    :param str area_id: area identifier from https://api.hh.ru/areas
    :param list specialization_ids: specialization identifiers from https://api.hh.ru/specializations
    :param int search_period: the number of days for search,
                              available values: 0 - all period, 1 - day,
                              3 - three days, 7 - week, 30 - month, 365 - year,
                              all other values are equivalent 0
    :param int num_pages: number of pages
    :param int requests_interval: time interval between requests (sec.)
    :param int max_requests_number: maximum number of requests
    :return: list
    """
    resume_ids = []

    for specialization_id in tqdm(specialization_ids, file=sys.stdout):
        resume_ids.extend(download_specialization_resume_ids(area_id, specialization_id, search_period, num_pages,
                                                             requests_interval, max_requests_number))

    resume_ids = list(set(resume_ids))

    return resume_ids


def download_specialization_vacancy_ids(area_id, specialization_id, search_period, num_pages,
                                        requests_interval=10, max_requests_number=100):
    """
    :param str area_id: area identifier from https://api.hh.ru/areas
    :param str specialization_id: specialization identifiers from https://api.hh.ru/specializations
    :param int search_period: the number of days for search, max value 30
    :param int num_pages: page number, max value 19
    :param int requests_interval: time interval between requests (sec.)
    :param int max_requests_number: maximum number of requests
    :return: list
    """
    vacancy_ids = []

    for num_page in tqdm(range(num_pages), file=sys.stdout):
        page = download_vacancy_search_page(area_id, specialization_id, search_period, num_page,
                                            requests_interval, max_requests_number)
        vacancy_ids.extend([vacancy["id"] for vacancy in page["items"]])

    return vacancy_ids


def download_vacancy_ids(area_id, specialization_ids, search_period, num_pages,
                         requests_interval=10, max_requests_number=100):
    """
    :param str area_id: area identifier from https://api.hh.ru/areas
    :param list specialization_ids: specialization identifiers from https://api.hh.ru/specializations
    :param int search_period: the number of days for search, max value 30
    :param int num_pages: page number, max value 19
    :param int requests_interval: time interval between requests (sec.)
    :param int max_requests_number: maximum number of requests
    :return: list
    """
    vacancy_ids = []

    for specialization_id in tqdm(specialization_ids, file=sys.stdout):
        vacancy_ids.extend(download_specialization_vacancy_ids(area_id, specialization_id, search_period, num_pages,
                                                               requests_interval, max_requests_number))

    vacancy_ids = list(set(vacancy_ids))

    return vacancy_ids

