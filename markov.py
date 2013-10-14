import re
import random
from pprint import pprint

class Markov(object):

    def __init__(self, input_string):
        self.input_string = input_string
        self.words = dict()

    def process(self):

        # seperate into verses to find average verse length and amount of verses
        verses = [ l for l in self.input_string.split('\n\n') ]
        self.verse_count = len(verses)
        self.avg_verse_length = sum([ len(l.splitlines()) for l in verses ]) / len(verses)

        # seperate into lines 
        lines = [ l.strip() for l in self.input_string.splitlines() ]
        # filter out empty lines and lines that begin with [, e.g. [Verse], [Hook]
        lines = [ l for l in lines if not l.startswith('[') and l ]
        # line count and average line length for generation later
        self.line_count = len(lines)
        self.avg_line_length = sum([ len(line.split(' ')) for line in lines ]) / len(lines)

        # seperate words by whitespace
        word_list = [ word.lower() for line in lines for word in line.split(' ') ]
        # remove non alphanumeric characters and empty strings
        word_list = [re.sub(r'\W+', '', w) for w in word_list if w]

        return word_list

    def analyze(self):
        word_list = self.process()
        self.words = {w:{ 'prefix': [], 'suffix': [] }for w in word_list}
        
        # Populate the words dictionary with a list of words that come after it
        for i in range(len(word_list)-1):
            if (i < len(word_list)-2 ):
                self.words[word_list[i]]['suffix'].append(word_list[i+1])
            if (i > 0):
                self.words[word_list[i]]['prefix'].append(word_list[i-1])

    def manual_generate(self, line_length, line_count, verse_length):
        verse_count = line_count / verse_length
        out = '' 
        for i in range(verse_count):
            # Pick a random word as a starting seed for every verse
            seed = random.choice(self.words.keys())
            for j in range(verse_length):
                for k in range(line_length):
                    out += seed + ' ' 
                    if (self.words[seed]['suffix']):
                        choices = [ w['suffix'] for w in self.words.values() if seed in w['prefix'] ] 
                        choices = sum(choices, []) #flatten
                        seed = random.choice(choices)
                    else:
                        seed = random.choice(self.words.keys())
                out += '\n'
            out += '\n'
        return out

    def generate(self):
        return self.manual_generate(self.avg_line_length, self.line_count, self.avg_verse_length)
        
    def debug(self):
        self.analyze()
        print 'Input: \n'
        print self.input_string
        print '\n'
        print 'Words: \n'
        pprint(self.words)
        print '\n'
        print 'Generates: \n'
        print self.generate()
        print 'Stats: \n'
        print 'Verse Count: ' + str(self.verse_count)
        print 'Average Verse Length: ' + str(self.avg_verse_length)
        print 'Line Count: ' + str(self.line_count)
        print 'Average Line Length: ' + str(self.avg_line_length)
