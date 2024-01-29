import generate_station as gs
import process_image as pi

def main():
    gs.check_os()
    gs.delete_pnml_files()
    names_to_replace = gs.get_vox_names()
    gs.replace_names(names_to_replace)
    gs.run_gorender('')
    gs.delete_png_files()
    gs.copy_png_files()
    gs.append_to_lng(names_to_replace)
    gs.append_to_pnml(names_to_replace)
    pi.mirror_image('gfx')
    print('Finish mirroring images.')

if __name__ == "__main__":
    main()