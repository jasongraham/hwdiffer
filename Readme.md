# Homework Differ #

## Overview ##

This script is a grading aid and is intended to compute diffs between
all files found under the current working directory of a given
extension.  It stores the percentage by which files differ, and
flags file pairs that differ by less than a given percentage.

It is intended to be a quick and crude cheating detection method for
programming homework assignments.

It has serious shortcomings, however, and is able to be defeated quite easily.
As with all software, no guarantees are made, and is intended to be used in
conjunction with some common sense :)

## Usage ##

	Usage: hwdiffer.py [options]

	Options:
	-h, --help               show this help message and exit

	-p DIR,                  The root directory to be recursively searched.
	--basepath=DIR           Defaults to your current directory.

	-f FILTER,               The filename filter (ie, *.c).  If no options
    --filter=FILTER          are specified, this defaults to *.py (yes,
                             that's arbitrary, but it is what the original
                             script purpose was.)

	-t THRESHOLD,            Optional.  Files which differ by greater than this
	--thresh=THRESHOLD	     percentage will be ignored.  Defaults to 20.
                             (Only relavent when not using `--summary`)

	-s, --summary            Optional.  Print out a summary over every file

## Sample output ##

Using the provided test files,

	$ python3.1 hwdiffer.py -f *.txt
	Note: Close matches will have small percent differences.

	Difference %    |   Files
		 0.0        |  ./test/dir2/file2.txt <==> ./test/dir1/file1.txt
		18.2	    |  ./test/dir2/file2.txt <==> ./test/dir3/file3.txt
		18.2	    |  ./test/dir3/file3.txt <==> ./test/dir1/file1.txt

Using the `--summary` and `--basepath` options:

	$ python3.1 hwdiffer.py -s -f *.txt -p test/
	Note: Close matches will have small percent differences.

	Difference %    |   Files
		  0.0       |  test/dir2/file2.txt <==> test/dir1/file1.txt
		 18.2       |  test/dir2/file2.txt <==> test/dir3/file3.txt
		 18.2       |  test/dir3/file3.txt <==> test/dir1/file1.txt
		100.0       |  test/dir2/file4.txt <==> test/dir3/file3.txt
		100.0       |  test/dir2/file2.txt <==> test/dir2/file4.txt
		100.0       |  test/dir2/file4.txt <==> test/dir1/file1.txt

Getting no close matches.

    $ python3.1 hwdiffer.py -f *.c
    No close matches found.

## License ##

[MIT][] Licensed.  Specifically, see below.

[MIT]:http://en.wikipedia.org/wiki/MIT_License

Copyright (C) 2011 by Jason Graham

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

