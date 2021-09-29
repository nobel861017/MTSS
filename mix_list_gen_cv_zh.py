import os
import argparse
import random
import glob
from collections import defaultdict
from tqdm import tqdm
from pathlib import Path

def write_out(args, output_filename, mix_list):
    if not os.path.exists(args.output_dir): Path(args.output_dir).mkdir(mode=0o744, parents=True, exist_ok=True)
    with open(os.path.join(args.output_dir, output_filename), 'w') as f:
        for s in mix_list:
            f.write("%s\n" % s)
        f.close()

def gen_mix_list(args, speaker_wav_dict, output_filename):
    mix_list = []
    total_tasks = 0
    spk_list = list(speaker_wav_dict.keys())[:args.spknum]
    spk_mix_pair_list = [(spk_list[i], spk_list[j]) for i in range(len(spk_list)) for j in range(i+1, len(spk_list))]
    total_tasks += len(spk_mix_pair_list)
    for _, (spk1, spk2) in enumerate(spk_mix_pair_list):
        for i in range(args.k):
            for j in range(args.k):
                db = round(random.uniform(0.0, 2.5), 6)
                string = ' '.join([speaker_wav_dict[spk1][i], str(db), speaker_wav_dict[spk2][j], str(-db)])
                mix_list.append(string)
    write_out(args, output_filename, mix_list)
    print('total_tasks', total_tasks)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='/home/gerber531/Desktop/Data/common-voice-zh-split-4s/zh-CN')
    parser.add_argument('--lang', type=str, default='zh-CN')
    parser.add_argument('--output_dir', type=str, default='create-speaker-mixtures_cv_zh/')
    parser.add_argument('--spknum', type=int, default=29, help='number of speakers to use')
    parser.add_argument('--k', type=int, default=3, help='number of data for each speaker')
    parser.add_argument('--do_tr', action='store_true')
    parser.add_argument('--do_cv', action='store_true')
    parser.add_argument('--do_tt', action='store_true')
    args = parser.parse_args()

    split_dirs = []
    if args.do_tr: split_dirs.append(['train/'])
    if args.do_cv: split_dirs.append(['dev/'])
    if args.do_tt: split_dirs.append(['test/'])
    data_dir = os.path.join(args.data_dir, args.lang)
    for split_dir in split_dirs:
        wav_list = []
        for d in split_dir:
            speaker_wav_dict = {}
            speakers_dir = os.path.join(data_dir, d)
            speakers_all = os.listdir(speakers_dir)
            speaker_utt_dict = defaultdict(list)
            for spk in speakers_all:
                spk_wav_dir = os.path.join(speakers_dir, spk)
                if len(os.listdir(spk_wav_dir)) < args.k: continue
                for p in Path(spk_wav_dir).glob('*.wav'):
                    abs_path_split = str(p.absolute()).split('/')
                    speaker_utt_dict[spk].append('/'.join(abs_path_split[-5:]))
            if d == 'train/':
                gen_mix_list(args, speaker_utt_dict, 'mix_2_spk_tr.txt')
            elif d == 'dev/':
                gen_mix_list(args, speaker_utt_dict, 'mix_2_spk_cv.txt')
            elif d == 'test/':
                gen_mix_list(args, speaker_utt_dict, 'mix_2_spk_tt.txt')
