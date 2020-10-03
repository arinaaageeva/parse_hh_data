# Parse HH Data Project

Данный модуль предназначен для удобного скачивания вакансий и резюме с сайта `hh.ru`

```python
from parse_hh_data import download, parse

vacancy = download.vacancy("36070814")

resume = download.resume("d40ce6f80001a8c8380039ed1f5874726f5a6e")
resume = parse.resume(resume)
```

**Вакансии** скачиваются с помощью [API HH](https://dev.hh.ru/) и возвращаются в формате описанном 
[здесь](https://github.com/hhru/api/blob/master/docs/vacancies.md#%D0%BF%D1%80%D0%BE%D1%81%D0%BC%D0%BE%D1%82%D1%80-%D0%B2%D0%B0%D0%BA%D0%B0%D0%BD%D1%81%D0%B8%D0%B8).

Обезличенные **резюме** скачиваются непосредственно с [сайта](https://hh.ru/search/resume) в html-формате, 
а затем могут быть преобразованны в json-формат:
    
    birth_date : str - день рождения
    gender : str - пол
    area : str - город проживания
    title : str - желаемая должность
    specialization : list - специализации соискателя
        name : str - название специализации
        profarea_name : str - название профессиональной области, в которую входит специализация
    salary : dict - желаемая зарплата
        amount : int - сумма
        currency : str - валюта
    education_level : str - уровень образования
    education : list - образование
        year : int - год окончания
        name : str - название учебного заведения
        organization : str - организация, специальность / специализация
    language : list - список языков, которыми владеет соискатель
        name : str - название языка
        level : str - уровень знания языка
    experience : list - опыт работы
        start : str - начало работы (дата в формате dd-MM-yyyy)
        end : str - окончание работы (дата в формате dd-MM-yyyy)
        position : str - должность
        description : str - обязанности, функции, достижения (может содержать html-код)
    skills : str - дополнительная информация, описание навыков в свободной форме (может содержать html-код)
    skill_set : list - ключевые навыки
            
с помощью `parse_hh_data.parse.resume`.

Скачать списки идентификаторов вакансий или резюме можно используя 
`parse_hh_data.download.vacancy_ids` или `parse_hh_data.download.resume_ids`, соответсвенно.

### Command line interface

`download ~/resumes resume --area_ids 113 --specialization_ids 1 --search_period 30`

`parse ~/data/resumes ~/data/resumes_json`