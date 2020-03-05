import os
import sys
import json
import argparse

from tqdm import tqdm
from itertools import chain
from requests.exceptions import HTTPError
from download_utils import specializations, download_vacancy_ids, download_resume_ids, vacancy, resume

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("data", choices=["vacancies", "resumes"])
    parser.add_argument("path")
    parser.add_argument("directory")
    parser.add_argument("path_specializations")
    parser.add_argument("--update_specializations", action='store_true')
    parser.add_argument("--area_id", type=int, default=113)
    parser.add_argument("--search_period", type=int, default=1)
    parser.add_argument("--num_pages", type=int, default=None)
    parser.add_argument("--timeout", type=int, default=10)
    parser.add_argument("--requests_interval", type=int, default=10)
    parser.add_argument("--max_requests_number", type=int, default=100)
    parser.add_argument("--break_reasons", nargs='+', default=["Forbidden", "Not Found"])

    args = parser.parse_args()

    download_params = {"timeout": args.timeout,
                       "requests_interval": args.requests_interval,
                       "max_requests_number": args.max_requests_number,
                       "break_reasons": args.break_reasons}

    # Download specializations

    if args.update_specializations:
        with open(args.path_specializations, "w") as fl:
            json.dump(specializations(**download_params), fl)

    try:
        with open(os.path.join(args.path, "queue.json")) as fl:
            queue = json.load(fl)["ids"]

    except FileNotFoundError:
        with open(args.path_specializations) as fl:
            specializations = json.load(fl)

        specializations = [pofarea["specializations"] for pofarea in specializations]
        specializations = [specialization["id"] for specialization in chain(*specializations)]

        if args.data == "vacancies":
            queue = download_vacancy_ids(args.area_id, specializations, args.search_period, args.num_pages, **download_params)
        if args.data == "resumes":
            queue = download_resume_ids(args.area_id, specializations, args.search_period, args.num_pages, **download_params)

        with open(os.path.join(args.path, "queue.json"), "w") as fl:
            json.dump({"ids": queue}, fl)

    downloaded_ids = [files for _, _, files in os.walk(args.path)]
    downloaded_ids = [file[:-5] for file in chain(*downloaded_ids)]

    queue = set(queue) - set(downloaded_ids)
    for item_id in tqdm(queue, file=sys.stdout):
        try:
            if args.data == "vacancies":
                item = vacancy(item_id, **download_params)
            if args.data == "resumes":
                item = resume(item_id, **download_params)

        except HTTPError as http_error:
            print(f"HTTP error occurred: {http_error}", file=sys.stderr)

        else:
            if args.data == "vacancies":
                item_id = f"{item_id}.json"
                item = json.dumps(item)
            if args.data == "resumes":
                item_id = f"{item_id}.html"
                item = str(item)

            with open(os.path.join(args.path, args.directory, item_id), "w") as fl:
                fl.write(item)

    os.remove(os.path.join(args.path, "queue.json"))
