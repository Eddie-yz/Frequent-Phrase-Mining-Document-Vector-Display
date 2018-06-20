# Frequent-Phrase-Mining-Document-Vector-Display
A phrase mining implementation of ToPMine framework &amp; Using MDS algorithm to display the document vector.

Reference Paper：

El-Kishky, A., Song, Y., Voss, C. R., Voss, C. R., & Han, J. (2014). Scalable topical phrase mining from text corpora. Proceedings of the Vldb Endowment, 8(3), 305-316.

http://www.vldb.org/pvldb/vol8/p305-ElKishky.pdf

DIRECTORY:

rawDocData: 该文件夹下有5个独立的文件夹，分别存放5位作者的全部书籍

docAfterPreprocess: 程序运行后将在该文件夹下生成5个txt文档，每个文档存放经过预处理后的一位作者的全部书籍内容，文档内每一行为原书籍中的一句话

frequent phrases: 程序运行后，将在该文件夹下生成5个txt文档，分别对应从每位作者所有书籍中的挖掘到的频繁短语

DBLP: 存放DBLP数据库中的30万条题目数据及程序输出




CODE:

DocPreprocess.py: 其中的docPrep类负责预处理每位作者的所有书籍，将每一句话变成一行存放在新生成的文档中

PhraseMining.py: 其中的PhraseMining类负责从每个预处理后的文档中挖掘frequent phrases并将其存于新生成的文档中

DocDistribute.py: 其中的AuthorClassifier类负责根据所有得到的frequent phrase将每位作者的每本书都转化为一个向量，并对其降维，在2维图像上展示每位作者的书籍分布情况

runGutenberg.py: 面对Gutenberg数据集的主函数，将未处理的数据放入rawDocData文件夹后，直接运行本程序，它将自动调用以上函数，完成频繁词组挖掘和书籍分布展示的工作

runDBLP.py: 面对DBLP数据集的主函数。运行本程序，将对DBLP文件夹下的 titleData.txt进行频繁短语挖掘，并在同一文件夹输出挖掘到的高质量短语及未满足重要性阈限的低质量搭配。

