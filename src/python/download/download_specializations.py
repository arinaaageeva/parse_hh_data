import os
import json
import argparse

from download_utils import download_specializations

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--requests_interval", type=int, default=10)
    parser.add_argument("--max_requests_number", type=int, default=100)
    args = parser.parse_args()

    specializations = download_specializations(args.requests_interval, args.max_requests_number)
    with open(os.path.join(args.path, "specializations.json"), "w") as fl:
        json.dump(specializations, fl)
