import operator
import os
import traceback


class NGrams:
    def __init__(self, n):
        self.n = n
        self.ngrams = dict()
        self.posgrams = dict()

    def get_frequency_sorted_ngrams(self):
        sorted_ngrams = sorted(self.ngrams.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_ngrams

    def get_frequency_sorted_posgrams(self):
        sorted_ngrams = sorted(self.posgrams.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_ngrams

    def add_ngram(self, ngram):

        ngram_string = ' '.join(ngram)
        # try:
        #     if ngram_string == "back to paradise estate":
        #         raise RuntimeWarning
        # except RuntimeWarning:
        #     print("back to paradise estate")
        #     print("sentence: " + str(sentence))
        #     print("ngram: " + str(ngram))
        #     traceback.print_stack()
        try:
            self.ngrams[ngram_string] += 1
        except KeyError:
            self.ngrams[ngram_string] = 1

    def add_posgram(self, posgram):
        posgram_string = ' '.join(posgram)
        try:
            self.posgrams[posgram_string] += 1
        except KeyError:
            self.posgrams[posgram_string] = 1

    def add_sentence(self, sentence):
        if len(sentence) >= self.n:
            for i in range(0, len(sentence) - self.n + 1):
                temp_ngram = list()
                temp_posgram = list()
                for j in range(i, i + self.n):
                    temp_ngram.append(sentence[j][0])
                    temp_posgram.append(sentence[j][1])
                self.add_ngram(temp_ngram)
                self.add_posgram(temp_posgram)


class NGramData:
    def __init__(self, file_name_prepend):
        self.file_name_prepend = file_name_prepend
        self.grams = dict()
        self.grams[2] = NGrams(2)
        self.grams[3] = NGrams(3)
        self.grams[4] = NGrams(4)
        self.grams[5] = NGrams(5)
        self.grams[6] = NGrams(6)

    def add_sentence(self, sentence):
        for n in self.grams.keys():
            self.grams[n].add_sentence(sentence)

    def get_ngrams(self, n):
        self.grams[n].get_frequency_sorted_ngrams()

    def get_posgrams(self, n):
        self.grams[n].get_frequency_sorted_posgrams()

    def print_gram_dict(self, grams, gramtype, n):
        filename = "grams/" + self.file_name_prepend + "_" + str(n) + "-" + gramtype + ".csv"
        outfile = open(filename, "w")
        outfile.write("sequence, count\n")
        for gram_tuple in grams:
            outfile.write(gram_tuple[0] + ", " + str(gram_tuple[1]) + "\n")
        outfile.close()

    def print_ngrams(self, n):
        ngrams = self.grams[n].get_frequency_sorted_ngrams()
        self.print_gram_dict(ngrams, "ngram", n)

    def print_posgrams(self, n):
        posgrams = self.grams[n].get_frequency_sorted_posgrams()
        self.print_gram_dict(posgrams, "posgram", n)

    def print_all_grams(self):
        if not os.path.exists("grams"):
            os.makedirs("grams")
        for n in self.grams.keys():
            self.print_ngrams(n)
            self.print_posgrams(n)

