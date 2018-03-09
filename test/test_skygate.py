from parse_pdf import convert_pdf_to_txt


def test_pdf_convert():
    pdf_file = '../data/pdf/wang_fractured_systems.pdf'
    text = convert_pdf_to_txt(pdf_file)
    print(text[:200])
    # ofile = pdf_file.replace(".pdf", ".txt")
    # open(ofile, 'w').write(text)
