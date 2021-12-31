import pdfplumber

pdf = pdfplumber.open("아뱅.pdf")
text = ""
for i in range(len(pdf.pages)):
    first_page = pdf.pages[i]
    text += first_page.extract_text()
print(text)
pdf.close()