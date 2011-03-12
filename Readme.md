# Homework Differ #

## Overview ##

This script is a grading aid and is intended to compute diffs between
all files found under the current working directory of a given
extension.  It stores the percentage by which files differ, and
flags file pairs that differ by less than a given percentage.

It is intended to be a quick and crude cheating detection method for
programming homework assignments.

## Usage ##

	hwdiffer [options] extension

### Options ###

+ `extension`

	`py`, `c`, `cpp`, ...

+ `--path="/base/path"`

	By default, hwdiffer starts from $CWD (current working directory), but
	this may be specified to start from another path.

## Details ##

An arbirary example directory structure with `hwdiffer` looks as follows.

	./
	./somedir
	./somedir/subdir/file1.ext
	./dir2/file2.ext
	./dir3/anothersubdir/file3.ext
	./dir3/anothersubdir/file4.ext

Other files may be interspersed, but assume that only `file1.ext`,
`file2.ext`, `file3.ext`, and `file4.ext` are the files with the extensions
that we care about.  Note that the naming of `file1.ext`, `file2.ext`, ...
don't matter (ie, they don't all need to be named like fileX.ext), only the
extension does.

`hwdiffer` will compute the diffs between:

+ file1.ext and file2.ext
+ file1.ext and file3.ext
+ file1.ext and file4.ext
+ file2.ext and file3.ext
+ ...

It will find the number of lines by which these differ, normalize by the
length of the shorter of these two files, and then store the results into
a two dimensional matrix structure[^1].

[^1]: Note: This matrix will be symetric, and the principle diagonal, the diff
	between fileX.ext and fileX.ext, isn't of interest.  Thus, only the upper
	triangular section above the principle diagonal will be looked at and used.

After computing all the (normalized) diffs, any diffs found to be less than
a specified amount is flagged, the user is notified, and can then check these
files manually.

