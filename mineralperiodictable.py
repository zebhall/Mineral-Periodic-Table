

from tkinter import *
from tkinter.ttk import Progressbar, Treeview
from tkinter import ttk, messagebox, filedialog
from tkinter import font as tkFont
from ttkthemes import ThemedTk
import pandas as pd
import xerox
import csv
import time
import re



superrorcount = 0
suberrorcount = 0
tables = []

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

def importMinerals():
    with open('minerals.csv', encoding='utf-8') as file:
        f = csv.reader(file)
        headers = next(f)

        mineralnames_list = []
        mineralformulas_list = []
        mineralelements_list = []

        for row in f:
            #print(row)
            mineralname = row[0]
            mineralnameplain = row[1]
            plainformula = row[2]
            elements = row[3]

            currently_sup = False
            currently_sub = False

            if '[box]' in plainformula:
                plainformula = plainformula.replace('[box]','\u25A1')

            processedformula = ''
            global charfailcount
            charfailcount = 0

            for char in plainformula:

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
            
            #print(f'Processed Formula: {processedformula}')

            elementslist = elements.split(' ')
            # elementsregex = re.compile('[^a-zA-Z]')
            # elementscleanlist = []
            # for e in elementslist:
            #     cleaned = elementsregex.sub('', e)
            #     elementscleanlist.append(cleaned)
            
            mineralnames_list.append(mineralname)
            mineralformulas_list.append(processedformula)
            mineralelements_list.append(elementslist)


            #addMineralToTable(mineralname, processedformula, elementslist)
            

            #if charfailcount >= 1: time.sleep(2)
    global mineral_dataframe
    mineral_dataframe = pd.DataFrame({'Name':mineralnames_list, 'Formula':mineralformulas_list, 'Elements':mineralelements_list})
    #print(mineral_dataframe)
    global mineralCount
    mineralCount = len(mineral_dataframe)
    for index, row in mineral_dataframe.iterrows():
            tables[0].insert(parent='', index=END, text='', values=list(row))

    print(f'Error counts: {superrorcount} sup errors, {suberrorcount} sub errors ')



# COLOURS FOR ELEMENT GROUPS
ALKALI_METALS = '#f7ab59'            #'goldenrod1'
ALKALINE_EARTH_METALS = '#fccc95'    #'DarkOrange1'
TRANSITION_METALS = '#6390FF'        #'RoyalBlue1'
OTHER_METALS = '#93C9FB'     #'SteelBlue1'
METALLOIDS = '#AB93FB'       #'light slate gray'
NON_METALS = '#F993FB'       #'light goldenrod'
HALOGENS = '#FBF593'         #'plum1'
NOBLE_GASES = '#FF6A96'       #'MediumOrchid1'
LANTHANIDES = '#e84f51'     #'firebrick1'
ACTINIDES = '#5bd48f'        #'spring green'


