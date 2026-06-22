from pypdf import PdfReader


def extract_text(uploaded_files):

    text = ""

    for pdf in uploaded_files:

        reader = PdfReader(pdf)

        for page in reader.pages:

            content = page.extract_text()

            if content:

                text += content + "\n"

    return text