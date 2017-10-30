import os
import sys
from PIL import Image


__fluff = "*" * 50  # Purely cosmetic purpose ;)
__choices = (1, 2, 3)

__intro_text = "{0}\n" \
               "Welcome to the TextureBox\nCreated By\nAndrew \'teessider\' Bell.\n" \
               "{0}\n" \
               "This command line tool is for packing textures without the need to go into more advanced programs.\n" \
               "For more information on what packing textures means, please visit the Polycount Wiki entry for Channel Packing:\n" \
               "http://wiki.polycount.com/wiki/ChannelPacking\n".format(__fluff)
# For string formatting which includes __choices list, I use automatic one as the choices could expand in the future
__main_choice_text = "Select:\n{}) Create new packed texture from existing ones\n{}) Repack a pre-packed texture \n{}) Exit Program\n\n".format(*__choices)


def main_menu():
    """Displays the main menu of the program which are the user's main choices. Includes exiting the program.
    """
    while True:
        try:
            # This can be done better i feel for now....the choice's are basically copy and paste every time xD
            choice = int(user_input(__main_choice_text))
            if choice in (__choices[0], __choices[1]):
                break
            elif choice == __choices[-1]:
                sys.exit(0)
            else:
                error_response("Invalid number")
                continue
        except ValueError:
            error_response("It must be a number")
            continue
    if choice == __choices[0]:
        create_new_menu()

    elif choice == __choices[1]:
        swizzle_menu()


def create_new_menu():
    print("TO DO")  # Nothing for now ;)
    # 1) Create new texture (from existing ones)
    #   1a) Size - preset or user defined (eg. non-square)


def swizzle_menu():
    """The menu which the user can repack(swizzle) an existing packed texture.\n
    The user can optionally add an alpha channel too.
    """
    swizzle_menu_text = "Select:\n{}) Swap RGB channels\n{}) Add Alpha Channel\n{}) Back to Main Menu\n".format(*__choices)
    while True:
        try:
            choice = int(user_input(swizzle_menu_text))
            if choice in (__choices[0], __choices[1], __choices[-1]):
                break
            else:
                error_response("Invalid number")
                continue
        except ValueError:
            error_response("It must be a number")
            continue
    if choice == __choices[0]:
        swap_rgba()
    elif choice == __choices[1]:
        add_alpha()
    elif choice == __choices[-1]:
        main_menu()


def user_input(text):
    return input("{0}What would you like to do?\n".format(text))


def error_response(response):
    print("{}! Please pick {}, {} or {}\n".format(response, *__choices))


def swap_rgba():
    # Get file input from user - how? Maybe read from a file can be an option (WAY IN THE FUTURE - batching).
    # Put in some facts to verify it is the texture the user wanted to swizzle
    # Needs to be valid file path, supported file extension
    # Support for single and multiple operations (R > G, R > B etc.)
    # Ability to overwrite old file (copy old file just in case)
    # Undo? Or Reset to original texture state

    # input_image = input("Image path: ")
    input_image = "E:\Projects\\test\\test1.tga"  # test file for now
    # input_image = "E:\Projects\\test\\test2_alpha.tga"
    while True:
        try:
            # image1a = "E:\Projects\\test\\test1_16bit.png"
            image = Image.open(input_image)  # type: Image.Image
            print("Opened {file_name}\nFormat: {format}\n"
                  "Size: {size}\nMode: {mode}".format(file_name=os.path.basename(input_image), format=image.format, size=image.size, mode=image.mode))

            if image.mode == 'RGB':
                # Splitting creates copies of the image anyway ;)
                red, green, blue = image.split()
                blue.show()
            elif image.mode == 'RGBA':
                red, green, blue, alpha = image.split()
                alpha.show()
            break

        except IOError:
            print("Can't open the image - Invalid file path or it doesn't exist!\n"
                  "Check the file extension and/or the folder!")
            continue


def add_alpha():
    print("TO DO")

if __name__ == '__main__':
    print(__intro_text)
    main_menu()
