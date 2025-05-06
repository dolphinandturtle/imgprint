from typing import Callable
from dataclasses import dataclass


"""

0x ab cd ef &
0x 00 ff 00 =
-----------
0x 00 cd 00

0xff << (0x4 * n) = 0xff0..n..0

(0x10 << 0x4 * n) - 1 = 0xf..n..f

"""


@dataclass(slots=True, frozen=True)
class Image:
    header: str
    width: int
    height: int
    span: int
    pixels: list[list[int]]

    @classmethod
    def ppm_read(cls, file):
        s = file.read()
        i_header = s.index(b'\n')
        header = s[:i_header].decode('ascii')
        i_size = s[i_header + 1:].index(b'\n') + i_header + 1
        width, height = map(int, s[i_header+1:i_size].split(b' '))
        i_span = s[i_size + 1:].index(b'\n') + i_size + 1
        span = int(s[i_size+1:i_span])
        data = s[i_span+1:]
        pixels = [[
            data[3*width*y:3*width*(y+1)][3 * x + 0] * 0x10000 +
            data[3*width*y:3*width*(y+1)][3 * x + 1] * 0x100 +
            data[3*width*y:3*width*(y+1)][3 * x + 2]
            for x in range(width)
        ] for y in range(height)]
        return cls(header, width, height, span, pixels)

def xterm256(rgb: int):
    r = (rgb & 0xff0000) >> 0x8 * 2
    g = (rgb & 0x00ff00) >> 0x8 * 1
    b = (rgb & 0x0000ff) >> 0x8 * 0
    if abs(abs(r - g) - abs(g - b)) < 2 and r / 10 < 24:
        rid = round(r / 10)
        return rid + 232
    else:
        rid = round((r - 95) / 40) + 1 if r > 95 else (r > 43)
        gid = round((g - 95) / 40) + 1 if g > 95 else (g > 43)
        bid = round((b - 95) / 40) + 1 if b > 95 else (b > 43)
        return rid * 36 + gid * 6 + bid + 16

def downscale(buf, img):
    # p: "padding"          # dx: "pixel width" 
    # w: "weight"           # dy: "pixel height"
    # bml: "bitmask large"  # bp: "bytes padding"
    # bm8: "bitmask 8-byte" # ch: "channel"      
    WIDTH, HEIGHT = len(buf[0]), len(buf)
    DX, DY = round(img.width / WIDTH), round(img.height / HEIGHT)
    P = max(DX, DY) + 1
    W = DX * DY
    BML = ((0x10 << 0x4 * (P + 1)) - 1)
    BM8 = 0xff
    BP = 0x4 * P
    CH = 0x4 * (P + 2)
    # PADDING RGB CHANNELS.
    pixels = [[((rgb & 0xff0000) << (2 * BP)) +
               ((rgb & 0x00ff00) << (1 * BP)) +
               ((rgb & 0x0000ff) << (0 * BP))
               for rgb in row] for row in img.pixels]
    # AVERAGING PIXELS OVER RECTANGULAR AREA.
    for y in range(HEIGHT):
        for x in range(WIDTH):
            # UN-WEIGHTED SUM OF PIXEL ENSEMBLE.
            rgb = sum(sum(row[x*DX:(x+1)*DX]) for row in pixels[y*DY:(y+1)*DY])
            # NORMALIZATION AND COLOR RANGE CLAMPING.
            buf[y][x] = (
                # Shift padded mask onto the red channel,
                # clamp the channel and normalize it.
                + ((round(((BML << (CH * 2)) & rgb) / W)
                    # remove normalization residuals with 8byte-mask
                    # shifted onto the red channel.
                    & (BM8 << (CH * 2))) >> (2 * BP))
                # Shift padded mask onto the green channel,
                # clamp the channel and normalize it.
                + ((round((rgb & (BML << (CH * 1))) / W)
                    # remove normalization residuals with 8byte-mask
                    # shifted onto the green channel.
                    & (BM8 << (CH * 1))) >> (1 * BP))
                # Shift padded mask onto the blue channel,
                # clamp the channel and normalize it.
                + ((round((rgb & (BML << (CH * 0))) / W)
                    # remove normalization residuals with 8byte-mask
                    # shifted onto the blue channel.
                    & (BM8 << (CH * 0))) >> (0 * BP))
            )

def print256(buf):
    print('\n'.join(''.join(f"\033[48;5;{x}m \033[0m" for x in row) for row in buf))


if __name__ == "__main__":
    fname = "warrior.ppm"
    with open(fname, 'rb') as file:
        img = Image.ppm_read(file)
        WIDTH, HEIGHT = 80, 80
        buf = [[0 for x in range(WIDTH)] for y in range(HEIGHT)]
        downscale(buf, img)
        buf = [list(map(xterm256, row)) for row in buf]
        print256(buf)
