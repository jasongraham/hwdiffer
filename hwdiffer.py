#!/usr/bin/python3.1
#
# Author: Jason Graham

# Maybe we can do this entirely in python
# http://docs.python.org/release/3.1.3/library/difflib.html#differ-example
import sys
import difflib

# Walking a directory to find files
# http://stackoverflow.com/questions/2186525/use-a-glob-to-find-files-recursively-in-python
import fnmatch
import os.path

# For optparse
import optparse

from pprint import pprint

# 2-d array in python (by appending)
# http://ubuntuforums.org/showthread.php?t=128110

class DiffTable:
    def __init__(self, opts):
        # data will hold the 2-d array of diffs
        self.data = []
        # filenames will hold a list of the pathnames of each files
        self.filelist = []

        # populate list of filenames
        self.populate(opts.basepath, opts.namefilter)

        # perform the diffs
        self.differ()

        pprint(self.filelist)
        pprint(self.data)

    # find all the files we need
    def populate(self, basepath, namefilter):
        for root, dirnames, filenames in os.walk(basepath):
            for filename in fnmatch.filter(filenames, namefilter):
                self.filelist.append(os.path.join(root, filename))

    # perfom the diffs
    def differ(self):
        d = difflib.Differ()
        # by the time we get to the last one, we've compared them all
        for i in range(len(self.filelist)-1):
            # make a new row in the data list
            self.data.append([])

            code1 = open(self.filelist[i], 'r').read().splitlines(1)
            # we only care about the upper triangular portion of the array
            # with python having lists inside lists, we don't have to represent
            # the entire matrx though, so horray?
            for j in range(len(self.filelist)-i-1):
                code2 = open(self.filelist[i+j+1], 'r').read().splitlines(1)

                # compute the diff
                result = list(d.compare(code1, code2))
                minlen = min([len(self.filelist[i]),len(self.filelist[i+j+1])])
                counter = 0
                for k in range(len(result)):
                    # Count the number of non-matching lines in the diff.
                    # note that this will 'double count' at best
                    if result[k][0] == '+' or result[k][0] == '-':
                        counter += 1

                # append the diff stats to the current row
                counter = counter / 2
                self.data[i].append(100 * counter / minlen)

    def close_matches(self, opts):
        matches = []
        percents = []

        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                # When opts.summary is specified, then we want to print out
                # all of the diff percentages.
                if (self.data[i][j] <= opts.threshold) or opts.summary:
                    matches.append(' '.join([self.filelist[i],self.filelist[i+j+1]]))
                    percents.append(self.data[i][j])

        return matches, percents

#def main(basepath, namefilter, threshold=15):
def main():
    parser = optparse.OptionParser()
    parser.add_option("-p", "--basepath", dest="basepath",
            default=os.curdir,
            help="The root directory to be recursively searched."+
            " Defaults to your current directory.",
            metavar="DIR")
    parser.add_option("-f", "--filter", dest="namefilter",
            help="The filename filter (ie, *.py)",
            metavar="FILTER")
    parser.add_option("-t", "--thresh", dest="threshold", default=15,
            help="Optional.  The percentage by which files must differ " +
            "(only relavent when not using `--summary`). " +
            "Defaults to 15.")
    parser.add_option("-s", "--summary", action="store_true",
            dest="summary", default=False,
            help="Optional.  Print out a summary over every file")

    (opts, args) = parser.parse_args()

    # Do some checking that we have the options that we need.
    # The only one strictly necessary and w/o defaults is
    # opts.namefilter
    if not opts.namefilter:
        parser.print_help()
        print("\nERROR: You must specify a filename filter (-f)")
        return False

    # Need to do some option parsing in here I think
    dt = DiffTable(opts)

    (matches, percents) = dt.close_matches(opts)
    pprint(matches)
    pprint(percents)

    return True

if __name__ == '__main__':
    if main():
        sys.exit(0)
    else:
        sys.exit(-1)

