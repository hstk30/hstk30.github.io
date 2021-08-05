import re
p = re.compile(r'\d+')
p.findall('12 drummers drumming, 11 pipers piping, 10 lords a-leaping')
p = re.compile('\d+')
p.findall('12 drummers drumming, 11 pipers piping, 10 lords a-leaping')
p = re.compile('\section')
p.findall('wegwg\section')
p = re.compile(r'\section')
p.findall('wegwg\section')
p = re.compile(r'\\section')
p.findall('wegwg\section')
p = re.compile(r'\\\\section')
p.findall('wegwg\section')
p = re.compile(r'\\\section')
p.findall('wegwg\section')
'\s'
'\\t'
'\\a'
'\a'
p = re.compile('\\\\section')
p.findall('wegwg\section')
p = re.compile('\section')
p.findall('wegwg\section')
p = re.compile(r'\\section')
p = re.compile('\\section')
p.findall('wegwg\section')
p = re.compile('\\pection')
p = re.compile('\\pection')
p = re.compile('\\pection')
p = re.compile('\\\pection')
'\p'
p.findall('wegwg\pection')
p = re.compile(r'\pection')
p = re.compile(r'\\pection')
p.findall('wegwg\pection')
p = re.compile('\section')
p.findall('wegwg\section')
p = re.compile('\\section')
p.findall('wegwg\section')
p = re.compile('\\\section')
p.findall('wegwg\section')
p = re.compile(r'\\section')
p.findall('wegwg\section')
'\s'
'\\\secotr'
'\\\\secotr'
'\\\\\secotr'
'\\\\\\secotr'
'\\\\\\tecotr'
'\\\\\tecotr'
'\\\\tecotr'
'\\\tecotr'
'\\tecotr'
'\tecotr'
'\t ecotr'
'\t'
'\\t'
'个人股\t'
'个人股\t gfweg'
'个人股\n gfweg'
print('gweg \t weg')
print('gweg \n weg')
print('\s')
print('\\s')
print('\\\s')
print('\\\\s')
print('\\\\t')
print('\\\t')
print('\\\tfewg')
p = re.compile('\section')
p.findall('wegwg ection')
p = re.compile('\pection')
p = re.compile('\\pection')
p = re.compile('\\\pection')
p.findall('wegwg\pection')
p = re.compile('\\\\pection')
p.findall('wegwg\pection')
p = re.compile('\tection')
p.findall('wegwg\tection')
print(p.findall('wegwg\tection')[0])
print('\s')
print('\s')
print('\\s')
print('\\t')
print('\t')
'\'
print('\')
print('\\')
'\\'
？print
? print
%history -f re_escape.py
