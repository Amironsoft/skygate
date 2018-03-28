from xml.etree import ElementTree

import requests


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
        ans = str(response.content)
        print([l for l in ans.split('\n') if "has returned " in l])
        # print('total_n:', total_n)

if __name__ == '__main__':
    download_data_xml_one("test.xml", "geomechanics")
