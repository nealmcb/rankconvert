#!/usr/bin/env python
"""Convert ranked ballots from the CSV format provided by CIVS
(http://www.cs.cornell.edu/andru/civs.html) to the BLT format
used by, e.g., OpenSTV (www.openstv.org/).

Note that both formats list ranks, rather than putting choices in order.
For example, given these ranks:
A,B,C,D,E
1,4,3,2,5
5,4,3,2,1

it produces this blt file:
5 1
1 1 4 3 2 0
1 5 4 3 2 0
0
"A"
"B"
"C"
"D"
"E"
"testdata0.civs"

Note: this uses the specified filename as the title of the election (last line of BLT file).

http://code.google.com/p/stv/wiki/BLTFileFormat

TODO:
 * support the popular ordered "text" format and equal rankings via the "=" delimiter.
 * support initial multiplier, provided as <integer>x, e.g. "3X"

%InsertOptionParserUsage%
"""
import os
import sys
import optparse
from optparse import make_option
import logging
import operator
import re

__author__ = "Neal McBurnett <http://neal.mcburnett.org/>"
__copyright__ = "Copyright (c) 2009 Neal McBurnett"
__license__ = "GPL"
__version__ = "0.1.0"

usage = """Usage: rankconvert.py [options] file"""

option_list = (
    make_option("-n", "--numwin", dest="numwin", default=1,
                  help="number of winners", metavar="N"),

    make_option("-d", "--delimiter", dest="delimiter", default=',',
                  help="specify CSV delimiter", metavar="DELIMITER"),

    make_option("-v", "--verbose",
                  action="store_true", default=False,
                  help="verbose output" ),

    make_option("-D", "--debug",
                  action="store_true", default=False,
                  help="turn on debugging output"),
)

parser = optparse.OptionParser(prog="rankconvert", usage=usage, option_list=option_list)

# incorporate OptionParser usage documentation into our docstring
__doc__ = __doc__.replace("%InsertOptionParserUsage%\n", parser.format_help())

def rankconvert(parser):
    """convert file with ranked ballots to different format"""

    (options, args) = parser.parse_args()

    if options.debug:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    logging.basicConfig(level=loglevel) # format='%(message)s'

    logging.debug("args = %s" % list(args))

    if len(args) != 1:
        logging.error("exactly one file should be specified")
        sys.exit(1)

    delimiter = options.delimiter

    infilename = args[0]

    reader = open(infilename)

    # parse dominion-ranked-marks format
    # Skip first 3 lines
    next(reader)
    next(reader)

    ranked_header_re = r"(\w+ \w+)\((\d+)\)"

    h = next(reader)

    # Establish mapping between columns and assignments of marks to rankings
    mark_map = []

    max_ranking = '0'

    for name in h.split(','):
        match = re.search(ranked_header_re, name)
        if match:
            name, rank = match.groups()
            # print(f'{name}, {rank}')
            mapping = [name, rank]
            # Code later on relies on this assumption
            # FIXME if it matters: use numeric comparison, so '10' is not less than '2'
            if rank < max_ranking:
                print(f'Assumption failure: rankings not monotonic, next {rank=}, less than {max_ranking=}', file=sys.stderr)
                sys.exit()
            max_ranking = rank
        else:
            mapping = None

        mark_map.append(mapping)

    # Skip row of conventional headers
    next(reader)

    # Interpret marks on CVRs
    for r in reader:
        ranked = []
        ranknums = []
        dups = 0
        numdups = 0
        numskips = 0
        cols = r.split(',')
        cvrid = cols[0]
        print(cvrid, end=': ')
        for col, mapping in zip(cols, mark_map):
            if mapping and col == '1':
                name, rank = mapping
                # Check for overvotes
                if rank in ranknums:
                    # print(f'{cvrid=}, }: overvote', file=sys.stderr)
                    numdups += 1
                    ranked.pop()
                    ranknums.pop()
                    break

                # Check for skipped rankings
                if len(ranknums) > 0  and  int(rank) > int(ranknums[-1]) + 1:
                    print(f'{cvrid=}, {mapping}: skiped rank', file=sys.stderr)
                    numskips += 1
                    break

                if rank in ranknums:
                    # print(f'{cvrid=}, }: overvote', file=sys.stderr)
                    numdups += 1
                    ranked.pop()
                    ranknums.pop()
                    break

                # Check for duplicate votes
                if name in ranked:
                    dups += 1
                    continue
                ranked.append(name)
                ranknums.append(rank)
                print(f'{mapping=}', end='\t')
        print()
        if dups > 0:
            print(f'dup in {cvrid=}', file=sys.stderr)
            #print(f'dup: {r}')
        if numdups > 0:
            print(f'overvote in {cvrid=}', file=sys.stderr)
        if numskips > 0:
            print(f'skip in {cvrid=}', file=sys.stderr)

    sys.exit()

    # FIXME: deal with quoted commas. Perhaps just use csv module.
    choices = r.rstrip().split(delimiter)
    n = len(choices)

    print(n,options.numwin)

    for r in reader:
        ranks = []
        for c in r.rstrip().split(delimiter):
            try:
                ranks.append(int(c))
            except:
                ranks.append('-')

        # Each BLT line begins with a count.
        print("1", end=' ')

        last = max(ranks)

        for i, w in sorted(enumerate(ranks), key=operator.itemgetter(1)):
            # FIXME: why leave out the last rank?
            if w == last:
                break
            # FIXME: if there are more and ranks are equal print = otherwise >
            print(i+1, end=' ')

        # Each BLT line ends with a 0
        print("0")

    print("0")
    for choice in choices:
        print('"%s"' % choice)
    print('"%s"' % infilename)

if __name__ == "__main__":
    rankconvert(parser)
