import os
import locale
import glob
import re

# where is coca?
coca_path = "D:\corpora\COCA"
coca_fiction_path = os.path.join(coca_path, "text_fiction_awq")
coca_source_index = os.path.join(coca_path, "sources/coca-sources.txt")
juvenile_fiction_subgenre_code = 117

output_file_juvenile = os.path.join(coca_path, "thomas/juvenile_fiction.txt")


# find all fiction text ids
juvenile_fiction_ids = list()
other_fiction_ids = list()

encoding = locale.getpreferredencoding()


def get_id_lists():
    index = open(coca_source_index, encoding=encoding, errors='ignore')
    for line in index:
        trimmed_line = line.strip()
        if trimmed_line != "":
            data = trimmed_line.split()
            genre = data[2]
            if genre == "FIC":
                id = data[0]
                subgenre = data[3]
                if subgenre == "117":
                    juvenile_fiction_ids.append(id)
                else:
                    other_fiction_ids.append(id)


def print_id_lists():
    print("\nJUVENILE FICTION IDS\n")
    for id in juvenile_fiction_ids:
        print(id)

    print("\nNON-JUVENILE FICTION IDS\n")
    for id in other_fiction_ids:
        print(id)


def clean_line(line):
    cleaned = line.strip().lower()
    cleaned = re.sub('(<.>|@ @ @ @ @ @ @ @ @ @)', '', cleaned)
    return cleaned


def scan_file_for_fiction(file_name):
    input_file_name = os.path.join(coca_fiction_path, file_name)
    juvenile_output_file_name = os.path.join(coca_fiction_path, "juvenile", file_name)
    other_output_file_name = os.path.join(coca_fiction_path, "other", file_name)
    input_file = open(input_file_name, encoding=encoding, errors='ignore')
    juvenile_output_file = open(juvenile_output_file_name, 'w')
    other_output_file = open(other_output_file_name, 'w')
    for line in input_file:
        m = re.match(r'^##([0-9]+) ', line)
        if m is not None and m.groups() is not None and m.groups()[0] is not None:
            id = m.groups()[0]
            if id in other_fiction_ids:
                other_output_file.write(clean_line(line[m.end():]) + "\n")
            elif id in juvenile_fiction_ids:
                juvenile_output_file.write(clean_line(line[m.end():]) + "\n")
    input_file.close()
    juvenile_output_file.close()
    other_output_file.close()


# start here
get_id_lists()
#print_id_lists()
file_list = glob.glob(os.path.join(coca_fiction_path, "*.txt"))
num_files = len(file_list)
i = 0

print("\nStarting with {} juvenile fiction sources and {} non-juvenile fiction sources".format(len(juvenile_fiction_ids), len(other_fiction_ids)))

for file_name in file_list:
    i += 1
    print("scanning: " + file_name + ", " + str(i) + " of " + str(num_files))
    scan_file_for_fiction(os.path.basename(file_name))


