
# for recording:
from threading import Timer
# for random phrases:
import random 

text_file_name = 'texts/ukraine_history.txt'

def read_random_text(number_of_rows):
    f = open(text_file_name, "r", encoding="utf-8")

    # read all lines
    lines = f.readlines() 

    # choise random line
    rand_line = random.randint(0,len(lines)-number_of_rows-1) # this should make it work
    end_line = rand_line+number_of_rows

    text_to_output = ''
    # print lines 
    while rand_line < end_line:
        text_to_output+=lines[rand_line]
        rand_line += 1

    return text_to_output

# print(read_random_text(6))