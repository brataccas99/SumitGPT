import PyPDF2
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import Utilities


def CheckNewParagraphStartingWithNumber(header):
    if (header.startswith('1') and header[1] == '.') or (header.startswith('2') and header[1] == '.') \
            or (header.startswith('3') and header[1] == '.'):
        return True
    return False


def getSections(text):
    lines = text.split('\n')
    result = {}
    current_header = None
    current_section = []
    for line in lines:
        if CheckNewParagraphStartingWithNumber(line) or (len(line) < 40 and not line.endswith('.')):
            if current_header is not None:
                result[current_header] = current_section
                current_section = []
            current_header = line
        else:
            current_section.append(line)
    result[current_header] = current_section
    for key in list(result.keys()):
        if CheckNewParagraphStartingWithNumber(key):
            if not result[key]:
                del result[key]
    return result


def extractFromInput(filename):
    page_text = ''
    filepath = "C:/Users/roach/PycharmProject/SumitGPT/SumitGPT/input.pdf"
    with open(filepath, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in range(len(pdf_reader.pages)):
            page_text += pdf_reader.pages[page].extract_text()
    return getSections(page_text)


def initializeA4Format():
    c = canvas.Canvas('output.pdf', pagesize=(210 * mm, 297 * mm))
    page_width = c.pagesize[0] - 100
    line_height = 20
    current_x = 50
    page_num = 0
    current_y = 780
    return c, page_width, line_height, current_x, page_num, current_y


def writeHeader(c, header, current_y):
    c.setFont("Times-Roman", 18)
    c.drawString(50, current_y, header)
    current_y -= 50
    return current_y


def prepareText(c, text):
    c.setFont("Times-Roman", 14)
    if text.__contains__('\n\n'):
        text = text.replace('\n\n', '')
    if text.__contains__('Codificato in formato UTF-8:'):
        text = text.replace('Codificato in formato UTF-8:', '')
    if len(text) > 4000:
        text = Utilities.reduceString(text)
    return text


def write_text_to_pdf(diz):
    c, page_width, line_height, current_x, page_num, current_y = initializeA4Format()
    for header, text in diz.items():
        current_x = 50
        current_y = writeHeader(c, header, current_y)
        text = prepareText(c, text)
        if not text:
            continue
        for sub in text:
            if sub != '\n' and Utilities.detectEncoding(sub):
                sub = Utilities.convertLatinToUTF8(sub)
            char_width = c.stringWidth(sub)
            c.drawString(current_x, current_y, sub)
            current_x += char_width
            if current_x + char_width >= page_width:
                current_x = 50
                current_y -= line_height
            if current_y <= 50:
                c.showPage()
                page_num += 1
                current_x = 50
                current_y = 700
        current_y -= 80
    c.save()
    print('finito')
