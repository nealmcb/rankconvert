CIVS input files are csv files.  The first row has names for the candidates.  Then
each row is a ballot, and each column has the ranking that the voter
gave for that candidate.  Their top candidate(s) have the smallest rankings.

For example in this file, with 12 candidates named "a" thru "l", there are
two ballots.  The first ballot gives the top ranking of 1 to candidates g and h (7 and 8).
The next ones in order are (e,k), (b,c), (a,f) and then the rest all ranked at the bottom.

    a,b,c,d,e,f,g,h,i,j,k,l
    10,5,5,12,3,10,1,1,12,12,3,12
    4,12,5,10,8,2,1,11,3,9,6,7

That translates to an overall sequence, in selection order, of these candidates

    g h e k  b c a f d i j l

These candidate names are translated into numbers, in the order the rows were presented.
The ones at the bottom are left out by this code. [Is that appropriate?].
That leaves these rankings:

    7 8 5 11 2 3 1 6

Translated into BLT format gives this output, where the title at the end simply
indicates this software as having created the file:

```
12 1
1 7 8 5 11 2 3 1 6 0
1 7 6 9 1 3 11 12 5 10 4 8 0
0
"a"
"b"
"c"
"d"
"e"
"f"
"g"
"h"
"i"
"j"
"k"
"l"
"Ballot data converted by rankconvert"
```

---
details

a 10
b 5
c 5
d 12
e 3
f 10
g 1
h 1
i 12
j 12
k 3
l 12

sorting by ranking:

g 1
h 1
e 3
k 3
b 5
c 5
a 10
f 10
d 12
i 12
j 12
l 12
