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


RGB = 'RGB'
RGBA = RGB + 'A'
GRAY = 'L'


class ChannelPacker(object):
    # Takes in a string like "R <> G" and so do Image.merge(RGB or RGBA, (green, red, blue))
    # TODO: Need to change input and output as it doesn't make sense if user input is like the example above.
    def __init__(self, image, _input, output):
        self.image = image
        self._input = _input
        self.output = output
        self.output = output
        self.new_channels = ()

    def swizzle(self, mode=RGB):
        """
        Swizzles the two input channels of an RGB or RGBA texture.\n
        Returns:
            tuple: Swizzled texture channels ready to be merged into new texture.
        """
        if mode == RGB:
            if (self._input == 'R' and self.output == 'G') or (self._input == 'G' and self.output == 'R'):
                self.new_channels = (self.image.get_channel(1), self.image.get_channel(0), self.image.get_channel(2))
            elif (self._input == 'G' and self.output == 'B') or (self._input == 'B' and self.output == 'G'):
                self.new_channels = (self.image.get_channel(0), self.image.get_channel(2), self.image.get_channel(1))
            elif (self._input == 'B' and self.output == 'R') or (self._input == 'R' and self.output == 'B'):
                self.new_channels = (self.image.get_channel(2), self.image.get_channel(1), self.image.get_channel(0))
        elif mode == RGBA:
            # TODO: Add in RGBA support...but can i do without copy/pasting the above?
            pass


def main_menu():
    """Displays the main menu of the program which are the user's main choices. Includes exiting the program.
    """
    while True:
        try:
            # This can be done better i feel for now....the choice's are basically copy and paste every time xD
            choice = int(user_input(__main_choice_text))
            if choice in __choices[:2]:
                break
            elif choice == __choices[2]:
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
            if choice in __choices:
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
    elif choice == __choices[2]:
        main_menu()


def user_input(text):
    return input("{0}What would you like to do?\n".format(text))


def error_response(response):
    print("{}! Please pick {}, {} or {}\n".format(response, *__choices))


def swap_rgba():
    # TODO: Get file input from user - how? Maybe read from a file can be an option (WAY IN THE FUTURE - batching).
    # Support for single and multiple operations (R > G, R > B etc.)
    # Ability to overwrite old file (copy old file just in case)
    # Undo? Or Reset to original texture state

    # input_image = input("Image path: ")
    input_image = "E:\Projects\\test\\test1.tga"  # test file for now
    # input_image = "E:\Projects\\test\\test2_alpha.tga"  # also test file for now
    while True:
        try:
            # image1a = "E:\Projects\\test\\test1_16bit.png"
            with Image.open(input_image) as image:  # type: Image.Image
                print("Opened {file_name}\nFormat: {format}\nSize: {size}\nMode: {mode}"
                      .format(file_name=os.path.basename(input_image), format=image.format, size=image.size, mode=image.mode))

                if image.mode == RGB:
                    # TODO: USER INPUT AT THIS POINT - ChannelSwizzle(red, green)
                    # Splitting creates copies of the image anyway ;)
                    red, green, blue = image.split()
                    new_image = Image.merge(RGB, (green, blue, red)).getchannel(0)  # type: Image.Image
                    new_image.show()  # for testing

                elif image.mode == RGBA:
                    # TODO: NEED USER INPUT AT THIS POINT
                    red, green, blue, alpha = image.split()
                    alpha.show()  # for testing
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
