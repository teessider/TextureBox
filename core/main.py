import sys
from PIL import Image


class Program(object):
    __fluff = "*" * 50  # Purely cosmetic purpose ;)
    __choices = (1, 2, 3)

    __intro_text = "{0}\n" \
                   "Welcome to the Simple Texture Packer 0.1\nCreated By\nAndrew \'teessider\' Bell.\n" \
                   "{0}\n" \
                   "This command line tool is for packing textures without the need to go into more advanced programs.\n".format(__fluff)
    # For string formatting which includes __choices list, I use automatic one as the choices could expand in the future
    __main_choice_text = "Select:\n{}) Create new packed texture from existing ones\n{}) Repack (Swizzle) a pre-packed texture \n{}) Exit Program\n\n".format(*__choices)

    def __init__(self):
        self.choice = 0
        print(self.__intro_text)
        self.main_menu()

    def main_menu(self):
        """Displays the main menu of the program which are the user's main choices. Includes exiting the program.
        """
        while True:
            try:
                self.choice = int(self.user_input(self.__main_choice_text))
                if self.choice == self.__choices[0] or self.__choices[1]:
                    break
                elif self.choice == self.__choices[-1]:
                    sys.exit(0)
                else:
                    self.error_response("Invalid number")
                    continue
            except ValueError:
                self.error_response("It must be a number")
                continue
        if self.choice == self.__choices[0]:
            print("TO DO")  # Nothing for now ;)
            # 1) Create new texture (from existing ones)
            #   1a) Size - preset or user defined (eg. non-square)
        elif self.choice == self.__choices[1]:
            self.swizzle_menu()

    @staticmethod
    def user_input(text):
        return input("{0}What would you like to do?\n".format(text))

    def error_response(self, response):
        print("{}! Please pick {}, {} or {}\n".format(response, *self.__choices))

    def swizzle_menu(self):
        """The menu which the user can repack(swizzle) an existing packed texture.\n
                The user can optionally add an alpha channel too."""
        swizzle_menu_text = "Select:\n{}) Swizzle (Swap channels)\n{}) Add Alpha Channel\n{}) Back to Main Menu\n".format(*self.__choices)
        # 2) Repack existing texture
        #   2a) Swap channels
        #   2b) Add Alpha Channel
        while True:
            try:
                self.choice = int(self.user_input(swizzle_menu_text))
                if self.choice in (self.__choices[0], self.__choices[1], self.__choices[-1]):
                    break
                else:
                    self.error_response("Invalid number")
                    continue
            except ValueError:
                self.error_response("It must be a number")
                continue
        if self.choice == self.__choices[0]:
            pass
        elif self.choice == self.__choices[1]:
            pass
        elif self.choice == self.__choices[-1]:
            self.main_menu()

# TODO: User input for selecting images
# image1 = "E:\Projects\\test\\test1.tga"
# image2 = "E:\Projects\\test\\test2_alpha.tga"

# try:
#     picture = Image.open(image1)  # type: Image.Image
#     # double line so it is treating as folder
#     picture2 = Image.open(image2)  # type:Image.Image
#     images = [picture, picture2]
#     for image in images:
#         print(image.format, image.size, image.mode)
#     red_chan = picture.split()[0]
#     #red_chan.show()  # For debugging only
# except IOError:
#     print("Can't open an image, Invalid file path or it doesn't exist!")

# Names - TextureBox, SwizzleBox, Texture Swizzler, Channel Packer

if __name__ == '__main__':
    Program()
