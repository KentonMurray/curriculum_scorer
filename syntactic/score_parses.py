import sys
import argparse
import math

parser = argparse.ArgumentParser(description='Score Sentence by Dependency Parse')

parser.add_argument('--heads', dest='heads', type=str, nargs='?',
                    help='Comma separated list of Head IDs')

args = parser.parse_args()

with open(args.heads) as f:
  for line in f:
    line = line.rstrip('\n')
    heads = line.split(',')
    length = (float)(len(heads)) + 1.0
    ids = {}
    number = 0.0
    for head in heads:
      head = (int) (head)
      if head not in ids:
        number = number + 1.0
        ids[head] = 1.0
      else:
        count = ids[head] + 1.0
        ids[head] = count

    # Calculate Hellinger Divergence
    uniform = math.sqrt(1.0/length)
    ilength = (int)(length)
    runningsum = 0.0
    for i in range(0,ilength):
      #print(i)
      prob = 0.0
      if i in ids:
        #print(ids[i])
        prob = ids[i]/length
        #print(prob)
      else:
        #print("0.0")
        prob = 0.0
      runningsum = runningsum + math.pow(uniform - math.sqrt(prob),2)
    finalscore = 1.0/(math.sqrt(2.0))*math.sqrt(runningsum)
    print(finalscore)



