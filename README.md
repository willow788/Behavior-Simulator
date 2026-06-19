# Behavior-Simulator

A simple, exploratory agent-based behavioral simulator implemented in Python. The project demonstrates how stress, focus, and energy propagate through a population of agents on a 2D grid (and later as a small social network). It includes three progressively more complex versions (version1.py, version2.py, version3.py) and several screenshots showing the simulator and how global stress evolves.

Highlights
- Visual, animated simulation of stress spreading across agents using matplotlib.
- Models agent states: stress, focus (1 - stress), and energy.
- Adds per-agent behavioral traits (resilience, influence) and random stress events.
- A networked version (version3) where agents have explicit connections (friends) and the average stress trend is plotted.

Screenshots
- Main UI / animation: ![Simulator screenshot](https://raw.githubusercontent.com/willow788/Behavior-Simulator/main/screenshot.png)
- Version 2 demo: ![Version 2 demo](https://raw.githubusercontent.com/willow788/Behavior-Simulator/main/vers2demo.png.png)
- Version 3 demo: ![Version 3 demo](https://raw.githubusercontent.com/willow788/Behavior-Simulator/main/Version3demo.png.png)
- Average stress trend: ![Stress mean](https://raw.githubusercontent.com/willow788/Behavior-Simulator/main/stress_mean.png)

Table of contents
- Overview
- How the simulation works
- Files in this repository
- Quick start (requirements & run)
- Example usage and parameters to tweak
- Extensions & possible improvements
- License & contribution

Overview
--------
This repository contains a small set of Python scripts that simulate and visualize how "stress" spreads in a population. The simulator is intentionally simple and intended for experimentation, teaching, or quick prototyping of social contagion-like dynamics.

How the simulation works (conceptual)
------------------------------------
Each agent is represented by a cell in a 2D grid (N x N). Every agent has:
- stress: value in [0, 1], higher = more stressed.
- focus: computed as 1 - stress (so stress reduces focus).
- energy: value in [0, 1], used in recovery dynamics.

Propagation rules (summary)
- Neighbour or connection-based influence: if a neighbour/connection has stress above a threshold (0.7), it can increase the agent's stress proportional to a spread rate and possibly the neighbour's influence.
- Recovery: every step agents recover an amount proportional to recovery_rate, energy, and (in versions with resilience) the agent's resilience.
- Energy is updated each step (small passive recovery minus stress-driven drain) and clamped to [0,1].
- Additional stochastic events: periodic random stress injections to model sudden shocks.

Files in the repository
-----------------------
- version1.py — Basic grid-based stress spread using 4-neighbour interactions.
- version2.py — Adds per-agent traits: resilience (faster recovery) and influence (how strongly an agent spreads stress). Also includes periodic and one-off stress events.
- version3.py — Replaces local grid neighbours with a small explicit social network (each agent has 3 random connections); tracks and plots average stress over time.
- requirements.txt — Long list of packages; likely more than necessary for running the simple matplotlib-based scripts. The core dependencies needed to run the demos are minimal (see Quick start).
- screenshot.png, vers2demo.png.png, Version3demo.png.png, stress_mean.png — Visuals for the project.

Quick start
-----------
Prerequisites
- Python 3.8+ recommended.
- The demos use numpy and matplotlib.

Install minimal dependencies (recommended for running the demos)
1. Create and activate a virtual environment (optional but recommended)
   - python -m venv .venv
   - source .venv/bin/activate  (Linux/macOS)
   - .venv\Scripts\activate     (Windows)

2. Install minimal packages
   - pip install numpy matplotlib

Note: requirements.txt contains a very large set of packages that are not required for these demos; installing it may be unnecessary and heavy. If you want a full environment as listed, you can run:
   - pip install -r requirements.txt
but expect long install times and many packages you likely don't need.

Running the demos
- version1 (basic local-neighbour spread)
  - python version1.py

- version2 (adds resilience & influence + occasional events)
  - python version2.py

- version3 (networked connections + average stress history plot)
  - python version3.py

Each script opens a matplotlib window showing an animated heatmap (stress levels). version3 additionally plots the average stress history after the animation completes.

Key parameters you can edit in the scripts
- N: grid size (N x N). Default 20. Increasing N increases simulation size and runtime/memory.
- stress_spread_rate: multiplies incoming stress from high-stress neighbors (default ~0.5).
- recovery_rate: per-step recovery factor (default ~0.003).
- energy update: energy = clip(energy + 0.01 - stress * 0.02, 0, 1) — tweak to simulate different energy dynamics.
- Frames & interval: animation.FuncAnimation(..., frames=300, interval=2500) — change frames or interval for longer/shorter runs or faster updates.
- Random stress events:
  - In version2 and version3: every 30 frames a localized stress injection is added; at frame==100 a global injection is applied. You can change frequency, magnitude, and conditions to experiment.
- In version2/3 agent traits:
  - resilience = np.random.rand(N, N) — values in (0,1); higher values increase recovery.
  - influence = np.random.rand(N, N) — scales how much an agent’s stress affects others.

Design and implementation notes
-------------------------------
- Boundary handling: version1/2 implement 4-neighbour updates and check indices to avoid out-of-range indices.
- version3 replaces the 4-neighbour rule with predefined random connections per agent (each agent has 3 friends), demonstrating non-local contagion through social ties.
- All values (stress, focus, energy) are clamped to [0,1] using np.clip to keep states realistic/valid.
- Visualization uses matplotlib's matshow with the 'plasma' colormap.

Potential improvements / next steps
----------------------------------
- Add command-line arguments (argparse) to tweak N, spread rates, recovery rates, frames, injection frequency, etc., without editing the scripts.
- Make the network structure configurable (e.g., small-world, scale-free, or real-world graph inputs).
- Save animations to video files (matplotlib.animation.Animation.save) or add an interactive UI (streamlit or a small GUI).
- Add more realistic recovery dynamics, fatigue, thresholds, or adaptive behavior (agents change influence/resilience over time).
- Add random seeds and deterministic runs for reproducible experiments.
- Replace random initialization of resilience/influence with distributions or classes that create distinct agent types (e.g., "leaders", "vulnerable", "resilient").
- Optimize: vectorize neighbor interactions to speed up simulation for larger N.

Troubleshooting
---------------
- If the matplotlib window does not appear, ensure you run the scripts in an environment that supports GUI display (local machine). For headless environments, consider saving frames or using a non-interactive backend (Agg) and saving animations to file.
- If the animation is slow: decrease the interval value in FuncAnimation or reduce N.
- If you see import errors, ensure numpy and matplotlib are installed in the active Python environment.

License
-------
Add a license of your choice (MIT, Apache, etc.). Currently none specified in the repo. If you want, we can add an MIT license file.

Contributing
------------
Contributions and suggestions are welcome. Good first PRs:
- Add argument parsing for configurable runs.
- Add README as a file in the repo (if not already present).
- Add unit tests for state-update logic.
- Add a script to save an animation/video.

Contact / Author
----------------
Repository owner: willow788 (https://github.com/willow788)

Acknowledgements
----------------
This project is a compact educational example exploring simple agent-based dynamics and visualizations with numpy + matplotlib.
