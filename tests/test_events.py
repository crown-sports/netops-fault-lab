import copy
from dataclasses import replace
from pathlib import Path
import unittest

from netops_fault_lab import Case, diagnose, fit_noise
from netops_fault_lab.schema import read_json


class EventTests(unittest.TestCase):
    def setUp(self):
        self.raw = read_json(Path(__file__).resolve().parents[1] / 'examples/ambiguous.json')
        for probe in self.raw['observations']:
            probe['event_id'] = 'event-' + probe['id']

    def test_retransmission_leaves_posterior_recommendation_and_fit_unchanged(self):
        original = Case.from_dict(self.raw)
        for probe in list(self.raw['observations']):
            for index in range(4):
                self.raw['observations'].append({**probe, 'id': f'{probe["id"]}-copy-{index}'})
        repeated = Case.from_dict(self.raw)
        before, after = diagnose(original), diagnose(repeated)
        for key in ['ranking', 'next_probes', 'status', 'entropy_bits', 'observed_probes']:
            self.assertEqual(before[key], after[key])
        self.assertEqual(after['deduplicated_probe_records'], len(original.observed) * 4)
        self.assertEqual(after['missing_probes'], 0)
        self.assertEqual(fit_noise([(original, 'core')]), fit_noise([(repeated, 'core')]))
        self.assertEqual(len(after['event_deduplication']), len(original.observed))

    def test_different_event_ids_keep_independent_repeated_measurements(self):
        original = Case.from_dict(self.raw)
        probe = self.raw['observations'][0]
        self.raw['observations'].append({**probe, 'id': 'new-probe', 'event_id': 'new-event'})
        result = diagnose(Case.from_dict(self.raw))
        self.assertEqual(result['observed_probes'], len(original.observed) + 1)
        self.assertEqual(result['deduplicated_probe_records'], 0)
        self.assertNotEqual(result['ranking'], diagnose(original)['ranking'])

    def test_untagged_records_preserve_previous_behavior(self):
        for probe in self.raw['observations']:
            del probe['event_id']
        self.raw['observations'].append({**self.raw['observations'][0], 'id': 'copy'})
        self.assertEqual(len(Case.from_dict(self.raw).observed), len(self.raw['observations']))

    def test_conflicting_copy_rejected_in_json_and_direct_api(self):
        for field, value in [('outcome', 'pass'), ('path', ['r1', 'r2'])]:
            raw = copy.deepcopy(self.raw)
            raw['observations'].append({**raw['observations'][0], 'id': 'copy', field: value})
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, 'Conflicting'):
                Case.from_dict(raw)
        case = Case.from_dict(self.raw)
        conflict = replace(case.observations[0], id='copy', outcome='pass')
        with self.assertRaisesRegex(ValueError, 'Conflicting'):
            diagnose(replace(case, observations=(*case.observations, conflict)))

    def test_missing_event_copies_count_once_without_becoming_evidence(self):
        self.raw['observations'] = [dict(self.raw['observations'][0], outcome='missing')]
        self.raw['observations'].append({**self.raw['observations'][0], 'id': 'copy'})
        report = diagnose(Case.from_dict(self.raw))
        self.assertEqual((report['observed_probes'], report['missing_probes'],
                          report['deduplicated_probe_records']), (0, 1, 1))

    def test_bad_event_ids_and_candidates_rejected(self):
        for value in ['', None, 3, 'bad\nvalue']:
            raw = copy.deepcopy(self.raw)
            raw['observations'][0]['event_id'] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                Case.from_dict(raw)
        self.raw['available_probes'][0]['event_id'] = 'not-observed'
        with self.assertRaises(ValueError):
            Case.from_dict(self.raw)
