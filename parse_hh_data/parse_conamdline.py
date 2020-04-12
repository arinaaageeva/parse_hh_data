import os
import sys
import json
import argparse

from tqdm import tqdm
from bs4 import BeautifulSoup
from utils.parse import parse_resume

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("path_html")
    parser.add_argument("path_json")
    parser.add_argument("directory")
    parser.add_argument("path_specializations")

    args = parser.parse_args()

    with open(args.path_specializations) as fl:
        specializations = json.load(fl)

    for file in tqdm(os.listdir(os.path.join(args.path_html, args.directory)), file=sys.stdout):
        with open(os.path.join(args.path_html, args.directory, file)) as fl:
            page = BeautifulSoup(fl.read(), 'html.parser')

        try:
            page = parse_resume(page, specializations)
            with open(os.path.join(args.path_json, args.directory, f"{file[:-5]}.json"), "w") as fl:
                json.dump(page, fl)

        except KeyError as key_error:
            print(f"Key error occurred: {key_error}", file=sys.stderr)
            print(f"Delete file {file} from {os.path.join(args.path_html, args.directory)}")
            os.remove(os.path.join(args.path_html, args.directory, file))
