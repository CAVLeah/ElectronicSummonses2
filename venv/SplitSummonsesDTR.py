import sys
import os
import fitz
import PyPDF2
import re

pg = 0         #Super simplistic version of what I want to do with the summonses
while pg < 4:
    print(pg)
    pg += 2

pdf_document = input("Enter complete path of docket you wish to split: ")  #The document we're breaking apart.
road = input("Enter the correct road (DTR, 66, or 64): ")
docket_date = input("Enter docket date in the following format: MM-DD-YY ")
save_path = input("Enter the complete path of the folder you wish to save to: ")
payment_sheet = '/Users/Leah/Documents/Cavalier CPS/EST/RCP Process Insert_changes upd April 2019.pdf'
doc = fitz.open(pdf_document)  #Opening the document.
page_count = doc.pageCount  #Total number of pages.
pgs_to_split = []


def only_return_defendant(defendant):
    if len(defendant) > 1:
        defendant.remove(defendant[~(len(defendant)-1)])


def search_summonses(pagetosearch):
    searchpage = doc.loadPage(pagetosearch)  # Load the page you want to search
    pagetext = searchpage.getText("text")  # Extract the page you want to search
    defendant = re.findall('[A-Z]+,\s[A-Z]+', pagetext)  # Search the page
    def remove_incorrect_result(result):
        for line in defendant:
            if line == result:
                defendant.remove(result)
    remove_incorrect_result("MASTER, PAGE")
    remove_incorrect_result("LAST, FIRST")
    remove_incorrect_result("B, N")
    only_return_defendant(defendant)
    print(defendant)


def create_list_of_pgs_to_split():
    pgnumber = 0
    while pgnumber < (page_count-4):
        page1 = doc.loadPage(pgnumber)  # Page number
        page1text = page1.getText("text")  # Extract the page
        defendant_up = re.findall('[A-Z]+,\s[A-Z]+', page1text)  # Search the page
        defendant_low = re.findall('[A-Z][a-z]+,\s[A-Z][a-z]+', page1text)
        if defendant_up == re.findall('[A-Z]+,\s[A-Z]+', doc.loadPage(pgnumber+4).getText("text")):
            pgnumber += 4
        elif defendant_up != re.findall('[A-Z]+,\s[A-Z]+', doc.loadPage(pgnumber+4).getText("text")):
            if len(defendant_low)>2:
                pgs_to_split.append(pgnumber+3)
                pgnumber += 4
            else:
                pgs_to_split.append(pgnumber + 3)
                pgnumber += 4
            print(pgs_to_split)
    pgs_to_split.append(page_count)


def split_summonses(splitpages):
    splitstart = 0  #where the page split begins
    splitend = 0  #where the page split ends
    create_list_of_pgs_to_split()
    while splitend <= len(pgs_to_split):
        first_summons = fitz.open()  #Create new PDF
        first_summons.insertPDF(doc, from_page=splitstart, to_page=splitpages[splitend])  #Determines the range to split the new PDF
        searchpage = doc.loadPage(splitstart)  # Load the page you want to search
        pagetext = searchpage.getText("text")  # Extract the page you want to search
        defendant_up = re.findall('[A-Z]+,\s[A-Z]+', pagetext)  # Search the page for all uppercase
        defendant_low = re.findall('[A-Z][a-z]+,\s[A-Z][a-z]+', pagetext)  #Search the page for normal capitalization

        def remove_incorrect_result(result,list): #Remove results that aren't the defendant
            for line in list:
                if line == result:
                    list.remove(result)

        remove_incorrect_result("MASTER, PAGE",defendant_up)
        remove_incorrect_result("B, N",defendant_up)
        remove_incorrect_result("Express, Plaza",defendant_low)

        only_return_defendant(defendant_up) #call the function that eliminates other results
        only_return_defendant(defendant_low)
        print(defendant_up)

        if len(defendant_up) == 2:
            first_summons.save(save_path + defendant_up[0] + '-' + road + docket_date + '.pdf')
        else:
            first_summons.save(save_path + defendant_up[0] + '-' + road + docket_date + '.pdf')
        splitstart = splitpages[splitend] + 1
        splitend += 1
        print(first_summons.pageCount)
        print(pgs_to_split)
        print()



print(split_summonses(pgs_to_split))


