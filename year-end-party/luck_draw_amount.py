#!/usr/bin/env python3

import math
def lucky_draw_amount(input):
    intial_number = int(str(int(float(input)))[::-1])
    return (math.log(intial_number, 1.006) * -3.6 + 10000)


if __name__ == '__main__':
    import sys
    input = sys.argv[1]
    the_amount_of_lucky_draw = lucky_draw_amount(input)
    print(the_amount_of_lucky_draw)
