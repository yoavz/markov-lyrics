from markov import Markov
from os import listdir

def run(filename):
    with open ("data/" + filename, "r") as f:
        inpu = f.read()
    m = Markov(inpu)
    m.debug()

if __name__ == '__main__':
    files = [ f for f in listdir('data') ]
    print 'Pick a file: '
    for i in range(len(files)):
        print '(' + str(i) + '): ' + files[i]
    choice = input()
    if (choice not in range(len(files))):
        print 'Not a valid choice'
        exit(0)
    run(files[choice])
