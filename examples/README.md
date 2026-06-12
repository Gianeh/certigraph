# CertiGraph examples

## JSON certificates

- `sssp_valid.json`
- `msf_valid.json`
- `maxflow_valid.json`
- `topo_valid.json`
- `bipartition_valid.json`

Verify them with:

```bash
python -m certigraph verify sssp examples/sssp_valid.json
python -m certigraph verify msf examples/msf_valid.json
python -m certigraph verify maxflow examples/maxflow_valid.json
python -m certigraph verify topo examples/topo_valid.json
python -m certigraph verify bipartition examples/bipartition_valid.json
```

## Runnable demos

- `ai_solver_wrong_answer_demo.py`: shows CertiGraph rejecting a plausible but wrong result.
- `supply_chain_maxflow_demo.py`: max-flow/min-cut certificate for a tiny supply chain.
- `build_pipeline_topo_demo.py`: topological-order verification for a build pipeline.
- `networkx_adapter_demo.py`: optional NetworkX integration demo.

## Invalid examples

The `invalid/` directory contains tampered certificates useful for demos and regression tests.
