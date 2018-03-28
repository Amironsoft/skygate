import requests
from xml.etree import ElementTree
import pandas as pd
import os
import shutil

from Article import Article
from config import odir
from pdf2txt_converter import convert_pdf_dir


def download_data_xml_arxiv(xml_file, term):
    url = 'https://export.arxiv.org/api/query?search_query=all:{}&start=0&max_results=2000'.format(term)
    resp = requests.get(url)
    with open(xml_file, "w", encoding="utf-8") as ofile:
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


def parse_data_xml(xml_file, csv_file, term, need_download_pdf=False):
    articles = []
    tree = ElementTree.parse(xml_file)

    lines = ["\t".join(Article.header) + "\n"]

    for i, doc in enumerate(tree.findall(Article.ename("entry"))):
        article = Article(term)
        article.parse_arxiv(doc)
        pdf_file_name = odir + "pdf/" + term + "/" + article.cur_id + ".pdf"
        article.pdf_file_name = pdf_file_name
        if need_download_pdf:
            savefile_stream(article.link, pdf_file_name)
        article.print_meta()
        articles.append(article)
        lines.append(article.get_line() + "\n")

    with open(csv_file, 'w') as ofile_stats:
        ofile_stats.writelines(lines)


def parse_data_xml_one(xml_file, csv_file, term, need_download_pdf=False):
    articles = []
    tree = ElementTree.parse(xml_file)

    lines = ["\t".join(Article.header) + "\n"]

    for i, doc in enumerate(tree.findall("result-item")):
        article = Article(term)
        article.parse_arxiv(doc)
        pdf_file_name = odir + "pdf/" + term + "/" + article.cur_id + ".pdf"
        article.pdf_file_name = pdf_file_name
        if need_download_pdf:
            savefile_stream(article.link, pdf_file_name)
        article.print_meta()
        articles.append(article)
        lines.append(article.get_line() + "\n")

    with open(csv_file, 'w') as ofile_stats:
        ofile_stats.writelines(lines)


def get_arxiv(term):
    print(term)
    pdf_term_odir = odir + "pdf/" + term + "/"
    txt_term_odir = odir + "txt/" + term + "/"
    os.makedirs(pdf_term_odir, exist_ok=True)

    xml_file = r"{}xml/res_{}_data.xml".format(odir, term)
    if not os.path.exists(xml_file):
        download_data_xml_arxiv(xml_file, term)

    tsv_file = r"{}csv/res_{}_data.tsv".format(odir, term)
    parse_data_xml(xml_file, tsv_file, term, need_download_pdf=False)

    # convert_pdf_dir(pdf_term_odir, txt_term_odir)
    return xml_file, tsv_file


def download_data_xml_one(xml_file, term, start=2017, end=2018):
    print("download_data_xml_one")
    target = "https://www.onepetro.org/search?start={start_pos}&q={q}&from_year={start}&peer_reviewed=&published_between=on&rows={rows}&to_year={end}"
    headers = {'User-Agent':
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36'
                   ' (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    q = term
    start = start
    end = end
    start_pos = 0
    rows = 1000

    total_n = -1

    if True:
        response = requests.get(target.format(q=q, start=start, end=end, start_pos=0, rows=rows), headers=headers)
        ans = response.content
        tree = ElementTree.parse(ans)
        total_n = tree.find("total-results").find("h2").text
        print('total_n:', total_n)

        # with open(xml_file, 'wb') as ofile:
        #     ofile.write(ans)


def get_onepetro(term):
    # print(term)
    # pdf_term_odir = odir + "pdf/" + term + "/"
    # txt_term_odir = odir + "txt/" + term + "/"
    # os.makedirs(pdf_term_odir, exist_ok=True)
    #
    # xml_file = r"{}xml/res_{}_data.xml".format(odir, term)
    # if not os.path.exists(xml_file):
    #     download_data_xml_one(xml_file, term)
    # #
    # tsv_file = r"{}csv/res_{}_data.tsv".format(odir, term)
    # parse_data_xml_one(xml_file, tsv_file, term, need_download_pdf=False)
    # convert_pdf_dir(pdf_term_odir, txt_term_odir)

    html_files = ["static/html/Gmech_13auth_data_group.html",
                  "static/html/Gmech_14auth_data_group.html",
                  "static/html/Gmech_15auth_data_group.html",
                  "static/html/Gmech_16auth_data_group.html",
                  "static/html/Gmech_17auth_data_group.html"

                  ]
    json_files = [
        "static/json/Gmech_13auth_data.json",
        "static/json/Gmech_14auth_data.json",
        "static/json/Gmech_15auth_data.json",
        "static/json/Gmech_16auth_data.json",
        "static/json/Gmech_17auth_data.json",
        "static/json/Gmech_13comp_data.json",
        "static/json/Gmech_14comp_data.json",
        "static/json/Gmech_15comp_data.json",
        "static/json/Gmech_16comp_data.json",
        "static/json/Gmech_17comp_data.json",
    ]
    stats_files = []
    tsv_file = ""
    topic_file = "static/topic/text_ans_text_no_reg_64_64.txt"

    return [tsv_file, topic_file] + html_files + json_files


if __name__ == '__main__':
    print("skygate started")
    terms = ["geomechanics", "rock mechanics"]
    # terms = ["neural networks"]
    # terms = ["rock media", "petroleum rock"]

    for term in terms:
        get_arxiv(term)
        # get_onepetro(term)
