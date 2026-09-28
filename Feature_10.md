# Feature 10: Smart Segment Post-Processing

## Problem
Fixed-duration splitting (e.g., "every 10 minutes") creates poor UX:
- **Too-short segments** (< 5 min): often intros, outros, or transition fragments
- **Too-long segments** (> 15 min): the fixed grid missed a real track boundary

## Solution: Deterministic Post-Processing Rules
Apply simple heuristics *after* the fixed-duration split — no ML, no external deps, runs in milliseconds.

### Rules
1. **Merge short segments** (< 5 min): attach to previous segment (or next if first)
2. **Split long segments** (> 15 min): cut at midpoint, optionally snapped to nearest onset

### Pseudocode
```python
def post_process_segments(segments, min_dur=300, max_dur=900):
    """
    segments: list of (start_sec, end_sec) from fixed-duration splitter
    """
    # 1. Merge too-short segments
    merged = []
    for seg in segments:
        dur = seg[1] - seg[0]
        if dur < min_dur and merged:
            merged[-1] = (merged[-1][0], seg[1])  # extend previous
        else:
            merged.append(seg)

    # 2. Split too-long segments
    final = []
    for seg in merged:
        dur = seg[1] - seg[0]
        if dur > max_dur:
            mid = seg[0] + dur / 2
            final.append((seg[0], mid))
            final.append((mid, seg[1]))
        else:
            final.append(seg)

    return final
```

### Optional Refinement: Snap to Nearest Onset
Instead of splitting at exact midpoint, find the nearest energy dip (onset) within ±30s — cuts at musical moments.

```python
import librosa
import numpy as np

def split_at_nearest_onset(audio_path, target_mid, window=30):
    """Return adjusted split point near target_mid."""
    y, sr = librosa.load(audio_path, offset=target_mid - window, duration=2 * window)
    onsets = librosa.onset.onset_detect(y=y, sr=sr, units='time')
    if len(onsets) > 0:
        # onsets are relative to the loaded chunk; convert to absolute time
        absolute_onsets = target_mid - window + onsets
        return absolute_onsets[np.argmin(np.abs(absolute_onsets - target_mid))]
    return target_mid  # fallback
```

**Cost**: one extra `librosa.load()` per long segment (~50-100ms).

---

## Alternative Approaches (for Future Consideration)

| Approach | Effort | Accuracy | Dependencies |
|----------|--------|----------|--------------|
| **Current: Heuristic post-process** | Low | Removes worst UX issues | None |
| **MSAF (music structure analysis)** | Low-Med | Finds structural boundaries (verse/chorus), not necessarily track boundaries | `msaf` (Python) |
| **librosa custom pipeline** (onset + chroma + self-similarity) | Medium | Better, but needs tuning | `librosa` |
| **madmom / Essentia** (CNN structure models) | Medium-High | Good for electronic music | `madmom`, `essentia` |
| **Deep learning** (SOTA: CNNs/Transformers on mel-spec) | High | Best — learns "DJ transition" patterns | PyTorch/TensorFlow, GPU, training data |

### When to Upgrade
- Users report "still cuts in the middle of tracks" after heuristic rules
- You have labeled mixes (start/end timestamps) for training/eval
- You're willing to add `librosa` + model weights (~50-100MB) to the installer

---

## Implementation Notes
- Add as optional step in `MP3Splitter.split()` or new `SmartSplitter` subclass
- Configurable thresholds via settings (`MIN_SEGMENT_MINUTES`, `MAX_SEGMENT_MINUTES`)
- Keep FFmpeg path unchanged — post-process only adjusts *timestamps*, then re-runs split commands
- Unit tests: synthetic segments covering merge/split/both cases

---

## Related
- Feature 6: Windows installer (bundles FFmpeg)
- Current `MP3Splitter.split()` in `src/splitter.py`