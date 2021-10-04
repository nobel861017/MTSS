# MTSS
Transferability of Speech Separation with Meta-learning.

Scripts to create the testing set speech mixtures.

## CommonVoice
step 1: Download languages zh-CN, zh-TW, zh-HK from https://commonvoice.mozilla.org/zh-TW/datasets.

step 2: Convert mp3 to wav
```
python3 mp3_to_wav.py --data_dir /path/to/cv-corpus-6.1-2020-12-11/ \
                      --output_dir /path/to/common-voice-zh-split-4s \
                      --lang [lang] \
                      --split test
```
step 3: Generate mix list

2-speaker
```
python3 mix_list_gen_cv_zh.py --data_dir /path/to/common-voice-zh-split-4s \
                              --lang [lang] \
                              --do_tt
```
3-speaker
```
python3 mix_list_gen_cv_zh_3spk.py --data_dir /path/to/common-voice-zh-split-4s \
                              --lang [lang] \
                              --do_tt
```
step 4: Generate mixtures according to mix list
```
cd create-speaker-mixtures_cv_zh
octave
pkg load signal

create_wav_2speakers
create_wav_3speakers
```
repeat step 3 and 4 for each language

## Speech Accent Archive
Download Speech Accent Archive mp3 files from https://www.kaggle.com/rtatman/speech-accent-archive.

split audio and convert mp3 to wave
```
python3 split_SAA_audio.py --data_dir /path/to/recordings --output_dir /path/to/multi_accent_split_4s/
```
Generate mix list

2-speaker
```
python3 mix_list_gen_mac_2spk_task_English.py --data_dir /path/to/multi_accent_split_4s/ --do_tr --do_cv --do_tt
```

3-speaker
```
python3 mix_list_gen_mac_3spk_task_English.py --data_dir /path/to/multi_accent_split_4s/ --do_tr --do_cv --do_tt
```
Generate mixtures according to mix list
```
cd create-speaker-mixtures_mac_English
octave
pkg load signal
create_wav_2speakers
create_wav_3speakers
```
