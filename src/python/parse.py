import os
import sys
import json
import argparse

from tqdm import tqdm
from bs4 import BeautifulSoup
from parse_utils import parse_resume

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("path_html")
    parser.add_argument("path_json")
    parser.add_argument("directory")

    args = parser.parse_args()

    for file in tqdm(os.listdir(os.path.join(args.path_html, args.directory)), file=sys.stdout):
        with open(os.path.join(args.path_html, args.directory, file)) as fl:
            page = BeautifulSoup(fl.read(), 'html.parser')

        file = f"{file[:-5]}.json"
        with open(os.path.join(args.path_json, args.directory, file), "w") as fl:
            json.dump(parse_resume(page), fl)
