from PIL import Image


class Program(object):
    intro_text = "////////////////////////////\nWelcome to the Simple Texture Packer.\n" \
              "Created by Andrew \'teessider\' Bell.\n//////////////////////\n" \
              "This tool is for packing textures without the need to go into more advanced programs.\n" \
              "The choices are as follows:\n" \
              "1) Create new packed texture from existing ones\n" \
              "2) Repack a pre-packed texture\n"

    def __init__(self):
        print(self.intro_text)
        while True:
            try:
                self.choice = int(input("What would you like to do?\n"))
                if self.choice == 1:
                    print("Cool choice!")
                if self.choice == 2:
                    print("Most excellent!")
                else:
                    self.error_response("Invalid number")
                    continue
            except ValueError:
                self.error_response("It must be a number")
                continue

    @staticmethod
    def error_response(response):
        print("{0}! Please pick 1 or 2".format(response))

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

# Process (cmd options):
# 1) Create new texture (from existing ones)
#   1a) Size - preset or user defined (eg. non-square)
# 2) Repack existing texture
#   2a) Swap channels
#   2b) Add Alpha Channel

# Name - Mr Swizzler?

if __name__ == '__main__':
    Program()
