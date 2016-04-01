from bs4 import BeautifulSoup
import re
import urllib2
import os
import time
from warnings import warn
import argparse


ATTEMPTS = 5  # In case of timeout, number of attempts to make
WAIT_TIME = 5  # Time (in seconds) to wait between retries


def get_user_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'search_term', 
        help='the search term (use quotes for multi-word searches)',
        metavar='SEARCH_TERMS'
        )
    parser.add_argument(
        '--out',
        dest='output_directory',
        default=os.getcwd(),
        help='the output directory (defaults to current working directory)',
        metavar='OUTPUT_DIRECTORY'
        )
    return parser.parse_args()


def get_gimages(query, out_dir):
    filename_base = query
    directory = os.path.join(out_dir, query)
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except:
        t = str(time.time()).replace('.','')
        local_dir_name = "search_" + t
        filename_base = ""
        directory = os.path.join(saveloc, local_dir_name)
        warn("\nWarning: query no good for use as windows directory "
             "name.  Images from query {} will be saved in:\n{}"
             "".format(query, directory))
        os.makedirs(directory)

    query= query.split()
    query='+'.join(query)
    url="https://www.google.com/search?q=" + query + "&tbm=isch"

    header = {'User-Agent': 'Mozilla/5.0'}
    soup = BeautifulSoup(urllib2.urlopen(urllib2.Request(url, headers=header)), "lxml")

    images = [a['src'] for a in soup.find_all("img",
              {"src": re.compile("gstatic.com")})]

    for k, img in enumerate(images):
        img_num = k + 1
        raw_img = urllib2.urlopen(img).read()

        filename = filename_base + "_" + str(img_num) + '.jpg'
        with open(os.path.join(directory, filename), 'wb') as f:
            f.write(raw_img)


if __name__ == '__main__':
    options = get_user_args()

    for attempt in range(1, ATTEMPTS):
        try:
            get_gimages(options.search_term, options.output_directory)
            break
        except urllib2.URLError:
            print "Attempt {} / {} failed.  ".format(attempt, ATTEMPTS),
            if attempt < ATTEMPTS:
                print "Retrying in {} seconds...".format(WAIT_TIME)
                time.sleep(WAIT_TIME)
