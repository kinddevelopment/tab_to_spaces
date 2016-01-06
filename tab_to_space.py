#!/usr/bin/python

import sys
import os
import argparse

def get_all_source_files(root):
    all_files = get_all_files(root)
    src_files = [name for name in all_files if isValidSourceFile(name)]
    return src_files

def get_all_files(path):
    list_of_files = []

    for dirpath, _, filenames in os.walk(path):
        if (len(filenames) == 0):
            continue
        filenames = [os.path.join(dirpath, filename) for filename in filenames]

        # Add the files in this path to 
        [list_of_files.append(x) for x in filenames]
    return list_of_files

def isValidSourceFile(filename):
    return filename.endswith('.c') or filename.endswith('.h')

def replace_tabs_with_spaces_in_file(filepath, n_spaces, checkonly):
    lines = read_lines_from_file(filepath)
    spaced_lines, n_replaces = replace_tabs_with_spaces_for_lines(lines, n_spaces)
    if (n_replaces == 0):
        return

    # Something was replaced
    if (checkonly == False):
        write_spaced_lines_to_file(filepath, spaced_lines)
    print 'Replaced {0} line{1} in {2}'.format(n_replaces, 's' if (n_replaces > 1) else '', filepath)
    return
    
def read_lines_from_file(filepath):
    lines = []
    try:
        with open(filepath, "r") as src_file:
            lines = src_file.readlines()
    except IOError as e:
        print 'Skipping reading {0} because of I/O Error({1}): {2}'.format(filepath, e.errno, e.strerror)
        lines = []
    except:
        print 'Skipping reading {0} because of unknown error', sys.exc_info()
        lines = []

    return lines

def replace_tabs_with_spaces_for_lines(lines, n_spaces):
    n_replaces = 0
    spaced_lines = [line.replace('\t', (' ' * n_spaces)) for line in lines]

    # Count lines where tabs were replaced
    for line in lines:
        if (line.find('\t') != -1):
            n_replaces += 1

    return spaced_lines, n_replaces

def write_spaced_lines_to_file(filepath, spaced_lines):
    try:
        with open(filepath, "w") as dest_file:
            dest_file.writelines(spaced_lines)
    except IOError as e:
        print 'Skipping writing {0} because of I/O Error({1}): {2}'.format(filepath, e.errno, e.strerror)
    except:
        print 'Skipping reading {0} because of unknown error', sys.exc_info()
    return

def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='Root path of where to start replacing tabs')
    parser.add_argument('spaces', help='Number of spaces to replace a tab with.', type=int)
    parser.add_argument('--checkonly', help='Only check the files. Does not write or replace anything.', action='store_true')
    args = parser.parse_args()
    return args.path, args.spaces, args.checkonly

path, n_spaces, check_only = parse_argument()
src_files = get_all_source_files(path)
[replace_tabs_with_spaces_in_file(x, n_spaces, check_only) for x in src_files]
