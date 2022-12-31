import os
import random
import io
from fontTools.ttLib import TTFont
from string import ascii_letters
from bs4 import BeautifulSoup as BS


text = """
    In an invited talk to the 63rd Annual Meeting 
    of the American Physical Society Division of Plasma
    Physics on November 8, 2021,[2] the National Ignition Facility
    claimed[3] to have triggered ignition in the laboratory on
    Sunday, August 8, 2021 for the first time
    in the over-60-year history of the ICF program.[4][5] 
    The shot yielded 1.3 megajoules of fusion energy, an 8-fold
    improvement on tests done in spring 2021.[3]
    NIF estimates that 230 kJ of energy reached the fuel capsule,
    which resulted in an almost 6-fold energy output
    from the capsule.[3] A researcher from Imperial College
    London stated that the majority of the field agreed
    that ignition had been demonstrated.[3]
    In August 2022, the results of the experiment
    were confirmed in three peer-reviewed papers:
    one in Physical Review Letters and two
    in Physical Review E.[6] Researchers at NIF tried
    to replicate the August result without success.[7]
    However, on December 11, 2022, the US Department of Energy
    said it would announce a "major scientific
    breakthrough" which was believed to be
    that scientists at the National Ignition Facility
    at the Lawrence Livermore National Laboratory in California
    managed to trigger ignition.[8] On December 13,
    2022, the US Department of Energy announced on 
    Twitter that fusion ignition has been reached.[9]
    """


def g():
    
    chars = list(ascii_letters)  # list of all letters
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

    font = TTFont("font.ttf")
    file = io.StringIO()
    font.saveXML(file) # convert font to XML
    soup = BS(file.getvalue(), features='xml')

    glyphs = soup.find_all('TTGlyph') # list of <TTGlyph> tags
    for glyph in glyphs:
        for k, v in dict.items():
            if glyph['name'] == k:
                glyph['name'] = v # swap name attribute
                break

    new_file = 'new.xml'
    with open(new_file, 'w') as f:
        f.write(str(soup)) # write changed XML to file

    os.system(f'ttx -f -d static {new_file}') # execute fonttools command; convert XML to TTF

    return new_text
