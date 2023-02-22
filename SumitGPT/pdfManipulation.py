import PyPDF2
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import Utilities


def CheckNewParagraphStartingWithNumber(header: str):
    """
        This function checks if a line is a paragraph start and so checks if starts with a number between 1 and 3
        and 3 followed with a dot
        @param header the string to check
        @return boolean the result of the check
        """
    if (header.startswith('1') and header[1] == '.') or (header.startswith('2') and header[1] == '.') \
            or (header.startswith('3') and header[1] == '.'):
        return True
    return False


def getSections(text: str):
    """
        This function creates a dictionary based on the lines of the given string in the dictionary
        key are the headers identified by absence of the "." and lenght<40 chars or returns true on check
        @param text the text to check
        @return a dictionary where the division will be stored
        """
    # problema: dividere meglio i sotto-titoli, se hai una stringa del tipo "paure delle potenze mondiali. la guerra come occasione"
    # in questo caso "la guerra come occasione" deve essere trattato come header, quindi estratto dalla stringa
    lines = Utilities.removeTrashList(text.split('\n'))
    result = {}
    current_header = None
    current_section = []
    for line in lines:
        # da rivedere questa condizione per smistare meglio header e value, inoltre refactorarlo in altre piccole funzioni
        if CheckNewParagraphStartingWithNumber(line) or (40 > len(line) > 15 and not line.endswith('.')):
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


def extractFromInput(filename: str):
    """
        This function extracts the text from the specified pdf file
        @param filename: the path of the file where is the input
        @return a dictionary where the header are keys and text are the values
        """
    page_text = ''
    filepath = filename
    with open(filepath, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in range(len(pdf_reader.pages)):
            page_text += pdf_reader.pages[page].extract_text()
    return getSections(page_text)


def initializeA4Format():
    """
        This function initialize variables to fit the A4 format for pdf
        @return c: Canvas library object
        @return current_x: the current horizontal position of the cursor which will write the char in pdf
        @return current_y: the current vertical position of the cursor which will write the char in pdf
        @return page_width: number indicating the left page width
        @return line_height: number indicating the left page height
        @return page_num: number of pages
        """
    c = canvas.Canvas('output.pdf', pagesize=(210 * mm, 297 * mm))
    page_width = c.pagesize[0] - 100
    line_height = 20
    current_x = 50
    page_num = 0
    current_y = 780
    return c, page_width, line_height, current_x, page_num, current_y


def writeHeader(c: canvas, header: str, current_y: int):
    """
        This function writes a string as header then update the value of x and y cursors, it also sets font and size for the header
        @param c: Canvas library object
        @param current_y: the current vertical position of the cursor which will write the char in pdf
        @param header: the current string to write as header
        @return current_x: the current horizontal position of the cursor which will write the char in pdf assigning it to the value 50
        @return current_y: the modified vertical position of the cursor which will write the char in pdf
        """
    c.setFont("Times-Roman", 18)
    c.drawString(50, current_y, header)
    current_y -= 50
    return current_y, 50


def prepareText(c: canvas, text: str):
    """
        This function checks if the text contains useless elements and removes it, if the string is longer than 4000 it split it into 2 strings and appends both to a list of strings
        @param text: long string to write in the pdf as the value after the header
        @param c: Canvas library object
        @return text: the modified long string if necessary in both string or list of strings made by reduceString()
        """
    c.setFont("Times-Roman", 14)
    if text.__contains__('\n\n'):
        text = text.replace('\n\n', '')
    if text.__contains__('Codificato in formato UTF-8:'):
        text = text.replace('Codificato in formato UTF-8:', '')
    if len(text) > 4000:
        text = Utilities.reduceString(text)
    return text


def write_char_to_canvas(c: canvas, char: str, page_width: int, line_height: int, current_x: int, current_y: int, page_num: int):
    """
        This function takes a char and writes it into a pdf, it also adjust the cursors x,y and update page number
        @param c: Canvas library object
        @param char: the char to write in the pdf
        @param current_x: the current horizontal position of the cursor which will write the char in pdf
        @param current_y: the current vertical position of the cursor which will write the char in pdf
        @param page_width: number indicating the left page width
        @param line_height: number indicating the left page height
        @param page_num: number of pages
        @return current_x: the modified horizontal position of the cursor which will write the char in pdf
        @return current_y: the modified vertical position of the cursor which will write the char in pdf
        @return page_num: the modified number of pages if necessary
        """
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


def write_sub_to_canvas(c: canvas, sub: str, page_width: int, line_height: int, current_x: int, current_y: int, page_num: int):
    """
        This function
        @param c: Canvas library object
        @param sub: the string to write in the pdf
        @param current_x: the current horizontal position of the cursor which will write the char in pdf
        @param current_y: the current vertical position of the cursor which will write the char in pdf
        @param page_width: number indicating the left page width
        @param line_height: number indicating the left page height
        @param page_num: number of pages
        @return current_x: the modified horizontal position of the cursor which will write the char in pdf
        @return current_y: the modified vertical position of the cursor which will write the char in pdf
        @return page_num: the modified number of pages if necessary
        """
    if isinstance(sub, list):
        for char in sub:
            current_x, current_y, page_num = write_char_to_canvas(c, char, page_width, line_height, current_x,
                                                                  current_y, page_num)
        current_y -= 80
    else:
        current_x, current_y, page_num = write_char_to_canvas(c, sub, page_width, line_height, current_x, current_y,
                                                              page_num)

    return current_x, current_y, page_num


def write_text_to_canvas(c: canvas, diz: dict, page_width: int, line_height: int):
    """
        This function write text into the output pdf
        @param c: Canvas library object
        @param diz: dictionary
        @param page_width: number indicating the left page width
        @param line_height: number indicating the left page height
        """
    current_x = 50
    page_num = 1
    current_y = 700
    count = 0
    for header, text in diz.items():
        current_y, current_x = writeHeader(c, header, current_y)
        text = prepareText(c, text)
        if not text:
            continue
        for sub in text:
            current_x, current_y, page_num = write_sub_to_canvas(c, sub, page_width, line_height, current_x, current_y,
                                                                 page_num)
        current_y -= 80
        count += 1
        if count == 4:
            break
    c.save()


def write_text_to_pdf(diz: dict):
    """
       This function takes the formatted dictionary and gives it to write_text_to_canvas(), additionally it initialize the pdf to be in A4 format calling initializeA4Format()
       @param diz the dictionary with the text
       """
    c, page_width, line_height, current_x, page_num, current_y = initializeA4Format()
    write_text_to_canvas(c, diz, page_width, line_height)

    print('finito')
