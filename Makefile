.PHONY: test coverage lint typecheck ci demo demo-video docs serve clean

test:
	python -m unittest discover -v

coverage:
	python -m coverage run -m unittest discover
	python -m coverage report

lint:
	ruff check certigraph tests examples scripts

typecheck:
	mypy certigraph

ci: test coverage lint

demo:
	python examples/ai_solver_wrong_answer_demo.py
	python examples/supply_chain_maxflow_demo.py
	python -m certigraph verify sssp examples/sssp_valid.json

demo-video:
	python scripts/generate_demo_video.py

docs:
	mkdocs build --strict

serve:
	mkdocs serve

clean:
	rm -rf __pycache__ .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov build dist *.egg-info
	find . -name '__pycache__' -type d -prune -exec rm -rf {} +
	rm -rf docs/assets/demo_slides
