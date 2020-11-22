import os

from google.protobuf import text_format

from protobuf import fonts_public_pb2


def read_font_metadata(path):
    protobuf_file = open(path, 'r')
    protobuf = protobuf_file.read()

    font_family = fonts_public_pb2.FamilyProto()
    text_format.Merge(protobuf, font_family)
    return font_family


def read_all_fonts(root_dir='data/fonts'):
    fonts = []
    for subdir, dirs, files in os.walk(root_dir):
        if 'METADATA.pb' in files:
            md = read_font_metadata(path=f'{subdir}/METADATA.pb')
            for font in md.fonts:
                fonts.append((
                    font.name, font.style, font.weight, f'{subdir}/{font.filename}',
                    font.post_script_name, font.full_name,
                ))
    fonts.sort()
    return fonts
