FROM python:3.13-slim
WORKDIR /app
COPY . /app
RUN python -m pip install --no-cache-dir -U pip && python -m pip install --no-cache-dir -e .
CMD ["python", "-m", "unittest", "discover", "-v"]
