import unittest

from exception_desk.experiments import (
    HANDLING_TIME_ASSUMPTIONS,
    POLICY_NAMES,
    PREDECLARED_METRICS,
    generate_seeded_workload,
    run_scenario_sweep,
)


class ExperimentTests(unittest.TestCase):
    def test_handling_time_assumptions_are_explicit_and_ordered(self):
        self.assertEqual(
            set(HANDLING_TIME_ASSUMPTIONS),
            {"evidence_mismatch", "timeout_reconciliation", "delivery_recovery", "refund_investigation"},
        )
        for assumption in HANDLING_TIME_ASSUMPTIONS.values():
            self.assertLess(assumption["fast"], assumption["base"])
            self.assertLess(assumption["base"], assumption["slow"])

    def test_seeded_workloads_are_deterministic_and_seed_sensitive(self):
        first = generate_seeded_workload(7, case_count=12)
        self.assertEqual(first, generate_seeded_workload(7, case_count=12))
        self.assertNotEqual(first, generate_seeded_workload(8, case_count=12))

    def test_delays_change_only_actionability_and_duration_scaling_is_exact(self):
        base = generate_seeded_workload(11, case_count=20)
        delayed = generate_seeded_workload(
            11,
            case_count=20,
            duration_multiplier=2.0,
            evidence_delay_minutes=15,
            finality_delay_minutes=10,
        )
        for original, changed in zip(base, delayed):
            self.assertEqual(original["opened_at"], changed["opened_at"])
            self.assertEqual(original["deadline"], changed["deadline"])
            self.assertEqual(original["amount_atomic"], changed["amount_atomic"])
            self.assertEqual(original["duration_minutes"] * 2, changed["duration_minutes"])
            expected_delay = 25 if original["exception_type"] in {"evidence_mismatch", "timeout_reconciliation"} else 15
            self.assertEqual(changed["actionable_at"] - original["actionable_at"], expected_delay)

    def test_small_sweep_covers_cartesian_scenarios_and_is_deterministic(self):
        kwargs = {
            "seeds": (1, 2),
            "case_count": 12,
            "staffing_levels": (1, 2),
            "duration_multipliers": (0.5, 1.0),
            "evidence_delays": (0.0, 15.0),
            "finality_delays": (0.0, 10.0),
        }
        first = run_scenario_sweep(**kwargs)
        second = run_scenario_sweep(**kwargs)
        self.assertEqual(first, second)
        self.assertEqual(first["scenario_count"], 32)
        self.assertEqual(first["predeclared_metrics"], list(PREDECLARED_METRICS))

    def test_every_scenario_uses_one_workload_and_accounts_for_work(self):
        result = run_scenario_sweep(
            seeds=(4,),
            case_count=15,
            staffing_levels=(1, 3),
            duration_multipliers=(2.0,),
            evidence_delays=(15.0,),
            finality_delays=(10.0,),
            horizon_minutes=120,
        )
        for scenario in result["scenarios"]:
            fingerprints = {item["workload_fingerprint"] for item in scenario["results"].values()}
            self.assertEqual(fingerprints, {scenario["workload_fingerprint"]})
            for policy_result in scenario["results"].values():
                self.assertEqual(policy_result["touches"] + policy_result["unfinished_count"], 15)
                self.assertEqual(
                    policy_result["control_failures"] + policy_result["unfinished_control_failures"],
                    policy_result["total_control_failures"],
                )

    def test_win_credit_sums_to_one_and_distributions_are_ordered(self):
        result = run_scenario_sweep(
            seeds=(1, 2, 3),
            case_count=20,
            staffing_levels=(1,),
            duration_multipliers=(0.5, 2.0),
            evidence_delays=(0.0,),
            finality_delays=(0.0,),
        )
        for metric in PREDECLARED_METRICS:
            self.assertAlmostEqual(sum(result["summary"][policy][metric]["win_rate"] for policy in POLICY_NAMES), 1.0)
            for policy in POLICY_NAMES:
                distribution = result["summary"][policy][metric]
                self.assertLessEqual(distribution["minimum"], distribution["p50"])
                self.assertLessEqual(distribution["p50"], distribution["p95"])
                self.assertLessEqual(distribution["p95"], distribution["maximum"])

    def test_adverse_workloads_create_policy_tradeoffs(self):
        result = run_scenario_sweep(
            seeds=range(10),
            case_count=30,
            staffing_levels=(1,),
            duration_multipliers=(2.0,),
            evidence_delays=(0.0,),
            finality_delays=(0.0,),
        )
        overdue_winners = {tuple(scenario["winners"]["overdue_count"]) for scenario in result["scenarios"]}
        value_winners = {tuple(scenario["winners"]["value_weighted_overdue_minutes"]) for scenario in result["scenarios"]}
        self.assertNotEqual(overdue_winners, value_winners)

    def test_invalid_dimensions_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "at least one seed"):
            run_scenario_sweep(seeds=())
        with self.assertRaisesRegex(ValueError, "positive integer"):
            generate_seeded_workload(1, case_count=0)


if __name__ == "__main__":
    unittest.main()
