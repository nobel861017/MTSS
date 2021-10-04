import os
import argparse
import random
import glob
import collections
from tqdm import tqdm
from pathlib import Path
from itertools import groupby
from collections import defaultdict

TEST_ACCENTS = ['albanian', 'ga', 'hausa', 'italian', 'kurdish', 
                'lithuanian', 'mende', 'russian', 'tamil', 'thai']

def write_out(args, output_filename, mix_list):
    if not os.path.exists(args.output_dir): Path(args.output_dir).mkdir(mode=0o744, parents=True, exist_ok=True)
    with open(os.path.join(args.output_dir, output_filename), 'w') as f:
        for s in mix_list:
            f.write("%s\n" % s)
        f.close()

def gen_mix_list_tr(args, accents, accent_wav_dict, output_filename):
    mix_list = []
    for ac in accents:
        spkr_utt_dict = accent_wav_dict[ac]
        spk_list = list(spkr_utt_dict.keys())[:579]
        spk_mix_pair_list = [(spk_list[i], spk_list[j]) for i in range(len(spk_list)) for j in range(i+1, len(spk_list))]
        spk_mix_pair_list = random.sample(spk_mix_pair_list, 2222)
        for _, (spk1, spk2) in enumerate(tqdm(spk_mix_pair_list)):
            for i in range(args.k):
                for j in range(args.k):
                    db = round(random.uniform(0.0, 2.5), 6)
                    string = ' '.join([spkr_utt_dict[spk1][i], str(db), spkr_utt_dict[spk2][j], str(-db)])
                    mix_list.append(string)
    write_out(args, output_filename, mix_list)
    

def gen_mix_list(args, accents, accent_wav_dict, output_filename):
    mix_list = []
    total_tasks = 0
    for ac in accents:
        spkr_utt_dict = accent_wav_dict[ac]
        spk_list = list(spkr_utt_dict.keys())[:args.spknum]
        spk_mix_pair_list = [(spk_list[i], spk_list[j]) for i in range(len(spk_list)) for j in range(i+1, len(spk_list))]
        total_tasks += len(spk_mix_pair_list)
        for _, (spk1, spk2) in enumerate(spk_mix_pair_list):
            for i in range(args.k):
                for j in range(args.k):
                    db = round(random.uniform(0.0, 2.5), 6)
                    string = ' '.join([spkr_utt_dict[spk1][i], str(db), spkr_utt_dict[spk2][j], str(-db)])
                    mix_list.append(string)
    write_out(args, output_filename, mix_list)
    print('total_tasks', total_tasks)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='/home/gerber531/Desktop/Data/multi_accent_split_4s/')
    parser.add_argument('--output_dir', type=str, default='create-speaker-mixtures_mac_English/')
    parser.add_argument('--spknum', type=int, default=12, help='maximum number of speakers to use for each task')
    parser.add_argument('--k', type=int, default=3, help='number of data for each speaker')
    parser.add_argument('--do_tr', action='store_true')
    parser.add_argument('--do_cv', action='store_true')
    parser.add_argument('--do_tt', action='store_true')
    args = parser.parse_args()
    
    accents_all = os.listdir(args.data_dir)
    accent = []
    accent_wav_dict = defaultdict(list)
    for ac in accents_all:
        accent_path = os.path.join(args.data_dir, ac)
        if len(os.listdir(accent_path)) < 2: continue
        accent.append(ac)
        speaker_utt_dict = defaultdict(list)
        for p in Path(accent_path).rglob('*.wav'):
            abs_path_split = str(p.absolute()).split('/')
            speaker_name = abs_path_split[-2]
            speaker_utt_dict[speaker_name].append('/'.join(abs_path_split[-4:]))

        accent_wav_dict[ac] = speaker_utt_dict
    accent_num = len(accent)
    #import pdb
    #pdb.set_trace()
    english_idx = accent.index('english')
    accent.remove('english')
    if args.do_tr:
        gen_mix_list_tr(args, ['english'], accent_wav_dict, 'mix_2_spk_tr.txt')
    if args.do_cv:
        gen_mix_list(args, accent[:int(accent_num*0.5)], accent_wav_dict, 'mix_2_spk_cv.txt')
    if args.do_tt:
        gen_mix_list(args, TEST_ACCENTS, accent_wav_dict, 'mix_2_spk_tt.txt')
    