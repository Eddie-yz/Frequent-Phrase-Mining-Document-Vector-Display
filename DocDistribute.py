import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.metrics import euclidean_distances
from sklearn import manifold
from sklearn.svm import SVC
import os
import re

class AuthorClassifier(object):
    def __init__(self):
        self.phrase_dict = Counter()

    def dictConstruct(self, dir_name):
        """
        Construct a dictionary which contains all the meaningful
        phrase appearing in these documents.
        """
        for _, _, files in os.walk(dir_name):
            for file in files:
                f = open(dir_name + '/' + file)
                con = f.readlines()
                for line in con:
                    phrases = re.split(r'[:,]', line.strip())
                    self.phrase_dict[phrases[0].strip()] += int(phrases[1].strip())
        print ('Amount of phrases in dictionary:  ', len(self.phrase_dict))
        print ('\n')

    def doc2vec(self, docDir_name):
        """
        This function can transform each document in docDir_name to a vector
        The vector is represented by the phrase-verion of tf-idf
        """
        print('Processing files in ' + docDir_name)
        for _, _, files in os.walk(docDir_name):
            docMat = np.zeros((len(files), len(self.phrase_dict)))
            for doc_index, file in enumerate(files):
                f = open(docDir_name + '/' + file)
                con = f.read()
                con = con.replace('\n', ' ')
                for phrase_index, phrase in enumerate(self.phrase_dict.keys()):
                    docMat[doc_index, phrase_index] = con.count(phrase) / self.phrase_dict[phrase]

        return docMat

    def _matJoint(self, matArray):
        """
        This puts the document matrix from each author all
        together and label them.
        And also this can perfrom PCA on the document matrixes.
        """
        docsMat = np.zeros((0, len(self.phrase_dict)))
        labelsMat = np.zeros((0, 1))
        for label, mat in enumerate(matArray):
            docsMat = np.concatenate((docsMat, mat), axis=0)
            labelsMat = np.concatenate((labelsMat, np.full((mat.shape[0], 1), label)), axis=0)

        return docsMat, labelsMat

    def plotDistribution(self, docVecArray, authors_name):
        """
        Using Multi-dimension scaling algorithm to compress each
        document vector to a 2-dimension vector, and plot it on
        a 2-D figure.
        """
        docM, labelM = self._matJoint(docVecArray)
        print('Calculating similarities...')
        similarity = euclidean_distances(docM)
        print('Running MDS...')
        mds = manifold.MDS(n_components=2, metric=True, max_iter=4000,
                           eps=1e-6, dissimilarity='precomputed', random_state=1)
        docM = mds.fit_transform(similarity)

        plt.figure(figsize=(15, 9))
        plt.xlim([-5, 5])
        plt.ylim([-4, 3])
        plt.scatter(docM[labelM.ravel() == 0, 0], docM[labelM.ravel() == 0, 1], c='r', label=authors_name[0])
        plt.scatter(docM[labelM.ravel() == 1, 0], docM[labelM.ravel() == 1, 1], c='b', label=authors_name[1])
        plt.scatter(docM[labelM.ravel() == 2, 0], docM[labelM.ravel() == 2, 1], c='g', label=authors_name[2])
        plt.scatter(docM[labelM.ravel() == 3, 0], docM[labelM.ravel() == 3, 1], c='y', label=authors_name[3])
        plt.scatter(docM[labelM.ravel() == 4, 0], docM[labelM.ravel() == 4, 1], c='black', label=authors_name[4])
        plt.legend()
        plt.title('Documents Distribution')
        plt.savefig('distribution.png')
        plt.show()
        return