# ELEMENT LIST FOR BUTTONS - FORMAT IS (ATOMIC NUMBER, SYMBOL, NAME, PERIODIC TABLE ROW, PERIODIC TABLE COLUMN, CLASS for bg colour)
element_info = [
    (1, 'H', 'Hydrogen', 1, 1, NON_METALS),
    (2, 'He', 'Helium', 1, 18, NOBLE_GASES),
    (3, 'Li', 'Lithium', 2, 1, ALKALI_METALS),
    (4, 'Be', 'Beryllium', 2, 2, ALKALINE_EARTH_METALS),
    (5, 'B', 'Boron', 2, 13, METALLOIDS),
    (6, 'C', 'Carbon', 2, 14, NON_METALS),
    (7, 'N', 'Nitrogen', 2, 15, NON_METALS),
    (8, 'O', 'Oxygen', 2, 16, NON_METALS),
    (9, 'F', 'Fluorine', 2, 17, HALOGENS),
    (10, 'Ne', 'Neon', 2, 18, NOBLE_GASES),
    (11, 'Na', 'Sodium', 3, 1, ALKALI_METALS),
    (12, 'Mg', 'Magnesium', 3, 2, ALKALINE_EARTH_METALS),
    (13, 'Al', 'Aluminium', 3, 13, OTHER_METALS),
    (14, 'Si', 'Silicon', 3, 14, METALLOIDS),
    (15, 'P', 'Phosphorus', 3, 15, NON_METALS),
    (16, 'S', 'Sulfur', 3, 16, NON_METALS),
    (17, 'Cl', 'Chlorine', 3, 17, HALOGENS),
    (18, 'Ar', 'Argon', 3, 18, NOBLE_GASES),
    (19, 'K', 'Potassium', 4, 1, ALKALI_METALS),
    (20, 'Ca', 'Calcium', 4, 2, ALKALINE_EARTH_METALS),
    (21, 'Sc', 'Scandium', 4, 3, TRANSITION_METALS),
    (22, 'Ti', 'Titanium', 4, 4, TRANSITION_METALS),
    (23, 'V', 'Vanadium', 4, 5, TRANSITION_METALS),
    (24, 'Cr', 'Chromium', 4, 6, TRANSITION_METALS),
    (25, 'Mn', 'Manganese', 4, 7, TRANSITION_METALS),
    (26, 'Fe', 'Iron', 4, 8, TRANSITION_METALS),
    (27, 'Co', 'Cobalt', 4, 9, TRANSITION_METALS),
    (28, 'Ni', 'Nickel', 4, 10, TRANSITION_METALS),
    (29, 'Cu', 'Copper', 4, 11, TRANSITION_METALS),
    (30, 'Zn', 'Zinc', 4, 12, TRANSITION_METALS),
    (31, 'Ga', 'Gallium', 4, 13, OTHER_METALS),
    (32, 'Ge', 'Germanium', 4, 14, METALLOIDS),
    (33, 'As', 'Arsenic', 4, 15, METALLOIDS),
    (34, 'Se', 'Selenium', 4, 16, NON_METALS),
    (35, 'Br', 'Bromine', 4, 17, HALOGENS),
    (36, 'Kr', 'Krypton', 4, 18, NOBLE_GASES),
    (37, 'Rb', 'Rubidium', 5, 1, ALKALI_METALS),
    (38, 'Sr', 'Strontium', 5, 2, ALKALINE_EARTH_METALS),
    (39, 'Y', 'Yttrium', 5, 3, TRANSITION_METALS),
    (40, 'Zr', 'Zirconium', 5, 4, TRANSITION_METALS),
    (41, 'Nb', 'Niobium', 5, 5, TRANSITION_METALS),
    (42, 'Mo', 'Molybdenum', 5, 6, TRANSITION_METALS),
    (43, 'Tc', 'Technetium', 5, 7, TRANSITION_METALS),
    (44, 'Ru', 'Ruthenium', 5, 8, TRANSITION_METALS),
    (45, 'Rh', 'Rhodium', 5, 9, TRANSITION_METALS),
    (46, 'Pd', 'Palladium', 5, 10, TRANSITION_METALS),
    (47, 'Ag', 'Silver', 5, 11, TRANSITION_METALS),
    (48, 'Cd', 'Cadmium', 5, 12, TRANSITION_METALS),
    (49, 'In', 'Indium', 5, 13, OTHER_METALS),
    (50, 'Sn', 'Tin', 5, 14, OTHER_METALS),
    (51, 'Sb', 'Antimony', 5, 15, METALLOIDS),
    (52, 'Te', 'Tellurium', 5, 16, METALLOIDS),
    (53, 'I', 'Iodine', 5, 17, HALOGENS),
    (54, 'Xe', 'Xenon', 5, 18, NOBLE_GASES),
    (55, 'Cs', 'Caesium', 6, 1, ALKALI_METALS),
    (56, 'Ba', 'Barium', 6, 2, ALKALINE_EARTH_METALS),
    (57, 'La', 'Lanthanum', 6, 3, LANTHANIDES),
    (58, 'Ce', 'Cerium', 9, 4, LANTHANIDES),
    (59, 'Pr', 'Praseodymium', 9, 5, LANTHANIDES),
    (60, 'Nd', 'Neodymium', 9, 6, LANTHANIDES),
    (61, 'Pm', 'Promethium', 9, 7, LANTHANIDES),
    (62, 'Sm', 'Samarium', 9, 8, LANTHANIDES),
    (63, 'Eu', 'Europium', 9, 9, LANTHANIDES),
    (64, 'Gd', 'Gadolinium', 9, 10, LANTHANIDES),
    (65, 'Tb', 'Terbium', 9, 11, LANTHANIDES),
    (66, 'Dy', 'Dysprosium', 9, 12, LANTHANIDES),
    (67, 'Ho', 'Holmium', 9, 13, LANTHANIDES),
    (68, 'Er', 'Erbium', 9, 14, LANTHANIDES),
    (69, 'Tm', 'Thulium', 9, 15, LANTHANIDES),
    (70, 'Yb', 'Ytterbium', 9, 16, LANTHANIDES),
    (71, 'Lu', 'Lutetium', 9, 17, LANTHANIDES),
    (72, 'Hf', 'Hafnium', 6, 4, TRANSITION_METALS),
    (73, 'Ta', 'Tantalum', 6, 5, TRANSITION_METALS),
    (74, 'W', 'Tungsten', 6, 6, TRANSITION_METALS),
    (75, 'Re', 'Rhenium', 6, 7, TRANSITION_METALS),
    (76, 'Os', 'Osmium', 6, 8, TRANSITION_METALS),
    (77, 'Ir', 'Iridium', 6, 9, TRANSITION_METALS),
    (78, 'Pt', 'Platinum', 6, 10, TRANSITION_METALS),
    (79, 'Au', 'Gold', 6, 11, TRANSITION_METALS),
    (80, 'Hg', 'Mercury', 6, 12, TRANSITION_METALS),
    (81, 'Tl', 'Thallium', 6, 13, OTHER_METALS),
    (82, 'Pb', 'Lead', 6, 14, OTHER_METALS),
    (83, 'Bi', 'Bismuth', 6, 15, OTHER_METALS),
    (84, 'Po', 'Polonium', 6, 16, METALLOIDS),
    (85, 'At', 'Astatine', 6, 17, HALOGENS),
    (86, 'Rn', 'Radon', 6, 18, NOBLE_GASES),
    (87, 'Fr', 'Francium', 7, 1, ALKALI_METALS),
    (88, 'Ra', 'Radium', 7, 2, ALKALINE_EARTH_METALS),
    (89, 'Ac', 'Actinium', 7, 3, ACTINIDES),
    (90, 'Th', 'Thorium', 10, 4, ACTINIDES),
    (91, 'Pa', 'Protactinium', 10, 5, ACTINIDES),
    (92, 'U', 'Uranium', 10, 6, ACTINIDES),
    (93, 'Np', 'Neptunium', 10, 7, ACTINIDES),
    (94, 'Pu', 'Plutonium', 10, 8, ACTINIDES),
    (95, 'Am', 'Americium', 10, 9, ACTINIDES),
    (96, 'Cm', 'Curium', 10, 10, ACTINIDES),
    (97, 'Bk', 'Berkelium', 10, 11, ACTINIDES),
    (98, 'Cf', 'Californium', 10, 12, ACTINIDES),
    (99, 'Es', 'Einsteinium', 10, 13, ACTINIDES),
    (100, 'Fm', 'Fermium', 10, 14, ACTINIDES),
    (101, 'Md', 'Mendelevium', 10, 15, ACTINIDES),
    (102, 'No', 'Nobelium', 10, 16, ACTINIDES),
    (103, 'Lr', 'Lawrencium', 10, 17, ACTINIDES),
    (104, 'Rf', 'Rutherfordium', 7, 4, TRANSITION_METALS),
    (105, 'Db', 'Dubnium', 7, 5, TRANSITION_METALS),
    (106, 'Sg', 'Seaborgium', 7, 6, TRANSITION_METALS),
    (107, 'Bh', 'Bohrium', 7, 7, TRANSITION_METALS),
    (108, 'Hs', 'Hassium', 7, 8, TRANSITION_METALS),
    (109, 'Mt', 'Meitnerium', 7, 9, TRANSITION_METALS),
    (110, 'Ds', 'Darmstadtium', 7, 10, TRANSITION_METALS),
    (111, 'Rg', 'Roentgenium', 7, 11, TRANSITION_METALS),
    (112, 'Cn', 'Copernicium', 7, 12, TRANSITION_METALS),
    (113, 'Nh', 'Nihonium', 7, 13, OTHER_METALS),
    (114, 'Fl', 'Flerovium', 7, 14, OTHER_METALS),
    (115, 'Mc', 'Moscovium', 7, 15, OTHER_METALS),
    (116, 'Lv', 'Livermorium', 7, 16, OTHER_METALS),
    (117, 'Ts', 'Tennessine', 7, 17, HALOGENS),
    (118, 'Og', 'Oganesson', 7, 18, NOBLE_GASES)]

