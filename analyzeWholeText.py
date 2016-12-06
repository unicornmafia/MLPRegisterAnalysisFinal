import glob
import nltk
from nltk import word_tokenize
from textStats import TextStats    # weirdly, pycharm thinks this is an error
from statWriter import StatWriter  # weirdly, pycharm thinks this is an error
from nltk.tokenize import sent_tokenize
from ngrams import NGramData
import re

#
# set up variables
#
output_file_name = "mlp_analysis.csv"
output_file = open(output_file_name, "w")

diff_file_name = "stat_diffs.csv"
diff_file = open(diff_file_name, "w")

print("Output File: " + output_file_name + "\n")

files = glob.glob("*_dialog.txt")
sorted_files = sorted(files)

all_tags = set()
file_stats = dict()
group_stats = dict()

ngram_data = dict()

stat_writer = StatWriter(output_file, diff_file, file_stats, group_stats)


#
# add a tuple in the form (word:pos-tag)
#
def add_tuple(tuple, file_name, group_name):
    # keep track of all tags
    tag = tuple[1]
    if tag == ",":
        tag = "comma"

    all_tags.add(tag)

    # add to file stats
    if file_name not in file_stats:
        file_stats[file_name] = TextStats(file_name)
    file_stats[file_name].add_tuple(tuple)

    # add to group stats
    if group_name not in group_stats:
        group_stats[group_name] = TextStats(group_name)
    group_stats[group_name].add_tuple(tuple)


#
# add a sentence
#
def add_sentence(sentence, file_name, group_name):
    # add to file stats
    if file_name not in file_stats:
        file_stats[file_name] = TextStats(file_name)
    file_stats[file_name].add_sentence(sentence)

    # add to group stats
    if group_name not in group_stats:
        group_stats[group_name] = TextStats(group_name)
    group_stats[group_name].add_sentence(sentence)


def analyze_file(file_name, group_name):
    input_file = open(file_name, encoding="utf-8")
    line_num = 1
    text = ""
    for line in input_file:
        text += line.strip() + ' '

    sentences = sent_tokenize(text)
    num_sentences = len(sentences)

    tokenized_sents = list()
    for sentence in sentences:
        lcsent = sentence.lower()
        lcsent = re.sub(r'[^ a-zA-Z0-9_\'-]+', '', lcsent)  # take out everything but real words.

        tokenized_sents.append(word_tokenize(lcsent))
        add_sentence(lcsent, file_name, group_name)

    pos_tags = nltk.pos_tag_sents(tokenized_sents)

    for pos_tag_sent in pos_tags:
        ngram_data[group_name].add_sentence(pos_tag_sent)

        for tuple in pos_tag_sent:
            add_tuple(tuple, file_name, group_name)

        print(file_name + " - line: " + str(line_num) + " of " + str(num_sentences))
        print(str(pos_tag_sent))
        line_num += 1

        # for debugging
        # if line_num > 100:
        #     return


def get_group_name_from_file_name(file_name):
    parts = file_name.split(".")
    return parts[0]


def add_ngram_data_group(group_name):
    try:
        data = ngram_data[group_name]
    except KeyError:
        ngram_data[group_name] = NGramData(group_name)


def print_ngram_data(group_name):
    ngram_data[group_name].print_all_grams()

#
# START HERE
#
for file_name in sorted_files:
    print("\nAnalyzing: " + file_name)
    group_name = get_group_name_from_file_name(file_name)
    add_ngram_data_group(group_name)
    analyze_file(file_name, group_name)
    print_ngram_data(group_name)

sorted_tags = sorted(all_tags)
stat_writer.output_analysis(sorted_tags)
stat_writer.output_most_significant_differences_between_groups("mlpaf", "mlpfim", sorted_tags)
output_file.close()
diff_file.close()



