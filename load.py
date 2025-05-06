from dataclasses import dataclass


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
