# workstation-software-license-audit

Audit installed software per workstation against licences: UNLICENSED when software is installed but has no licence entry at all, OVER SEATS when it is installed on more workstations than its licensed seat count — workstations with unlicensed software first, then the over-seats summary.

Sample input is included (sample-installed.csv and sample-licenses.csv).

## How to run

```sh
python3 main.py sample-installed.csv sample-licenses.csv
```

## Example output

```
WS-2: UNLICENSED - Video Editor
Office Suite: OVER SEATS - installed on 3 workstation(s), only 2 seat(s) licensed
1 unlicensed install(s) across 1 workstation(s); 1 software title(s) over seats.
```

Standard library only. Run the tests with `python3 -m unittest discover`.
