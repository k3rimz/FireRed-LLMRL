# Pokemon FireRed RL Agent

A reinforcement learning agent that learns to play Pokemon FireRed using computer vision and deep learning.

## Setup

1. Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) if you haven't already.

2. Clone this repository:
```bash
git clone https://github.com/yourusername/pokemon-firered-rl.git
cd pokemon-firered-rl
```

3. Create and activate the conda environment:
```bash
conda env create -f environment.yml
conda activate pokemon-rl
```

4. Install the environment in Jupyter:
```bash
python -m ipykernel install --user --name pokemon-rl --display-name "Python (Pokemon-RL)"
```

## GPU Support

This project uses PyTorch with CUDA support. If you don't have a GPU, edit `environment.yml` and replace the PyTorch dependencies with:

```yaml
  - pytorch
  - torchvision
  - torchaudio
  - cpuonly
```

## Project Structure

- `environment.yml` - Conda environment configuration
- `src/` - Source code directory
  - `env/` - Pokemon game environment
  - `models/` - YOLO and CLIP models
  - `agents/` - RL agent implementation
  - `utils/` - Utility functions

## Requirements

- Python 3.10
- CUDA-capable GPU (recommended)
- VisualBoyAdvance-M emulator
- Pokemon FireRed ROM (not included)