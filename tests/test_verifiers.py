import unittest

from certigraph import (
    bellman_ford_certificate,
    bipartition_certificate,
    check_bipartition,
    check_max_flow_certificate,
    check_minimum_spanning_forest_certificate,
    check_sssp_certificate,
    check_topological_order,
    edmonds_karp_certificate,
    kruskal_msf_certificate,
    topological_order_certificate,
)


class TestCertigraphVerifiers(unittest.TestCase):
    def test_sssp_valid_with_negative_edge_and_unreachable(self):
        vertices = ["s", "a", "b", "c", "z"]
        edges = [("s", "a", 2), ("s", "b", 5), ("a", "b", -1), ("b", "c", 2), ("a", "c", 5)]
        distance, parent = bellman_ford_certificate(vertices, edges, "s")
        result = check_sssp_certificate(vertices, edges, "s", distance, parent)
        self.assertTrue(result.ok, result)
        self.assertEqual(distance["c"], 3)
        self.assertIsNone(distance["z"])

    def test_sssp_rejects_tampered_distance(self):
        vertices = ["s", "a", "b"]
        edges = [("s", "a", 1), ("a", "b", 1), ("s", "b", 10)]
        distance, parent = bellman_ford_certificate(vertices, edges, "s")
        distance["b"] = 3
        result = check_sssp_certificate(vertices, edges, "s", distance, parent)
        self.assertFalse(result.ok)

    def test_sssp_rejects_unreachable_marked_after_reachable_edge(self):
        vertices = ["s", "a"]
        edges = [("s", "a", 1)]
        result = check_sssp_certificate(vertices, edges, "s", {"s": 0, "a": None}, {"s": None, "a": None})
        self.assertFalse(result.ok)

    def test_msf_valid_and_tampered(self):
        vertices = ["a", "b", "c", "d", "e"]
        edges = [("a", "b", 1), ("b", "c", 2), ("a", "c", 5), ("d", "e", -3)]
        chosen = kruskal_msf_certificate(vertices, edges)
        result = check_minimum_spanning_forest_certificate(vertices, edges, chosen)
        self.assertTrue(result.ok, result)
        self.assertEqual(set(chosen), {0, 1, 3})

        bad = check_minimum_spanning_forest_certificate(vertices, edges, [0, 2, 3])
        self.assertFalse(bad.ok)
        self.assertIn("cycle optimality", bad.message)

    def test_msf_rejects_non_spanning_forest(self):
        vertices = ["a", "b", "c"]
        edges = [("a", "b", 1), ("b", "c", 2)]
        result = check_minimum_spanning_forest_certificate(vertices, edges, [0])
        self.assertFalse(result.ok)

    def test_maxflow_valid_and_tampered(self):
        vertices = ["s", "a", "b", "t"]
        edges = [("s", "a", 3), ("s", "b", 2), ("a", "t", 2), ("b", "t", 3), ("a", "b", 1)]
        flow, cut = edmonds_karp_certificate(vertices, edges, "s", "t")
        result = check_max_flow_certificate(vertices, edges, "s", "t", flow, cut)
        self.assertTrue(result.ok, result)
        self.assertAlmostEqual(result.details["value"], 5)

        bad_flow = list(flow)
        bad_flow[0] -= 1
        bad = check_max_flow_certificate(vertices, edges, "s", "t", bad_flow, cut)
        self.assertFalse(bad.ok)

    def test_topological_order(self):
        vertices = ["parse", "typecheck", "optimize", "emit"]
        edges = [("parse", "typecheck"), ("typecheck", "optimize"), ("typecheck", "emit"), ("optimize", "emit")]
        order = topological_order_certificate(vertices, edges)
        self.assertTrue(check_topological_order(vertices, edges, order).ok)
        self.assertFalse(check_topological_order(vertices, edges, list(reversed(order))).ok)

    def test_bipartition(self):
        vertices = ["u1", "u2", "v1", "v2"]
        edges = [("u1", "v1"), ("u1", "v2"), ("u2", "v1")]
        color = bipartition_certificate(vertices, edges)
        self.assertTrue(check_bipartition(vertices, edges, color).ok)
        color["v1"] = color["u1"]
        self.assertFalse(check_bipartition(vertices, edges, color).ok)

    def test_bipartition_rejects_odd_cycle(self):
        vertices = [1, 2, 3]
        edges = [(1, 2), (2, 3), (3, 1)]
        with self.assertRaises(ValueError):
            bipartition_certificate(vertices, edges)


if __name__ == "__main__":
    unittest.main()
