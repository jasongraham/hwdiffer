#!/usr/bin/python3.1
#
# Author: Jason Graham

# Maybe we can do this entirely in python
# http://docs.python.org/release/3.1.3/library/difflib.html#differ-example
import difflib

# Walking a directory to find files
# http://stackoverflow.com/questions/2186525/use-a-glob-to-find-files-recursively-in-python
import fnmatch
import os.path

from pprint import pprint

# 2-d array in python (by appending)
# http://ubuntuforums.org/showthread.php?t=128110

class DiffTable:
    def __init__(self, basepath, namefilter):
        # data will hold the 2-d array of diffs
        self.data = []
        # filenames will hold a list of the pathnames of each files
        self.filelist = []

        # populate list of filenames
        self.populate(basepath, namefilter)

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

    def close_matches(self, thresh):
        matches = []
        percents = []

        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if self.data[i][j] <= thresh:
                    matches.append(' '.join([self.filelist[i],self.filelist[i+j+1]]))
                    percents.append(self.data[i][j])

        return matches, percents

#def main(basepath, namefilter, threshold=15):
def main():
    basepath = 'test'
    namefilter = '*.txt'
    threshold = 15

    # Need to do some option parsing in here I think
    dt = DiffTable(basepath, namefilter)

    matches, percents = dt.close_matches(threshold)
    pprint(matches)
    pprint(percents)


if __name__ == '__main__':
    main()

