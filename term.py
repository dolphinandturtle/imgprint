def print256(buf):
    print('\n'.join(''.join(f"\033[48;5;{x}m \033[0m" for x in row) for row in buf))


if __name__ == "__main__":
    from load import Image
    from transform import downscale
    from encode import xterm256
    fname = "warrior.ppm"
    with open(fname, 'rb') as file:
        img = Image.ppm_read(file)
        WIDTH, HEIGHT = 80, 80
        buf = [[0 for x in range(WIDTH)] for y in range(HEIGHT)]
        downscale(buf, img)
        buf = [list(map(xterm256, row)) for row in buf]
        print256(buf)
