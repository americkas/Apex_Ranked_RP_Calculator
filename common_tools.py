from prettytable import PrettyTable
from tabulate import tabulate

def print_array (array):
    """ Print 2D array """
    for i in array:
        for j in i:
            print(j, end=" ")
        print()

def print_table(dat_array):
    """ Print a table using dtype """
    table = PrettyTable(dat_array.dtype.names)
    for row in dat_array:
        table.add_row(row)
    # Change some column alignments; default was 'c'
    print (table)