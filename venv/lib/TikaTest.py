from tika import parser

raw = parser.from_file('/Users/Leah/Documents/Cavalier CPS/EST/TestSummonses.pdf')
print(raw['content'])