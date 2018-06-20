import numpy as np
from collections import Counter
import math
import heapq


class PhraseMining(object):
    def __init__(self, min_support=10, max_phrase_length=5, threshold=10):
        self.min_support = min_support
        self.max_phrase_length = max_phrase_length
        self.threshold = threshold

    def _StopwordsRemove(self, documents, filename='./stopwords.txt'):
        """
        Load the stop words list from the '/Data/stopwords.txt',remove every
        stop word appears in the documents.
        """
        print("Stop words removing...")
        f = open(filename)
        stopwords = f.readlines()
        stopwords = [x.strip() for x in stopwords]
        new_document = []
        for line in documents:
            line = line.strip().split()
            line = [word for word in line if word not in stopwords]
            line = " ".join(line)
            new_document.append(line)
        return new_document

    def _WordFrequency(self, document):
        """
        This function counts the word frequency.
        Each word is a length-1 phrase.
        For DBLP database, the input 'document' means a several-line doc with a title in each line.
        The output are a Counter() that stores the occurrence times of each word and a
        integer holds the total word numbers.
        """
        print("Counting words...")
        word_frequency = Counter()
        word_number = 0

        for line in document:
            # each line is a title in DBLP
            words = line.strip().split()
            word_number += len(words)
            for word in words:
                # this will remove the phrase with number in it
                if word.strip().isdigit():
                    word_frequency[word] = 0
                else:
                    word_frequency[word] += 1

        return word_number, word_frequency

    def _FrequentPhraseMining(self, document, word_frequency):
        """
        This function performs finding all the phrases that occur more than min_support times.
        For DBLP database, the input 'document' means a several-line doc with a title in each line.
        The input word_frequency is a Counter of length-1 words.
        """
        print("Mining frequent phrase...")
        phrase_counter = word_frequency
        n = 2
        # indices of all length-1 phrases
        phrase_indices = [range(len(line.split())) for line in document]

        while len(document) != 0:
            new_phrase_indices = []
            lines_remain = []
            for index, line in enumerate(document):
                phrase_index = phrase_indices[index]
                new_phrase_index = []
                words = line.strip().split()

                # Candidate phrases of length n-1 are pruned if they do not satisfy the minimum
                # support threshold and their starting position is removed from the active indices.
                for word_i in phrase_index:
                    if word_i + n - 2 <= len(words) - 1:
                        phrase = ""
                        for i in range(word_i, word_i + n - 1):
                            phrase = phrase + words[i] + " "
                        phrase = phrase.strip()

                        if phrase_counter[phrase] >= self.min_support:
                            new_phrase_index.append(word_i)

                if len(new_phrase_index) > 1:
                    # lines_remain.append(line)
                    # new_phrase_indices.append(new_phrase_index)
                    new_phrase_index_ = []
                    for i, word_i in enumerate(new_phrase_index[:-1]):
                        if new_phrase_index[i + 1] == word_i + 1:
                            phrase = ""
                            for j in range(i, i + n):
                                phrase = phrase + words[j] + " "
                            phrase = phrase.strip()
                            phrase_counter[phrase] += 1
                            new_phrase_index_.append(word_i)
                    if len(new_phrase_index_) != 0:
                        lines_remain.append(line)
                        new_phrase_indices.append(new_phrase_index_)

            document = lines_remain
            phrase_indices = new_phrase_indices
            n += 1
            if n > self.max_phrase_length:
                break

        frequent_phrase = Counter(
            phrase for phrase in phrase_counter.elements() if phrase_counter[phrase] >= self.min_support)

        return frequent_phrase

    def _RectifiedPhraseFreq(self, phrase_pool):
        """
        if the raw frequency of "x y" is c1, "x y z" is c2:
        then the rectified frequency of "x y" should be c2 - c1
        Compare (c2 - c1) with min_support, remove "x y" if it doesn't reach min_support
        """
        for phrase in phrase_pool.keys():
            words = phrase.strip().split()
            if len(words) >= 3 and phrase_pool[phrase][0] > self.min_support:
                sub_phrase_1 = " ".join(words[:-1])
                sub_phrase_2 = " ".join(words[1:])
                if phrase_pool.get(sub_phrase_1) is not None:
                    phrase_pool[sub_phrase_1][0] = phrase_pool[sub_phrase_1][0] - phrase_pool[phrase][0]
                if phrase_pool.get(sub_phrase_2) is not None:
                    phrase_pool[sub_phrase_2][0] = phrase_pool[sub_phrase_2][0] - phrase_pool[phrase][0]

        # frequent_phrase = Counter(phrase for phrase in phrase_counter.elements() if phrase_counter[phrase] >= self.min_support)
        new_phrase_pool = {k: v for k, v in phrase_pool.items() if v[0] > self.min_support}
        return new_phrase_pool

    def _calSignificanceScore(self, word_num, phrase_1, phrase_2, phrase_counter):
        """
        We use a significance score to provide a quantitative measure of which two
        consecutive phrases form the best collocation at each merging iteration. This
        is measured by comparing the actual frequency with the expected occurrence.
        """
        p_p1 = float(phrase_counter[phrase_1]) / word_num
        p_p2 = float(phrase_counter[phrase_2]) / word_num
        miu = word_num * p_p1 * p_p2
        phrase_merge = phrase_1 + " " + phrase_2
        occurrence = phrase_counter[phrase_merge]
        if occurrence == 0:
            return 0
        else:
            return (occurrence - miu) / math.sqrt(occurrence)

    def _PhraseFiltering(self, document, word_num, phrase_counter):
        """
        use significance score to filter low quality phrase
        """
        print("Low quality phrase removing...")
        new_doc = []
        phrase_pool = {}
        for line in document:
            words = line.strip().split()
            score_pool = {}
            while (True):
                max_score = 0
                max_index = -1
                for i, word in enumerate(words[:-1]):
                    phrase = words[i] + " " + words[i + 1]
                    if phrase_counter[phrase] >= self.min_support:
                        if phrase not in score_pool:
                            score = self._calSignificanceScore(word_num, words[i], words[i + 1], phrase_counter)
                            score_pool[phrase] = score
                        if score_pool[phrase] > max_score:
                            max_score = score_pool[phrase]
                            max_index = i
                if max_score < self.threshold:
                    break
                else:
                    score_pool[words[max_index - 1] + " " + words[max_index]] = 0
                    words[max_index] = words[max_index] + " " + words[max_index + 1]
                    phrase_pool[words[max_index]] = [phrase_counter[words[max_index]], max_score]
                    words.remove(words[max_index + 1])
                    # print (", ".join(words[:]))
            line = ", ".join(words[:])
            new_doc.append(line)

        return new_doc, phrase_pool

    def output(self, doc, output_file, is_DBLP=False):
        """
        The main function of this class.
        It will automatically excute above functions.
        For Gutenberg data, the well-selected frequent phrases will store in 'output_file'.
        For DBLP data, the qualified phrases will be written in './DBLP/DBLP phrases.txt',
                       and the frequent phrases that have low significance score will be
                       written in './DBLP/underThreshold.txt'
        """
        print ('Starting... ')
        doc = self._StopwordsRemove(doc)
        wn, wf = self._WordFrequency(doc)
        fp = self._FrequentPhraseMining(doc, wf)

        new_doc, pp = self._PhraseFiltering(doc, wn, fp)
        pp = self._RectifiedPhraseFreq(pp)

        if is_DBLP:
            out2 = open(output_file + '/underThreshold.txt', 'w')
            for i in sorted(fp.keys()):
                if len(i.split()) >= 2:
                    phrase_1 = i.split()[0]
                    phrase_2 = " ".join(i.split()[1:])
                    score = self._calSignificanceScore(wn, phrase_1, phrase_2, fp)
                    if score < self.threshold:
                        out2.write("%s : %d,  %.2f" % (i, fp[i], score))
                        out2.write('\n')
            out2.close()
            output_file = './DBLP/DBLP phrases.txt'
            # out3 = open(output_dir + '/result_3.txt', 'w')
            # for i in sorted(pp.keys()):
            #     out3.write("%s : %d,  %.2f" % (i, pp[i][0], pp[i][1]))
            #     out3.write('\n')
            # out3.close()

        out4 = open(output_file , 'w')
        for i in sorted(pp.keys()):
            out4.write("%s : %d,  %.2f" % (i, pp[i][0], pp[i][1]))
            out4.write('\n')
        out4.close()
        print ('\n')
        return



