def print256(buf):
    print('\n'.join(''.join(f"\033[38;5;{x}m\033[48;5;{y}m\u2580\033[0m" for x, y in zip(row, _row)) for row, _row in zip(buf[::2], buf[1::2])))

def print24(buf):
    print('\n'.join(''.join(
        f"\033[38;2;{(x & 0xff0000)>>0x8*2};{(x & 0x00ff00)>>0x8*1};{(x & 0x0000ff)>>0x8*0}m" +
        f"\033[48;2;{(y & 0xff0000)>>0x8*2};{(y & 0x00ff00)>>0x8*1};{(y & 0x0000ff)>>0x8*0}m\u2580\033[0m"
        for x, y in zip(row, _row)
    ) for row, _row in zip(buf[::2], buf[1::2])))

if __name__ == "__main__":
    from load import Image
    from transform import downscale
    from encode import xterm256
    from sys import argv
    fname = argv[1] if len(argv) > 3 else "warrior.ppm"
    width, height = (int(argv[2]), int(argv[3])) if len(argv) > 3 else (80, 80)
    with open(fname, 'rb') as file:
        img = Image.ppm_read(file)
        buf = [[0x0 for x in range(width)] for y in range(height)]
        downscale(buf, img)
        print24(buf)
        #buf = [list(map(xterm256, row)) for row in buf]
        #print256(buf)
