import os

from os import path
from wordcloud import WordCloud

import transcript

class WordCloudHelper(object):
    def __init__(self, series='Xfm_Series_1'):
        self.series = series
        self.text = None
  
    def _get_all_text(self):
        if self.text:
            return self.text
        links = transcript.getLinksForTranscripts(self.series)
        transcripts = [transcript.Transcript(link) for link in links]
        self.text = ''
        for tp in transcripts:
            self.text += " ".join([line.text for line in tp.getAllLines()])
        return self.text

    def show(self):
        text = self._get_all_text()
        wordcloud = WordCloud(max_font_size=200, width=1200, height=600).generate(text)
        image = wordcloud.to_image()
        image.show()

WordCloudHelper('Xfm_Series_2').show()