import PhraseMining as PM
import DocDistribute as DD
import DocPreprocess as DP

# Change all the books from each author to a bunch of lines and store them in an txt
dp1 = DP.docPrep(inputDir_name='./rawDocData/D H Lawrence', outputFile_name='./docAfterPreprocess/Lawrence.txt')
dp1.process()

dp2 = DP.docPrep(inputDir_name='./rawDocData/Jack London', outputFile_name='./docAfterPreprocess/Jack_London.txt')
dp2.process()

dp3 = DP.docPrep(inputDir_name='./rawDocData/Mark Twain', outputFile_name='./docAfterPreprocess/Mark_twain.txt')
dp3.process()

dp4 = DP.docPrep(inputDir_name='./rawDocData/Charles Darwin', outputFile_name='./docAfterPreprocess/Charles_Darwin.txt')
dp4.process()

dp5 = DP.docPrep(inputDir_name='./rawDocData/Abraham Lincoln', outputFile_name='./docAfterPreprocess/Abraham_Lincoln.txt')
dp5.process()

# Mine the frequent phrase in the authors' documents
f = open('./docAfterPreprocess/Lawrence.txt')
doc = f.readlines()
f.close()
pm = PM.PhraseMining(min_support=20, threshold=5.4)
pm.output(doc, output_file='./frequent phrases/Lawrence.txt')

f = open('./docAfterPreprocess/Jack_London.txt')
doc = f.readlines()
f.close()
pm = PM.PhraseMining(min_support=60, threshold=6)
pm.output(doc, output_file='./frequent phrases/Jack_London.txt')

f = open('./docAfterPreprocess/Mark_twain.txt')
doc = f.readlines()
f.close()
pm = PM.PhraseMining(min_support=60, threshold=6)
pm.output(doc, output_file='./frequent phrases/Mark_twain.txt')

f = open('./docAfterPreprocess/Charles_Darwin.txt')
doc = f.readlines()
f.close()
pm = PM.PhraseMining(min_support=60, threshold=6)
pm.output(doc, output_file='./frequent phrases/Charles_Darwin.txt')

f = open('./docAfterPreprocess/Abraham_Lincoln.txt')
doc = f.readlines()
f.close()
pm = PM.PhraseMining(min_support=20, threshold=5.4)
pm.output(doc, output_file='./frequent phrases/Abraham_Lincoln.txt')

# Transform each document to a  vector based on the frequent phrases we have already found above
AC = DD.AuthorClassifier()
AC.dictConstruct('./frequent phrases')

mat_charles = AC.doc2vec('./rawDocData/Charles Darwin')
mat_lawrence = AC.doc2vec('./rawDocData/D H Lawrence')
mat_jack = AC.doc2vec('./rawDocData/Jack London')
mat_mark = AC.doc2vec('./rawDocData/Mark Twain')
mat_abraham = AC.doc2vec('./rawDocData/Abraham Lincoln')

AC.plotDistribution(docVecArray=[mat_charles, mat_lawrence, mat_jack, mat_mark, mat_abraham],
                                      authors_name=['Charles Darwin', 'Lawrence', 'Jack London', 'Mark Twain',
                                      'Abraham Lincoln'])