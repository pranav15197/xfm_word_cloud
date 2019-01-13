import collections
from bs4 import BeautifulSoup
import requests
import json

Line = collections.namedtuple('Line', ['speaker', 'text'])
BASE_URL = "http://www.pilkipedia.co.uk"

def getLinksForTranscripts(series='Xfm_Series_1'):
    url = "{base}/wiki/index.php?title={series}".format(base=BASE_URL,series=series)
    soup = BeautifulSoup(requests.get(url).content)
    rows = soup.find('table').find_all('tr')
    links = []
    index = 1
    while index < len(rows): # wierd structure of the table on the page forced me to write this shit code
        row = rows[index]
        links.append("{base}{href}/Transcript".format(base=BASE_URL, href=row.find_all('a')[1]['href']))
        index += 3
    return links

class Transcript(object):
    def __init__(self, url):
        self.url = url
        self.lines = self._fetch_lines()
    
    def _create_line_from_p(self, p):
        childs = list(p.children)
        speaker = childs[0].text.replace(':', '')
        text = childs[1].replace('\n', '')
        print Line(speaker, text)
        return Line(speaker, text)

    def _fetch_lines(self):
        soup = BeautifulSoup(requests.get(self.url).content)
        paras = soup.find_all('p')
        # Checking for 2 childs in the para covers 99% of all lines in the transcript
        return [self._create_line_from_p(p) for p in paras if len(list(p.children)) is 2]
    
    def getAllLines(self):
        return self.lines

if __name__ == '__main__':
    # fetch lines from all 4 series
    links = []
    for i in range(1,5):
        links += getLinksForTranscripts('Xfm_Series_' + str(i))
    tps = [Transcript(link) for link in links ]
    lines = []
    for tp in tps:lines += tp.getAllLines()
    data = {i:{"speaker": line.speaker, "text": line.text} for i,line in enumerate(lines)}
    with open('data.json', 'w+') as f:
        json.dump(data, f) 