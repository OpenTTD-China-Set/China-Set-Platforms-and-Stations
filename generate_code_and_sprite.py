import subprocess
import glob
import os
from typing import List

def GetUpdatedFiles(path, type = 'vox', database_path = 'updated_list.txt'):
    '''
    receives: path string, database_path string
    returns: list of files, compares the files in the given path with the database_path
    '''
    def GetLastModifiedTime(file):
        return os.path.getmtime(file)

    def GetModifiedList(input_path):
        try:
            with open(input_path, 'r') as file:
                lines = file.read().splitlines()
        except FileNotFoundError:
            return []

        data = []
        for line in lines:
            items = line.split('|')
            data.append(items)

        return data

    def compare_lists(list1, list2):
        diff = []
        dict2 = {item[0]: item[1] for item in list2}  # convert list to dict

        for item in list1:
            filename = item[0]
            timestamp = item[1]
            if filename not in dict2 or dict2[filename] != str(timestamp):
                # I hate comparing floats with strings. I hate it so much.
                diff.append(filename)

        return diff

    last_modified_time_and_files = [[file, GetLastModifiedTime(file)]
                                    for file in glob.glob(f'{path}/*.{type}')]

    modified_list = GetModifiedList(database_path)
    # write the new list to the file
    with open(database_path, 'w+') as file:
        for item in last_modified_time_and_files:
            file.write(f'{item[0]}|{item[1]}\n')
    return compare_lists(last_modified_time_and_files, modified_list)


def GetFileList(path, type, prefix = '', suffix = ''):
    '''
    receives: path string, type string, prefix string, suffix string
    returns: list of files in path with the given type, prefix and suffix
    '''
    files = glob.glob(f'{path}/{prefix}*{suffix}.{type}')
    return files if files else []


def RunGorender(
        file, param, manifest_path = 'vox/files/manifest.json',
        palette_path = 'vox/files/ttd_palette.json'):
    '''
    receives: file string, param string, manifest_path string, palette_path string
    returns: None, runs gorender with the given parameters
    '''
    subprocess.run(['gorender', '-s', '4', '-m',
                    manifest_path, '-palette', palette_path,
                    '-i', file, param])


def CopyFiles(path, type, target, prefix = '', suffix = ''):
    '''
    receives: path string, type string, target string, prefix string, suffix string
    returns: None, moves files from path to target with the given type, prefix and suffix
    '''
    for file in glob.glob(f'{path}/{prefix}*{suffix}.{type}'):
        os.replace(file, f'{target}/{os.path.basename(file)}')


def DeleteFiles(path, type, prefix = '', suffix = ''):
    '''
    receives: path string, type string, prefix string, suffix string
    returns: None, deletes files from path with the given type, prefix and suffix
    '''
    for file in glob.glob(f'{path}/{prefix}*{suffix}.{type}'):
        os.remove(file)


def ProcessPnmlFile(template_path: str, names_to_replace: str|list) -> str:
    '''
    receives: template_path string, names_to_replace string or list
    returns: string, replaces %name and $name in the template file with the given names_to_replace
    '''
    if isinstance(names_to_replace, str):
        with open(template_path, 'r') as file:
            file_data = file.read()
            file_data = file_data.replace('%name', names_to_replace)
            file_data = file_data.replace('$name', names_to_replace.upper())
    elif isinstance(names_to_replace, list):
        with open(template_path, 'r') as file:
            file_data = file.read()
            for index,name in enumerate(names_to_replace):
                file_data = file_data.replace(f'%name{index}', name)
                file_data = file_data.replace(f'$name{index}', name.upper())
    else:
        raise ValueError('names_to_replace must be a string or a list')
    return file_data


def WriteFile(path, content):
    '''
    receives: path string, content string or list
    returns: None, writes the content to the file in the given path
    '''
    with open(path, 'w+') as file:
        if isinstance(content, list):
            content = '\n'.join(content) if '\n' not in content[0] else '\n'.join(content)
        file.write(content)


def ReadFile(path, type = 'list'):
    '''
    receives: path string, type string
    returns: string or list, reads the file in the given path
    '''
    with open(path, 'r') as file:
        content = file.read()
    return content if type == 'string' else content.splitlines()


