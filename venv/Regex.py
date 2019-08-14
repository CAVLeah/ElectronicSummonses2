import re
import fitz

pdf_document = "/Users/Leah/Documents/Cavalier CPS/EST/TestSummonses.pdf"  #The document we're breaking apart.
doc = fitz.open(pdf_document)  #Opening the document.
pgnumber = 16 #Variable for page numbers.
page1 = doc.loadPage(pgnumber)  #Page number
page1text = page1.getText("text")

defendant = re.findall('[A-Z]+,\s[A-Z]+',page1text)

def remove_incorrect_result(result):
    for line in defendant:
        if line == result:
            defendant.remove(result)
remove_incorrect_result("MASTER, PAGE")
remove_incorrect_result("LAST, FIRST")
remove_incorrect_result("B, N")
print(defendant)

