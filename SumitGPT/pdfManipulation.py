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
    filepath = "C:/Users/roach/Desktop/Storia_contemporanea.pdf"
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


def write_char_to_canvas(c, char, page_width, line_height, current_x, current_y, page_num):
    if char != '\n' and Utilities.detectEncoding(char):
        char = Utilities.convertLatinToUTF8(char)
    char_width = c.stringWidth(char)
    c.drawString(current_x, current_y, char)
    current_x += char_width
    if current_x + char_width >= page_width:
        current_x = 50
        current_y -= line_height
    if current_y <= 50:
        c.showPage()
        page_num += 1
        current_x = 50
        current_y = 700
    return current_x, current_y, page_num


def write_sub_to_canvas(c, sub, page_width, line_height, current_x, current_y, page_num):
    if len(sub) != 1:
        for char in sub:
            current_x, current_y, page_num = write_char_to_canvas(c, char, page_width, line_height, current_x,
                                                                  current_y, page_num)
        current_y -= 80
    else:
        current_x, current_y, page_num = write_char_to_canvas(c, sub, page_width, line_height, current_x, current_y,
                                                              page_num)
        current_y -= 80
    return current_x, current_y, page_num


def write_text_to_canvas(c, diz, page_width, line_height):
    current_x = 50
    page_num = 1
    current_y = 700
    for header, text in diz.items():
        current_y = writeHeader(c, header, current_y)
        text = prepareText(c, text)
        if not text:
            continue
        for sub in text:
            current_x, current_y, page_num = write_sub_to_canvas(c, sub, page_width, line_height, current_x, current_y,
                                                                 page_num)
    c.save()


def write_text_to_pdf(diz):
    c, page_width, line_height, current_x, page_num, current_y = initializeA4Format()
    write_text_to_canvas(c, diz, page_width, line_height)

    print('finito')
