import os
import random
import io
from fontTools.ttLib import TTFont
import string
from bs4 import BeautifulSoup as BS

def font_mod(text):
    chars = list(string.ascii_letters)  # list of all letters
    random.shuffle(chars)
    half = int(len(chars) / 2)
    first_half = chars[:half]
    second_half = chars[half:]

    dict1 = {k: v for (k, v) in zip(first_half, second_half)} # create letter pairs
    dict2 = {v: k for (k, v) in dict1.items()} # reverse all pairs
    dict = {**dict1, **dict2} # join dicts 

    new_text = ''

    for char in text: 
        if char in dict.keys():
            new_text += dict[char] # append corresponding letter
            continue
        new_text += char # append original letter

    font = TTFont("static/ShareTechMono-Regular.ttf")
    file = io.StringIO()
    font.saveXML(file) # convert font to XML
    soup = BS(file.getvalue(), features='xml')

    glyphs = soup.find_all('TTGlyph') # list of <TTGlyph> tags
    for glyph in glyphs:
        for k, v in dict.items():
            if glyph['name'] == k:
                glyph['name'] = v # swap name attribute
                break

    random_string = ''.join(random.choice(
        string.ascii_letters + string.digits
    ) for _ in range(10))

    new_file = f'{random_string}.xml'

    with open(new_file, 'w') as f:
        f.write(str(soup)) # write changed XML to file

    os.system(f'ttx -f -d output {new_file}') # execute fonttools command; convert XML to TTF

    return new_text, random_string # modified text and random query to prevent caching   
