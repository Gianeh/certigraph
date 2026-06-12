# Run log

Environment: Python 3.13 in the execution sandbox.

## Commands executed successfully

```bash
python -m unittest discover -v
python scripts/validate_examples.py
python examples/ai_solver_wrong_answer_demo.py
python examples/supply_chain_maxflow_demo.py
python examples/build_pipeline_topo_demo.py
python -m certigraph verify sssp examples/sssp_valid.json
python -m certigraph verify msf examples/msf_valid.json
python -m certigraph verify maxflow examples/maxflow_valid.json
python -m certigraph verify topo examples/topo_valid.json
python -m certigraph verify bipartition examples/bipartition_valid.json
python -m certigraph hash examples/sssp_valid.json
python -m coverage run -m unittest discover
python -m coverage report
python -m compileall -q certigraph examples scripts benchmarks tests
python scripts/generate_assets.py
python scripts/generate_demo_video.py
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,duration,nb_frames docs/assets/certigraph-demo.mp4
```

## Observed results

- Unit tests: 26 tests passed.
- Valid JSON examples: 5 accepted.
- Invalid JSON examples: 4 rejected.
- Coverage, excluding CLI subprocess boundary, optional adapters, and `__main__`: 81%.
- Video demo: `docs/assets/certigraph-demo.mp4`, 1920×1080, 24 fps, 57 seconds, 1368 frames.
- Teaser GIF, thumbnail, SRT captions, social preview, SVG diagrams, and root visual assets regenerated after the layout review.
- Markdown/internal asset links: checked with a local link scanner; no missing relative targets found.
- JSON, YAML, TOML, and CFF files: parsed successfully with local parsers.

## Notes

`ruff` and `mypy` are configured in `pyproject.toml` and run in GitHub Actions after installing the `dev` extra. They were not installed in the sandbox before package installation, so they were not run locally here.
