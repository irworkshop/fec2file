""" Split a large csv into parts of at most N records, each with the original header row,
so every part is a valid csv on its own.

    $python split_csv.py /data/schedules/ScheduleA-2024_annotated.csv --rows 30000000

writes ScheduleA-2024_annotated-part1.csv, -part2.csv, ... next to the input.

Counts records, not lines: memo and comment fields contain embedded newlines, so a
line-based split (e.g. `split -l`) would cut records in half. A record ends at a
newline only when the number of double quotes seen so far in it is even -- in csv
a literal quote is escaped as "", so quotes inside a field always come in pairs.
Bytes are copied through untouched rather than parsed and re-written, which keeps
the parts byte-identical to the original and is several times faster than the
csv module.
"""

import argparse
import os
from datetime import datetime

NOTIFY = 10000000


def part_path(infile, part):
    root, ext = os.path.splitext(infile)
    return "%s-part%s%s" % (root, part, ext)


def split(infile, max_rows):
    start = datetime.now()
    with open(infile, 'rb') as f:
        header = f.readline()
        if not header:
            raise SystemExit("%s is empty" % infile)

        part = 0
        out = None
        rows_in_part = 0
        total = 0
        pending = False   # inside a quoted field that spans lines
        written = []

        for line in f:
            if out is None:
                part += 1
                path = part_path(infile, part)
                out = open(path, 'wb')
                out.write(header)
                written.append(path)

            out.write(line)
            if line.count(b'"') % 2:
                pending = not pending
            if pending:
                continue

            # a complete record ended on this line
            rows_in_part += 1
            total += 1
            if total % NOTIFY == 0:
                print("%s rows, part %s, elapsed %s" % (total, part, datetime.now() - start), flush=True)

            if rows_in_part == max_rows:
                out.close()
                print("wrote %s (%s rows)" % (written[-1], rows_in_part), flush=True)
                out = None
                rows_in_part = 0

        if pending:
            print("WARNING: file ended inside a quoted field -- last record is incomplete")

        if out is not None:
            out.close()
            print("wrote %s (%s rows)" % (written[-1], rows_in_part), flush=True)

    print("Done: %s rows into %s parts in %s" % (total, len(written), datetime.now() - start))
    return written


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Split a csv into header-bearing parts of at most N records.")
    parser.add_argument('infile')
    parser.add_argument('--rows', type=int, default=30000000, help="max records per part (default 30,000,000)")
    args = parser.parse_args()
    split(args.infile, args.rows)
