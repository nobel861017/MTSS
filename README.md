# MTSS
Transferability of Speech Separation with Meta-learning

## Speech Accent Archive
## CommonVoice
command line example
```
python3 mp3_to_wav.py --data_dir /path/to/cv-corpus-6.1-2020-12-11/ \
                      --output_dir [output dir] \
                      --lang [lang] \
                      --split test
python3 mix_list_gen_cv_zh.py --data_dir /path/to/[output dir] \
                              --lang [lang] \
                              --do_tt

python3 mix_list_gen_cv_zh_3spk.py --data_dir /path/to/[output dir] \
                              --lang [lang] \
                              --do_tt

octave
pkg load signal
create_wav_2speakers
```
