from PIL import Image
import os
import shutil
from enum import IntEnum

if os.path.exists("resourcepack/"):
    shutil.rmtree("resourcepack/")

class PaintingSizes(IntEnum):
    ONE_X_ONE = 0
    TWO_X_ONE = 1
    ONE_X_TWO = 2
    TWO_X_TWO = 3
    FOUR_X_TWO = 4
    FOUR_X_THREE = 5
    FOUR_X_FOUR = 6

paintings_and_sizes = {
    'alban': PaintingSizes.ONE_X_ONE,
    'aztec': PaintingSizes.ONE_X_ONE,
    'aztec2': PaintingSizes.ONE_X_ONE,
    'bomb': PaintingSizes.ONE_X_ONE,
    'kebab': PaintingSizes.ONE_X_ONE,
    'plant': PaintingSizes.ONE_X_ONE,
    'wasteland': PaintingSizes.ONE_X_ONE,

    'courbet': PaintingSizes.TWO_X_ONE,
    'pool': PaintingSizes.TWO_X_ONE,
    'sea': PaintingSizes.TWO_X_ONE,
    'creebet': PaintingSizes.TWO_X_ONE,
    'sunset': PaintingSizes.TWO_X_ONE,

    'graham': PaintingSizes.ONE_X_TWO,
    'wanderer': PaintingSizes.ONE_X_TWO,

    'bust': PaintingSizes.TWO_X_TWO,
    'match': PaintingSizes.TWO_X_TWO,
    'skull_and_roses': PaintingSizes.TWO_X_TWO,
    'stage': PaintingSizes.TWO_X_TWO,
    'void': PaintingSizes.TWO_X_TWO,
    'wither': PaintingSizes.TWO_X_TWO,

    'fighters': PaintingSizes.FOUR_X_TWO,

    'donkey_kong': PaintingSizes.FOUR_X_THREE,
    'skeleton': PaintingSizes.FOUR_X_THREE,

    'burning_skull': PaintingSizes.FOUR_X_FOUR,
    'pigscene': PaintingSizes.FOUR_X_FOUR,
    'pointer': PaintingSizes.FOUR_X_FOUR,
}
paintings_wanted = {}

def make_gif_sheet(path: str, painting_type: int) -> Image.Image:
    if painting_type < PaintingSizes.ONE_X_ONE and painting_type > PaintingSizes.FOUR_X_FOUR:
        return None

    w: int = 0
    h: int = 0
    match painting_type:
        case PaintingSizes.ONE_X_ONE:
            w, h = 16, 16
        case PaintingSizes.TWO_X_ONE:
            w, h = 32, 16
        case PaintingSizes.ONE_X_TWO:
            w, h = 16, 32
        case PaintingSizes.TWO_X_TWO:
            w, h = 32, 32
        case PaintingSizes.FOUR_X_TWO:
            w, h = 64, 32
        case PaintingSizes.FOUR_X_THREE:
            w, h = 64, 48
        case PaintingSizes.FOUR_X_FOUR:
            w, h = 64, 64
        case other:
            ...

    im = Image.open(path)
    nframes = im.n_frames
    target = Image.new('RGBA', (w, h*nframes))

    for i in range(nframes):
        newsize = (w, h)
        target.paste(im.resize(newsize), (0, h*i))
        im.seek(i)

    return target

dirs_path = "resourcepack/assets/minecraft/textures/painting/"
os.makedirs(dirs_path, exist_ok=True)

def setup_resource_pack(image: Image.Image, pname: str):
    '''
    name.zip
    |_assets/
      |_minecraft/
        |_textures/
          |_painting/
            |_burning_skull.png
            |_burning_skull.png.mcmeta
    |_pack.mcmeta
    |_pack.png
    '''
    pack_mcmeta_str = '''{
    "pack": {
        "pack_format": 13,
        "description": "Woo-hoo"
    }
}
    '''
    pack_png = Image.effect_noise((64, 64), 200)
    img_png_mcmeta_str = '''{
    "animation": {}
}
    '''

    os.chdir("resourcepack/")

    # Write data
    f = open("pack.mcmeta", "w")
    f.write(pack_mcmeta_str)

    pack_png.save('pack.png')

    f = open(f"assets/minecraft/textures/painting/{pname}.png.mcmeta", "w")
    f.write(img_png_mcmeta_str)

    image.save(f'assets/minecraft/textures/painting/{pname}.png')
    print(pname)

    f.close()

print("Possible painting names and sizes:")
for k, v in paintings_and_sizes.items():
    size_str = ""
    match v:
        case 0: size_str = "1x1"
        case 1: size_str = "2x1"
        case 2: size_str = "1x2"
        case 3: size_str = "2x2"
        case 4: size_str = "4x2"
        case 5: size_str = "4x3"
        case 6: size_str = "4x4"

    print(f"|{k}: {size_str}|", end='')

print()

while True:
    entry_split = input("> ").split("|")
    if entry_split[0] == "q":
        break

    try:
        paintings_wanted[entry_split[0]] = [entry_split[1], paintings_and_sizes[entry_split[0]]]
    except KeyError:
        print("hello")
        exit(1)

for pname, pdata in paintings_wanted.items():
    gif_name = pdata[0]
    psize = pdata[1]
    pic = make_gif_sheet(gif_name, psize)
    setup_resource_pack(pic, pname)
    os.chdir("..")

shutil.make_archive("out", "zip", "resourcepack/")
shutil.rmtree("resourcepack/")
