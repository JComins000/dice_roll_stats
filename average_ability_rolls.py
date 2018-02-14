import argparse
import matplotlib.pylab as plt
import numpy as np
import operator as op
from functools import reduce
from itertools import combinations_with_replacement
from collections import defaultdict

def ncr(n, r):
    r = min(r, n-r)
    if r == 0: return 1
    numer = reduce(op.mul, range(n, n-r, -1))
    denom = reduce(op.mul, range(1, r+1))
    return numer//denom

def num_similar_permutations(lst):
	permutations = 1
	size = len(lst)
	appearances = defaultdict(int)
	for item in lst:
		appearances[item] += 1
	for val in appearances.values():
		permutations *= ncr(size, val)
		size -= val
	return permutations

def get_score_frequencies(num_faces, num_rolls, lowest):
	score_totals = defaultdict(int)
	dice = range(1, num_faces+1)
	all_rolls = list(combinations_with_replacement(dice, num_rolls))

	for roll in all_rolls:
		score = sum(roll[lowest:])
		score_totals[score] += num_similar_permutations(roll)
	return score_totals

def print_prob_over_n(title, scores, frequencies, n=15):
	out_str = 'Probability of at least one {0} over {1}: {2}'
	num_abilities = 6
	total = sum(frequencies)
	score_above_n = next(x[0] for x in enumerate(scores) if x[1] > n)
	frequency_over_n = sum(frequencies[score_above_n:])
	percentage = 1-(1-frequency_over_n/total)**num_abilities
	percent_str = str(percentage*100)[:5]+'%'
	print(out_str.format(title, n, percent_str))

def print_expected_roll(title, totals):
	out_str = 'Most likely {0}: {1}'
	total_score, total_freq = 0, 0
	for k,v in totals.items():
		total_score += k * v
		total_freq += v
	print(out_str.format(title, total_score/total_freq))
	

def plot_scores(num_faces=6, num_rolls=4, lowest=1, bar_color='C0',
								font_color='w', facecolor='LightSteelBlue'):
	total_combinations = num_faces**num_rolls
	score_totals = get_score_frequencies(num_faces, num_rolls, lowest)
	scores, frequencies = zip(*sorted(score_totals.items()))

	title = '[{0}d{1} - Lowest {2}]'.format(num_rolls, num_faces, lowest)
	print_expected_roll(title, score_totals)
	print_prob_over_n(title, scores, frequencies)
	position = np.arange(len(scores))
	fontsize = 125/len(scores)
	
	fig, ax = plt.subplots(facecolor=facecolor)
	ax.set_facecolor(facecolor)
	plt.title('Ability Rolls '+ title, fontsize=25)
	plt.xticks(position, scores, fontsize=fontsize)
	plt.ylabel('Frequency', fontsize=15)
	plt.xlabel('Score', fontsize=15)
	for spine in plt.gca().spines.values():
	    spine.set_visible(False)
	plt.tick_params(top='off', bottom='off', left='off', right='off',
											labelleft='off', labelbottom='on')
	
	percentages = np.array(frequencies)/total_combinations
	bars = plt.bar(position, percentages, align='center', color=bar_color)
	max_height = max([bari.get_height() for bari in bars])
	for bari in bars:
		color = font_color
		height = bari.get_height() - max_height*fontsize/250
		if height < fontsize/1000:
			height = bari.get_height() + max_height*fontsize/3/250
			color = 'black'
		plt.gca().text(bari.get_x() + bari.get_width()/2,
						height,
						str(int(height*100))+'%',
						ha='center',
						color=color,
						fontsize=fontsize)

	plt.tight_layout()
	fig.savefig(title+'.png', facecolor=facecolor, edgecolor='none')
	plt.close()

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', type=int, default=6)
	parser.add_argument('-n', type=int, default=4)
	parser.add_argument('-l', type=int, default=1)
	parser.add_argument('-bc', type=str, default='C0')
	parser.add_argument('-fc', type=str, default='w')
	parser.add_argument('-bg', type=str, default='LightSteelBlue')
	args = parser.parse_args()
	plot_scores(args.d, args.n, args.l, args.bc, args.fc, args.bg)