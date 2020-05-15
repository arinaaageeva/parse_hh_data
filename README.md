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

    name : str - название резюме
    description : str - дополнительная информация, описание навыков в свободной форме (может содержать html-код)
    key_skills : list - список ключевых навыков
            name : str - название ключевого навыка
    experiences : list - опыт работы
            start : str - начало работы (дата в формате dd-MM-yyyy)
            end : str - окончание работы (дата в формате dd-MM-yyyy)
            position : str - должность
            description : str - обязанности, функции, достижения (может содержать html-код)

с помощью `parse_hh_data.parse.resume`.

Скачать списки идентификаторов вакансий или резюме можно используя 
`parse_hh_data.download.vacancy_ids` или `parse_hh_data.download.resume_ids`, соответсвенно.

### Command line interface

`download_data resumes ~/data/resumes 13-04-2020 specializations.json`

`parse_resumes ~/data/resumes ~/data/resumes_json 13-04-2020 specializations.json`