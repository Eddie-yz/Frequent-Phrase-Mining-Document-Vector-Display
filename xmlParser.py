import xml.parsers.expat
import re

flag = False;

fr = open('dblp-2016-11-02.xml', 'r')
ffr = fr.read()
fw = open('title.txt', 'w')


# 3 handler functions
def start_element(name, attrs):
    if name.strip() == 'title':
        global flag
        flag = True


def end_element(name):
    if name.strip() == 'title':
        global flag
        flag = False


def char_data(data):
    global flag
    global fw
    if flag:
        title = repr(data)[1: -1].lower()
        title = re.sub(r"[^a-z0-9]+", " ", title)
        if title is not " ":
            fw.write(title.strip())
            fw.write('\n')


p = xml.parsers.expat.ParserCreate()

p.StartElementHandler = start_element
p.EndElementHandler = end_element
p.CharacterDataHandler = char_data

p.Parse(ffr)

fr.close()
fw.close()
print('Done!')