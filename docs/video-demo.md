# Video demo

<video controls width="100%" poster="assets/certigraph-demo-thumbnail.png">
  <source src="assets/certigraph-demo.mp4" type="video/mp4">
</video>

The demo shows CertiGraph's core promise in under one minute: a plausible but wrong AI-generated shortest-path result is rejected, while a proof-carrying result with a valid certificate is accepted.

## Assets

- Full video: [`assets/certigraph-demo.mp4`](assets/certigraph-demo.mp4)
- Teaser GIF for README and social previews: [`assets/certigraph-demo-teaser.gif`](assets/certigraph-demo-teaser.gif)
- Thumbnail: [`assets/certigraph-demo-thumbnail.png`](assets/certigraph-demo-thumbnail.png)
- Captions: [`assets/certigraph-demo.srt`](assets/certigraph-demo.srt)

## Storyboard

1. Introduce CertiGraph as proof-carrying graph results for untrusted and AI-generated solvers.
2. Show why graph answers increasingly come from black boxes: LLM agents, remote APIs, GPU jobs, and distributed solvers.
3. Explain the contract: instance plus result plus certificate goes to a small checker.
4. Demonstrate a wrong shortest-path answer and the rejection message.
5. Demonstrate a valid shortest-path certificate and successful CLI verification.
6. List the shipped checkers: SSSP, MSF/MST, max-flow/min-cut, topological order, and bipartition.
7. Invite contributions: new checkers, integrations, fuzzing, exact numerics, and formal verification.

## Rebuild

The video can be regenerated from repository assets with:

```bash
python -m pip install pillow
python scripts/generate_demo_video.py
```

The script expects `ffmpeg` to be available on `PATH`. CertiGraph itself remains dependency-free; Pillow and ffmpeg are only needed to regenerate marketing assets.
