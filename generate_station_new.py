import subprocess
import glob
import os

def GetFiles(path, type, prefix = '', suffix = ''):
    files = glob.glob(f'{path}/{prefix}*{suffix}.{type}')
    return files if files else []

def RunGorender(
        files, param, manifest_path = 'vox/files/manifest.json',
        palette_path = 'vox/files/ttd_palette.json'):
    for file in files:
        subprocess.run(['gorender', '-s', '4', '-m',
                        manifest_path, '-palette', palette_path,
                        '-i', file, param])

def CopyFiles(path, type, target, prefix = '', suffix = ''):
    for file in glob.glob(f'{path}/{prefix}*{suffix}.{type}'):
        os.replace(file, f'{target}/{os.path.basename(file)}')

def DeleteFiles(path, type, prefix = '', suffix = ''):
    for file in glob.glob(f'{path}/{prefix}*{suffix}.{type}'):
        os.remove(file)

def ProcessPnmlFile(template_path, names_to_replace):
    with open(template_path, 'r') as file:
        file_data = file.read()
        file_data = file_data.replace('%name', names_to_replace)
        file_data = file_data.replace('$name', names_to_replace.upper())
    return file_data

def AppendToLng(names_to_replace, keyword, path = 'lang/english.lng'):
    with open(path, 'r') as file:
        index = file.read().find(keyword) if file.read() else -1
        if index == -1:
            raise ValueError(f'"{keyword}" not found in {path}')

        content = file.read()[:index]
        for name in names_to_replace:
            content += f'STR_NAME_{name.upper():<30}:{name[3:].replace('_', " ").capitalize()} platform\n'
    return content

def AppendToPnml(names_to_replace, keyword, path):
    with open(path, 'r') as file:
        index = file.read().find(keyword) if file.read() else -1
        if index == -1:
            raise ValueError(f'"{keyword}" not found in {path}')

        content = file.read()[:index]
        for name in names_to_replace:
            content += f'include "{name}.pnml"\n'

def WriteFile(path, content):
    with open(path, 'w') as file:
        file.write(content)

if __name__ == "__main__":
    def ProcessList(list, list1):
        local_list = [(os.path.basename(item)).split('.')[0] for item in list]
        local_list1 = [(os.path.basename(item)).split('.')[0] for item in list1]
        return [item for index, item in enumerate(list) if local_list[index] not in local_list1]

    from tqdm import tqdm
    import time

    start_time = time.time()

    vox_files = GetFiles('vox', 'vox')
    pnml_files = GetFiles('generated', 'pnml')
    if input("Do you want to reprocess all the graphics? (y/n) ") == "y":
        render_list = vox_files
    else:
        render_list = ProcessList(vox_files, pnml_files)

    try:
        if render_list:
            if input("Do you want to enable fast mode? (y/n) ") == "y":
                gorender_param = '-f'
            for file in tqdm.tqdm(render_list, desc='Rendering', unit='file', ncols = 120):
                RunGorender([file], gorender_param)
            for file in tqdm.tqdm(GetFiles('vox', 'png'), desc='Moving', unit='file', ncols = 120):
                CopyFiles('vox', 'png', 'gfx', '', '_32bpp')
                DeleteFiles('vox', 'png', '', '_8bpp')
                DeleteFiles('vox', 'png', '', '_mask')
            for file in tqdm.tqdm(vox_files, desc = 'Writing', unit='file', ncols = 120):
                WriteFile(f'generated/{(os.path.basename(file)).split('.')[0].pnml}',
                          ProcessPnmlFile(f'src/{file[:3]}_template.pnml', file))
                WriteFile('lang/english.lng', AppendToLng(file, f'#{file[:2].upper()}'))
            pnml_files = GetFiles('generated', 'pnml')
            for file in tqdm.tqdm(pnml_files, desc = 'Writing', unit='file', ncols = 120):
                WriteFile('cnsplatmenu.pnml', AppendToPnml(file, f'//{file[:2]}', f'generated/{file}'))

            print("All done!")
    except Exception as e:
        print(f"An error occurred: {e}")

    print("--- %s seconds ---" % (time.time() - start_time))