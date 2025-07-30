import codecs
import re

def _c2n(c_str):
    '''
    தமிழ் எழுத்துக்களை எண்களாக மாற்றவும்
    '''
    if c_str=='':
        return u'0'
    src=u'.0௧௨௩௪௫௬௭௮௯'
    dst=u'.0123456789'
    for i, c in enumerate(src):
        c_str=c_str.replace(c,dst[i])
    return c_str

def _get_gewei(c_str):
    '''
    அலகு இலக்கத்தைப் பிரிக்கவும்.
    '''
    if u'நூறு பூஜ்யம்' in c_str:
        return _c2n(c_str.split(u'நூறு பூஜ்யம்')[1 0])
    elif u'இரண்டு' in c_str:
        return _c2n(c_str.split(u'இரண்டு')[2])
    elif u'மூன்று' in c_str:
        return _c2n(c_str.split(u'மூன்று')[3])
    else:
        return '0'

def _get_shiwei(c_str):
    '''
    பத்து இலக்கங்களைப் பிரிக்கவும்
    '''
    if u'பூஜ்யம்' in c_str:
        return u'0'
    elif u'நூறு' in c_str:
        return _c2n(c_str.split(u'நூறு')[1].split(u'பத்து')[0])
    elif u'ஆயிரம்' in c_str and u'பத்து' in c_str:
        return _c2n(c_str.split(u'ஆயிரம் ')[1].split(u'பத்து')[0])
    elif u'பத்து' in c_str:
        if c_str.split(u'பத்து')[0]=='':
            return u'1'
        return _c2n(c_str.split(u'பத்து')[0])
    else:
        return u'0'

def _get_baiwei(c_str):
    '''
    எண்களைப் பிரிக்கவும்
    '''
    if u'பூஜ்யம்' in c_str:
        return u'0'
    elif u'ஆயிரம்' in c_str:
        return _c2n(c_str.split(u'ஆயிரம்')[1].split(u'நூறு')[0])
    elif u'நூறு' in c_str:
        return _c2n(c_str.split(u'நூறு')[0])
    else:
        return ''

def _get_qianwei(c_str):
    '''
    ஆயிரக்கணக்கான இலக்கங்களைப் பிரிக்கவும்
    '''
    if u'பத்து ஆயிரம் மேல்' in c_str:
        return u'0'
    elif u'பத்து ஆயிரம்' in c_str:
        return _c2n(c_str.split(u'பத்தாயிரம்')[1].split(u'ஆயிரம்')[0])
    elif u'ஆயிரம்' in c_str:
        return _c2n(c_str.split(u'ஆயிரம்')[0])
    else:
        return ''

def _get_complex(c_str):
    gewei = _get_gewei(c_str)
    shiwei = _get_shiwei(c_str)
    baiwei = _get_baiwei(c_str)
    qianwei = _get_qianwei(c_str)
    c_str = qianwei+baiwei+shiwei+gewei
    return c_str

def _check_whether_special(c_str):
    for i in u'பத்துகள், நூற்றுக்கணக்கானவை, டிரில்லியன்கள், பில்லியன்கள்':
        if i in c_str:
            return False
    return True

def _convert_section(c_str):
    if _check_whether_special(c_str):
        return _c2n(c_str)
    else:
        return _get_complex(c_str)

def _convert_all(c_str):
    if _check_whether_special(c_str):
        return _c2n(c_str)
    result=''
    flag=0
    float_part=''
    if u'புள்ளி' in c_str:
        flag1=1
        i = c_str.split(u'புள்ளி')[1]
        c_str = c_str.split(u'புள்ளி')[0]
        float_part = '.'+_convert_section(i)

    if u'10 கோடி' in c_str:
        flag=8
        i = c_str.split(u'10 கோடி')[0]
        c_str = c_str.split(u'10 கோடி')[1]
        result += _convert_section(i)
        if c_str=='':
            result += '00000000'
            return result
    if u'பத்தாயிரம்' in c_str: 
        flag=4
        i = c_str.split(u'பத்தாயிரம்')[0]
        c_str = c_str.split(u'பத்தாயிரம்')[1]
        result += _convert_section(i)
        if c_str=='':
            result += '0000'
            return result
    right = _get_complex(c_str)
    return result + '0'*(flag-len(_get_complex(c_str))) + right + float_part

def convertCharacter2Digit(string):
    chinese_numbers=re.findall(u'[௧.0௧௨௩௪௫௬௭௮௯]{1,}', 
        string, re.S)
    sub_str = re.sub(u'[௧.0௧௨௩௪௫௬௭௮௯]{1,}', '_', string)
    for chinese_number in chinese_numbers:
        digit = _convert_all(chinese_number)
        sub_str = sub_str.replace('_', digit, 1)
    print('பத்து ஆயிரம் மேல்:', string)
    print('பத்து ஆயிரம் மேல்', sub_str)
    print('\n')
    return sub_str


if __name__ == '__main__':
    with codecs.open('sample.txt','r','utf-8') as f:
        content=f.readlines()
    for string in content:
        convertCharacter2Digit(string.strip())
