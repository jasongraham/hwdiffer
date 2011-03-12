#!/usr/bin/python
#
# Tested as working under both
# Python 3.1.3, and Python 2.6.5
#
# Author: Jason Graham

import difflib
import fnmatch
import os.path
import sys
import optparse


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
                counter = counter
                self.data[i].append(100 * counter / minlen)

    def close_matches(self, opts):
        # Results will be organized in a tuple
        results = []

        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                # When opts.summary is specified, then we want to print out
                # all of the diff percentages.
                if (self.data[i][j] <= opts.threshold) or opts.summary:
                    file1 = self.filelist[i]
                    file2 = self.filelist[i+j+1]
                    percent = self.data[i][j]
                    results.append( (file1, file2, percent) )

        return results

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
    parser.add_option("-t", "--thresh", dest="threshold", default=20,
            help="Optional.  Files which differ by greater than this " +
            "percentage will be ignored.  Defaults to 20. " +
            "(only relavent when not using `--summary`)")
    parser.add_option("-s", "--summary", action="store_true",
            dest="summary", default=False,
            help="Optional.  Print out a summary over every file")

    (opts, args) = parser.parse_args()

    # When run in windows via double clicking, there will be no command line
    # arguments.  To hopefully make this work on Windows, check for this
    # and fill in with useful defaults for checking python files.
    if len(sys.argv) < 2:
        opts.namefilter = "*.py"

    # Convert the threshold option to an integer.
    # Since we have a default value for it, we don't
    # need to check that it exists first.
    try:
        opts.threshold = int(opts.threshold)
    except:
        parser.print_help()
        print("\nERROR: Threshold must be an integer value")
        return False

    # Do some checking that we have the options that we need.
    # The only one strictly necessary and w/o defaults is
    # opts.namefilter
    if not opts.namefilter:
        parser.print_help()
        print("\nERROR: You must specify a filename filter (-f)")
        return False

    # Need to do some option parsing in here I think
    dt = DiffTable(opts)

    results = dt.close_matches(opts)

    if len(results) > 0:
        # print out a message to help interpret the results
        print("Note: Close matches will have small percent differences.\n")

        # Sort the results by what percent different they show,
        # ordered least to greatest
        results = sorted(results, key=lambda diff: diff[2])

        # Print out the results
        print("Difference %\t|   Files")
        for line in results:
            print("    %4.1f\t|  %s <==> %s" % (line[2], line[0], line[1]))

    else:
        print("No close matches found.")

    return True

if __name__ == '__main__':
    if main():
        sys.exit(0)
    else:
        sys.exit(-1)

