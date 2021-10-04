# MTSS
Transferability of Speech Separation with Meta-learning.

Scripts to create the testing set speech mixtures.

## CommonVoice
Download languages zh-CN, zh-TW, zh-HK from https://commonvoice.mozilla.org/zh-TW/datasets.

Convert mp3 to wav
```
python3 mp3_to_wav.py --data_dir /path/to/cv-corpus-6.1-2020-12-11/ \
                      --output_dir [output dir] \
                      --lang [lang] \
                      --split test
```
Generate mix list

2-speaker
```
python3 mix_list_gen_cv_zh.py --data_dir /path/to/[output dir] \
                              --lang [lang] \
                              --do_tt
```
3-speaker
```
python3 mix_list_gen_cv_zh_3spk.py --data_dir /path/to/[output dir] \
                              --lang [lang] \
                              --do_tt
```
Generate mixtures according to mix list
```
cd create-speaker-mixtures_cv_zh
octave
pkg load signal
create_wav_2speakers
create_wav_3speakers
```

## Speech Accent Archive

```

```
