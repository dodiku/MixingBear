
[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

# MixingBear
Automatic beat-mixing of music files in Python, using [AudioOwl](https://github.com/dodiku/AudioOwl) 🎚

**Jump to:**
- [Quickstart](https://github.com/dodiku/MixingBear#quickstart)
- [Installation](https://github.com/dodiku/MixingBear#installation)
- [Usage](https://github.com/dodiku/MixingBear#usage)


![MixingBear](https://raw.githubusercontent.com/dodiku/MixingBear/master/Images/MixingBear.png)

# Quickstart
Mix two WAV files -
```python
import mixingbear
mixingbear.mix('track01.wav', 'track02.wav', 'output.wav')
```
# Installation
> Tested on Python 3.6 or later


> ⚠️ AudioOwl needs **ffmpeg** to be installed on your machine.
> The easiest way to install ffmpeg (at least on a Mac) is using homebrew. [See instructions here](https://gist.github.com/clayton/6196167).


The latest stable release is available on PyPI.  
Install it using the following command -

```bash
$ pip install mixingbear
```

# Usage

## ``mixingbear.mix()``
Saves a mixed WAV file locally to ``output_file_path``

Supported keyword arguments for ``audioowl.get_waveform()``:
- ``top_file`` - Path to a WAV file you want to mix onto ``bottom_file``. e.g. ``top_file=wav_file.wav``
- ``bottom_file`` - Path to a WAV file you want to mix ``top_file`` onto. e.g. ``bottom_file=wav_file.wav``
- ``output_file_path`` - Path for the mixed output WAV file you want to mix ``output_file_path`` onto. e.g. ``bottom_file=output.wav``
- ``mix_mode`` *[optional, default == 'random']* - String:
  - ``random`` - MixingBear will find the best mixing points, and will mix the tracks starting on a random one out of them.
  - ``first`` - MixingBear will find the best mixing points, and will mix the tracks on the **first** one.
- ``sr`` *[optional, default == 22050]* - Integer. Sample rate.
- ``offset`` *[optional, default == 880, equal to ~20 milliseconds on a track with 44100 sample rate]* - Integer. Number of samples to use as padding on beats, to choose sync points. e.g. With offset=880, beats will be considered as 'matching' is they are positioned away from each other in 880 samples or less.
- ``trim_silence`` *[optional, default == True]* - Boolean. If True, MixingBear will trim leading silence on ``top_file``.
