import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import audit

def installed(workstation, software, version="1.0"):
    return {"workstation": workstation, "software": software, "version": version}

def licensed(software, seats):
    return {"software": software, "licensed_seats": str(seats)}

class TestLicenseAudit(unittest.TestCase):
    def test_unlicensed_flagged(self):
        unlicensed, _ = audit([installed("WS-1", "Video Editor")],
                              [licensed("Office Suite", 2)])
        self.assertEqual(unlicensed, {"WS-1": ["Video Editor"]})

    def test_licensed_not_flagged(self):
        unlicensed, _ = audit([installed("WS-1", "Office Suite")],
                              [licensed("Office Suite", 2)])
        self.assertEqual(unlicensed, {})

    def test_over_seats_detected(self):
        _, over = audit([installed("WS-1", "Office Suite"),
                         installed("WS-2", "Office Suite"),
                         installed("WS-3", "Office Suite")],
                        [licensed("Office Suite", 2)])
        self.assertEqual(over, [("Office Suite", 3, 2)])

    def test_exactly_at_seats_is_ok(self):
        _, over = audit([installed("WS-1", "Office Suite"),
                         installed("WS-2", "Office Suite")],
                        [licensed("Office Suite", 2)])
        self.assertEqual(over, [])

    def test_multiple_unlicensed_sorted(self):
        unlicensed, _ = audit([installed("WS-1", "Video Editor"),
                               installed("WS-1", "Photo Editor")],
                              [licensed("Office Suite", 2)])
        self.assertEqual(unlicensed["WS-1"], ["Photo Editor", "Video Editor"])

    def test_duplicate_install_same_workstation_counted_once(self):
        unlicensed, _ = audit([installed("WS-1", "Video Editor"),
                               installed("WS-1", "Video Editor")],
                              [licensed("Office Suite", 2)])
        self.assertEqual(unlicensed["WS-1"], ["Video Editor"])

    def test_over_seats_sorted_by_software(self):
        _, over = audit([installed("WS-1", "B App"), installed("WS-2", "B App"),
                         installed("WS-1", "A App"), installed("WS-2", "A App")],
                        [licensed("A App", 1), licensed("B App", 1)])
        self.assertEqual([o[0] for o in over], ["A App", "B App"])

    def test_empty_input(self):
        self.assertEqual(audit([], []), ({}, []))
