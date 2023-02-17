from pdfManipulation import write_text_to_pdf, verifyValueLength, extractFromInput, makeSingkeValuePerKey
from openAi import openAiCallSummary


def summaryGPT(filename):
    # Define the input text
    text = verifyValueLength(makeSingkeValuePerKey(extractFromInput(filename)))
    print('hola')
    write_text_to_pdf(openAiCallSummary(text))


def main():
    summaryGPT("Storia_contemporanea_Dalla_Grande_Guerra_a_oggi_Nuova_ediz_Giovanni")


if __name__ == '__main__':
    main()
