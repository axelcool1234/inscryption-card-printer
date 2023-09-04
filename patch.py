import subprocess
from helpers import ImageMagickCommandBuilder
IM = ImageMagickCommandBuilder

class Patch:
    base = 'resource'
    scale = 1

    def __init__(self, filename, type):
        self.filename = filename
        if type == 'patch':
            self.original_patch_height = 85 # px
        else:
            self.original_patch_height = 75 # px

    def generate_patch_image(self):
        im = self.initialize_image_builder()
        im = self.add_patch_background(im)
        im = self.add_sigil(im)
        return self.generate_image_buffer(im)


    def initialize_image_builder(self):
        im = IM()
        im.background('None')
        im.filter('Box')
        return im

    def add_patch_background(self, im):
        directory = f'{self.base}/patches'
        background_path = f'{directory}/patch.png'
        im.resource(background_path)
        return im

    def add_sigil(self, im):
        directory = f'{self.base}/sigils'
        sigil_path = f'{directory}/{self.filename}.png'
        for i in [False, True]:
            sigil = IM(sigil_path).command('-fill', 'rgb(161,247,186)', '-colorize', '100').resizeExt(lambda g: g.scale(self.scale * 100)).gravity('Center')
            if i == True:
                sigil.command('-blur', '0x1')
            im.parens(sigil).composite()
        return im

    def generate_image_buffer(self, im):
        return buffer_from_command_builder(im)

def buffer_from_command_builder(im, input_data=None, filetype='PNG'):
    command_args = ['magick'] + im.parts() + [f'{filetype}:-']
    command = ' '.join(command_args)
    print(command)
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = process.communicate(input=input_data)

    if process.returncode != 0:
        print(f"ImageMagick Error: {stderr.decode('utf-8')}")
        #raise RuntimeError(f"ImageMagick Error: {stderr.decode('utf-8')}")

    return stdout







