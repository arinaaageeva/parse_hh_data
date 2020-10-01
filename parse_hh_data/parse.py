from datetime import datetime

MONTHS = {"Январь": "January",
          "Февраль": "February",
          "Март": "March",
          "Апрель": "April",
          "Май": "May",
          "Июнь": "June",
          "Июль": "July",
          "Август": "August",
          "Сентябрь": "September",
          "Октябрь": "October",
          "Ноябрь": "November",
          "Декабрь": "December"}


def num_pages(page):
    """
    :param bs4.BeautifulSoup page: resumes search page
    :return: int
    """
    num = page.find("div", {"data-qa": "pager-block"})

    if not num:
        return 1

    num = num.findAll("a", {"class": "bloko-button"})

    if not num:
        return 1

    return int(num[-2].getText())


def resume_hashes(page):
    """
    :param bs4.BeautifulSoup page: resumes search page
    :return: list
    """
    hashes = []
    page = page.find("div", {"data-qa": "resume-serp__results-search"})

    if page is not None:
        hashes = page.findAll("div", {"data-qa": "resume-serp__resume"})
        hashes = [item.find("a")["href"][8:46] for item in hashes]

    return hashes


def header(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: bs4.Tag
    """
    return page.find("div", {"class": "resume-header-block"})


def header_gender(header_page):
    """
    :param bs4.Tag position_block: position block
    :return: str
    """
    gender = header_page.find("span", {"data-qa": "resume-personal-gender"})

    if gender is not None:
        gender = gender.getText()

    return gender


def header_birthday(header_page):
    """
    :param bs4.Tag position_block: position block
    :return: str
    """
    birthday = header_page.find("span", {"data-qa": "resume-personal-birthday"})

    if birthday is not None:
        birthday = birthday.getText()

    return birthday


def header_address(header_page):
    """
    :param bs4.Tag position_block: position block
    :return: str
    """
    address = header_page.find("span", {"data-qa": "resume-personal-address"})

    if address is not None:
        address = address.getText()

    return address


def position(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: bs4.Tag
    """
    return page.find("div", {"class": "resume-block", "data-qa": "resume-block-position"})


def position_name(position_block):
    """
    :param bs4.Tag position_block: position block
    :return: str
    """
    name = position_block.find("span", {"class": "resume-block__title-text",
                                        "data-qa": "resume-block-title-position"})

    return name.getText()


def position_salary(position_block):
    """
    :param bs4.Tag position_block: position block
    :return: str
    """
    salary = position_block.find("span", {"class": "resume-block__salary resume-block__title-text_salary",
                                          "data-qa": "resume-block-salary"})

    if salary is not None:
        salary = salary.getText()

    return salary


def position_specializations(position_block):
    """
    :param bs4.Tag position_block: position block
    :return: list
    """
    position_block = position_block.find("div", {"class": "bloko-gap bloko-gap_bottom"})

    profarea_name = position_block.find("span", {"data-qa": "resume-block-specialization-category"})
    profarea_name = profarea_name.getText()

    profarea_specializations = position_block.find("ul")
    profarea_specializations = profarea_specializations.findAll("li", {"class": "resume-block__specialization",
                                                                       "data-qa": "resume-block-position-specialization"})

    profarea_specializations = [item.getText() for item in profarea_specializations]
    profarea_specializations = [{"name": specialization_name, "profarea_name": profarea_name}
                                for specialization_name in profarea_specializations]

    return profarea_specializations


def description(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: str
    """
    page_description = page.find("div", {"data-qa": "resume-block-skills-content"})

    if page_description is None:
        page_description = ""
    else:
        description_child = page_description.findChild()
        page_description = page_description.getText() if description_child is None else str(description_child)

    return page_description


def key_skills(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: list
    """
    page_key_skills = page.find("div", {"data-qa": "skills-table", "class": "resume-block"})

    if page_key_skills is None:
        page_key_skills = []
    else:
        page_key_skills = page_key_skills.findAll("div", {"class": "bloko-tag bloko-tag_inline bloko-tag_countable",
                                                  "data-qa": "bloko-tag bloko-tag_inline"})
        page_key_skills = [{"name": key_skill.getText()} for key_skill in page_key_skills]

    return page_key_skills


def date(date, format="%d-%m-%Y"):
    """
    :param date str: date in format "Month (russian) Year"
    :param format str: desired data format
    :return: str
    """
    if date in ["по настоящее время", "currently"]:
        return None

    month, year = date.split()

    if month in MONTHS:
        month = MONTHS[month]

    date = f"{month} {year}"
    date = datetime.strptime(date, "%B %Y").strftime(format)

    return date


def experiences(page, format="%d-%m-%Y"):
    """
    :param bs4.BeautifulSoup page: resume page
    :param format str: desired data format
    :return: list
    """
    page_experiences = []
    page = page.find("div", {"class": "resume-block", "data-qa": "resume-block-experience"})

    if page is not None:
        page = page.find("div", {"class": "resume-block-item-gap"})
        for experience_item in page.findAll("div", {"class": "resume-block-item-gap"}):
            time_interval = experience_item.find("div", {"class": "bloko-column bloko-column_xs-4 bloko-column_s-2 bloko-column_m-2 bloko-column_l-2"})
            time_interval.div.extract()

            start, end = time_interval.getText().replace("\xa0", " ").split(' — ')
            
            item_position = experience_item.find("div",  {"class": "resume-block__sub-title", "data-qa": "resume-block-experience-position"})
            item_position = "" if item_position is None else item_position.getText()

            item_description = experience_item.find("div", {"data-qa": "resume-block-experience-description"})
            description_child = item_description.findChild()
            item_description = item_description.getText() if description_child is None else str(description_child)

            page_experiences.append(
                {"start": date(start, format=format),
                 "end": date(end, format=format),
                 "position": item_position,
                 "description": item_description}
            )

    return page_experiences


def resume(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: dict
    """
    page = page.find("div", {"id": "HH-React-Root"})
    resume_header = header(page)
    resume_position = position(page)

    return {
        "gender": header_gender(resume_header),
        "birthday": header_birthday(resume_header),
        "address": header_address(resume_header),
        "name": position_name(resume_position),
        "salary": position_salary(resume_position),
        "specializations":  position_specializations(resume_position),
        "description": description(page),
        "key_skills": key_skills(page),
        "experiences": experiences(page)
    }

    return resume
