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
__main_choice_text = "Select:\n{0}) Create new packed texture from existing ones\n{1}) Repack a pre-packed texture \n{2}) Exit Program\n\n".format(*__choices)


RGB = 'RGB'
RGBA = RGB + 'A'
GRAY = 'L'


class ChannelPack:
    # Takes in a string like "R <> G" and so do Image.merge(RGB or RGBA, (green, red, blue))
    def __init__(self, image):
        self.image = image  # type: Image.Image
        self.input_channels = []
        self.new_channels = ()

        self.form_text = "\"[{mode} {channel}] <> [{mode} {channel}]\"".format(mode=image.mode, channel="Channel letter")

    def parse_input(self, user_action):
        """
        Parses the user input (which is formatted in a certain way for aesthetic purposes) into a list containing the RGB channels to be swapped.\n
        Returns:
            list: RGB channels that will be swapped.

        """
        error_text_part = "Please specify the channels that will be swapped using the form: {0}".format(self.form_text)
        try:
            user_action = user_action.upper()
            if ' ' not in user_action:
                user_string = "{0} {1}{2} {3}".format(*user_action).split(' ')  # Need the spaces so it can be turned into a list for later.
            else:
                user_string = user_action.split(' ')

            if (user_string[0] and user_string[2] in self.image.mode) and (user_string[1] == '<>'):
                # Checks to make sure the string is in the way that is wanted: "[Swizzle Input 1]<>[Swizzle Input 2]"
                # Make sure only the letters are put into the list.
                self.input_channels = user_string[::2]
                return self.input_channels
            else:
                raise IndexError

        except ValueError:
            print("This must be a string! {0}".format(error_text_part))
            return
        except IndexError:
            print("Invalid input! {0}".format(error_text_part))
            return

    def swizzle(self, rgb_swizzle_channels):
        """
        Swizzles the two input channels of an RGB or RGBA texture.\n
        Returns:
            tuple: Swizzled texture channels ready to be merged into new texture.
        """
        swizzle_1 = rgb_swizzle_channels[0]
        swizzle_2 = rgb_swizzle_channels[1]

        # Instead of using the global variables RGB and RGBA, the letters are used for code readability.
        # RGB Possibilities
        if (swizzle_1 == 'R' and swizzle_2 == 'G') or (swizzle_1 == 'G' and swizzle_2 == 'R'):
            self.new_channels = (self.image.getchannel(1), self.image.getchannel(0), self.image.getchannel(2))

        elif (swizzle_1 == 'G' and swizzle_2 == 'B') or (swizzle_1 == 'B' and swizzle_2 == 'G'):
            self.new_channels = (self.image.getchannel(0), self.image.getchannel(2), self.image.getchannel(1))

        elif (swizzle_1 == 'B' and swizzle_2 == 'R') or (swizzle_1 == 'R' and swizzle_2 == 'B'):
            self.new_channels = (self.image.getchannel(2), self.image.getchannel(1), self.image.getchannel(0))

        # Alpha Possibilities
        elif (swizzle_1 == 'R' and swizzle_2 == 'A') or (swizzle_1 == 'A' and swizzle_2 == 'R'):
            self.new_channels = (self.image.getchannel(3), self.image.getchannel(1), self.image.getchannel(2), self.image.getchannel(0))

        elif (swizzle_1 == 'G' and swizzle_2 == 'A') or (swizzle_1 == 'A' and swizzle_2 == 'G'):
            self.new_channels = (self.image.getchannel(0), self.image.getchannel(3), self.image.getchannel(2), self.image.getchannel(1))

        elif (swizzle_1 == 'B' and swizzle_2 == 'A') or (swizzle_1 == 'A' and swizzle_2 == 'B'):
            self.new_channels = (self.image.getchannel(0), self.image.getchannel(1), self.image.getchannel(3), self.image.getchannel(2))

        return self.new_channels

    def merge(self, mode):
        return Image.merge('RGB', self.new_channels) if mode == 'RGB' else Image.merge('RGBA', self.new_channels)


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
    swizzle_menu_text = "Select:\n{0}) Swap RGB channels\n{1}) Add Alpha Channel\n{2}) Back to Main Menu\n".format(*__choices)
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
    print("{0}! Please pick {1}, {2} or {3}\n".format(response, *__choices))


def swap_rgba():
    # TODO: Get file input from user - Maybe also reading from a file can be an option (WAY IN THE FUTURE - batching).
    # Support for single and multiple operations (R > G, R > B etc.)?
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
                try:
                    formatted_string = new_image.parse_input(input("Which channels should be swapped?\nPlease use the form: {}".format(new_image.form_text)))
                    new_image.swizzle(formatted_string)
                except TypeError:
                    print("One of the specified channels does not exist in the original texture!")
                    continue

                if image.mode == RGB:
                    merged_image = new_image.merge(mode=RGB)

                    merged_image.show()  # for testing

                elif image.mode == RGBA:
                    merged_image = new_image.merge(mode=RGBA)

                    merged_image.getchannel(3).show()  # for testing
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
