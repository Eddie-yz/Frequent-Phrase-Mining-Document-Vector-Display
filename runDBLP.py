import PhraseMining as PM

f = open('./DBLP/titleData.txt')
doc = f.readlines()
f.close()
pm = PM.PhraseMining(min_support=120, threshold=10)
pm.output(doc, output_file='./DBLP', is_DBLP=True)
