from .mixer import mixer

def mix(top_file, bottom_file, output_file_path, mix_mode='random', sr=22050, offset=880, trim_silence=False, sync_sample=None, timestamp=None):
    return mixer(top_file=top_file, bottom_file=bottom_file, output_file_path=output_file_path, sr=sr, mix_mode=mix_mode, offset=offset, trim_silence=trim_silence, sync_sample=sync_sample, timestamp=timestamp)
