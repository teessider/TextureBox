import os
import sys

from PIL import Image

import texturebox.core

_fluff = "*" * 50  # Purely cosmetic purpose ;)
_choices = (1, 2, 3)

_intro_text = "{0}\n" \
               "Welcome to the TextureBox\nCreated By\nAndrew \'teessider\' Bell.\n" \
               "{0}\n" \
               "This command line tool is for packing textures without the need to go into more advanced programs.\n" \
               "For more information on what packing textures means, please visit the Polycount Wiki entry for Channel Packing:\n" \
               "http://wiki.polycount.com/wiki/ChannelPacking\n".format(_fluff)
# For string formatting which includes _choices list, I use automatic one as the choices could expand in the future
_main_choice_text = "Select:\n{0}) Create new packed texture from existing ones\n{1}) Repack a pre-packed texture \n{2}) Exit Program\n\n".format(*_choices)


RGB = 'RGB'
RGBA = RGB + 'A'
GRAY = 'L'


def main_menu():
    """Displays the main menu of the program which are the user's main choices. Includes exiting the program.
    """
    while True:
        try:
            # This can be done better i feel for now....the choice's are basically copy and paste every time xD
            choice = int(input_question(_main_choice_text))
            if choice in _choices[:2]:
                break
            elif choice == _choices[2]:
                sys.exit(0)
            else:
                error_response("Invalid number")
                continue
        except ValueError:
            error_response("It must be a number")
            continue
    if choice == _choices[0]:
        create_new_menu()

    elif choice == _choices[1]:
        swizzle_menu()


def create_new_menu():
    print("TO DO")  # Nothing for now ;)
    # 1) Create new texture (from existing ones)
    #   1a) Size - preset or user defined (eg. non-square)


def swizzle_menu():
    """The menu which the user can repack(swizzle) an existing packed texture.\n
    The user can optionally add an alpha channel too.
    """
    swizzle_menu_text = "Select:\n{0}) Swap RGB channels\n{1}) Add Alpha Channel\n{2}) Back to Main Menu\n".format(*_choices)
    while True:
        try:
            choice = int(input_question(swizzle_menu_text))
            if choice in _choices:
                break
            else:
                error_response("Invalid number")
                continue
        except ValueError:
            error_response("It must be a number")
            continue
    if choice == _choices[0]:
        swizzle_rgba()
    elif choice == _choices[1]:
        add_alpha()
    elif choice == _choices[2]:
        main_menu()


def swizzle_rgba():
    # TODO: Get file input from user - Maybe also reading from a file can be an option (WAY IN THE FUTURE - batching).
    # Support for single and multiple operations (R > G, R > B etc.)?
    # Ability to overwrite old file (copy old file just in case)
    # Undo? Or Reset to original texture state

    # input_image = "E:\\Projects\\test\\test1.tga"  # test file for now
    # input_image = "E:\\Projects\\test\\test2_alpha.tga"  # also test file for now
    while True:
        try:
            # TODO: Make sure path is valid (as it needs to have \\ as the directories)
            input_image = input("Image path: ")
            image_dir = os.path.dirname(input_image)
            image_name = os.path.basename(input_image)
            image_ext = os.path.splitext(input_image)[1]

            with Image.open(input_image) as image:  # type: Image.Image
                print("Opened {file_name}\nFormat: {format}\nSize: {size}\nMode: {mode}".format(file_name=image_name, format=image.format, size=image.size, mode=image.mode))

                new_image = texturebox.core.ChannelPack(image)
                try:
                    new_image.swizzle(new_image.parse_input(input("Which channels should be swapped?\nPlease use the form: {}\n".format(new_image.form_text))))
                except TypeError:
                    # Would be cool to have the none existing channel in the error message.
                    print("One of the specified channels does not exist in the original texture!\n")
                    continue

                # TODO: Continue with what happens after the operation has been done - another menu with another operation or to save file(overwrite old one or make new one(then new filename))?
                # For now the new file is saved in the same folder as the old one.
                saved_image = save_image(image_dir, image, new_image, image_ext)

                if saved_image:
                    print("Saved to: {}\n".format(os.path.normpath(image_dir)))
                    main_menu()

        except IOError:
            print("Can't open the image - Invalid file path or it doesn't exist!\nCheck the file extension and/or the folder!")
            continue


def add_alpha():
    print("TO DO")


def input_question(text):
    return input("{0}What would you like to do?\n".format(text))


def error_response(response):
    print("{0}! Please pick {1}, {2} or {3}\n".format(response, *_choices))


def save_image(directory, old_image, new_image, extension):
    while True:
        try:
            save_response = input("Save the file? ").upper()
            if save_response == 'Y':
                merged_image = new_image.merge(mode=RGB) if old_image.mode == RGB else new_image.merge(mode=RGBA)  # type: Image.Image

                merged_file = os.path.join(directory, input("New Image name (without extension): ") + extension)

                merged_image.save(merged_file)
                return True
            elif save_response == 'N':
                new_image.swizzle(new_image.parse_input(input("Which channels should be swapped?\nPlease use the form: {}\n".format(new_image.form_text))))
                return False
            else:
                raise ValueError
        except ValueError:
            print("Invalid response! Please pick \'Y\' or \'N\'")
            continue


if __name__ == '__main__':
    print(_intro_text)
    main_menu()
