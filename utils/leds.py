encoding = ("1000000",
            "1111001",
            "0100100",
            "0110000",
            "0011001",
            "0010010",
            "0000010",
            "1111000",
            "0000000",
            "0010000")

leds_st = ["{0:010b}".format(2**n -1) for n in range(1, 11)]

encoding = tuple(map(lambda x: int(x, 2), encoding))
leds_st = tuple(map(lambda x: int(x, 2), leds_st))