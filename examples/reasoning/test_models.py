from fractions import Fraction as F
from itertools import combinations, product
import random
import unittest

from .models import (bayes_binary, check_entailment, implies, iter_solutions,
                     minimize_cost, relative_change, weighted_mean)


class LogicTests(unittest.TestCase):
    def test_implication_all_rows(self):
        self.assertEqual([implies(p, q) for p, q in product((False, True), repeat=2)],
                         [True, True, False, True])

    def test_contrapositive_and_converse(self):
        for p, q in product((False, True), repeat=2):
            self.assertEqual(implies(p, q), implies(not q, not p))
        result = check_entailment(['p', 'q'], [lambda a: implies(a['p'], a['q']), lambda a: a['q']], lambda a: a['p'])
        self.assertFalse(result['entails'])
        self.assertEqual(result['counterexample'], {'p': False, 'q': True})

    def test_modus_ponens(self):
        result = check_entailment(['p', 'q'], [lambda a: implies(a['p'], a['q']), lambda a: a['p']], lambda a: a['q'])
        self.assertEqual(result, {'entails': True, 'premise_models': 1, 'counterexample': None})

    def test_inconsistent_premises_are_identified(self):
        result = check_entailment(['p'], [lambda a: a['p'], lambda a: not a['p']], lambda a: False)
        self.assertTrue(result['entails'])
        self.assertEqual(result['premise_models'], 0)

    def test_quantifier_negation_on_all_small_predicates(self):
        for n in range(5):
            for predicate in product((False, True), repeat=n):
                self.assertEqual(not all(predicate), any(not p for p in predicate))
                self.assertEqual(not any(predicate), all(not p for p in predicate))

    def test_invalid_variables(self):
        for names in (['p', 'p'], list(range(17))):
            with self.assertRaises(ValueError):
                check_entailment(names, [], lambda a: True)


class QuantitativeTests(unittest.TestCase):
    def test_percent_and_percentage_points(self):
        self.assertEqual(relative_change(20, 25), F(1, 4))
        self.assertEqual(relative_change(100, 120), F(1, 5))
        self.assertEqual(relative_change(120, 100), -F(1, 6))

    def test_weighted_mean_matches_expanded_population(self):
        rng = random.Random(72)
        for _ in range(100):
            values = [rng.randrange(-20, 21) for _ in range(5)]
            weights = [rng.randrange(1, 6) for _ in range(5)]
            population = [v for v, count in zip(values, weights) for _ in range(count)]
            self.assertEqual(weighted_mean(values, weights), F(sum(population), len(population)))

    def test_weight_scale_and_decimal_exactness(self):
        self.assertEqual(weighted_mean([80, 50], [20, 80]), 56)
        self.assertEqual(weighted_mean([80, 50], [2, 8]), 56)
        self.assertEqual(weighted_mean(['0.1', '0.2'], [1, 1]), F(3, 20))

    def test_bayes_matches_population_counts(self):
        self.assertEqual(bayes_binary('0.01', '0.9', '0.05'), F(2, 13))
        for affected in (1, 5, 20, 50):
            for hit in (F(1, 2), F(3, 4), F(1)):
                for false in (F(1, 10), F(1, 5)):
                    true_events = affected * hit
                    false_events = (100-affected) * false
                    self.assertEqual(bayes_binary(F(affected, 100), hit, false),
                                     true_events/(true_events+false_events))

    def test_bayes_limits(self):
        self.assertEqual(bayes_binary(F(1, 3), F(2, 5), F(2, 5)), F(1, 3))
        self.assertEqual(bayes_binary(F(1, 3), 1, 0), 1)
        self.assertEqual(bayes_binary(0, 1, 1), 0)

    def test_invalid_inputs(self):
        calls = [(weighted_mean, ([1], [0])), (weighted_mean, ([1], [-1])),
                 (weighted_mean, ([1, 2], [1])), (relative_change, (0, 1)),
                 (bayes_binary, (F(1, 2), 0, 0)), (bayes_binary, (2, 1, 1))]
        for function, args in calls:
            with self.assertRaises(ValueError):
                function(*args)


