import os
import re
import csv
import sys
import argparse
from collections import defaultdict
from pathlib import Path
from tqdm import tqdm
from pydub import AudioSegment

def split_audio(wav_input_path, wav_output_path_prefix, speaker, num, ext, seg_len=4000):
    #print(wav_input_path)
    if not os.path.exists(wav_output_path_prefix):
        os.makedirs(wav_output_path_prefix, exist_ok=True)
    origin_audio = AudioSegment.from_mp3(wav_input_path)
    origin_audio_milliseconds = origin_audio.duration_seconds*1000
    start_time = 0 # in milli seconds
    segment_idx = 0
    while start_time <= origin_audio_milliseconds:
        if start_time + seg_len*0.7 > origin_audio_milliseconds: break
        wav_output_path = os.path.join(wav_output_path_prefix, speaker + '-' + num + '-' + str(segment_idx) + ext)
        newAudio = origin_audio[start_time:start_time+seg_len]
        newAudio.export(wav_output_path, format="wav")
        segment_idx += 1
        start_time += seg_len

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='/path/to/cv-corpus-6.1-2020-12-11/')
    parser.add_argument('--output_dir', type=str, default='/path/to/common-voice-zh-split-4s/')
    parser.add_argument('--lang', type=str, default='zh-CN')
    parser.add_argument('--split', type=str, default='test')
    parser.add_argument('--seg_len', type=int, default=4000, help='segment duration in milliseconds')
    args = parser.parse_args()
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir, exist_ok=True)
    data_dir = os.path.join(os.path.join(args.data_dir, args.lang), 'clips')
    output_dir = os.path.join(args.output_dir, os.path.join(args.lang, args.split))
    tsv_file = open(os.path.join(args.data_dir, os.path.join(args.lang, args.split+'.tsv')))
    read_tsv = csv.reader(tsv_file, delimiter="\t")
    audio_dict = defaultdict(list)
    for idx, row in enumerate(read_tsv):
        if idx == 0: continue
        client_id, path = row[0], row[1]
        audio_dict[client_id].append(path)
    for snum, speaker in enumerate(tqdm(list(audio_dict.keys()))):
        for anum, audio_path in enumerate(audio_dict[speaker]):
            split_audio(os.path.join(data_dir, audio_path), 
                        os.path.join(output_dir, str(snum)), 
                        str(snum), 
                        str(anum), 
                        '.wav', 
                        args.seg_len)
