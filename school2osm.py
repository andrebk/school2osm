#!/usr/bin/env python3
# -*- coding: utf8

# school2osm
# Converts schools from Kunnskapsdirektoratet api feed to osm format for import/update
# Usage: python school2osm.py [output_filename.osm]
# Default output filename: "skoler.osm"


import errno
import html
import sys
import time
import urllib.error
import urllib.request
import requests
import argparse
import logging
from model import NsrEnhetTinyApiModel, NsrEnhetTinyApiModelApiPageResult, NsrEnhetApiModel
from tqdm import tqdm
from pathlib import Path
from osm import Data, Node
from school import create_school_node

version = "1.1.0"


logger = logging.getLogger(__name__)


def try_urlopen(url):
    """Open file/api, try up to 5 times, each time with double sleep time"""
    tries = 0
    while tries < 5:
        try:
            return urllib.request.urlopen(url)

        except OSError as e:  # Mostly "Connection reset by peer"
            if e.errno == errno.ECONNRESET:
                tries += 1
                sleep_time = 5 * (2**tries)
                print(f"    Retry {tries} in {sleep_time} seconds...\n")
                time.sleep(sleep_time)

    print(f"Error: {e.reason}")
    print(f"{url.get_full_url()}")
    sys.exit()


def get_data(api_path: str, use_cache: bool = True):
    """
    Get data from an API endpoint.
    Optionally write it to cache and use that cached file instead.
    """

    api_base = "https://data-nsr.udir.no/v3/"
    cache_dir = "cache/"

    cache_file = Path(cache_dir + api_path + ".json")
    data = None
    if use_cache and cache_file.exists():
        with cache_file.open("r") as file:
            data = file.read()
            logger.debug(f"Loaded data from cache for {api_path}")
    else:
        response = requests.get(api_base + api_path)
        response.raise_for_status()  # TODO: Retry on failure
        data = response.text
        logger.debug(f"Downloaded data from API for {api_path}")
        if use_cache:
            cache_file.parent.mkdir(parents=True, exist_ok=True)
            with cache_file.open("w") as file:
                file.write(response.text)
                logger.debug(f"Saved data to cache for {api_path}")

    if not data:
        raise IOError(f"No data found for {api_path}")

    return data


def get_all_units() -> NsrEnhetTinyApiModelApiPageResult:
    """Load basic information of all schools"""

    data = get_data("enheter?sidenummer=1&antallPerSide=30000")
    school_data = NsrEnhetTinyApiModelApiPageResult.model_validate_json(data)

    # TODO: Handle pagination
    if school_data.num_pages > 1:
        print("*** Note: There are more data from API than loaded")

    return school_data


def get_unit_details(school: NsrEnhetTinyApiModel) -> NsrEnhetApiModel:
    """Load school details"""

    data = get_data(f"enhet/{school.org_num}")
    return NsrEnhetApiModel.model_validate_json(data)


def main(filename: str = 'skoler.osm'):
    """Main program"""

    print("Loading data ...")

    # Load earlier ref from old API (legacy ref)
    '''
    old_refs = {}

    url = "https://data-nsr.udir.no/enheter"
    file = urllib.request.urlopen(url)
    school_data = json.load(file)
    file.close()

    for school in school_data:
        if school['NSRId'] and school['OrgNr']:
            if school['OrgNr'] in old_refs:
                message("%s %s already exists\n" % (school['OrgNr'], school['Navn']))
            else:
                old_refs[ school['OrgNr'] ] = school['NSRId']
    '''

    nsr_data = get_all_units()
    schools = [unit for unit in nsr_data.units if unit.is_relevant_school]

    print(f" {len(nsr_data.units)} NSR objects")
    print(f" {len(schools)} schools")
    print(f"Converting to file '{filename}' ...")

    osm_data = Data(generator=f"school2osm v{version}")

    # Iterate all schools and produce OSM file
    for school_entry in tqdm(schools):
        # Load school details
        school = get_unit_details(school_entry)

        node = create_school_node(school)

        # Done with OSM node
        osm_data.nodes.append(node)

    # Produce OSM file footer
    with open(filename, "w") as file:
        osm_data.xml(file)

    print(f"{len(schools)} schools written to file")
    print(f"{sum('GEOCODE' in node.tags for node in osm_data.nodes)} schools need geocoding")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="school2osm",
                                     description="Extracts schools from the Norwegian National School Register (NSR)")
    parser.add_argument("filename", nargs="?", default="skoler.osm", help="Name of output file (default: skoler.osm)")
    args = parser.parse_args()

    start = time.perf_counter()
    main(args.filename)
    stop = time.perf_counter()
    print(f"Elapsed time: {stop - start:.4f}")
