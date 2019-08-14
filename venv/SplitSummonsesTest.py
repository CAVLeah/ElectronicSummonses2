mport os
import fitz
import PyPDF2
import re


pdf_document = "/Users/Leah/Documents/Cavalier CPS/EST/TestSummonses.pdf"  #The document we're breaking apart.
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


def split_summonses(splitpages):
    splitstart = 0  #where the page split begins
    splitend = 0  #where the page split ends
    create_list_of_pgs_to_split()
    while splitend <= len(pgs_to_split):
        first_summons = fitz.open()  #Create new PDF
        first_summons.insertPDF(doc, from_page=splitstart, to_page=splitpages[splitend])  #Determines the range to split the new PDF
        searchpage = doc.loadPage(splitstart)  # Load the page you want to search
        pagetext = searchpage.getText("text")  # Extract the page you want to search
        defendant = re.findall('[A-Z]+,\s[A-Z]+', pagetext)  # Search the page

        def remove_incorrect_result(result): #Remove results that aren't the defendant
            for line in defendant:
                if line == result:
                    defendant.remove(result)

        remove_incorrect_result("MASTER, PAGE")
        remove_incorrect_result("B, N")
        remove_incorrect_result("Express, Plaza")

        only_return_defendant(defendant) #call the function that eliminates other results
        print(defendant)
        first_summons.save('/Users/Leah/Documents/Cavalier CPS/EST/' + defendant[1] +'.pdf')
        splitstart = splitpages[splitend] + 1
        splitend += 1
        print(first_summons.pageCount)
        print(pgs_to_split)



print(split_summonses(pgs_to_split))

