import os
import sys
import json
import argparse

from tqdm import tqdm
from itertools import chain
from requests.exceptions import HTTPError
from download_utils import download_specializations, download_resume_ids, download_vacancy_ids, download_vacancy, download_resume

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
    parser.add_argument("--requests_interval", type=int, default=10)
    parser.add_argument("--max_requests_number", type=int, default=100)

    args = parser.parse_args()

    # Download specializations

    if args.update_specializations:
        specializations = download_specializations(args.requests_interval, args.max_requests_number)
        with open(args.path_specializations, "w") as fl:
            json.dump(specializations, fl)

    # Initialize functions

    if args.data == "vacancies":
        download_ids = download_vacancy_ids
        download_item = download_vacancy
        create_name = lambda item_id: f"{item_id}.json"
        dump = lambda item: json.dumps(item)

    else:
        download_ids = download_resume_ids
        download_item = download_resume
        create_name = lambda item_id: f"{item_id}.html"
        dump = lambda item: str(item)

    # Read or create download queue

    try:
        with open(os.path.join(args.path, "queue.json")) as fl:
            queue = json.load(fl)["ids"]

    except FileNotFoundError:
        with open(args.path_specializations) as fl:
            specializations = json.load(fl)

        specializations = [pofarea["specializations"] for pofarea in specializations]
        specializations = [specialization["id"] for specialization in chain(*specializations)]

        queue = download_ids(args.area_id, specializations, args.search_period, args.num_pages,
                             args.requests_interval, args.max_requests_number)

        with open(os.path.join(args.path, "queue.json"), "w") as fl:
            json.dump({"ids": queue}, fl)

    downloaded_ids = [files for _, _, files in os.walk(args.path)]
    downloaded_ids = [file[:-5] for file in chain(*downloaded_ids)]

    queue = set(queue) - set(downloaded_ids)
    for item_id in tqdm(queue, file=sys.stdout):
        try:
            item = download_item(item_id, args.requests_interval, args.max_requests_number)
        except HTTPError as http_error:
            print(f"HTTP error occurred: {http_error}", file=sys.stderr)
        else:
            with open(os.path.join(args.path, args.directory, create_name(item_id)), "w") as fl:
                fl.write(dump(item))

    os.remove(os.path.join(args.path_resumes, "queue.json"))
