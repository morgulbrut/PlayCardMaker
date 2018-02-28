#!/usr/bin/env python3
import csv
import subprocess
from string import Template
import os

def generate_card(card_no):
    col = cardstripecols[card_no].strip('#')
    ret =  '\definecolor{tempcolor}{HTML}{'+col+'}\n'
    ret += '\\begin{tikzpicture}\n'
    # Image if any
    try:
        ret += '\cardbackground{' + cardimgs[card_no] + '}\n'
    except TypeError:
        pass
    # card type
    try:
        ret += '\cardtype{tempcolor}{'+cardtypes[card_no].upper()+'}\n'
    except TypeError:
        pass

    try:
        ret += '\cardcontent{' + cardtexts1[card_no] + '}{'+ cardtexts2[card_no] + '}\n'
    except TypeError:
        pass
    ret += '\cardborder\n'
    ret += '\end{tikzpicture}\n'
    return ret

def generate_cards():
    ret = ''
    for card_id in range(len(cardtypes)):
        ret += generate_card(card_id)
        if card_id % 9 == 8:
            ret += '\n\pagebreak\n'
        elif card_id % 3 == 2:
            ret += '\n\\vspace{5mm}\n'
        else:
            ret += '\hspace{5mm}\n'
    return ret

def generate_markers():
    ret = ''
    for i in [1,2,5]:
        for c in range(30):
            ret += '\\begin{tikzpicture}\n'
            ret += '\\markerborder\n'
            ret += '\\marker{'+str(i)+'}\n'
            ret += '\end{tikzpicture}\n'
            if c % 42 == 41:
                ret += '\n\pagebreak\n'
            elif c % 6 == 5:
                ret += '\n\\vspace{2mm}\n'
            else:
                ret += '\hspace{2mm}\n'
    return ret

def generate_field():
    ret = ''
    for i in range(120):
        ret += '\\begin{tikzpicture}\n'
        ret += '\\fieldborder\n'
        ret += '\\field{'+str(i)+'}\n'
        ret += '\end{tikzpicture}\n'
        if i % 10 == 9:
            ret += '\n\\vspace{1mm}\n'
        else:
            ret += '\hspace{1mm}\n'
    return ret

cardtitles = []
cardtexts1 = []
cardtexts2 = []
cardimgs = []
cardtypes = []
cardstripecols = []

with open('input/cards.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cardtitles.append(row["cardtitle"])
        cardtexts1.append(row['cardtext1'])
        cardtexts2.append(row['cardtext2'])
        cardtypes.append(row['class'])
        cardimgs.append(row['cardimg'])
        cardstripecols.append(row['cardstripecol'])

cards = generate_cards()
markers = generate_markers()
field = generate_field()

d = {'cards':cards, 'markers':markers, 'field':field}

template_file = open('input/game_template.tex')
template = Template(template_file.read())

with open('game.tex','w') as outfile:
    outfile.write(template.substitute(d))

subprocess.call(["xelatex", "-interaction=nonstopmode", "game.tex"])
