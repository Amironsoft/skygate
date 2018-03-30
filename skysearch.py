from skygate import get_arxiv, get_onepetro


def prepare_content_dict():
    content_dict = {}
    s = ""
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


def get_link(link):
    url_link = link.replace("static/", "").replace("/", "___")
    link = link.replace("static/", "")
    return "<a href='./data?file={url_link}' target='_blank'>{link}</a>".format(url_link=url_link, link=link)


def print_res(res):
    if len(res) > 0:
        ans_list = []

        for item in res:
            ans_line = get_link(item)
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

        res = get_arxiv(query)
        ans = "<br>arxiv:<br>" + print_res(res)+"<br>"

        if query == 'geomechanics':
            res2 = get_onepetro(query)
            ans += "one petro:<br>" + print_res(res2) + "<br>"
        else:
            ans += "one petro:<br>" + "support only geomechanics query" + "<br>"
    else:
        ans = "уточните пожалуйста"
    return ans


if __name__ == '__main__':
    while True:
        question = input(">:")
        print(get_answer(question))
