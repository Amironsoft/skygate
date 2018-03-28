import pandas as pd


class Article:
    header = ["id", "link", "date", "title", "authors", "summary"]

    def __init__(self, term):
        self.link = None
        self.cur_id = None
        self.title = None
        self.date = None
        self.authors = None
        self.term = term
        self.pdf_file_name = None
        self.topic = None
        self.summary = None
        self.keywords = None

    @staticmethod
    def ename(name):
        return "{{http://www.w3.org/2005/Atom}}{}".format(name)

    def parse_arxiv(self, doc):
        self.link = doc.findall(".//*[@title='pdf']")[0].attrib['href']
        self.cur_id = self.link.split('/')[-1]
        self.title = doc.find(self.ename("title")).text.replace("\n", " ")
        self.date = pd.to_datetime(doc.find(self.ename("updated")).text).year
        self.summary = doc.find(self.ename("summary")).text
        self.authors = []
        for auth_tag in doc.findall(self.ename("author")):
            auth = auth_tag.find(self.ename("name")).text
            self.authors.append(auth)
        self.keywords = self.get_keywords(doc)

    def parse_one(self, doc):
        self.link = doc.find(".//h3[@class='book-title']/a").attrib['href']
        self.cur_id = self.link.split('/')[-1]
        self.title = doc.find(self.ename("title")).text.replace("\n", " ")
        self.date = pd.to_datetime(doc.find(self.ename("updated")).text).year
        self.summary = doc.find(self.ename("summary")).text
        self.authors = []
        for auth_tag in doc.findall(self.ename("author")):
            auth = auth_tag.find(self.ename("name")).text
            self.authors.append(auth)
        self.keywords = self.get_keywords(doc)

    def get_summary_keywords(self, summary):
        keywords = summary.lower().split("keywords:")[-1]
        repl_dict = {".": " ",
                     ";": ","}
        for k, v in repl_dict.items():
            keywords = keywords.replace(k, v)
        return keywords

    def get_keywords(self, doc):
        keywords = ""
        if "keywords:" in self.summary.lower():
            keywords = self.get_summary_keywords(self.summary)
        else:
            comment_tag = doc.find(self.ename("arxiv:comment"))
            if comment_tag:
                comment_text = comment_tag.text
                if "keywords-" in comment_text.lower():
                    keywords = comment_text.split("keywords-")[-1]
                elif "keywords:" in comment_text.lower():
                    keywords = comment_text.split("keywords:")[-1]
        return keywords

    def print_meta(self):
        print("\tcur_id:", self.cur_id)
        print("\tlink:", self.link)
        print('\tpdf_file_name', self.pdf_file_name)
        print('\tdate:', self.date)
        print('\ttitle:', self.title)
        for auth in self.authors:
            print("\t\tauthor:", auth)
        print("\tkeywords:", self.keywords)
        print('\t', "_" * 30)

    def get_line(self):
        auth_line = "|".join(a for a in self.authors)
        line_items = [self.cur_id,
                self.link,
                self.date,
                self.title,
                auth_line,
                self.prep_summary(self.summary),
                self.keywords]
        return "\t".join(map(str, line_items))

    def prep_summary(self, summary):
        return summary.replace("\n", " ").replace("\t", " ")
