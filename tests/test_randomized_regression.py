import random
import unittest

from certigraph import (
    bellman_ford_certificate,
    bipartition_certificate,
    check_bipartition,
    check_connected_components,
    check_max_flow_certificate,
    check_minimum_spanning_forest_certificate,
    check_sssp_certificate,
    check_topological_order,
    connected_components_certificate,
    edmonds_karp_certificate,
    kruskal_msf_certificate,
    topological_order_certificate,
)


class TestRandomizedRegression(unittest.TestCase):
    def test_random_nonnegative_sssp_certificates(self):
        rng = random.Random(1337)
        for n in range(2, 9):
            vertices = list(range(n))
            edges = []
            for u in vertices:
                for v in vertices:
                    if u != v and rng.random() < 0.22:
                        edges.append((u, v, rng.randint(0, 9)))
            distance, parent = bellman_ford_certificate(vertices, edges, 0)
            self.assertTrue(check_sssp_certificate(vertices, edges, 0, distance, parent).ok)

    def test_random_msf_certificates(self):
        rng = random.Random(2026)
        for n in range(2, 10):
            vertices = list(range(n))
            edges = []
            for u in vertices:
                for v in range(u + 1, n):
                    if rng.random() < 0.35:
                        edges.append((u, v, rng.randint(-5, 20)))
            chosen = kruskal_msf_certificate(vertices, edges)
            self.assertTrue(check_minimum_spanning_forest_certificate(vertices, edges, chosen).ok)

    def test_random_maxflow_certificates(self):
        rng = random.Random(9001)
        for n in range(3, 8):
            vertices = list(range(n))
            source, sink = 0, n - 1
            edges = []
            for u in vertices:
                for v in vertices:
                    if u != v and rng.random() < 0.22:
                        edges.append((u, v, rng.randint(0, 8)))
            # Ensure at least one possible route in many cases.
            edges.extend((i, i + 1, rng.randint(1, 5)) for i in range(n - 1))
            flow, cut = edmonds_karp_certificate(vertices, edges, source, sink)
            self.assertTrue(check_max_flow_certificate(vertices, edges, source, sink, flow, cut).ok)

    def test_random_topological_orders(self):
        rng = random.Random(17)
        for n in range(2, 12):
            vertices = list(range(n))
            edges = []
            for u in range(n):
                for v in range(u + 1, n):
                    if rng.random() < 0.3:
                        edges.append((u, v))
            order = topological_order_certificate(vertices, edges)
            self.assertTrue(check_topological_order(vertices, edges, order).ok)

    def test_random_bipartitions(self):
        rng = random.Random(314)
        for left_size in range(1, 6):
            right_size = left_size + 1
            left = [f"L{i}" for i in range(left_size)]
            right = [f"R{i}" for i in range(right_size)]
            vertices = left + right
            edges = [(u, v) for u in left for v in right if rng.random() < 0.4]
            color = bipartition_certificate(vertices, edges)
            self.assertTrue(check_bipartition(vertices, edges, color).ok)

    def test_random_connected_components(self):
        rng = random.Random(4242)
        for n in range(1, 16):
            vertices = list(range(n))
            edges = []
            for u in range(n):
                for v in range(u + 1, n):
                    if rng.random() < 0.25:
                        edges.append((u, v))
            component = connected_components_certificate(vertices, edges)
            self.assertTrue(check_connected_components(vertices, edges, component).ok)


if __name__ == "__main__":
    unittest.main()
