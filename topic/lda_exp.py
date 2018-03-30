from gensim.models import LdaModel
from nltk.stem.porter import PorterStemmer
from gensim import corpora
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words


def run():
    doc_a = "Brocolli is good to eat. My brother likes to eat good brocolli, but not my mother."
    doc_b = "My mother spends a lot of time driving my brother around to baseball practice."
    doc_c = "Some health experts suggest that driving may cause increased tension and blood pressure."
    doc_d = "I often feel pressure to perform well at school," \
            " but my mother never seems to drive my brother to do better."
    doc_e = "Health professionals say that brocolli is good for your health."

    doc_set = [doc_a, doc_b, doc_c, doc_d, doc_e]
    perform_lda(doc_set)


def perform_lda(doc_set, num_topics=64):
    print('lda started')
    tokenizer = RegexpTokenizer(r'\w+')
    raw = " ".join([doc.lower() for doc in doc_set])
    tokens = tokenizer.tokenize(raw)

    en_stop = get_stop_words('en')
    stopped_tokens = [i for i in tokens if not i in en_stop]
    # p_stemmer = PorterStemmer()
    # texts = [p_stemmer.stem(i) for i in stopped_tokens]
    texts = stopped_tokens
    dictionary = corpora.Dictionary([stopped_tokens])
    corpus = [dictionary.doc2bow(text.split()) for text in texts]
    ldamodel = LdaModel(corpus, num_topics=64, id2word=dictionary, passes=20)

    for line in ldamodel.print_topics(num_topics=num_topics, num_words=10):
        print('\t', line)


if __name__ == '__main__':
    run()
