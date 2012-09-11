import requests
from bs4 import BeautifulSoup
import sys

def main(args):
    context = None
    counter = 0
    
    #try:
    #    context = get_context(args[1])
    #except Exception as e:
    #    print("Error: unable to get context, exiting.")
    #    sys.exit(1)
    
    get_threads("b")

    #for i in xrange(477000,478000):
    #    final_url = url_template % ("po",i)
    #    r = requests.get(final_url)
    #    if r.ok:
    #        print(r.content)
    #        counter += 1
    #    if i % 10 == 0:
    #        print(i)
    #    
    #print counter

    
def get_threads(board, page=None):
    board_home_template = "http://www.4chan.org"
    soup = BeautifulSoup('<head></head>')
    print soup
def get_context(input_location):
    '''gives the context of the database by providing metadata.
    Returns a dictionary of all the configurations needed to continue
    ingest of 4chan boards.'''
    
    context = {}
    #flat file implementation
    if os.path.isfile(input_location):
        with open(input_location) as f:
            for line in f:
                k,v = line.split("\t")
                context[k] = v
                
    return context

##### CONSTANTS ######
#helping me remember what all the abbrevs are for
board_map = {"g":"Technology",
             "sci":"Science & Math",
             "int":"International",
             "b":"random",
             }

# board, image number, extension
image_url_template = "images.4chan.org/%s/src/%d.%s" 

#board , thread number
url_template = "https://api.4chan.org/%s/res/%d.json"

if __name__=="__main__": main(sys.argv[1:])