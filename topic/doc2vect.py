import pandas as pd
import os
from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedLineDocument
import numpy as np
from sklearn.cluster import KMeans

from topic.lda_exp import perform_lda


def file2model(df, ofile):
    print("columns:", df.columns.tolist())

    lines = []
    for cur_id, row in df.groupby('id_df'):
        title = row['title_df'].values[0].replace("\n", ' ').replace("\r\n", ' ').replace("\r", ' ')
        abstract = row['abstract'].values[0].replace("\n", ' ').replace("\r\n", ' ').replace("\r", ' ')
        keywords = row['keywords'].values[0]
        keywords = keywords.replace("\n", ' ') if keywords is str else ""
        line = " ".join(map(str, [cur_id, "\t", title, abstract, keywords]))
        lines.append(line.lower().replace(".", " "))

    open(ofile, 'w').writelines(l + "\n" for l in lines)

    sentences = TaggedLineDocument(ofile)
    model = Doc2Vec(sentences, size=100, window=300, min_count=10, workers=4)
    # model = Doc2Vec(sentences, size=100, window=300, min_count=10, workers=4)
    id_list = [s[0][0] for s in sentences]
    vect_list = []

    need_vect_list = True
    if need_vect_list:
        for s in sentences:
            sent = " ".join(s.words)
            vect_list.append(model.infer_vector(sent))

    return model, vect_list, id_list


def test_doc2vect(model):
    test_sentence_list = ["network", "water", "rock", "borehole drilling", "wellbore", "mechanical failure"]
    for test_sentence in test_sentence_list:
        q = test_sentence.split()
        print(test_sentence)
        for s, p in model.most_similar(q):
            print('\t', s, p)
        print()


def clust_data(data, n_clusters=64):
    print(data.shape)
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(data)
    labels = kmeans.labels_
    return labels


def perform_doc2vect(df, ifile, ofile, odir_sentence):
    model, vect_list, id_list = file2model(df, ofile)
    data = np.array(vect_list)
    labels = clust_data(data)
    df['labels'] = labels
    df.to_csv(odir_sentence + ifile.replace(".csv", ".labels.csv"))

    if need_test:
        test_doc2vect(model)


if __name__ == '__main__':
    idir = r'/home/o/PycharmProjects/skygate/data/Gmech/'
    odir_sentence = r'/home/o/PycharmProjects/skygate/topic/txt/'
    need_test = False
    need_doc2vect = False
    need_lda = True

    for ifile in os.listdir(idir):
        print(ifile)
        ofile = odir_sentence + ifile.replace(".csv", ".text.txt")
        df = pd.read_csv(idir + ifile, encoding='cp1251')
        if need_lda:
            doc_set = df[['title_df', 'abstract']].sum(axis=1).values
            perform_lda(doc_set, num_topics=64)

        if need_doc2vect:
            perform_doc2vect(df, ifile, ofile, odir_sentence)
