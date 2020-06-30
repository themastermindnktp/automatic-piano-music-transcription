#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, division, print_function
import numpy as np
import sys
from madmom.processors import SequentialProcessor
import matplotlib.pyplot as plt

from amt.converter import CONVERTER_FOLDER


class PianoNoteProcessor(SequentialProcessor):
    def __init__(self, **kwargs):
        from madmom.audio.signal import SignalProcessor, FramedSignalProcessor
        from madmom.audio.stft import ShortTimeFourierTransformProcessor
        from madmom.audio.spectrogram import (
            FilteredSpectrogramProcessor, LogarithmicSpectrogramProcessor,
            SpectrogramDifferenceProcessor)
        from madmom.processors import SequentialProcessor, ParallelProcessor

        # define pre-processing chain
        sig = SignalProcessor(num_channels=1, sample_rate=44100)
        # process the multi-resolution spec & diff in parallel
        multi = ParallelProcessor([])
        for frame_size in [4096]:
            frames = FramedSignalProcessor(frame_size=frame_size, fps=100)
            stft = ShortTimeFourierTransformProcessor(window=np.hamming(frame_size))  # caching FFT window
            filt = FilteredSpectrogramProcessor(
                num_bands=12, fmin=30, fmax=16000, norm_filters=True)
            spec = LogarithmicSpectrogramProcessor(mul=5, add=1)
            # diff = SpectrogramDifferenceProcessor(diff_ratio=0.5, positive_diffs=True, stack_diffs=np.hstack)
            # process each frame size with spec and diff sequentially
            multi.append(SequentialProcessor((frames, stft, filt, spec)))
            # multi.append(SequentialProcessor((frames, stft, filt)))

        # stack the features and processes everything sequentially
        pre_processor = SequentialProcessor((sig, multi, np.hstack))
        super(PianoNoteProcessor, self).__init__(pre_processor)


def transform(file_name):
    proc = PianoNoteProcessor()
    act = proc(file_name)
    np.savetxt(f'{CONVERTER_FOLDER}/transform.txt', act, fmt='%.4f')
