import audioowl
import librosa
import numpy as np
from pydub import AudioSegment
from pydub.utils import which
import time
from random import randint

def find_best_sync_point(bottom_file_beats, top_file_beats, max_mix_sample, offset, mode):

    offset = offset
    matches_per_round = []

    # turning args to numpy arrays
    bottom_file_beats = np.array(bottom_file_beats)
    top_file_beats = np.array(top_file_beats)

    for rn in range(bottom_file_beats.shape[0]):

        try:

            zero_sync_samples = bottom_file_beats[rn] - top_file_beats[0]
            slider = top_file_beats + (zero_sync_samples)

            for i in range(len(slider)):
                if slider[i] <= max_mix_sample:
                    continue
                else:
                    slider[i] = slider[i] - max_mix_sample

            matches = []
            tested_beat_index = 0
            all_sample_beats = np.concatenate((slider, bottom_file_beats))
            all_sample_beats.sort()

            for i in range (1, all_sample_beats.shape[0]):
                if all_sample_beats[i] == all_sample_beats[tested_beat_index] or abs(all_sample_beats[i] - all_sample_beats[tested_beat_index]) <= offset:
                    matches.append(all_sample_beats[i])
                    matches.append(all_sample_beats[tested_beat_index])
                    tested_beat_index+=1

                else:
                    tested_beat_index+=1

            matches_per_round.append(len(matches)/2/len(top_file_beats))

        except Exception as err:
            # exc_type, exc_value, exc_traceback = sys.exc_info()
            # print ('\t🔎  We had a sliding window problem :|\n\tError message: {}\n\tError on file: {}\n\tError on line: {}\n'.format(err, exc_traceback.tb_frame.f_code.co_filename, exc_traceback.tb_lineno))
            matches_per_round.append(0)

    if mode == 'first':
        sync_beat_number = np.argmax(matches_per_round)

    else: # random (default)
        sync_beat_number = np.random.choice(np.argwhere(matches_per_round == np.amax(matches_per_round)).reshape(-1,))

    sync_sample = bottom_file_beats[sync_beat_number] - top_file_beats[0]
    sync_beat_accuracy = np.max(matches_per_round)

    return sync_sample, sync_beat_number, sync_beat_accuracy





def mixer(top_file, bottom_file, output_file_path, sr=22050, mix_mode='random', offset=880, trim_silence=False, sync_sample=None, timestamp=None):

    # loading top file
    y_top_file, sr = librosa.load(top_file, sr=sr)

    if trim_silence:
        try:
            yt, i = librosa.effects.trim(y_top_file, top_db=28)

            # trimming only the leading silence
            y_top_file = y_top_file[i[0]:]
        except:
            print ('[MixingBear] Failed to trim leading silence')
            pass

    # loading bottom file
    y_bottom_file, sr = librosa.load(bottom_file, sr=sr)

    # checking if the durations allow proper mixing
    y_bottom_file_repetitions = 1
    while (y_bottom_file.shape[0] * y_bottom_file_repetitions) < y_top_file.shape[0] :
        y_bottom_file_repetitions+=1

    # repeating y_bottom_file if needed
    if (y_bottom_file_repetitions > 1):
        y_bottom_file_duplications = []
        for i in range(y_bottom_file_repetitions):
            y_bottom_file_duplications.append(y_bottom_file)
        y_bottom_file = np.hstack((y_bottom_file_duplications))


    # analyzing the files
    top_file_data = audioowl.analyze_samples(y_top_file, sr)
    bottom_file_data = audioowl.analyze_samples(y_bottom_file, sr)

    # find mixing point
    sync_sample, sync_beat_number, sync_beat_accuracy = find_best_sync_point(
                                                        top_file_beats=top_file_data['beat_samples'],
                                                        bottom_file_beats=bottom_file_data['beat_samples'],
                                                        max_mix_sample=y_bottom_file.shape[0],
                                                        offset=offset,
                                                        mode=mix_mode)


    # mix the files
    sync_time_ms = sync_sample / sr * 1000

    # loading files as pydub audiosegments
    sound_seg = AudioSegment.from_file(top_file)
    mix_seg = AudioSegment.from_file(bottom_file)

    if sync_time_ms < 0:

        position = (bottom_file_data['duration'] * 1000) + sync_time_ms
        played_togther = mix_seg.overlay(sound_seg[:abs(int(sync_time_ms))], position=position, loop=False)
        new = played_togther
        played_togther = new.overlay(sound_seg[abs(int(sync_time_ms)):], position=0, loop=False)

        del new
        del position

    elif (sync_time_ms + (top_file_data['duration'] * 1000)) > (bottom_file_data['duration'] * 1000):

        sound_cut_point = int(bottom_file_data['duration']*1000 - sync_time_ms)

        # mixing sound and mix at 2 points
        played_togther = mix_seg.overlay(sound_seg[:sound_cut_point], position=int(sync_time_ms), loop=False)
        new = played_togther
        played_togther = new.overlay(sound_seg[sound_cut_point:], position=0, loop=False)

        del new

    else:

        # mixing sound and mix at sync_time_ms
        played_togther = mix_seg.overlay(sound_seg, position=sync_time_ms, loop=False)

    # clearning audio segment from the memory
    del mix_seg
    del sound_seg

    # levelizing the final output
    if played_togther.max_dBFS >= 0:
        played_togther = played_togther.apply_gain(0-played_togther.max_dBFS)
    else:
        played_togther = played_togther.apply_gain(-1 * played_togther.max_dBFS)

    # saving the output file locally
    file_handle = played_togther.export(output_file_path, format='wav')

    return sync_beat_accuracy
