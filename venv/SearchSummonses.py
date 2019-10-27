import os
import fitz
import PyPDF2
import re

pg = 0         #Super simplistic version of what I want to do with the summonses
while pg < 4:
    print(pg)
    pg += 2

pdf_document = "/Users/Leah/Google Drive (leah@cavaliercps.com)/VDOT/Norfolk 64/092319 - 64/09-23-199-23 i64.pdf"  #The document we're breaking apart.
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

def search_summonses():
    pgnumber = 0
    while pgnumber < (page_count - 4):
        page1 = doc.loadPage(pgnumber)  # Page number
        searchpage = doc.loadPage(pgnumber)  # Load the page you want to search
        pagetext = searchpage.getText("text")  # Extract the page you want to search
        defendant = re.findall('[A-Z]+,\s[A-Z]+', pagetext)  # Search the page
        defendantsuffix = re.findall('[A-Z]+\s[A-Z]+,\s[A-Z]+', pagetext)
        pgnumber += 4
        if defendantsuffix[0] = True
            badresult = re.findall(',\sVA',defendantsuffix[0])
            if badresult[0] = True
                defendantsuffix.remove(defendantsuffix[0])
        print(defendantsuffix)

search_summonses()