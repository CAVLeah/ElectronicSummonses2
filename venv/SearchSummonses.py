import os
import fitz
import PyPDF2

pg = 0         #Super simplistic version of what I want to do with the summonses
while pg < 4:
    print(pg)
    pg += 2

pdf_document = "/Users/Leah/Documents/Cavalier CPS/EST/TestSummonses.pdf"  #The document we're breaking apart.
doc = fitz.open(pdf_document)  #Opening the document.
page_count = doc.pageCount  #Total number of pages.
pgnumber = 0  #Variable for page numbers.
page1 = doc.loadPage(pgnumber)  #Page number
page1text = page1.getText("text")

def search_summonses():
    pgnumber = 0
    while pgnumber < 32:
        if page1text == doc.loadPage(pgnumber + 3).getText("text"):
            print('yay')
            pgnumber += 3
        else:
            print('sad')
            pgnumber += 3

print(search_summonses())