class ConstraintTests(unittest.TestCase):
    def normalize(self, solutions, names):
        return {tuple(s[n] for n in names) for s in solutions}

    def brute(self, domains, constraints):
        names = tuple(domains)
        return [dict(zip(names, values)) for values in product(*(domains[n] for n in names))
                if all(predicate(dict(zip(names, values))[x], dict(zip(names, values))[y])
                       for x, y, predicate in constraints)]

    def test_three_slot_example(self):
        domains = {x: [1, 2, 3] for x in 'ABC'}
        constraints = [(x, y, lambda a, b: a != b) for x, y in combinations(domains, 2)]
        constraints += [('A', 'B', lambda a, b: a < b), ('B', 'C', lambda b, c: b < c)]
        self.assertEqual(list(iter_solutions(domains, constraints)), [{'A': 1, 'B': 2, 'C': 3}])

    def test_random_models_against_exhaustive_reference(self):
        rng = random.Random(2219)
        for _ in range(80):
            domains = {x: [0, 1, 2] for x in 'ABCD'}
            constraints = []
            for x, y in combinations(domains, 2):
                if rng.random() < .7:
                    allowed = {(a, b) for a, b in product(range(3), repeat=2) if rng.random() < .5}
                    constraints.append((x, y, lambda a, b, allowed=allowed: (a, b) in allowed))
            expected = self.brute(domains, constraints)
            self.assertEqual(self.normalize(iter_solutions(domains, constraints), domains), self.normalize(expected, domains))
            costs = {x: {v: rng.randrange(-5, 11) for v in domains[x]} for x in domains}
            assignment, cost = minimize_cost(domains, constraints, costs)
            if not expected:
                self.assertIsNone(assignment)
                self.assertIsNone(cost)
            else:
                self.assertIn(assignment, expected)
                self.assertEqual(cost, min(sum(costs[x][s[x]] for x in domains) for s in expected))

    def test_arc_consistency_not_global_solution(self):
        domains = {x: [0, 1] for x in 'ABC'}
        constraints = [(x, y, lambda a, b: a != b) for x, y in combinations(domains, 2)]
        self.assertEqual(list(iter_solutions(domains, constraints)), [])

    def test_repeated_pair_constraints_and_reverse_orientation(self):
        domains = {'A': [1, 2, 3], 'B': [1, 2, 3]}
        constraints = [('A', 'B', lambda a, b: a < b), ('B', 'A', lambda b, a: b-a == 2)]
        self.assertEqual(list(iter_solutions(domains, constraints)), [{'A': 1, 'B': 3}])

    def test_minimum_and_equal_cost_ties(self):
        domains = {'A': [1, 2], 'B': [1, 2]}
        constraints = [('A', 'B', lambda a, b: a != b)]
        costs = {'A': {1: -2, 2: 2}, 'B': {1: 0, 2: 0}}
        self.assertEqual(minimize_cost(domains, constraints, costs), ({'A': 1, 'B': 2}, -2))
        assignment, cost = minimize_cost(domains, constraints, {x: {1: 0, 2: 0} for x in domains})
        self.assertEqual(cost, 0)
        self.assertIn(assignment, [{'A': 1, 'B': 2}, {'A': 2, 'B': 1}])

    def test_empty_and_disconnected_models(self):
        self.assertEqual(list(iter_solutions({}, [])), [{}])
        self.assertEqual(minimize_cost({}, [], {}), ({}, 0))
        self.assertEqual(list(iter_solutions({'A': []}, [])), [])
        self.assertEqual(len(list(iter_solutions({'A': [1, 1, 2], 'B': [4, 5]}, []))), 4)

    def test_input_not_mutated_and_invalid_model(self):
        domains = {'A': [1, 2], 'B': [1, 2]}
        list(iter_solutions(domains, [('A', 'B', lambda a, b: a < b)]))
        self.assertEqual(domains, {'A': [1, 2], 'B': [1, 2]})
        with self.assertRaises(ValueError):
            list(iter_solutions(domains, [('A', 'X', lambda a, b: True)]))


if __name__ == '__main__':
    unittest.main()
