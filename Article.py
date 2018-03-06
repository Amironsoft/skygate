import pandas as pd


class Article:
    def __init__(self, term):
        self.link = None
        self.cur_id = None
        self.title = None
        self.date = None
        self.authors = None
        self.term = term
        self.pdf_file_name = None
        self.topic = None

    @staticmethod
    def ename(name):
        return "{{http://www.w3.org/2005/Atom}}{}".format(name)

    def parse_arxiv(self, doc):
        self.link = doc.findall(".//*[@title='pdf']")[0].attrib['href']
        self.cur_id = self.link.split('/')[-1]
        self.title = doc.find(self.ename("title")).text.replace("\n", " ")
        self.date = pd.to_datetime(doc.find(self.ename("updated")).text).year

        self.authors = []
        for auth_tag in doc.findall(self.ename("author")):
            auth = auth_tag.find(self.ename("name")).text
            self.authors.append(auth)

    def print_meta(self):
        print("\t", self.cur_id)
        print("\t", self.link)
        print('\t', self.pdf_file_name)
        print('\t', self.date, self.title)
        for auth in self.authors:
            print("\t\t", auth)
        print('\t', "_" * 30)
