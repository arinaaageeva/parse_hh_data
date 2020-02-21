def parse_num_pages(page):
    """
    :param bs4.BeautifulSoup page: resumes search page from hh.ru
    :return: int
    """
    num_pages = page.findAll("a", {"class": "bloko-button HH-Pager-Control"})
    num_pages = int(num_pages[-1].getText()) if num_pages else 1

    return num_pages

def parse_resume_hashes(page):
    """
    :param bs4.BeautifulSoup page: resumes search page from hh.ru
    :return: list
    """
    hashes = page.find("div", {"data-qa": "resume-serp__results-search"})

    if hashes is None:
        return []

    hashes = hashes.findAll("div", {"data-qa": "resume-serp__resume"})
    hashes = [item["data-hh-resume-hash"] for item in hashes]

    return hashes
