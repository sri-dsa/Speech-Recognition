

import re
import os
import codecs

def convertDigit2Character(string): 
    '''
    Main function to be called for converting digits
    into characters in a sentence
    '''
    return _prepString(string)

def _replaceDecimal(decimal_set, sub_str):
    ''' 
    Replacing decimal numbers with Tamil expression
    '''
    dec_str_set = []
    for dec in decimal_set:
        dec_str=_float2Tamil(float(dec))
        dec_str_set.append(dec_str)
    newStr=''
    count=0
    for c in sub_str:
        if c=='_':
            newStr+=dec_str_set[count]
            count+=1
        else:
            newStr+=c
    return newStr
    
def _replaceInteger(integer_set, sub_str):
    ''' 
    Replacing integer numbers with Tamil expression
    '''
    int_str_set = []
    for inte in integer_set:
        int_str=_integer2Tamil(int(inte))
        int_str_set.append(int_str)
    newStr=''
    count=0
    for c in sub_str:
        if c=='_':
            newStr+=int_str_set[count]
            count+=1
        else:
            newStr+=c
    return newStr

def _replaceSpecial(integer_set, sub_str):
    ''' 
    Replacing special numbers with Tamil expression, eg: 2018 ஆண்டு --> ௨௦௧௮
    '''
    charNumSet=['பூஜ்யம்', 'ஒன்று', 'இரண்டு', 'மூன்று', 'நான்கு', 'ஐந்து', 'ஆறு',
'ஏழு', 'எட்டு', 'ஒன்பது']
    int_str_set = []
    for inte in integer_set:
        int_sub_result=''
        for c in inte:
            if c=='ஆண்டு':
                int_sub_result+='ஆண்டு'
            else:
                int_sub_result+=charNumSet[int(c)]
        int_str_set.append(int_sub_result)
    newStr=''
    count=0
    for c in sub_str:
        if c=='_':
            newStr+=int_str_set[count]
            count+=1
        else:
            newStr+=c
    return newStr

def _prepString(string):
    '''
    Preprocessing the sentence and splitting the decimal, integer or special
    '''
    decimal_set = re.findall(r'\d+\.\d+', string)
    sub_str = re.sub(r'\d+\.\d+', '_', string)
    newStr=_replaceDecimal(decimal_set, sub_str)

    integer_set = re.findall(r'\d+ஆண்டு', newStr)
    sub_str = re.sub(r'\d+年', '_', newStr)
    newStr=_replaceSpecial(integer_set, sub_str)

    integer_set = re.findall(r'\d+', newStr)
    sub_str = re.sub(r'\d+', '_', newStr)
    newStr=_replaceInteger(integer_set, sub_str)
    print('அசல் வாக்கியம்:', string)
    print('புதிய வாக்கியங்கள்:', newStr)
    print('\n')
    return newStr

def _section2Tamil(section):
    '''
    Converting section to Tamil expression
    '''
    result=''
    charNumSet=['0', '1', '2', '3', '4',
'5', '6', '7', '8', '9']
    charUnitSet=[, 'பத்து', 'நூறு', 'ஆயிரம்']
    zero=True
    unitPos=0
    while section>0:
        v=section%10
        if v==0:
            if section==0 or zero is False:
                zero=True
                result=charNumSet[v]+result
        elif (section//10)==0 and v==1 and unitPos==1:
            result=charUnitSet[1]+result
        else:
            zero=False
            strIns=charNumSet[v]
            strIns+=charUnitSet[unitPos] 
            result=strIns+result
        unitPos+=1
        section=section//10
    return result

def _integer2Tamil(number):
    '''
    Converting integer to Tamil expression
    '''
    charSectionSet=['', '10,000', '100 மில்லியன்', '1 டிரில்லியன்']
    result=''
    zero=False
    unitPos=0
    if number==0:
        return 'பூஜ்யம்'
    while number>0:
        section=number%10000
        if zero:
            result='பூஜ்யம்'+result
        sec_result = _section2Tamil(section)
        if section!=0:
            sec_result+=charSectionSet[unitPos]
        result=sec_result+result
        if section<1000 and section>0:
            zero=True
        number=number//10000
        unitPos+=1
    return result

def _float2Tamil(number):
    '''
    Converting floating number to Tamil expression
    '''
    charNumSet=['பூஜ்யம்', 'ஒன்று', 'இரண்டு', 'மூன்று', 'நான்கு', 'ஐந்து', 'ஆறு',
'ஏழு', 'எட்டு', 'ஒன்பது']
    integer_part, decimal_part=str(number).split('.')
    int_result=_integer2Tamil(int(integer_part))
    dec_result=''
    for c in decimal_part:
        dec_result+=charNumSet[int(c)]
    return int_result+'புள்ளி'+dec_result

def convertDigit2Character(string): 
    return _prepString(string)

if __name__ == '__main__':
    with codecs.open('sample.txt','r','utf-8') as f:
        content=f.readlines()
    for string in content:
        convertDigit2Character(string.strip())

    '''
    rootdir='/media/pony/DLdigest/data/ASR_zh'
    r1 = re.compile(r'\d+')
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            fullFilename = os.path.join(subdir, file)
            filenameNoSuffix =  os.path.splitext(fullFilename)[0]
            if file.endswith('.label'):
                with open(fullFilename, 'r') as f:
                    line = f.read()
                    if re.match(r1, line):
                        print(fullFilename)
                        try:
                            prepString(line)
                        except IndexError:
                            pass
    '''
