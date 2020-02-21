import os
import sys
import json
import argparse

from tqdm import tqdm
from itertools import chain
from requests.exceptions import HTTPError
from download_utils import download_resume_ids, download_resume

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("path_resumes")
    parser.add_argument("directory_batch")
    parser.add_argument("path_specializations")
    parser.add_argument("--area_id", type=int, default=113)
    parser.add_argument("--search_period", type=int, default=1)
    parser.add_argument("--num_pages", type=int, default=None)
    parser.add_argument("--requests_interval", type=int, default=10)
    parser.add_argument("--max_requests_number", type=int, default=100)

    args = parser.parse_args()

    try:
        with open(os.path.join(args.path_resumes, "queue.json")) as fl:
            queue = json.load(fl)
        queue = queue["ids"]

    except FileNotFoundError as file_error:
        print(f"File not found error occurred: {file_error}", file=sys.stderr)

        with open(os.path.join(args.path_specializations, "specializations.json")) as fl:
            specialization_ids = json.load(fl)

        specialization_ids = [pofarea["specializations"] for pofarea in specialization_ids]
        specialization_ids = [specialization["id"] for specialization in chain(*specialization_ids)]

        queue = download_resume_ids(args.area_id, specialization_ids, args.search_period, args.num_pages,
                                    args.requests_interval, args.max_requests_number)

        with open(os.path.join(args.path_resumes, "queue.json"), "w") as fl:
            json.dump({"ids": queue}, fl)

    download_hashes = [files for _, _, files in os.walk(args.path_resumes)]
    download_hashes = [file[:-5] for file in chain(*download_hashes)]

    queue = set(queue) - set(download_hashes)
    for resume_id in tqdm(queue, file=sys.stdout):
        try:
            resume = download_resume(resume_id, args.requests_interval, args.max_requests_number)
        except HTTPError as http_error:
            print(f"HTTP error occurred: {http_error}", file=sys.stderr)
        else:
            with open(os.path.join(args.path_resumes, args.directory_batch, f"{resume_id}.html"), "w") as fl:
                fl.write(str(resume))

    os.remove(os.path.join(args.path_resumes, "queue.json"))
