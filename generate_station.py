import os
import glob
import subprocess

def delete_pnml_files():
    for file in glob.glob('generated/*.pnml'):
        os.remove(file)

def get_vox_names():
    return [os.path.splitext(os.path.basename(file))[0] for file in glob.glob('vox/stn_*.vox')]

def get_roof_names():
    return [os.path.splitext(os.path.basename(file))[0] for file in glob.glob('vox/roof_*.vox')]

def replace_names(names_to_replace):
    for name_to_replace in names_to_replace:
        with open('src/station_template.pnml', 'r') as file:
            file_data = file.read()

        file_data = file_data.replace('%name', name_to_replace)
        file_data = file_data.replace('$name', name_to_replace.upper())

        with open(f'generated/{name_to_replace}.pnml', 'w') as file:
            file.write(file_data)

def run_gorender(gorender_param):
    # to enable fast mode, add '-f' to the command line
    files = glob.glob('vox/*.vox')
    counter = 0
    total_files = len(files)
    align = len(str(total_files))
    for file in files:
        counter += 1
        print(f'{counter:<{align}}/{total_files} Processing {file}...')
        subprocess.run(['gorender', '-s', '4', '-m', 'vox/files/manifest.json', '-palette', 'vox/files/ttd_palette.json', '-i', file, gorender_param])

def delete_png_files():
    for file in glob.glob('gfx/*.png'):
        if os.path.basename(file) != 'empty.png':
            os.remove(file)

def copy_png_files():
    for file in glob.glob('vox/*_32bpp.png'):
        os.replace(file, os.path.join('gfx', os.path.basename(file)))
    for file in glob.glob('vox/*_8bpp.png'):
        os.remove(file)
    for file in glob.glob('vox/*_mask.png'):
        os.remove(file)

def append_to_lng(names_to_replace):
    with open('lang/english.lng', 'r') as file:
        content = file.read()

    index = content.find('# class 1')
    if index == -1:
        raise ValueError('# class 1 not found in english.lng')

    # keep # class 1 and its previous content
    index += len('# class 1')
    content = content[:index]

    # add new text, align the text
    for name in names_to_replace:
        content += f'\nSTR_NAME_{name.upper():<48}:Platform {name}'

    # write to english.lng file
    with open('lang/english.lng', 'w') as file:
        file.write(content)

def append_to_pnml(names_to_replace):
    with open('cnsplatmenu.pnml', 'r') as file:
        content = file.read()

    index = content.find('// stations')
    if index == -1:
        raise ValueError('// stations not found in cnsplatmenu.pnml')

    # keep // stations and its previous content
    index += len('// stations')
    content = content[:index]

    # add new text
    for name in names_to_replace:
        content += f'\n#include "generated/{name}.pnml"'

    # write to cnsplatmenu.pnml file
    with open('cnsplatmenu.pnml', 'w') as file:
        file.write(content)