import os
import fnmatch
from stop_words import get_stop_words
swords = get_stop_words('en')


def remove_stopwords(line):
    line = " ".join(e for e in line.split() if e not in swords) + "\n"
    return line


print("txt2vw")
idir = 'txt/'
odir = 'vw/'
for file_name in fnmatch.filter(os.listdir(idir), '*.txt'):
    ofile_name = file_name.lower().replace(".txt", ".vw")
    with open(idir+file_name) as ifile, open(odir+ofile_name, 'w') as ofile:
        for line in ifile:
            ind = line.find("\t")
            cur_id = line[:ind]
            other_line = line[ind:]
            other_line = remove_stopwords(other_line)
            newline = cur_id + " |text "+other_line.replace("|", ' ').replace(":", " ")
            ofile.write(newline)
