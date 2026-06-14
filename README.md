# Underwater Propeller Fault Diagnosis Dataset

Original dataset for the paper:

**Quality-Aware Gated Cross-Modal Transformer for Noise-Robust Underwater Propeller Fault Diagnosis**

## Scope

This repository contains only the original synchronized samples used in the paper.
Generated degraded/robustness evaluation scenarios are not included.

The data is distributed as seven Git LFS tar archives under `archives/`, one archive per paper label. Extracting the archives restores:

```text
gcm_t_input_dataset_with_rpm_info/
```

## Dataset Summary

- Samples: 5,554 synchronized 1-second recordings
- Categories: 7 propeller conditions
- Speeds: 400, 600, and 800 RPM
- Modalities per sample: hydrophone audio, underwater image frames, electrical/RPM trace, metadata
- Audio: `audio_1s.npy`, float32, 64 kHz, shape `(64000,)`
- Visual frames: `frames/frame_00.png` to `frames/frame_14.png`, RGB, 224x224
- Electrical trace: `elec.npy`, float32, shape `(50, 4)`
- Metadata: `meta.json` with `label` and `control_rpm`

## Archives

| Archive | Label | Samples | Data bytes | Archive bytes |
|---|---:|---:|---:|---:|
| `archives/healthy.tar` | `healthy` | 946 | 723,068,401 | 753,725,440 |
| `archives/minor.tar` | `minor` | 712 | 546,068,948 | 569,180,160 |
| `archives/serious.tar` | `serious` | 704 | 535,892,920 | 558,694,400 |
| `archives/loss.tar` | `loss` | 834 | 802,488,471 | 829,542,400 |
| `archives/fishnet.tar` | `fishnet` | 683 | 655,917,141 | 678,072,320 |
| `archives/plastic.tar` | `plastic` | 1006 | 1,020,687,348 | 1,053,317,120 |
| `archives/3mm.tar` | `3mm` | 669 | 593,980,417 | 615,680,000 |
| **Total** |  | **5554** | **4,878,103,646** | **5,058,211,840** |

## Labels

| Label | Paper category | Samples |
|---|---:|---:|
| `healthy` | Healthy | 946 |
| `minor` | Minor Damage | 712 |
| `serious` | Serious Damage | 704 |
| `loss` | Propeller Loss | 834 |
| `fishnet` | Fishnet | 683 |
| `plastic` | Plastic bag | 1006 |
| `3mm` | 3 mm Rope | 669 |
| **Total** |  | **5554** |

## Metadata

Metadata files are in `metadata/`:

- `metadata/dataset_summary.json`
- `metadata/archive_manifest.csv`
- `metadata/sample_manifest.csv`
- `metadata/label_distribution.csv`
- `metadata/rpm_distribution.csv`

## Download

Install Git LFS before cloning:

```bash
git lfs install
git clone https://github.com/mailier1973/underwater-propeller-fault-diagnosis-dataset.git
cd underwater-propeller-fault-diagnosis-dataset
git lfs pull
```

Verify archive checksums:

```bash
python scripts/verify_archives.py
```

Extract the original dataset:

```bash
python scripts/extract_archives.py
```

After extraction, samples are available under `gcm_t_input_dataset_with_rpm_info/`.

## Usage

```python
from pathlib import Path
import json
import numpy as np
from PIL import Image

root = Path("gcm_t_input_dataset_with_rpm_info")
sample = next(root.iterdir())

audio = np.load(sample / "audio_1s.npy")
elec = np.load(sample / "elec.npy")
frames = [Image.open(sample / "frames" / f"frame_{i:02d}.png") for i in range(15)]
meta = json.loads((sample / "meta.json").read_text(encoding="utf-8"))

print(audio.shape, elec.shape, len(frames), meta)
```

## Notes

This repository intentionally excludes all non-paper labels and all generated degraded datasets. The public subset matches the paper's seven-category original dataset distribution.
