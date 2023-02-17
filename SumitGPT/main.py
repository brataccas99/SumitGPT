import openai
import PyPDF2
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


def reduceString(text):
    substrings = []
    for word in text:
        word_substrings = [word[i:i + 85] for i in range(0, len(word), 85)]
        substrings.extend(word_substrings)
        substrings.append(' ')
    if substrings:  # Check if substrings is not empty before removing last item
        substrings.pop()  # Remove the last space character
    return substrings


def write_text_to_pdf(diz, filename):
    c = canvas.Canvas(filename, pagesize=(210 * mm, 297 * mm))
    page_width = c.pagesize[0] - 100
    line_height = 20
    current_x = 50
    page_num = 0
    c.setFont("Helvetica", 18)
    for header, text in diz.items():
        c.drawString(50, 780, header)
        current_y = 700
        c.setFont("Helvetica", 14)
        if text.__contains__('\n\n'):
            text = text.replace('\n\n', '')
        for word in text:
            substrings = reduceString(word)
            for sub in substrings:
                for char in sub:
                    char_width = c.stringWidth(char)
                    if current_x + char_width >= page_width:
                        current_x = 50
                        current_y -= line_height
                    c.drawString(current_x, current_y, char)
                    current_x += char_width
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


def summaryGPT(filename):
    # Set your API key
    openai.api_key = "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"
    # Define the input text
    text = verifyValueLength(makeSingkeValuePerKey(extractFromInput(filename)))

    # Use the GPT-3 API to generate a summary
    model_engine = "text-davinci-003"

    for section, value in text.items():
        if not text[section]:
            continue
        prompt = f"riassumi il seguente testo in meno di {len(value[0])} parole e codificalo in formato utf-8, il testo è il seguente: \n {value[0]}"
        completions = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=len(value[0]), n=1,
                                               stop=None, temperature=0.5)
        text[section] = completions.choices[0].text
    write_text_to_pdf(text, "output.pdf")


def main():
    summaryGPT("Storia_contemporanea_Dalla_Grande_Guerra_a_oggi_Nuova_ediz_Giovanni")


if __name__ == '__main__':
    main()
