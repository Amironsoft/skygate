import io
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from config import odir
import os
import fnmatch


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                                  password=password,
                                  caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

if __name__ == '__main__':
    print("parse_df started")
    idir = r"data/pdf/"
    odir = r"data/txt/"

    for file in fnmatch.filter(os.listdir(idir), "*.pdf"):
        text = convert_pdf_to_txt(idir+file)
        print(text[:200])
        ofile = odir + file.replace(".pdf", ".txt")
        open(ofile, 'w').write(text)
        print("_"*30)
