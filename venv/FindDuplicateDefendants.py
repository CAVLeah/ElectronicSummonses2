import sys
import os
import fitz
import PyPDF2
import re
import csv

filename = '/Users/Leah/Google Drive (leah@cavaliercps.com)/VDOT/DefendantList.csv'
open_file = (open(filename, 'r'))

defen = ('MACK, ALVERINE').split(',')

def defendant_exists(defendant):
    with open_file as csv_file:
        file = csv.reader(csv_file)
        for row in file:
            if all([x in row for x in defendant]):
                with open('/Users/Leah/Google Drive (leah@cavaliercps.com)/VDOT/Duplicates.csv','a+') as duplicates:
                    duplicates.write('\n' + row[0] + ',' + row[1] + ',' + row[2] + '\n'+ 'MACK, ALVERINE' + ',' + '1/23/19')
                print(row)

def add_defendant(defendant_name, court_date):
    open_file_writer = (open(filename, 'a+'))
    with open_file_writer as file:
        file.write('\n' + defendant_name + ',' + court_date)


defendant_exists(defen)

