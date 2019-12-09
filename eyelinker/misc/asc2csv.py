#!/usr/bin/env python

import argparse
import glob
import os
import re
import sys


def convert_to_csv(filename, header, overwrite):
    file_base = filename.rstrip('.asc')
    newfile = file_base + '.csv'
    if not overwrite:
        i = 1
        while os.path.isfile(newfile):
            newfile = file_base + '(%i).csv' % i
            i += 1

    with open(newfile, 'w') as newfile:
        if header:
            newfile.write(header+'\n')

        with open(filename) as old_file:
            first = old_file.readline().strip()
            match = re.match('[0-9]+.?[0-9]+', first[-5:])

        if match is None:
            add_bools = True
        else:
            add_bools = False

        # TODO refactor this
        with open(filename) as old_file:
            block = 0
            trial = 0
            for line in old_file.readlines():
                if re.match('[0-9].*', line):
                    newfile.write(str(block) + ',' + str(trial) + ',')
                    if add_bools:
                        base_line = line.strip()[:-6]
                        base_line = base_line.replace('   .', 'NA')
                        newfile.write(base_line.replace('\t', ','))

                        bools = []
                        for c in line.strip()[-5:]:
                            if c == '.':
                                bools.append(False)
                            else:
                                bools.append(True)

                        for b in bools:
                            newfile.write(',' + str(b))

                        newfile.write('\n')
                    else:
                        line = line.replace('   .', 'NA')
                        newfile.write(line.replace('\t', ','))
                else:
                    if re.match('MSG\t[0-9]+\tBLOCK ([0-9]+)', line):
                        block = re.match('MSG\t[0-9]+\tBLOCK ([0-9]+)', line).group(1)
                    if re.match('MSG\t[0-9]+\tTRIAL ([0-9]+)', line):
                        trial = re.match('MSG\t[0-9]+\tTRIAL ([0-9]+)', line).group(1)


def find_files():
    files = []

    if not sys.stdin.isatty():
        for file in sys.stdin:
            file = file.strip().lstrip('./')
            if file[-4:] == '.asc':
                files.append(file)
    else:
        files = glob.glob('*.asc')

    return files


def main():
    ap = argparse.ArgumentParser(description='Converts asc files into csvs.')
    ap.add_argument(
        '-f', '--filename', help='The filename to convert (also accepts a list from stdin).'
    )
    ap.add_argument('-H', '--header', help='The header for the csv files.')
    ap.add_argument('-o', '--overwrite', help='Files will be overwritten.', action='store_true')

    args = vars(ap.parse_args())

    overwrite = args['overwrite']

    if args['filename']:
        filename = args['filename']
    else:
        filename = None

    if args['header'] is None:
        try:
            # TODO: Find a good place for this
            with open('/usr/local/bin/asc2csv/asc2csv_header.txt') as f:
                header = f.readline()
        except FileNotFoundError:
            header = None
    else:
        header = args['header']

    if filename:
        convert_to_csv(filename, header, overwrite)
    else:
        for filename in find_files():
            convert_to_csv(filename, header, overwrite)


if __name__ == '__main__':
    main()
