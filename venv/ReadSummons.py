import os
import fitz

pdf_document = "/Users/Leah/Documents/Cavalier CPS/EST/TestSummonses.pdf"
doc = fitz.open(pdf_document)
print('number of pages: %i' %doc.pageCount)
print(doc.metadata)

pgnumber = 0
page1 = doc.loadPage(pgnumber)
page1text = page1.getText("text")
print(str(page1text))



