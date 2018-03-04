import requests
from xml.etree import ElementTree
import pandas as pd

from config import odir


def download_data_xml(term):
    url = 'https://export.arxiv.org/api/query?search_query=all:{}&start=0&max_results=2000'.format(term)
    resp = requests.get(url)
    with open("{}/xml/res_{}_data.xml".format(odir, term), "w", encoding="utf-8") as ofile:
        ofile.write(resp.text)
        # tree = ElementTree.fromstring(resp.content)
        # print(tree)


def ename(name):
    return "{{http://www.w3.org/2005/Atom}}{}".format(name)


def parse_data_xml(ifile):
    tree = ElementTree.parse(ifile)
    for i, doc in enumerate(tree.findall(ename("entry"))):
        title = doc.find(ename("title")).text
        date = pd.to_datetime(doc.find(ename("updated")).text).year
        print(date, title)
        for auth in doc.findall(ename("author")):
            print("\t", auth.find(ename("name")).text)
        print("_"*30)


if __name__ == '__main__':
    print("skygate started")
    terms = ["geomechanics", "rock mechanics", "mechanical failure"]
    for term in terms:
        download_data_xml(term)
        ifile = r"{}/xml/res_{}_data.xml".format(odir, term)
        parse_data_xml(ifile)
