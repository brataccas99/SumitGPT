import PyPDF2
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from openAi import convertToUTF
import chardet


def convertLetter(c):
    return convertToUTF(c)


def detectEncoding(s):
    if ord(s) > 127:
        byte_str = s.encode()
        result = chardet.detect(byte_str)
        if result['encoding'] != 'ascii':
            return True
    return False


def reduceString(text):
    substrings = []
    for word in text:
        word_substrings = [word[i:i + 85] for i in range(0, len(word), 85)]
        substrings.extend(word_substrings)
        substrings.append(' ')
    if substrings:  # Check if substrings is not empty before removing last item
        substrings.pop()  # Remove the last space character
    return substrings


def prepareA4Format():
    c = canvas.Canvas('output.pdf', pagesize=(210 * mm, 297 * mm))
    page_width = c.pagesize[0] - 100
    line_height = 20
    current_x = 50
    page_num = 0
    return c, page_width, line_height, current_x, page_num


def writeHeader(c, header):
    c.setFont("Helvetica", 18)
    c.drawString(50, 780, header)


def prepareText(c, text):
    c.setFont("Helvetica", 14)
    if text.__contains__('\n\n'):
        text = text.replace('\n\n', '')
    if text.__contains__('Codificato in formato UTF-8:'):
        text = text.replace('Codificato in formato UTF-8:', '')
    return text


def write_text_to_pdf(diz):
    c, page_width, line_height, current_x, page_num = prepareA4Format()
    for header, text in diz.items():
        writeHeader(c, header)
        current_y = 700
        text = prepareText(c, text)
        for word in text:
            substrings = reduceString(word)
            for sub in substrings:
                if detectEncoding(sub):
                    sub = convertToUTF(sub)
                char_width = c.stringWidth(sub)
                if current_x + char_width >= page_width:
                    current_x = 50
                    current_y -= line_height
                c.drawString(current_x, current_y, sub)
                current_x += char_width
                if current_y < 50:
                    c.showPage()
                    page_num += 1
                    current_x = 50
                    current_y = 700
        if not text:
            continue
        c.showPage()
        current_x = 50
        page_num += 1
    c.save()
    print('finito')


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


def makeSingkeValuePerKey(diz):
    return {k: " ".join(v) for k, v in diz.items()}


def verifyValueLength(dictionary):
    result = {}
    for k, v in dictionary.items():
        result[k] = [v[i:i + 4097] for i in range(0, len(v), 4097)]
    return result