active_filter_elements = []


def elementZtoSymbol(Z):        # Returns 1-2 character Element symbol as a string
    if Z <= 118:
        elementSymbols = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og']
        return elementSymbols[Z-1]
    else:
        return 'Error: Z out of range'

def elementZtoSymbolZ(Z):       # Returns 1-2 character Element symbol formatted WITH atomic number in brackets
    if Z <= 118:
        elementSymbols = ['H (1)', 'He (2)', 'Li (3)', 'Be (4)', 'B (5)', 'C (6)', 'N (7)', 'O (8)', 'F (9)', 'Ne (10)', 'Na (11)', 'Mg (12)', 'Al (13)', 'Si (14)', 'P (15)', 'S (16)', 'Cl (17)', 'Ar (18)', 'K (19)', 'Ca (20)', 'Sc (21)', 'Ti (22)', 'V (23)', 'Cr (24)', 'Mn (25)', 'Fe (26)', 'Co (27)', 'Ni (28)', 'Cu (29)', 'Zn (30)', 'Ga (31)', 'Ge (32)', 'As (33)', 'Se (34)', 'Br (35)', 'Kr (36)', 'Rb (37)', 'Sr (38)', 'Y (39)', 'Zr (40)', 'Nb (41)', 'Mo (42)', 'Tc (43)', 'Ru (44)', 'Rh (45)', 'Pd (46)', 'Ag (47)', 'Cd (48)', 'In (49)', 'Sn (50)', 'Sb (51)', 'Te (52)', 'I (53)', 'Xe (54)', 'Cs (55)', 'Ba (56)', 'La (57)', 'Ce (58)', 'Pr (59)', 'Nd (60)', 'Pm (61)', 'Sm (62)', 'Eu (63)', 'Gd (64)', 'Tb (65)', 'Dy (66)', 'Ho (67)', 'Er (68)', 'Tm (69)', 'Yb (70)', 'Lu (71)', 'Hf (72)', 'Ta (73)', 'W (74)', 'Re (75)', 'Os (76)', 'Ir (77)', 'Pt (78)', 'Au (79)', 'Hg (80)', 'Tl (81)', 'Pb (82)', 'Bi (83)', 'Po (84)', 'At (85)', 'Rn (86)', 'Fr (87)', 'Ra (88)', 'Ac (89)', 'Th (90)', 'Pa (91)', 'U (92)', 'Np (93)', 'Pu (94)', 'Am (95)', 'Cm (96)', 'Bk (97)', 'Cf (98)', 'Es (99)', 'Fm (100)', 'Md (101)', 'No (102)', 'Lr (103)', 'Rf (104)', 'Db (105)', 'Sg (106)', 'Bh (107)', 'Hs (108)', 'Mt (109)', 'Ds (110)', 'Rg (111)', 'Cn (112)', 'Nh (113)', 'Fl (114)', 'Mc (115)', 'Lv (116)', 'Ts (117)', 'Og (118)']
        return elementSymbols[Z-1]
    else:
        return 'Error: Z out of range'

