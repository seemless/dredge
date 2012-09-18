#!/usr/bin/python
import requests
from bs4 import BeautifulSoup
import json
import sys
import re
from collections import Counter

def main(args):
    context = None
    counter = 0
    boards = ['g']
    num_pages = 5
    keywords = {'lulsec':5,'lulzsec':5,'hack':1}
    threshold = 5

    for board in boards:
        
        thread_nums = gen_thread_numbers(board,num_pages)
        threads = gen_thread(board, thread_nums)
        tagged = gen_interesting(threads, keywords,threshold)
        json_threads = gen_json_threads(tagged, board)
        for j in json_threads:
            comments = ''
            for post in j['posts']:
                print(post)
                try:
                    comments += " "+post['com']
                except KeyError as e:
                    continue
            #replace all the quoting with nothing
            comment_text = BeautifulSoup(comments).text.replace(">",'')
            print (comment_text)

def gen_json_threads(tagged_threads, board):
    url_template = "http://api.4chan.org/%s/res/%d.json"
    for num in tagged_threads:
        url = url_template % (board, num)
        r = requests.get(url)
        yield json.loads(r.content)
        
def gen_interesting(threads, keywords, threshold):
    count = 0
    for num,thread in threads:
        words = re.findall('\w+', BeautifulSoup(thread).text)
        c = Counter(words)
        for key in keywords:
            #multiply by the "relevance" coefficient
            count += c[key]*keywords[key]
        if count >= threshold:
            yield num
             
        

def gen_thread(board,numbers):
    #board , thread number
    for num in numbers:
        url = "http://boards.4chan.org/%s/res/%d" % (board, num)
        r = requests.get(url)
        yield (num, r.content)
    
def gen_thread_numbers(board, num_pages):
    '''generates thread numbers from the 4chan boards. An optional page
    argument is provided to access non frontpage material.'''
    for page in xrange(num_pages):
    #summarized pages of threads
        url = "http://boards.4chan.org/%s/%d" % (board,page)
        r = requests.get(url)
        soup = BeautifulSoup(r.content)
        threads = soup.find_all(class_="thread")
    
        for thread in threads:
            yield int(str(thread['id'])[1:])
        
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