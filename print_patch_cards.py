import os
import subprocess

from helpers import ImageMagickCommandBuilder


def process_images(input_folder, output_folder, base_image_path):
    for filename in os.listdir(input_folder):
        for i in range(3):
            if i == 0:
                coordinate_x = 90
                coordinate_y = 170
            if i == 1:
                coordinate_x = 90
                coordinate_y = 460
            if i == 2:
                coordinate_x = 355
                coordinate_y = 75
            if filename.endswith(".png"):
                base_cmd = ImageMagickCommandBuilder(resource = base_image_path)

                base_cmd.size(825, 1125)
                base_cmd.extent(825, 1125)
                base_cmd.alpha('transparent')

                input_path = os.path.join(input_folder, filename)

                cmd = ImageMagickCommandBuilder(resource=input_path)

                if i != 2:
                    cmd.filter('Point')
                    cmd.resize(345, 345)
                else:
                    cmd.filter('Point')
                    cmd.resize(245, 245)
                    cmd.command('-distort', 'SRT', '-15')

                cmd.geometry(coordinate_x, coordinate_y)

                base_cmd.parens(cmd)
                base_cmd.composite()

                cmd_args = ['magick'] + base_cmd.parts() + [output_folder + f"/{i}_{filename}"]
                command = ' '.join(cmd_args)
                print(command)

                process = subprocess.Popen(command, stdin = subprocess.PIPE, stdout = subprocess.PIPE,
                                           stderr = subprocess.PIPE)

                stdout, stderr = process.communicate(input =None)

                if process.returncode != 0:
                    print(f"ImageMagick Error: {stderr.decode('utf-8')}")
                    #raise RuntimeError(f"ImageMagick Error: {stderr.decode('utf-8')}")

if __name__ == "__main__":
    input_folder = "./output/sigils"
    output_folder = "./output/patch_cards"
    base_image_path = "./output/transparent_card.png"

    process_images(input_folder, output_folder, base_image_path)
