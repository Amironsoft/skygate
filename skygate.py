import requests
from xml.etree import ElementTree
import pandas as pd
import os
import shutil

from Article import Article
from config import odir
from parse_pdf import convert_pdf_dir


def download_data_xml(term):
    url = 'https://export.arxiv.org/api/query?search_query=all:{}&start=0&max_results=2000'.format(term)
    resp = requests.get(url)
    with open("{}/xml/res_{}_data.xml".format(odir, term), "w", encoding="utf-8") as ofile:
        ofile.write(resp.text)
        # tree = ElementTree.fromstring(resp.content)
        # print(tree)


def savefile(link, ofile):
    response = requests.get(link)
    with open(ofile, 'wb') as f:
        f.write(response.content)


def savefile_stream(link, ofile):
    link = link.replace("http://", "https://")
    response = requests.get(link, stream=True)
    chunk_size = 20000
    if response.status_code == 200:
        with open(ofile, 'wb') as fd:
            for chunk in response.iter_content(chunk_size):
                fd.write(chunk)
    else:
        print("downloading failed")


def parse_data_xml(ifile, term):
    articles = []
    tree = ElementTree.parse(ifile)
    for i, doc in enumerate(tree.findall(Article.ename("entry"))):
        article = Article(term)
        article.parse_arxiv(doc)
        pdf_file_name = odir + "pdf/" + term + "/" + article.cur_id + ".pdf"
        article.pdf_file_name = pdf_file_name
        # savefile_stream(article.link, pdf_file_name)
        article.print_meta()
        articles.append(article)


if __name__ == '__main__':
    print("skygate started")
    terms = ["geomechanics", "rock mechanics", "mechanical failure"]
    # terms = ["neural networks"]

    for term in terms:
        print(term)
        pdf_term_odir = odir + "pdf/" + term + "/"
        txt_term_odir = odir + "txt/" + term + "/"
        os.makedirs(pdf_term_odir, exist_ok=True)
        download_data_xml(term)
        ifile = r"{}/xml/res_{}_data.xml".format(odir, term)
        # parse_data_xml(ifile, term)
        convert_pdf_dir(pdf_term_odir, txt_term_odir)
