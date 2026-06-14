import unittest

from certigraph import (
    check_bipartition,
    check_connected_components,
    check_max_flow_certificate,
    check_minimum_spanning_forest_certificate,
    check_sssp_certificate,
    check_topological_order,
)


class TestInvalidInputs(unittest.TestCase):
    def test_duplicate_vertices_rejected(self):
        self.assertFalse(check_topological_order(["a", "a"], [], ["a", "a"]).ok)

    def test_bad_edge_shape_rejected_without_exception(self):
        result = check_sssp_certificate(["s"], [object()], "s", {"s": 0}, {"s": None})
        self.assertFalse(result.ok)
        self.assertIn("edge", result.message)

    def test_bad_parent_edge_index_rejected_without_exception(self):
        result = check_sssp_certificate(
            ["s", "a"],
            [("s", "a", 1)],
            "s",
            {"s": 0, "a": 1},
            {"s": None, "a": {"u": "s", "edge": 0.5}},
        )
        self.assertFalse(result.ok)

    def test_negative_capacity_rejected(self):
        result = check_max_flow_certificate(["s", "t"], [("s", "t", -1)], "s", "t", [0], ["s"])
        self.assertFalse(result.ok)

    def test_msf_rejects_duplicate_chosen_edges(self):
        result = check_minimum_spanning_forest_certificate(["a", "b"], [("a", "b", 1)], [0, 0])
        self.assertFalse(result.ok)

    def test_bipartition_missing_color(self):
        result = check_bipartition(["a", "b"], [("a", "b")], {"a": 0})
        self.assertFalse(result.ok)

    def test_connected_components_bad_edge_shape(self):
        result = check_connected_components(["a", "b"], [object()], {"a": 0, "b": 0})
        self.assertFalse(result.ok)
        self.assertIn("edge", result.message)

    def test_connected_components_missing_label(self):
        result = check_connected_components(["a", "b"], [("a", "b")], {"a": 0})
        self.assertFalse(result.ok)


if __name__ == "__main__":
    unittest.main()