def elementZtoName(Z):          # Returns Element name 
    if Z <= 118:
        elementNames = ['Hydrogen', 'Helium', 'Lithium', 'Beryllium', 'Boron', 'Carbon', 'Nitrogen', 'Oxygen', 'Fluorine', 'Neon', 'Sodium', 'Magnesium', 'Aluminium', 'Silicon', 'Phosphorus', 'Sulfur', 'Chlorine', 'Argon', 'Potassium', 'Calcium', 'Scandium', 'Titanium', 'Vanadium', 'Chromium', 'Manganese', 'Iron', 'Cobalt', 'Nickel', 'Copper', 'Zinc', 'Gallium', 'Germanium', 'Arsenic', 'Selenium', 'Bromine', 'Krypton', 'Rubidium', 'Strontium', 'Yttrium', 'Zirconium', 'Niobium', 'Molybdenum', 'Technetium', 'Ruthenium', 'Rhodium', 'Palladium', 'Silver', 'Cadmium', 'Indium', 'Tin', 'Antimony', 'Tellurium', 'Iodine', 'Xenon', 'Caesium', 'Barium', 'Lanthanum', 'Cerium', 'Praseodymium', 'Neodymium', 'Promethium', 'Samarium', 'Europium', 'Gadolinium', 'Terbium', 'Dysprosium', 'Holmium', 'Erbium', 'Thulium', 'Ytterbium', 'Lutetium', 'Hafnium', 'Tantalum', 'Tungsten', 'Rhenium', 'Osmium', 'Iridium', 'Platinum', 'Gold', 'Mercury', 'Thallium', 'Lead', 'Bismuth', 'Polonium', 'Astatine', 'Radon', 'Francium', 'Radium', 'Actinium', 'Thorium', 'Protactinium', 'Uranium', 'Neptunium', 'Plutonium', 'Americium', 'Curium', 'Berkelium', 'Californium', 'Einsteinium', 'Fermium', 'Mendelevium', 'Nobelium', 'Lawrencium', 'Rutherfordium', 'Dubnium', 'Seaborgium', 'Bohrium', 'Hassium', 'Meitnerium', 'Darmstadtium', 'Roentgenium', 'Copernicium', 'Nihonium', 'Flerovium', 'Moscovium', 'Livermorium', 'Tennessine', 'Oganesson']
        return elementNames[Z-1]
    else:
        return 'Error: Z out of range'


