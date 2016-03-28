from bs4 import BeautifulSoup
import re
import urllib2
import os
import time


def get_soup(url,header):
  return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),
                       "lxml")


def get_gimages(query, saveloc=None, showimages=False):
    filename_base = query
    if saveloc is not None:
        directory = os.path.join(saveloc, query)
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except WindowsError:
                t = str(time.time()).replace('.','')
                local_dir_name = "search_" + t
                filename_base = local_dir_name
                print "\n Warning: query no good for use as windows "\
                    "directory name.  Images from query " + query + "will be "\
                    "saved in:\n"
                directory = os.path.join(saveloc, local_dir_name)
                os.makedirs(directory)
                print directory
    else:
        directory = os.getcwd()

    # you can change the query for the image  here
    query= query.split()
    query='+'.join(query)
    url="https://www.google.com/search?q=" + query + "&tbm=isch"

    #print url
    header = {'User-Agent': 'Mozilla/5.0'}
    soup = get_soup(url,header)

    images = [a['src'] for a in soup.find_all("img",
              {"src": re.compile("gstatic.com")})]
    #print images
    for k, img in enumerate(images):
        img_num = k + 1
        raw_img = urllib2.urlopen(img).read()
        #add the directory for your image here

        print img_num,
        filename = filename_base + "_" + str(img_num) + '.jpg'
        f = open(os.path.join(directory, filename), 'wb')
        f.write(raw_img)
        f.close()


#test
test_queries = ["amazing",
                "cool",
                "super crazy awesome photo",
                "42?"]
save_location = "C:\\Users\\Andy\\Desktop\\gimages\\"
attempts = 5
pausetime = 5
for q in test_queries:
    print '\n' + q + ":"
    for attempt in range(1,attempts):
        try:
            get_gimages(q, saveloc=save_location)
            break
        except urllib2.URLError:
            print "Attempt %s / %s failed." % (attempt, attempts)
            if attempt >= attempts:
                print "Moving on."
                break
            print "Retrying in %s seconds..." % pausetime
            time.sleep(pausetime)


    time.sleep(5)  # seems to prevent a time-out when

