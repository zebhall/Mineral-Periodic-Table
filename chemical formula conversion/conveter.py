
# this script is supposed to take a CSV file export from the RRUFF database (https://rruff.info/ima/), and convert it to a format usable by mineralperiodictable.
# the downloaded CSV file should have the following export options (columns):
# Mineral Name (plain)
# IMA Chemistry (concise)
# Valence Elements



import csv
import time

superrorcount = 0
suberrorcount = 0

def sup(char):
    char = str(char)
    match char:
        case '0': return '\u2070' 
        case '1': return '\u00B9'
        case '2': return '\u00B2'
        case '3': return '\u00B3'
        case '4': return '\u2074'
        case '5': return '\u2075'
        case '6': return '\u2076'
        case '7': return '\u2077'
        case '8': return '\u2078'
        case '9': return '\u2079'
        case '+': return '\u207A'
        case '-': return '\u207B'
        case '=': return '\u207C'
        case '(': return '\u207D'
        case ')': return '\u207E'
        case ',': return ' '
        case ' ': return ' '
        case _: 
            global superrorcount
            superrorcount += 1
            global charfailcount
            charfailcount += 1
            return '&'

            
def sub(char):
    char = str(char)
    match char:
        case '0': return '\u2080' 
        case '1': return '\u2081'
        case '2': return '\u2082'
        case '3': return '\u2083'
        case '4': return '\u2084'
        case '5': return '\u2085'
        case '6': return '\u2086'
        case '7': return '\u2087'
        case '8': return '\u2088'
        case '9': return '\u2089'
        case '+': return '\u208A'
        case '-': return '\u208B'
        case '=': return '\u208C'
        case '(': return '\u208D'
        case ')': return '\u208E'
        case '.': return '.'
        case 'Σ': return '\u03A3'
        case '/': return '/'
        case 'x': return '\u2093'   #subscript x
        case 'y': return '\u1D67'   #subscript ᵧ
        case 'z': return '\u1D69'   #subscript ᵩ   
        case 'm': return '\u2098'
        case 'a': return '\u2090'
        case 'n': return '\u2099'
        case ' ': return ' '
        case '~': return '~'
        case _: 
            global suberrorcount
            suberrorcount += 1
            global charfailcount
            charfailcount += 1
            return '&'



with open('minerals.csv', encoding='utf-8') as file:
    f = csv.reader(file)
    headers = next(f)
    for row in f:
        print(row)
        mineralname = row[1]
        plainformula = row[2]
        elements = row[3]

        currently_sup = False
        currently_sub = False

        if '[box]' in plainformula:
            plainformula = plainformula.replace('[box]','\u25A1')

        processedformula = ''
        charfailcount = 0

        for char in plainformula:
            newchar = ''
            
            if char == '_':
                currently_sub = not currently_sub
                continue
            if char == '^':
                currently_sup = not currently_sup
                continue
            
            if currently_sub*currently_sup:
                print('Error: both superscript and subscript?')
                break

            if currently_sub:
                processedformula += sub(char)
                continue
            
            if currently_sup:
                processedformula += sup(char)
                continue

            if char == 'z':
                processedformula += '\u03D5'
                continue

            processedformula += char
        
        print(f'Processed Formula: {processedformula}')

        

        if charfailcount >= 1: time.sleep(2)

print(f'Error counts:  sup errors {superrorcount}, sub errors {suberrorcount}')


# html to unicode