import requests
from bs4 import BeautifulSoup
import sys

def main(args):
    context = None
    counter = 0
    boards = ['g']
    #try:
    #    context = get_context(args[1])
    #except Exception as e:
    #    print("Error: unable to get context, exiting.")
    #    sys.exit(1)
    for board in boards:
        nums = gen_thread_numbers(board)
        threads = gen_thread(board, nums)
        for thread in threads:
            print thread
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

def gen_thread(board,numbers):
    #board , thread number
    for num in numbers:
        url = "https://api.4chan.org/%s/res/%d.json" % (board, num)
        r = requests.get(url)
        yield r.content
    
def gen_thread_numbers(board, page=0):
    '''generates thread numbers from the 4chan boards. An optional page
    argument is provided to access non frontpage material.'''
    url = "http://boards.4chan.org/%s/%d" % (board,page)
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    threads = soup.find_all(class_="thread")
    
    for thread in threads:
        yield int(str(thread['id'])[1:])
        
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

if __name__=="__main__": main(sys.argv[1:])