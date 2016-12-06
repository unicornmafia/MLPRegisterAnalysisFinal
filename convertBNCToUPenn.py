import glob
import re

file_names = glob.glob("bnc_c5_tagged_dialog/*.txt")

all_sentences = dict()


def make_sentence_tuple_from_c5_sentence(sentence):
    converted_sentence = list()
    m = re.finditer(r'(\S+)_([A-Z0-9]+)', sentence)
    for matchNum, match in enumerate(m):
        groups = match.groups()
        if len(groups) != 3:
            word = groups[0].lower()
            tag = groups[1]
            if tag[:2] == "VV":
                tag = "VV"
            if tag[:2] == "VB":
                tag = "VB"
            if tag[:2] == "NN":
                tag = "NN"
            if tag != "PUN":
                converted_sentence.append((word, tag))

    print(str(converted_sentence))
    return converted_sentence


def convert_from_c5_to_penn(file_name):
    with open(file_name, 'r') as content_file:
        content = content_file.read()
    sentences = re.split(r"\s\S+_SENT\s", content)
    for sentence in sentences:
        #print(sentence)
        converted_sentence = make_sentence_tuple_from_c5_sentence(sentence)
        if len(converted_sentence) > 0:
            all_sentences[file_name].append(converted_sentence)


def read_tagged_dialog_c5():
    for file_name in file_names:
        all_sentences[file_name] = list()
        convert_from_c5_to_penn(file_name)
    return all_sentences

