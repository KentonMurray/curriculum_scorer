import sys
import argparse

parser = argparse.ArgumentParser(description='Score Sentence by Vocab')

parser.add_argument('--sc', dest='sc', type=str, nargs='?',
                    help='Counts of Src Tokens')
parser.add_argument('--tc', dest='tc', type=str, nargs='?',
                    help='Counts of Trg Tokens')
parser.add_argument('--src', dest='src', type=str, nargs='?',
                    help='Src Training Data')
parser.add_argument('--trg', dest='trg', type=str, nargs='?',
                    help='Trg Training Data')
parser.add_argument('--maxrank', dest='maxrank', type=bool, nargs='?',
                    help='Use max rank of source and trg', default=False)
parser.add_argument('--combinedrank', dest='combinedrank', type=str, nargs='?',
                    help='Counts of Combined Source and Target Tokens')

args = parser.parse_args()

src_vocabulary = {}
src_vocabulary_size = 0.0;
trg_vocabulary = {}
trg_vocabulary_size = 0.0;
combined_vocabulary = {}
combined_vocabulary_size = 0.0;

#Process Src Counts
with open(args.sc) as f:
  rank = 0.0
  for line in f:
    line = line.rstrip('\n')
    words = line.split()
    count = (float) (words[0])
    src_vocabulary_size = src_vocabulary_size + count
    word = words[1]
    src_vocabulary[word] = (count, rank)
    rank = rank + 1.0

#Process Trg Counts
with open(args.tc) as f:
  rank = 0.0
  for line in f:
    line = line.rstrip('\n')
    words = line.split()
    count = (float) (words[0])
    trg_vocabulary_size = trg_vocabulary_size + count
    word = words[1]
    trg_vocabulary[word] = (count, rank)
    rank = rank + 1.0

#Process Combined Counts
with open(args.combinedrank) as f:
  rank = 0.0
  for line in f:
    line = line.rstrip('\n')
    words = line.split()
    count = (float) (words[0])
    combined_vocabulary_size = combined_vocabulary_size + count
    word = words[1]
    combined_vocabulary[word] = (count, rank)
    rank = rank + 1.0
    
# Score Src Data
print("Source Ranks")
src_maxranks = []
combined_src_maxranks = []
avg_src_ranks = []
with  open(args.src) as f:
  for line in f:
    src_maxrank = src_vocabulary_size
    combined_src_maxrank = combined_vocabulary_size
    avg_src_rank = []
    line = line.rstrip('\n')
    words = line.split()
    for word in words:
      if word in src_vocabulary:
        rank = src_vocabulary[word][1]
        avg_src_rank.append(rank)
        if rank < src_maxrank:
          src_maxrank = rank
      else:
        avg_src_rank.append(src_vocabulary_size)
      if word in combined_vocabulary:
        rank = combined_vocabulary[word][1]
        if rank < combined_src_maxrank:
          combined_src_maxrank = rank
    scaled = 1.0 - (src_maxrank/src_vocabulary_size)
    print(scaled)
    src_maxranks.append(scaled)
    combined_src_maxranks.append(combined_src_maxrank)
    avg_src_ranks.append(sum(avg_src_rank)/((float)(len(avg_src_rank))))

# Score Trg Data
print("Target Ranks")
trg_maxranks = []
combined_trg_maxranks = []
avg_trg_ranks = []
with  open(args.trg) as f:
  for line in f:
    trg_maxrank = trg_vocabulary_size
    combined_trg_maxrank = combined_vocabulary_size
    avg_trg_rank = []
    line = line.rstrip('\n')
    words = line.split()
    for word in words:
      if word in trg_vocabulary:
        rank = trg_vocabulary[word][1]
        avg_trg_rank.append(rank)
        if rank < trg_maxrank:
          trg_maxrank = rank
      else:
        avg_trg_rank.append(trg_vocabulary_size)
      if word in combined_vocabulary:
        rank = combined_vocabulary[word][1]
        if rank < combined_trg_maxrank:
          combined_trg_maxrank = rank
    scaled = 1.0 - (trg_maxrank/trg_vocabulary_size)
    print(scaled)
    trg_maxranks.append(scaled)
    combined_trg_maxranks.append(combined_trg_maxrank)
    avg_trg_ranks.append(sum(avg_trg_rank)/((float)(len(avg_trg_rank))))

# Score Max of Src & Trg Data
print("Max Rank of Source and Target")
for s, t in zip(src_maxranks, trg_maxranks):
  print(max(s,t))

# Score Combined of Src & Trg Data
print("Combined Rank of Source and Target")
for s, t in zip(combined_src_maxranks, combined_trg_maxranks):
  print(1.0 - (min(s,t)/combined_vocabulary_size))

# Score Average of Src Data
print("Average Rank of Source")
for s in avg_src_ranks:
  print (1.0 - (s/src_vocabulary_size))

# Score Average of Trg Data
print("Average Rank of Target")
for s in avg_trg_ranks:
  print (1.0 - (s/trg_vocabulary_size))

