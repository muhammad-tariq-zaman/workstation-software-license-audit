"""Audit installed software per workstation against licences.

Usage: python3 main.py installed.csv licenses.csv
installed.csv columns: workstation,software,version.
licenses.csv columns: software,licensed_seats.
Two problems are reported:
- UNLICENSED: software installed on a workstation that has no
  licence entry at all.
- OVER SEATS: software installed on more workstations than its
  licensed seat count.
Workstations with unlicensed software are listed first; the
over-seats summary follows.
"""
import argparse, csv, sys

def audit(installed_rows, license_rows):
    seats = {}
    for row in license_rows:
        seats[row["software"].strip()] = int(row["licensed_seats"])
    installs = {}
    per_workstation = {}
    for row in installed_rows:
        software = row["software"].strip()
        workstation = row["workstation"].strip()
        installs[software] = installs.get(software, 0) + 1
        per_workstation.setdefault(workstation, []).append(software)
    unlicensed = {}
    for workstation, software_list in per_workstation.items():
        bad = sorted({s for s in software_list if s not in seats})
        if bad:
            unlicensed[workstation] = bad
    over_seats = sorted(
        (software, count, seats[software])
        for software, count in installs.items()
        if software in seats and count > seats[software])
    return unlicensed, over_seats

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("installed")
    parser.add_argument("licenses")
    args = parser.parse_args(argv)
    with open(args.installed, newline="", encoding="utf-8") as f:
        installed_rows = list(csv.DictReader(f))
    with open(args.licenses, newline="", encoding="utf-8") as f:
        license_rows = list(csv.DictReader(f))
    unlicensed, over_seats = audit(installed_rows, license_rows)
    for workstation in sorted(unlicensed):
        print(f"{workstation}: UNLICENSED - {', '.join(unlicensed[workstation])}")
    for software, count, seat_count in over_seats:
        print(f"{software}: OVER SEATS - installed on {count} workstation(s), "
              f"only {seat_count} seat(s) licensed")
    total_unlicensed = sum(len(v) for v in unlicensed.values())
    print(f"{total_unlicensed} unlicensed install(s) across "
          f"{len(unlicensed)} workstation(s); {len(over_seats)} software title(s) over seats.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
