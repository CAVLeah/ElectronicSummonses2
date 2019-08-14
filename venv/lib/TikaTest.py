import os
import fitz
import PyPDF2
import re

pg = 0         #Super simplistic version of what I want to do with the summonses
while pg < 4:
    print(pg)
    pg += 2

pdf_document = "/Users/Leah/Documents/Cavalier CPS/EST/TestSummonses.pdf"  #The document we're breaking apart.
doc = fitz.open(pdf_document)  #Opening the document.
page_count = doc.pageCount  #Total number of pages.
pgs_to_split = []

def only_return_defendant():
    if len(defendant) > 1:
        defendant.remove(defendant[~(len(defendant)-1)])

def search_summonses():
    pgnumber = 0  # type: int
    while pgnumber < (page_count-4):
        page1 = doc.loadPage(pgnumber)  # Page number
        page1text = page1.getText("text")  # Extract the page
        defendant = re.findall('[A-Z]+,\s[A-Z]+', page1text)  # Search the page
        if defendant == re.findall('[A-Z]+,\s[A-Z]+', doc.loadPage(pgnumber+4).getText("text")):
            pgnumber += 4
        else:
            pgs_to_split.append(pgnumber+3)
            pgnumber += 4

def split_summonses(splitpages):
    splitstart = 0
    splitend = 0
    search_summonses()
    while splitend < len(pgs_to_split):
        first_summons = fitz.open()
        first_summons.insertPDF(doc, from_page=splitstart, to_page=splitpages[splitend])
        page = doc.loadPage(9)
        split_summons = page.getText('text')
        print(first_summons.pageCount)
        print(pgs_to_split)
        print(len(pgs_to_split))



print(split_summonses(pgs_to_split))

