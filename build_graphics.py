import generate_station as gs
import process_image as pi
import os

def main():
    gs.delete_pnml_files()
    names_to_replace = gs.get_vox_names()
    gs.replace_names(names_to_replace)
    gs.run_gorender('')
    gs.delete_png_files()
    gs.copy_png_files()
    gs.append_to_lng(names_to_replace)
    gs.append_to_pnml(names_to_replace)
    pi.mirror_image('gfx')
    print('Done!')

if __name__ == "__main__":
    if os.name != 'nt':
        raise SystemExit('This script can only be run on Windows.')
    main()