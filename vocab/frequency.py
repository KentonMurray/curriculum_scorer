import sys
import argparse

parser = argparse.ArgumentParser(description='Get Vocabulary Ranks')

parser.add_argument('--datafile', dest='datafile', type=str, nargs='+',
                    help='file location')
#parser.add_argument('--train', dest='train', type=bool, nargs='+',
#                    help='true for train, false for test')

args = parser.parse_args()


vocabulary = {}
vocabulary_size = 0.0;

#Train
with open(args.datafile[0]) as f:
  for line in f:
    line = line.rstrip('\n')
    words = line.split()
    for word in words:
      vocabulary_size = vocabulary_size + 1.0
      if word in vocabulary:
        count = vocabulary[word]
        count = count + 1.0
        vocabulary[word] = count
      else:
        vocabulary[word] = 1.0

#print(vocabulary)

dataset = {}
minscore = 1.0
maxscore = 0.0

#Test
with open(args.datafile[0]) as f:
  for line in f:
    line = line.rstrip('\n')
    words = line.split()
    score = 0.0
    for word in words:
      if word in vocabulary:
        score = score + vocabulary[word] / vocabulary_size
      else:
        score = score + 0.0 #OOVs are least scored
    if len(words) > 0: #divide by 0 issues
      score = score / len(words)
    dataset[line] = score

    # For scaling
    if score < minscore:
      minscore = score
    if score > maxscore:
      maxscore = score

#print(dataset)

#Rescaled
rescale = 1.0 / (maxscore - minscore)
for sentence in dataset:
  score = rescale * (dataset[sentence] - minscore)
  print(score, end=' ||| ')
  print(sentence)

