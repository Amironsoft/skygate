from pprint import pprint

from elasticsearch import Elasticsearch

s = open("../input/input.txt").read()


def prepare_content_dict():
    content_dict = {}

    for line in s.splitlines():
        if len(line) > 1:
            if line.isupper():
                cur_section = line
            else:
                if cur_section in content_dict:
                    content_dict[cur_section].append(line)
                else:
                    content_dict[cur_section] = [line]
    return content_dict


def print_res(res):
    if len(res['hits']['hits']) > 0:
        ans_list = ["возможно вы искали: "]
        for item in res['hits']['hits']:
            ans_line = " ".join(["_____", item['_source']["chapter"], item['_source']["text"]])
            if ans_line not in ans_list:
                ans_list.append(ans_line)
        return "<br>\n".join(ans_list)
    else:
        return "уточните пожалуйста"


def clean_query(query):
    query = query.lower()
    ignore_words = {"привет", "пока", "здравствуйте", "добрый вечер"}

    for w in ignore_words:
        query = query.replace(w, "")

    return query


def del_punc(query):
    ignore_words = {".", ",", "!"}
    for w in ignore_words:
        query = query.replace(w, "")
    return query


def isthanks(query):
    query = del_punc(query)
    thanks_words = ["спасибо", "спс", "благодарю", "рахмат"]
    return any(w == query for w in thanks_words)


def ishello(query):
    thanks_words = ["здравствуйте", "добрый день", "привет", "привет, бот", "здорова", "доброе утро"]
    return any(w == query for w in thanks_words)


def define_question_type(query):
    if isthanks(query):
        return "Пожалуйста! Рады вам помочь :)"
    # elif ishello(query):
    #     return "введите вопрос :)"
    return None


def get_answer(query):
    if len(query) >= 3:
        query = clean_query(query)
        defined_ans = define_question_type(query)
        if defined_ans:
            return defined_ans
        res = es.search(index="some-index", body={'query': {'match': {'text': query}}})
        ans = print_res(res)
    else:
        ans = "уточните пожалуйста"
    return ans


def initialize():
    global es
    content_dict = prepare_content_dict()
    # pprint(content_dict)
    es = Elasticsearch()
    print("Здравствуйте! Чем могу помочь?")
    for i, (chapter, chapter_content) in enumerate(content_dict.items()):
        for cur_line in chapter_content:
            doc = {"chapter": chapter,
                   "text": cur_line}
            res = es.index(index="some-index", doc_type="text", body=doc)


initialize()

if __name__ == '__main__':
    initialize()

    while True:
        question = input(">:")
        print(get_answer(question))
