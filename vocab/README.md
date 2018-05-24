#Vocabulary
This subdirectory focuses on metrics related to the vocabulary, such as frequency/OOV/etc.

All methods should return a value for each sentence [0,1]

First you need to run calculate_ranks.sh This sorts a dataset by word frequency. It outputs a file with [count word]
Generally, you should run this three times: Src, Trg, Concatenated Src&Trg

score_data.py takes in the frequency files and datasets and scores them.
