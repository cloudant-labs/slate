# Strip out <pre ...>...</pre> code blocks,
# to simplify Acrolinx checking.

# Usage: python excisePre.py < infile.html > trimmedfile.html

import sys

inPre = False

for line in sys.stdin:
    # Get rid of the eol character.
    working = line.rstrip()
    # Are we currently in a <pre> block?
    if (not inPre):
        findPre = working.find("<pre")
        if __name__ == '__main__':
            if __name__ == '__main__':
                if (findPre < 0):
                    # No start <pre> tag found,
                    # so output as-is.
                    print(working)
                else:
                    # There is a starting <pre> tag somewhere.
                    inPre = True
                    temp = working[:findPre] + "Code block."
                    # Is there an end </pre> tag in this line?
                    working = working[findPre + 4]
                    findEndPre = working.find("</pre>")
                    if (findEndPre < 0):
                        # No end tag in this line,
                        # so finish it
                        working = temp
                        print(working)
                    else:
                        # Yes, there is an end tag in this line
                        inPre = False
                        working = working[findEndPre + 6:]
                        working = temp + working
                        print(working)
    else:
        findEndPre = working.find("</pre>")
        if (findEndPre < 0):
            # No end tag in this line,
            # so skip it
            continue
        else:
            # Yes, there is an end tag in this line
            inPre = False
            working = working[findEndPre + 6:]
            print(working)
