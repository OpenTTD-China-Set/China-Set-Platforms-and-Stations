import os
import glob
import subprocess

def check_os():
    if os.name != 'nt':
        raise SystemExit('This script can only be run on Windows.')

def delete_pnml_files():
    for file in glob.glob('src/stn_*.pnml'):
        os.remove(file)

def get_vox_names():
    return [os.path.splitext(os.path.basename(file))[0] for file in glob.glob('vox/*.vox')]

def replace_names(names_to_replace):
    for name_to_replace in names_to_replace:
        with open('src/station_template.pnml', 'r') as file:
            file_data = file.read()

        file_data = file_data.replace('%name', name_to_replace)
        file_data = file_data.replace('$name', name_to_replace.upper())

        with open(f'src/stn_{name_to_replace}.pnml', 'w') as file:
            file.write(file_data)

def run_gorender():
    for file in glob.glob('vox/*.vox'):
        subprocess.run(['gorender', '-s', '4', '-m', 'vox/files/manifest.json', '-palette', 'vox/files/ttd_palette.json', '-i', file])

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

    # 保留 # class 1 及其之前的内容
    index += len('# class 1')
    content = content[:index]

    # 添加新的文本，使文本对齐
    for name in names_to_replace:
        content += f'\nSTR_NAME_{name.upper():<20}:Platform {name}'

    # 覆盖写入 english.lng 文件
    with open('lang/english.lng', 'w') as file:
        file.write(content)

def main():
    check_os()
    delete_pnml_files()
    names_to_replace = get_vox_names()
    replace_names(names_to_replace)
    run_gorender()
    delete_png_files()
    copy_png_files()
    append_to_lng(names_to_replace)
    print('Done!')

if __name__ == "__main__":
    main()