#!/usr/bin/env python3

from luck_draw_amount import lucky_draw_amount

if __name__ == '__main__':
    input = '10421.09'
    the_final_amount_of_lucky_draw = lucky_draw_amount(input)
    print("The final amount of lucky draw is {} NTD".format(the_final_amount_of_lucky_draw))
    # the result is 4327.731520843061 NTD