def addMineralToTable(name, formula, elements):
    tables[0].insert(parent='', index=END, text='', values=(name, formula, elements))
    

def toggleElement(Z):
    global active_filter_elements

    button = buttonIDs[Z-1]
    element = elementZtoSymbol(Z)

    # if Z == 0:
    #     active_filter_elements = []
    #     print(f'Elements cleared. Current filter elements are: {active_filter_elements}')

    if element in active_filter_elements:
        active_filter_elements.remove(element)
        button.configure(bg = element_info[Z-1][5])
        print(f'{element} removed. Current filter elements are: {active_filter_elements}')
    else:
        active_filter_elements.append(element)
        button.configure(bg = 'white')
        print(f'{element} added. Current filter elements are: {active_filter_elements}')

    #print(f'{element} toggled. Current filter elements are: {active_filter_elements}')

    filterMineralTable()


def filterMineralTable():
    global active_filter_elements
    i = 0
    for item in tables[0].get_children():
      tables[0].delete(item)
    for index, row in mineral_dataframe.iterrows():
        if all(elem in row['Elements'] for elem in active_filter_elements):     # check if all active filter elements are in the mineral
            tables[0].insert(parent='', index=END, text='', values=list(row))
            i+=1
    mineralTableStatus.set(f'Minerals: {i}/{mineralCount} ')
    mineralTableFrames[0].configure(text = mineralTableStatus.get())


def clearElements():
    global active_filter_elements
    active_filter_elements = []
    i = 0
    for b in buttonIDs:
        b.configure(bg=element_info[i][5])
        i += 1
    print(f'Elements cleared. Current filter elements are: {active_filter_elements}')
    filterMineralTable()


def mineralSelected(event):
    selection = tables[0].item(tables[0].selection())
    global selected_formula
    global selected_name
    selected_formula = selection['values'][1]
    selected_name = selection['values'][0]
    print(selected_formula)
    xerox.copy(selected_formula)

def clickCopyFormula():
    xerox.copy(selected_formula)

def clickCopyName():
    xerox.copy(selected_name)


gui = Tk()
mineralTableStatus = StringVar()
mineralCount = 0
mineralTableFrames = []



