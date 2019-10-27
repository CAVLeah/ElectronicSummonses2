import sys
import os
import fitz
import PyPDF2
import re
import csv
import subprocess


pdf_document = input("Enter complete path of docket you wish to split: ")  #The document we're breaking apart.
road = input("Enter the correct road (DTR, 66, or 64): ")
docket_date = input("Enter docket date in the following format: MM-DD-YY ") #Court date for the summonses
save_path = input("Enter the complete path of the folder you wish to save to: ") #Path of the folder we're saving everything to
payment_sheet = '/Users/Leah/Documents/Cavalier CPS/EST/RCP Process Insert_changes upd April 2019.pdf'
doc = fitz.open(pdf_document)  #Opening the document.
page_count = doc.pageCount  #Total number of pages.
pgs_to_split = []
filename = '/Users/Leah/Google Drive (leah@cavaliercps.com)/VDOT/DefendantList.csv' #CSV that defendants are saved to.

def compress_toll_docs(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".pdf"):
                filename = os.path.join(root, file)
                print (filename)
                print (file)
                arg1= '-sOutputFile=' + folder + docket_date + file  #added a c to the filename
                p = subprocess.Popen(['/usr/local/Cellar/ghostscript/9.27_1/bin/gs',
                                    '-sDEVICE=pdfwrite',
                                    '-dCompatibilityLevel=1.4',
                                    '-dPDFSETTINGS=/ebook', '-dNOPAUSE',
                                    '-dBATCH', '-dQUIET', str(arg1), filename],
                                    stdout=subprocess.PIPE)
                print (p.communicate())

def add_defendant(defendant_name, court_date):
    open_file_writer = (open(filename, 'a+'))
    with open_file_writer as file:
        file.write('\n' + defendant_name + ',' + court_date)

def defendant_exists(defendant):
    open_file = (open(filename, 'r'))
    with open_file as csv_file:
        file = csv.reader(csv_file)
        for row in file:
            if all([x in row for x in defendant]):
                with open(save_path + 'Duplicates.csv','a+') as duplicates:
                    duplicates.write('\n' + row[0] + ',' + row[1] + ',' + row[2] + '\n'+ defendant[0] + ',' + defendant[1] + ',' + docket_date)
                print(row)

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
    print(len(pgs_to_split))
    while splitend <= len(pgs_to_split)-1:
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
        print(defendant_low)

        append_doc = fitz.open(payment_sheet)
        first_summons.insertPDF(append_doc)

        if (defendant_low[0]) != 'Blvd, Rm':
            def1 = defendant_low[0].split(',')
            defendant_exists(def1)
            first_summons.save(save_path + ' ' + defendant_low[0] + '.pdf')
            add_defendant(defendant_low[0],docket_date)
        elif len(defendant_up) == 2:
            def2 = defendant_up[1].split(',')
            defendant_exists(def2)
            first_summons.save(save_path + ' ' + defendant_up[1] + '.pdf')
            add_defendant(defendant_up[1],docket_date)
        else:
            def3 = defendant_up[0].split(',')
            defendant_exists(def3)
            first_summons.save(save_path + ' ' + defendant_up[0] + '.pdf')
            add_defendant(defendant_up[0],docket_date)
        splitstart = splitpages[splitend] + 1
        splitend += 1
        print(first_summons.pageCount)
        print(pgs_to_split)


print(split_summonses(pgs_to_split))
compress_toll_docs(save_path)
