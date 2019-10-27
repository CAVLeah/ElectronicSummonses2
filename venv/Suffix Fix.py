import sys
import os
import fitz
import PyPDF2
import re
import csv
import subprocess


pdf_document = input("Enter complete path of docket you wish to split: ")  #The document we're breaking apart.
doc = fitz.open(pdf_document)  #Opening the document.
page_count = doc.pageCount  #Total number of pages.


def search_summonses():
    splitend = 0
    while splitend <= 611:
        splitstart = 0  # where the page split begins
        searchpage = doc.loadPage(pagetosearch)  # Load the page you want to search
        pagetext = searchpage.getText("text")  # Extract the page you want to search
        defendant_up = re.findall('[A-Z]+,\s[A-Z]+', pagetext)  # Search the page for all uppercase
        defendant_low = re.findall('[A-Z][a-z]+,\s[A-Z][a-z]+', pagetext)  # Search the page for normal capitalization
        defendant_suffix = re.findall('[A-Z]+\s[A-Z]+,\s[A-Z]+', pagetext)
        print(defendant_up)
        print(defendant_low)
        print(defendant_suffix)
        splitstart += 1
        splitend += 1

search_summonses()