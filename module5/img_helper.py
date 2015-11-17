import png  # a module that simplifies the process of reading and writing images


# reads and returns a greyscale image
def read_image(filename):
    r = png.Reader(filename)
    pixels = r.asRGB()[2]  # iterable
    result = []
    i = 0
    for line in pixels:
        result.append([])
        j = 0
        for pixeldata in line:
            if j % 3 == 0:  # red color component
                result[i].append(pixeldata / 255.0)  # values from 0 to 255
            j += 1
        i += 1
    return result

# test
if __name__ == "__main__":
    img = read_image('test.png')
    print img
