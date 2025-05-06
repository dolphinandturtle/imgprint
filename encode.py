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
