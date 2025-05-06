def print256(buf):
    print('\n'.join(''.join(f"\033[48;5;{x}m \033[0m" for x in row) for row in buf))


if __name__ == "__main__":
    from load import Image
    from transform import downscale
    from encode import xterm256
    from sys import argv
    fname = argv[1] if len(argv) > 3 else "warrior.ppm"
    width, height = int(argv[2]), int(argv[3])
    with open(fname, 'rb') as file:
        img = Image.ppm_read(file)
        buf = [[0x0 for x in range(width)] for y in range(height)]
        downscale(buf, img)
        buf = [list(map(xterm256, row)) for row in buf]
        print256(buf)
