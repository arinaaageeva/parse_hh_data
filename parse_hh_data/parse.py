def parse_num_pages(page):
    """
    :param bs4.BeautifulSoup page: resumes search page
    :return: int
    """
    num_pages = page.findAll("a", {"class": "bloko-button HH-Pager-Control"})
    num_pages = int(num_pages[-1].getText()) if num_pages else 1

    return num_pages


def parse_resume_hashes(page):
    """
    :param bs4.BeautifulSoup page: resumes search page
    :return: list
    """
    hashes = []
    page = page.find("div", {"data-qa": "resume-serp__results-search"})

    if page is not None:
        hashes = page.findAll("div", {"data-qa": "resume-serp__resume"})
        hashes = [item["data-hh-resume-hash"] for item in hashes]

    return hashes


def parse_position(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: bs4.Tag
    """
    return page.find("div", {"class": "resume-block", "data-qa": "resume-block-position"})


def parse_name(position):
    """
    :param bs4.Tag position: position block
    :return: str
    """
    name = position.find("span", {"class": "resume-block__title-text",
                                  "data-qa": "resume-block-title-position"})
    name = name.getText()

    return name


def parse_specializations(position, specializations):
    """
    :param bs4.Tag position: position block
    :param dict specializations: specializations from https://api.hh.ru/specializations
    :return: list
    """
    specializations = {profarea["name"]: (profarea["id"], profarea["specializations"]) for profarea in specializations}

    position = position.find("div", {"class": "bloko-gap bloko-gap_bottom"})

    profarea_name = position.find("span", {"data-qa": "resume-block-specialization-category"})
    profarea_name = profarea_name.getText()

    profarea_specializations = position.find("ul")
    profarea_specializations = profarea_specializations.findAll("li", {"class": "resume-block__specialization",
                                                                       "data-qa": "resume-block-position-specialization"})
    profarea_specializations = [item.getText() for item in profarea_specializations]

    profarea_id, specializations = specializations[profarea_name]

    specializations = {item["name"]: item["id"] for item in specializations}

    profarea_specializations = [{"id": specializations[specialization_name], "name": specialization_name,
                                 "profarea_id": profarea_id, "profarea_name": profarea_name}
                                for specialization_name in profarea_specializations]

    return profarea_specializations


def parse_description(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: str
    """
    description = page.find("div", {"data-qa": "resume-block-skills-content"})

    if description is None:
        description = ""
    else:
        description_child = description.findChild()
        description = description.getText() if description_child is None else str(description_child)

    return description


def parse_key_skills(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: list
    """
    key_skills = page.find("div", {"data-qa": "skills-table", "class": "resume-block"})

    if key_skills is None:
        key_skills = []
    else:
        key_skills = key_skills.findAll("div", {"class": "bloko-tag bloko-tag_inline bloko-tag_countable",
                                                "data-qa": "bloko-tag bloko-tag_inline"})
        key_skills = [{"name": key_skill.getText()} for key_skill in key_skills]

    return key_skills


def parse_experiences(page):
    """
    :param bs4.BeautifulSoup page: resume page
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
            
            position = experience_item.find("div",  {"class": "resume-block__sub-title", "data-qa": "resume-block-experience-position"})
            position = "" if position is None else position.getText()

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


def parse_resume(page, specializations):
    """
    :param bs4.BeautifulSoup page: resume page
    :param dict specializations: specializations from https://api.hh.ru/specializations
    :return: dict
    """
    page = page.find("div", {"id": "HH-React-Root"})
    position = parse_position(page)

    resume = dict()
    resume["name"] = parse_name(position)
    resume["specializations"] = parse_specializations(position, specializations)
    resume["description"] = parse_description(page)
    resume["key_skills"] = parse_key_skills(page)
    resume["experiences"] = parse_experiences(page)

    return resume
