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


def create_list_of_pgs_to_split():
    pgnumber = 0
    while pgnumber < (page_count-4):
        page1 = doc.loadPage(pgnumber)  # Page number
        page1text = page1.getText("text")  # Extract the page
        defendant_up = re.findall('[A-Z]+,\s[A-Z]+', page1text)  # Search the page in uppercase
        defendant_low = re.findall('[A-Z][a-z]+,\s[A-Z][a-z]+', page1text)  #Search the page including lowercase
        if defendant_up == re.findall('[A-Z]+,\s[A-Z]+', doc.loadPage(pgnumber+4).getText("text")): #First summons pages are the same
            pgnumber += 4
        elif defendant_up != re.findall('[A-Z]+,\s[A-Z]+', doc.loadPage(pgnumber+4).getText("text")): #First summons pages aren't the same
            if len(defendant_low)>2:  #Defedant's name includes lowercase
                pgs_to_split.append(pgnumber+3)
                pgnumber += 4
            else:  #Defendant's number is completely capitalized.
                pgs_to_split.append(pgnumber + 3)
                pgnumber += 4
            print(pgs_to_split)
    pgs_to_split.append(page_count)

create_list_of_pgs_to_split()
print(page_count)
print(pgs_to_split)
