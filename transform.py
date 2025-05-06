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