def main():
    gui.title("Mineral Database")
    #gui.wm_attributes('-toolwindow', 'True',)
    gui.geometry('+5+5')
    #iconpath = resource_path("pss.ico")
    #gui.iconbitmap(iconpath)
    #gui.configure(bg = "#F8F9F9")

    # Fonts
    consolas24 = tkFont.Font(family='Consolas', size=24)
    consolas20 = tkFont.Font(family='Consolas', size=20)
    consolas18 = tkFont.Font(family='Consolas', size=18)
    consolas18B = tkFont.Font(family='Consolas', size=18, weight = 'bold')
    consolas16 = tkFont.Font(family='Consolas', size=16)
    consolas14 = tkFont.Font(family='Consolas', size=14)
    consolas14B = tkFont.Font(family='Consolas', size=14, weight = 'bold')
    consolas12 = tkFont.Font(family='Consolas', size=12)
    consolas10 = tkFont.Font(family='Consolas', size=10)
    consolas10B = tkFont.Font(family='Consolas', size=10, weight = 'bold')
    consolas09 = tkFont.Font(family='Consolas', size=9)
    consolas08 = tkFont.Font(family='Consolas', size=8)

    # Style definition for treeview and buttons
    guiStyle = ttk.Style()
    guiStyle.configure('mystyle.Treeview', highlightthickness=0, bd=0, font= consolas10)        # Modify the font of the body
    guiStyle.configure('mystyle.Treeview.Heading', font = consolas10B)                                    # Modify the font of the headings)
    
    # ptable Frame
    ptableFrame = LabelFrame(gui, width = 200, height = 10, pady = 5, padx = 5, fg = "#545454", font = consolas10, text = "Select Elements")
    ptableFrame.grid(row=1, column=1, columnspan=1, pady = 5, padx = 5, sticky= NSEW)

    # ptable Buttons
    global buttonIDs
    buttonIDs = []
    for e in element_info:
        button = Button(ptableFrame, text=(str(e[0])+'\n'+e[1]), width=5, height=2, bg=e[5], font=consolas10, command=lambda Z=int(e[0]): toggleElement(Z))
        button.grid(row=e[3], column=e[4], padx=1, pady=1, ipadx=0, ipady=0, sticky=NSEW)
        buttonIDs.append(button)

    clear_button = Button(ptableFrame, text='CLEAR ALL', width=5, height=2, bg='white', font=consolas10, command=clearElements)
    clear_button.grid(row=10, column=1, padx=1, pady=1, ipadx=0, ipady=0, columnspan=2, sticky=NSEW)


    # # mineral Frame
    # mineralFrame = LabelFrame(gui, width = 200, height = 10, pady = 5, padx = 5, fg = "#545454", font = consolas10, text = "Mineral")
    # mineralFrame.grid(row=2, column=1, columnspan=1, pady = 5, padx = 5, sticky= NSEW)
    # #mineralHTML = HtmlLabel(mineralFrame, text = "<b>NaPb<sup>2+</sup><sub>2</sub>(CO<sub>3</sub>)<sub>2</sub>(OH)</b>")
    # #mineralHTML.grid(row=1, column=1, columnspan=1, pady = 5, padx = 5, sticky= NSEW)
    # labeltest = Label(mineralFrame, font=consolas16, text="C\u2076\u2082")
    # labeltest.grid(row=2, column=1)



    #mineralTable Frame
    mineralTableStatus.set('Minerals')
    mineralTableFrame = LabelFrame(gui, width = 200, height = 10, pady = 5, padx = 5, fg = "#545454", font = consolas10, text = mineralTableStatus.get())
    mineralTableFrame.grid(row=2, column=1, columnspan=1, pady = 5, padx = 5, sticky= NSEW)
    global mineralTableFrames
    mineralTableFrames.append(mineralTableFrame)

    mineralColumns = ('t_name', 't_formula', 't_elements')
    mineralTable = Treeview(mineralTableFrame, columns = mineralColumns, height = "20", selectmode = "extended", style = 'mystyle.Treeview', show = 'headings')
    tables.append(mineralTable)
    mineralTable.grid(column=1, row=1, padx=0, pady=0, rowspan = 40, columnspan = 20, sticky = NSEW)

    mineralTable.heading('t_name', text = "Mineral Name", anchor = W)                  
    mineralTable.heading('t_formula', text = "Formula", anchor = W)                 
    mineralTable.heading('t_elements', text = "Elements", anchor = W)

    mineralTable.column('t_name', minwidth = 50, width = 190, anchor = W)
    mineralTable.column('t_formula', minwidth = 50, width = 500, anchor = W)
    mineralTable.column('t_elements', minwidth = 50, width = 150, anchor = W)

    mineralTableScrollbar = Scrollbar(mineralTableFrame, orient=VERTICAL, bg = 'red', command=mineralTable.yview)
    mineralTableScrollbar.grid(column=21, row=1, rowspan = 40, padx=0, pady=0, sticky = NS)
    mineralTable.configure(yscroll=mineralTableScrollbar.set)

    mineralTable.bind('<<TreeviewSelect>>', mineralSelected)

    copyFormula = Button(mineralTableFrame, width = 8, text = "Copy Formula", font = consolas10, fg = "#FDFEFE", bg = "#566573", command=clickCopyFormula)
    copyFormula.grid(column=2, row=42, padx=5, pady=5, ipadx=5, ipady=0, sticky=EW)

    copyName = Button(mineralTableFrame, width = 4, text = "Copy Name", font = consolas10, fg = "#FDFEFE", bg = "#566573", command=clickCopyName)
    copyName.grid(column=1, row=42, padx=5, pady=5, ipadx=5, ipady=0, sticky=EW)

    # formulas = ['PbS','C\u2076\u2082','PbCu']
    # formula = 'C\u2076\u2082'
    # xerox.copy(formulas[1])

    importMinerals()
    mineralTableStatus.set(f'Minerals: {mineralCount}/{mineralCount} ')
    mineralTableFrames[0].configure(text = mineralTableStatus.get())

    gui.mainloop()

if __name__ == "__main__": 
    main()