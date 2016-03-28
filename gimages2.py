#taken from https://stackoverflow.com/questions/20716842/python-download-images-from-google-image-search
import urllib2
import simplejson
import cStringIO
from PIL import Image
from os import path as os_path

def _get4results(query_, start_idx_):
    # Note: I don't know why, but apparently this method will only return 4 results at a time
    fetcher = urllib2.build_opener()
#    search_url = "http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q="\
    search_url = "https://www.google.com/search?q=" + query_ + "&tbm=isch"
    f = fetcher.open(search_url)
    return simplejson.load(f)


def get_gimages(query, n=1, saveloc="C:\\Users\\Andy\\Desktop\\gimages\\",
                showimages=False):
    query= query.split()
    query = '+'.join(query)

    for quad in range(n//4 + 1):
        start_idx = quad*4
        deserialized_output = _get4results(query, start_idx)
        for kof4 in range(4):
            image_number = kof4 + 4*quad
            if image_number > n:
                break
            imageUrl = deserialized_output['responseData']['results'][kof4]['unescapedUrl']
            file = cStringIO.StringIO(urllib2.urlopen(imageUrl).read())
            img = Image.open(file)
            if showimages:
                img.show()
            savename = query + str(image_number) + '.' + img.format
            savepath = os_path.join(saveloc, savename)
            img.save(savepath,img.format)

#test
get_gimages("test", 10)