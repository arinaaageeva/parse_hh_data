from functools import wraps
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


def get_optional_text(find_optional_element):
    @wraps(find_optional_element)
    def wrapper(page):
        """
        :param bs4.Tag element: element from resume
        :return: str or None
        """
        optional_element = find_optional_element(page)
        return None if optional_element is None else optional_element
    return wrapper

@get_optional_text
def birth_date(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: str or None
    """
    result = None
    
    if page != None and page.find("span", {"data-qa": "resume-personal-birthday"}) != None:
        result = page.find("span", {"data-qa": "resume-personal-birthday"}).getText()
    
    return result

@get_optional_text
def photo(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: str or None
    """
    photo = page.find("img", {"data-qa": "resume-photo-image"})
    
    return "" if photo is None else photo['src']

@get_optional_text
def personal_name(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: str or None
    """
    result = None
    
    if page != None and page.find("h2", {"data-qa": "resume-personal-name"}) != None:
        result = page.find("h2", {"data-qa": "resume-personal-name"}).getText()
    
    return result


@get_optional_text
def gender(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: str or None
    """
    return page.find("span", {"data-qa": "resume-personal-gender"}).getText()


@get_optional_text
def area(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: str or None
    """
    return page.find("span", {"data-qa": "resume-personal-address"}).getText()


@get_optional_text
def metro(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: str or None
    """
    result = None
    
    data = page.find("span", {"data-qa": "resume-personal-metro"})
    
    if data != None:
        result = data.getText()
    
    return result


@get_optional_text
def business_trip_agreeable(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: str or None
    """
    result = False
    
    span = page.find("span", {"data-qa": "resume-personal-metro"})
    
    if span != None and span.parent != None and span.parent.getText() != None:
        result = "готов к командировкам" in span.parent.getText()
        
    return result


@get_optional_text
def relocation_agreeable(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: str or None
    """
    result = False
    
    span = page.find("span", {"data-qa": "resume-personal-metro"})
    
    if span.parent != None and span.parent.getText() != None:
        result = "готов к переезду" in span.parent.getText()
        
    return result


def position(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: bs4.Tag
    """
    return page.find("div", {"class": "resume-block", "data-qa": "resume-block-position"})


def position_title(position_block):
    """
    :param bs4.Tag position_block: position block
    :return: str
    """
    title = position_block.find("span", {"class": "resume-block__title-text",
                                         "data-qa": "resume-block-title-position"})

    return title.getText()


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


def employment_type(position_block):
    """
    :param bs4.Tag position_block: position block
    :return: list
    """
    result = ""
    position_block = position_block.find("div", {"class": "resume-block-container"})
    
    for p in position_block.findAll("p"):
        if p != None and "Занятость" in p.getText():
            dirty_employment = p.getText()
            result = dirty_employment.split(":")[1]
            
            if isinstance(result, str):
                result = result.strip()
            
            break

    return result


def schedule(position_block):
    """
    :param bs4.Tag position_block: position block
    :return: list
    """
    result = ""
    position_block = position_block.find("div", {"class": "resume-block-container"})
    
    for p in position_block.findAll("p"):
        if p != None and "График работы" in p.getText():
            dirty_employment = p.getText()
            result = dirty_employment.split(":")[1]
            
            if isinstance(result, str):
                result = result.strip()
            
            break

    return result

def position_salary(position_block):
    """
    :param bs4.Tag position_block: position block
    :return: dict
    """
    salary = position_block.find("span", {"class": "resume-block__salary",
                                          "data-qa": "resume-block-salary"})
    amount = None
    currency = None
    if salary is not None:
        salary = salary.getText().replace('\u2009', '').replace('\xa0', ' ').strip().split()
        amount = int(salary[0])
        currency = ' '.join(salary[1:])

    salary = {"amount": amount,
              "currency": currency}

    return salary


def contact(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: bs4.Tag
    """
    return page.find("div", {"data-qa": "resume-block-contacts"})


def get_contacts(contacts):
    """
    :param bs4.Tag position_block: position block
    :return: list
    """
    result = []
    
    email_div = contacts.find("div", {"data-qa": "resume-contact-email"})
    
    if email_div != None and email_div.find() != None and email_div.find().next != None:
        email_address = email_div.find().next
        preferred = False if email_div.find("a",{"data-qa":"resume-contact-preferred"}) is None else True
        
        result.append({
            "value": str(email_address),
            "is_preferred": preferred,
            "is_verified": None,
            "type": "mail"
        })
        
    phone_div = contacts.find("div", {"data-qa": "resume-contacts-phone"})
    
    if phone_div != None and phone_div != None and phone_div.find("a") != None:
        phone_number = phone_div.find("a").getText()
        preferred = False if phone_div.find("a",{"data-qa":"resume-contact-preferred"}) is None else True
        
        verified_div = phone_div.find("div",{"class": "resume-search-item-phone-verification-status"})
        verified = False if verified_div.getText() != 'Телефон подтвержден' else True
        
        result.append({
            "value": phone_number,
            "is_preferred": preferred,
            "is_verified": verified,
            "type": "phone"
        })
        
    personalsite_div = contacts.find("div", {"data-qa": "resume-personalsite-personal"})
    
    if personalsite_div != None and personalsite_div.find("a") != None:
        personalsite_url = personalsite_div.find("a").getText()
        preferred = False if personalsite_div.find("a",{"data-qa":"resume-contact-preferred"}) is None else True
        
        result.append({
            "value": personalsite_url,
            "is_preferred": preferred,
            "is_verified": None,
            "type": "link"
        })
    
    return result


def education(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: bs4.Tag
    """
    return page.find("div", {"class": "resume-block", "data-qa": "resume-block-education"})


def additional_education(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: bs4.Tag
    """
    return page.find("div", {"class": "resume-block", "data-qa": "resume-block-additional-education"})


def attestation_education(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: bs4.Tag
    """
    return page.find("div", {"class": "resume-block", "data-qa": "resume-block-attestation-education"})


def education_level(education_block):
    """
    :param bs4.Tag education_block: education block
    :return: str
    """
    if education_block is not None:
        return education_block.find("span", {"class": "resume-block__title-text resume-block__title-text_sub"}) \
                              .getText()

    return "Образования нет"


def educations(education_block):
    """
    :param bs4.Tag education_block: education block
    :return: list
    """
    page_educations = []
    if education_block is not None:
        education_block = education_block.find("div", {"class": "resume-block-item-gap"}) \
                                         .find("div", {"class": "bloko-columns-row"})

        for education_item in education_block.findAll("div", {"class": "resume-block-item-gap"}):
            year = education_item.find("div", {"class": "bloko-column bloko-column_xs-4 bloko-column_s-2 bloko-column_m-2 bloko-column_l-2"}) \
                                 .getText()

            item_name = education_item.find("div", {"data-qa": "resume-block-education-name"}) \
                                      .getText()

            item_organization = education_item.find("div", {"data-qa": "resume-block-education-organization"})
            if item_organization is not None:
                item_organization = item_organization.getText()

            page_educations.append(
                {"year": int(year),
                 "name": item_name,
                 "organization": item_organization}
            )

    return page_educations


def driver_experience(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: bs4.Tag
    """
    return page.find("div", {"class": "resume-block", "data-qa": "resume-block-driver-experience"})


def has_vehicle(resume_driver_experience):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: bs4.Tag
    """
    result = None
    
    if resume_driver_experience != None:
        div = resume_driver_experience.find("div", {"class": "resume-block-item-gap"})
        result = div != None and div.getText() != None and "Имеется собственный автомобиль" in div.getText()
    
    return result



def driver_license(resume_driver_experience):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: bs4.Tag
    """
    result = None
    
    if resume_driver_experience != None:
        div = resume_driver_experience.find("div", {"class": "resume-block-item-gap"})

        if div != None and div.getText() != None:
            splited = div.getText().split("\xa0")
            if len(splited) == 2:
                result = splited[1]
        
    return result


def languages(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: list
    """
    page_languages = []
    page = page.find("div", {"class": "resume-block", "data-qa": "resume-block-languages"})

    if page is not None:
        for language in page.findAll("p", {"data-qa": "resume-block-language-item"}):
            language = language.getText().split(" — ")

            level = ' - '.join(language[1:])
            language = language[0]

            page_languages.append({"name": language,
                                   "level": level})

    return page_languages


def recommendations(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: list
    """
    page_recommendations = []
    page = page.find("div", {"class": "resume-block", "data-qa": "resume-block-recommendation"})

    if page is not None:
        for recomendation in page.findAll("div", {"data-qa": "recommendation-item-title"}):
            title = recomendation.getText()
            description = None
            
            if len(recomendation.parent.findAll("div")) == 2 and recomendation.parent.findAll("div")[1] != None:
                description = recomendation.parent.findAll("div")[1].getText()
            
            page_recommendations.append({"title": title, "description": description})

    return page_recommendations


def certificates(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: list
    """
    page_certificates = []
    page = page.find("div", {"class": "resume-block", "data-qa": "resume-block-certificate"})

    if page is not None:
        for certificate in page.findAll("a", {"class": "bloko-link"}):
            title = certificate.getText()
            url = certificate['href']
            year = None
            
            for parent in certificate.parents:
                year_div = parent.find("div",{"class": "resume-certificates-view__year-group-title"})
                
                if year_div != None:
                    year = year_div.getText()
                    break
    
            page_certificates.append({"title": title, "url": url, "year": year})

    return page_certificates

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
            
            item_position = experience_item.find("div",  {"class": "bloko-text bloko-text_strong", "data-qa": "resume-block-experience-position"})
            item_position = "" if item_position is None else item_position.getText()

            item_description = experience_item.find("div", {"data-qa": "resume-block-experience-description"})
            description_child = item_description.findChild()
            item_description = item_description.getText() if description_child is None else str(description_child)
            
            item_employer = experience_item.find("div",  {"class": "bloko-text bloko-text_strong"})
            item_employer_name = "" if item_employer is None else item_employer.getText()
            
            item_block_container = experience_item.find("div",  {"class": "resume-block-container"})
            
            item_employer_city = None
            item_employer_site = None

            if item_block_container != None and item_block_container.find("p") != None:
                item_block_container_text = item_block_container.find("p").getText()
                item_employer_city = item_block_container_text.split(",")[0]
                
                item_employer_a = item_block_container.find("p").find("a")
                
                if item_employer_a != None:
                    item_employer_site = item_employer_a['href']
            
            page_experiences.append(
                {"start": date(start, format=format),
                 "end": date(end, format=format),
                 "position": item_position,
                 "description": item_description,
                 "employer_name": item_employer_name,
                 "employer_city": item_employer_city,
                 "employer_site": item_employer_site
                 }
            )

    return page_experiences


def additional(page, format="%d-%m-%Y"):
    """
    :param bs4.BeautifulSoup page: resume page
    :param format str: desired data format
    :return: list
    """
    result = []
    page = page.find("div", {"class": "resume-block", "data-qa": "resume-block-additional"})

    if page is not None:
        div = page.find("div", {"class":"resume-block-item-gap"})
        
        if div is not None:
            for p in div.findAll("p"):
                result.append(p.getText())
            

    return result


def skill_set(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: list
    """
    page = page.find("div", {"data-qa": "skills-table", "class": "resume-block"})

    page_skill_set = []
    if page is not None:
        page_skill_set = page.findAll("div", {"class": "bloko-tag bloko-tag_inline bloko-tag_countable",
                                              "data-qa": "bloko-tag bloko-tag_inline"})
        page_skill_set = [skill.getText() for skill in page_skill_set]

    return page_skill_set


def skills(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: str
    """
    page = page.find("div", {"data-qa": "resume-block-skills-content"})

    page_skills = ""
    if page is not None:
        skills_child = page.findChild()
        page_skills = page.getText() if skills_child is None else str(skills_child)

    return page_skills


def resume(page):
    """
    :param bs4.BeautifulSoup page: resume page
    :return: dict
    """
    page = page.find("div", {"id": "HH-React-Root"})

    contacts = contact(page)
    resume_position = position(page)
    resume_education = education(page)
    resume_additional_education = additional_education(page)
    resume_attestation_education = attestation_education(page)
    resume_driver_experience = driver_experience(page)

    return {
        "personal_name": personal_name(page),
        "photo": photo(page),
        "birth_date": birth_date(page),
        "gender": gender(page),
        "area": area(page),
        "metro": metro(page),
        "business_trip_agreeable": business_trip_agreeable(page),
        "relocation_agreeable": business_trip_agreeable(page),
        "contacts": get_contacts(contacts),
        "title": position_title(resume_position),
        "specialization": position_specializations(resume_position),
        "employment_type": employment_type(resume_position),
        "schedule": schedule(resume_position),
        "salary": position_salary(resume_position),
        "education_level": education_level(resume_education),
        "education": educations(resume_education),
        "additional_education": educations(resume_additional_education),
        "attestation_education": educations(resume_attestation_education),
        "has_vehicle": has_vehicle(resume_driver_experience),
        "driver_license": driver_license(resume_driver_experience),
        "language": languages(page),
        "recommendations": recommendations(page),
        "certificates": certificates(page),
        "experience": experiences(page),
        "additional": additional(page),
        "skill_set": skill_set(page),
        "skills": skills(page)
    }