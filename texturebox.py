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


class ChannelPack:
    # Takes in a string like "R <> G" and so do Image.merge(RGB or RGBA, (green, red, blue))
    def __init__(self, image):
        self.image = image
        self.input_channels = []
        self.new_channels = ()

    def parse_input(self, user_action):
        """
        Parses the user input (which is formatted in a certain for aesthetic purposes) into a list containing the RGB channels to be swapped.\n
        Returns:
            list: RGB channels that will be swapped.

        """
        error_text_part = "Please specify the channels that will be swapped using the form: \"[RGB Channel 1] <> [RGB Channel 2]\""
        try:
            if ' ' not in user_action:
                user_string = "{} {}{} {}".format(*user_action).split(' ')  # Need the spaces so it can be turned into a list for later.
            else:
                user_string = user_action.split(' ')

            if (user_string[0].upper() in (RGB or RGBA)) and (user_string[1] == '<>') and (len(user_string) == 3):
                # Checks to make sure the string is in the way that is wanted: "[Swizzle Input 1]<>[Swizzle Input 2]"
                # Make sure only the letters are put into the list.
                self.input_channels = user_string[::2]
                return self.input_channels
            else:
                return error_text_part

        except ValueError:
            return "This must be a string! {}".format(error_text_part)
        except IndexError:
            return "Invalid input! {}".format(error_text_part)

    def swizzle(self, rgb_swizzle_channels, mode=RGB):
        """
        Swizzles the two input channels of an RGB or RGBA texture.\n
        Returns:
            tuple: Swizzled texture channels ready to be merged into new texture.
        """
        swizzle_1 = rgb_swizzle_channels[0]
        swizzle_2 = rgb_swizzle_channels[1]

        def __rgb_ops():
            # TODO: I CAN TURN THIS INTO A FUNCTION
            if (swizzle_1 == 'R' and swizzle_2 == 'G') or (swizzle_1 == 'G' and swizzle_2 == 'R'):
                self.new_channels = (self.image.get_channel(1), self.image.get_channel(0), self.image.get_channel(2))
                return self.new_channels

            elif (swizzle_1 == 'G' and swizzle_2 == 'B') or (swizzle_1 == 'B' and swizzle_2 == 'G'):
                self.new_channels = (self.image.get_channel(0), self.image.get_channel(2), self.image.get_channel(1))
                return self.new_channels

            elif (swizzle_1 == 'B' and swizzle_2 == 'R') or (swizzle_1 == 'R' and swizzle_2 == 'B'):
                self.new_channels = (self.image.get_channel(2), self.image.get_channel(1), self.image.get_channel(0))
                return self.new_channels

        if mode == RGB:
            __rgb_ops()

        elif mode == RGBA:
            __rgb_ops()

            if (swizzle_1 == 'R' and swizzle_2 == 'A') or (swizzle_1 == 'A' and swizzle_2 == 'R'):
                self.new_channels = (self.image.get_channel(3), self.image.get_channel(1), self.image.get_channel(2), self.image.get_channel(0))
                return self.new_channels

            elif (swizzle_1 == 'G' and swizzle_2 == 'A') or (swizzle_1 == 'A' and swizzle_2 == 'G'):
                self.new_channels = (self.image.get_channel(0), self.image.get_channel(3), self.image.get_channel(2), self.image.get_channel(1))
                return self.new_channels

            elif (swizzle_1 == 'B' and swizzle_2 == 'A') or (swizzle_1 == 'A' and swizzle_2 == 'B'):
                self.new_channels = (self.image.get_channel(0), self.image.get_channel(1), self.image.get_channel(3), self.image.get_channel(2))
                return self.new_channels

    def merge(self):
        # TODO: Add RGBA support
        return Image.merge(RGB, self.new_channels)


def main_menu():
    """Displays the main menu of the program which are the user's main choices. Includes exiting the program.
    """
    while True:
        try:
            # This can be done better i feel for now....the choice's are basically copy and paste every time xD
            choice = int(input_question(__main_choice_text))
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
            choice = int(input_question(swizzle_menu_text))
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


def input_question(text):
    return input("{0}What would you like to do?\n".format(text))


def error_response(response):
    print("{}! Please pick {}, {} or {}\n".format(response, *__choices))


def swap_rgba():
    # TODO: Get file input from user - Maybe also reading from a file can be an option (WAY IN THE FUTURE - batching).
    # Support for single and multiple operations (R > G, R > B etc.)
    # Ability to overwrite old file (copy old file just in case)
    # Undo? Or Reset to original texture state

    input_image = "E:\Projects\\test\\test1.tga"  # test file for now
    # input_image = "E:\Projects\\test\\test2_alpha.tga"  # also test file for now
    # image1a = "E:\Projects\\test\\test1_16bit.png"
    while True:
        try:
            # input_image = input("Image path: ")
            with Image.open(input_image) as image:  # type: Image.Image
                print("Opened {file_name}\nFormat: {format}\nSize: {size}\nMode: {mode}"
                      .format(file_name=os.path.basename(input_image), format=image.format, size=image.size, mode=image.mode))

                new_image = ChannelPack(image)
                # TODO: USER INPUT
                formatted_string = new_image.parse_input(input("TO DO: "))

                if image.mode == RGB:
                    new_image.swizzle(formatted_string, mode=RGB)
                    merged_image = new_image.merge()  # type: Image.Image

                    merged_image.getchannel(0).show()  # for testing

                elif image.mode == RGBA:
                    pass
                    # TODO: NEED USER INPUT AT THIS POINT
                    # new_image = ChannelPack(image).swizzle(mode=RGBA)  # type: Image.Image
                    # new_image.getchannel(3).show()  # for testing
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