def GenerateOtherStations(
        fenced_type: str, target_type: str, target_prefix:str, template_folder: str = 'src',
        input_folder: str = 'generated', target_folder: str = 'generated') -> tuple[list[str], list[str]]:
    '''
    receives: fenced_type string, template_folder string, input_folder string, target_folder string
    returns: None, generates fenced stations from the given template folder and input folder and writes them to the target folder
    '''
    fenced_type_list = GetFileList(input_folder, 'pnml', fenced_type)
    fence_list = GetFileList(input_folder, 'pnml', target_type)
    lng_write_list: List[str] = []
    menu_write_list: List[str] = []

    for item in fenced_type_list:
        item_base_name = os.path.basename(item).split(".")[0]

        for fence in fence_list:
            fence_base_name = os.path.basename(fence).split(".")[0]
            file_write_name = f'{target_prefix}_{item_base_name}_{fence_base_name}'

            file_path = os.path.join(target_folder, f'{file_write_name}.pnml')
            template_path = os.path.join(template_folder, f'{target_prefix}_{fenced_type}.pnml.template')

            content = ProcessPnmlFile(template_path, [item_base_name, fence_base_name, target_prefix])
            lng_write_list.append(f'STR_NAME_{file_write_name.upper():<48}:{file_write_name.replace("_"," ").capitalize()}')
            menu_write_list.append(f'#include "{file_path}"')

            with open(file_path, 'w+') as file:
                file.write(content)

    return lng_write_list, menu_write_list


def main():
    '''
    ### Use argparse to get the command line arguments,
    ### possible arguments are -r or --reprocess to reprocess all the graphics and -f or --fast to enable fast mode.

    Main logic goes here
    this is how this script works: the user will get two options, reprocess all the graphics or only the new ones,
    and if they want to enable fast mode. If the user chooses to reprocess all the graphics, the script will get all the
    files in the vox folder and render them. If the user chooses to only render the new files, the script will only
    render voxel files that are changed or new. After rendering, the script will move the files to the gfx folder and
    delete the old files. Then, the script will process the pnml files and write them to the generated folder. After
    that, the script will append the new pnml files to the cnsplatmenu.pnml file and the new names to the english.lng file.

    Note: this scripte accepts command line arguments, the first argument is for reprocessing all the graphics and the
    second argument is for enabling fast mode.
    '''
    try:
        from tqdm import tqdm
    except ModuleNotFoundError:
        raise ImportError("The tqdm module is required to run this script\n. Please install it with 'pip install tqdm'.")

    import time
    import argparse

    parser = argparse.ArgumentParser(description='Generate code and sprite files')
    parser.add_argument('-r', '--reprocess', action='store_true', help='Reprocess all the graphics')
    parser.add_argument('-f', '--fast', action='store_true', help='Enable fast mode')
    args = parser.parse_args()
    # utilitiy vars
    start_time = time.time()
    ncols_size = int((os.get_terminal_size().columns) * 0.8)
    voxel_list = GetFileList('vox', 'vox')

    # short circuit if there are no files to process
    if args.reprocess:
        render_list = voxel_list
    else:
        render_list = GetUpdatedFiles('vox', 'vox')

    if render_list:
        gorender_param = ''
        if args.fast:
            gorender_param = '-f'
        for item in tqdm(render_list, desc='Rendering', unit='file', ncols = ncols_size):
            RunGorender(item, gorender_param)

        # delete old files in the gfx folder
        if args.reprocess:
            # we only want to delete the files if we are reprocessing all the graphics
            DeleteFiles('gfx', 'png', '', '_32bpp')

        CopyFiles('vox', 'png', 'gfx', '', '_32bpp')
        DeleteFiles('vox', 'png', '', '_8bpp')
        DeleteFiles('vox', 'png', '', '_mask')

    DeleteFiles('generated', 'pnml')
    lng_write_list = ReadFile('lang/english.lng.template')
    menu_write_list = ReadFile('cnsps.pnml.template')

    for item in tqdm(voxel_list, desc = 'Writing', unit='file', ncols = ncols_size):
        file_original_name = (os.path.basename(item)).split('.')[0]
        # if file_original_name.split('_')[-1] == 'mirrored':
        #     continue
        WriteFile(f"generated/{file_original_name}.pnml",
                  ProcessPnmlFile(f'src/{file_original_name.split("_")[0]}.pnml.template', file_original_name))
        lng_write_list.append(f'STR_NAME_{file_original_name.upper():<48}:{" ".join(file_original_name.split("_")[1:]).replace("_"," ").capitalize()}')
        menu_write_list.append(f'#include "generated/{file_original_name}.pnml"')

    menu_write_list.append(ReadFile('cnspsend.pnml.template', 'string'))

    '''
    for item in tqdm(['plt'], desc='Writing fenced stations', unit='file', ncols = ncols_size):
        lng_write_list_func, menu_write_list_func = GenerateOtherStations(item, "fen_")
        lng_write_list.extend(lng_write_list_func)
        menu_write_list.extend(menu_write_list_func)
    '''
    for item in [['fen','plf'], ['she','psh']]:
        for item_2 in tqdm(['plt'], desc=f'Writing, {item[1]}', unit='file', ncols = ncols_size):
            lng_write_list_func, menu_write_list_func = GenerateOtherStations(item_2, item[0], item[1])
            lng_write_list.extend(lng_write_list_func)
            menu_write_list.extend(menu_write_list_func)

    WriteFile('lang/english.lng', lng_write_list)
    WriteFile('cnsps.pnml', menu_write_list)

if __name__ == "__main__":
    main()