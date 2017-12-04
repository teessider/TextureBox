from PIL import Image


class ChannelPack(object):
    """
    Takes in a string like "R <> G" and so do Image.merge(RGB or RGBA, (green, red, blue))
    """
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

            # Need the spaces so it can be turned into a list for later.
            user_string = "{0} {1}{2} {3}".format(*user_action).split(' ') if ' ' not in user_action else user_action.split(' ')

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

    def swizzle(self, swizzle_channels):
        """
        Swizzles the two input channels of an RGB or RGBA texture.\n
        Returns:
            tuple: Swizzled texture channels ready to be merged into new texture.
        """
        swizzle_1 = swizzle_channels[0]
        swizzle_2 = swizzle_channels[1]
        # TODO: Add in support for RGBA and it's RGB swapping possibilities as currently there is none! So unless one of the channels is the alpha, this will break

        # Instead of using the global variables RGB and RGBA, the letters are used for code readability.
        # RGBA Possibilities
        if 'A' in self.image.mode:
            if (swizzle_1 == 'R' and swizzle_2 == 'G') or (swizzle_1 == 'G' and swizzle_2 == 'R'):
                self.new_channels = (self.image.getchannel(1), self.image.getchannel(0), self.image.getchannel(2), self.image.getchannel(3))

            elif (swizzle_1 == 'R' and swizzle_2 == 'B') or (swizzle_1 == 'B' and swizzle_2 == 'R'):
                self.new_channels = (self.image.getchannel(2), self.image.getchannel(1), self.image.getchannel(0), self.image.getchannel(3))

            elif (swizzle_1 == 'G' and swizzle_2 == 'B') or (swizzle_1 == 'B' and swizzle_2 == 'G'):
                self.new_channels = (self.image.getchannel(0), self.image.getchannel(2), self.image.getchannel(1), self.image.getchannel(3))

            elif (swizzle_1 == 'R' and swizzle_2 == 'A') or (swizzle_1 == 'A' and swizzle_2 == 'R'):
                self.new_channels = (self.image.getchannel(3), self.image.getchannel(1), self.image.getchannel(2), self.image.getchannel(0))

            elif (swizzle_1 == 'G' and swizzle_2 == 'A') or (swizzle_1 == 'A' and swizzle_2 == 'G'):
                self.new_channels = (self.image.getchannel(0), self.image.getchannel(3), self.image.getchannel(2), self.image.getchannel(1))

            elif (swizzle_1 == 'B' and swizzle_2 == 'A') or (swizzle_1 == 'A' and swizzle_2 == 'B'):
                self.new_channels = (self.image.getchannel(0), self.image.getchannel(1), self.image.getchannel(3), self.image.getchannel(2))
        else:
            # RGB Possibilities
            if (swizzle_1 == 'R' and swizzle_2 == 'G') or (swizzle_1 == 'G' and swizzle_2 == 'R'):
                self.new_channels = (self.image.getchannel(1), self.image.getchannel(0), self.image.getchannel(2))

            elif (swizzle_1 == 'R' and swizzle_2 == 'B') or (swizzle_1 == 'B' and swizzle_2 == 'R'):
                self.new_channels = (self.image.getchannel(2), self.image.getchannel(1), self.image.getchannel(0))

            elif (swizzle_1 == 'G' and swizzle_2 == 'B') or (swizzle_1 == 'B' and swizzle_2 == 'G'):
                self.new_channels = (self.image.getchannel(0), self.image.getchannel(2), self.image.getchannel(1))

        return self.new_channels

    def merge(self, mode):
        return Image.merge('RGB', self.new_channels) if mode == 'RGB' else Image.merge('RGBA', self.new_channels)


if __name__ == '__main__':
    ChannelPack(Image.Image())
