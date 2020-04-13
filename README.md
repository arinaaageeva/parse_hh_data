# Parse HH Data Project

`from parse_hh_data import download, parse`

`resume = download.resume("d40ce6f80001a8c8380039ed1f5874726f5a6e")`

`resume = parse.resume(resume)`

`vacancy = download.vacancy("36070814")`

### Command line interface

`download_data resumes ~/data/resumes 13-04-2020 specializations.json`

`parse_resumes ~/data/resumes ~/data/resumes_json 13-04-2020 specializations.json`