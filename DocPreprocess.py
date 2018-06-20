import numpy as np
import os
import re


class docPrep(object):
    """
    A tool to preprocess the document.
    The input directory contains several docunments.
    The output is a text file
    """

    def __init__(self, inputDir_name, outputFile_name):
        self.dir_name = inputDir_name
        self.out_file = outputFile_name

    def process(self):
        """
        Read all the books in the specific author's directory 
        one by one and apply following steps on them:
        1. replace the '\n' to ' '
        2. segment the book by punctuation(,.?:!), because I assume that 
           meaningful phrases don't have punctuation within them.
        3. remove the line with only one word
        4. change all the letters to lower form
        5. remove all the non-alphabetic and non-number characters
        """
        new_doc = []
        line_sum = 0
        print('Processing files in ' + self.dir_name)
        for _, _, files in os.walk(self.dir_name):
            for file in files:
                f = open(self.dir_name + '/' + file)
                con = f.read()
                con = con.replace('\n', ' ')
                doc = re.split(r'[,.?:!]', con)
                doc_r = [x for x in doc if len(x.strip().split()) > 1]
                # print ("%s : %d" % (file, len(doc_r)))
                line_sum += len(doc_r)
                new_doc.extend(doc_r)
                f.close()
        print("line sum: ", line_sum)

        out = open(self.out_file, 'w')
        for line in new_doc:
            line = line.lower()
            line = re.sub(r"[^a-z0-9']+", " ", line)
            line = line.strip()
            # ' may appear in a sentence, but it can't appear at the start of a line
            line = line.strip("'")
            out.write(line)
            out.write('\n')
        out.close()

