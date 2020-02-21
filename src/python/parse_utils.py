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
    hashes = []
    page = page.find("div", {"data-qa": "resume-serp__results-search"})

    if page is not None:
        hashes = hashes.findAll("div", {"data-qa": "resume-serp__resume"})
        hashes = [item["data-hh-resume-hash"] for item in hashes]

    return hashes


def parse_position(page):
    """
    :param bs4.BeautifulSoup page: resume page from hh.ru
    :return: tuple(str or None, str or None, list)
    """
    title = None
    profarea = None
    specializations = []
    position = page.find("div", {"class": "resume-block", "data-qa": "resume-block-position"})

    if position is not None:
        title = position.find("span", {"class": "resume-block__title-text resume-block__title-text_position",
                                       "data-qa": "resume-block-title-position"})
        if title is not None:
            title = title.getText()

        profarea = position.find("span", {"data-qa": "resume-block-specialization-category"})
        if profarea is not None:
            profarea = profarea.getText()

        specializations = position.findAll("li", {"class": "resume-block__specialization",
                                                  "data-qa": "resume-block-position-specialization"})
        specializations = [specialization.getText() for specialization in specializations]

    return title, profarea, specializations


def parse_about_person(page):
    """
    :param bs4.BeautifulSoup page: resume page from hh.ru
    :return: str
    """
    about_person = page.find("div", {"data-qa": "resume-block-skills-content"})

    if about_person is not None:
        about_person_child = about_person.findChild()
        about_person = about_person.getText() if about_person_child is None else str(about_person_child)

    return about_person


def parse_key_skills(page):
    """
    :param bs4.BeautifulSoup page: resume page from hh.ru
    :return: list
    """
    key_skills = []
    page = page.find("div", {"data-qa": "skills-table"})

    if page is not None:
        key_skills = page.findAll("div", {"class": "bloko-tag bloko-tag_inline bloko-tag_countable"})
        key_skills = [key_skill.getText() for key_skill in key_skills]

    return key_skills


def parse_experiences(page):
    """
    :param bs4.BeautifulSoup page: resume page from hh.ru
    :return: list
    """
    experiences = []
    page = page.find("div", {"class": "resume-block", "data-qa": "resume-block-experience"})

    if page is not None:
        page = page.find("div", {"class": "resume-block-item-gap"})
        for experience_item in page.findAll("div", {"class": "resume-block-item-gap"}):
            time_interval = experience_item.find("div", {"class": "bloko-column bloko-column_xs-4 bloko-column_s-2 bloko-column_m-2 bloko-column_l-2"})

            time = time_interval.div.getText().replace("\xa0", " ")

            time_interval.div.extract()
            time_interval = time_interval.getText().replace("\xa0", " ")

            begin_time, end_time = time_interval.split(' — ')

            position = experience_item.find("div",  {"class": "resume-block__sub-title", "data-qa": "resume-block-experience-position"}) \
                                      .getText()

            description = experience_item.find("div", {"data-qa": "resume-block-experience-description"})
            description_child = description.findChild()
            description = description.getText() if description_child is None else str(description_child)

            experiences.append(
                {"time": time,
                 "begin_time": begin_time,
                 "end_time": end_time,
                 "position": position,
                 "description": description}
            )

    return experiences


def parse_resume(page):
    """
    :param bs4.BeautifulSoup page: resume page from hh.ru
    :return: dict
    """
    resume = {"title": None,
              "profarea": None,
              "specializations": [],
              "about_person": None,
              "key_skills": [],
              "experiences": []}

    page = page.find("div", {"id": "HH-React-Root"})

    if page is not None:
        title, profarea, specializations = parse_position(page)

        resume["title"] = title
        resume["profarea"] = profarea
        resume["specializations"] = specializations
        resume["about_person"] = parse_about_person(page)
        resume["key_skills"] = parse_key_skills(page)
        resume["experiences"] = parse_experiences(page)

    return resume





