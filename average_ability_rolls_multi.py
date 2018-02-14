import argparse
import matplotlib.pylab as plt
import numpy as np
from functools import reduce
from itertools import product
from collections import defaultdict

def get_score_frequencies(dice, lowest):
	score_totals = defaultdict(int)
	all_sets = [list(product(np.arange(1, d+1), repeat=n)) for d,n in dice]
	combined_sets = list(product(*all_sets))
	all_rolls = [[r for rolls in c for r in rolls] for c in combined_sets]
	
	for roll in all_rolls:
		score = sum(sorted(roll)[lowest:])
		score_totals[score] += 1
	return score_totals

def get_prob_over_n(scores, frequencies, n):
	if scores[-1] <= n:
		return 0
	num_abilities = 6
	total = sum(frequencies)
	score_above_n = next(x[0] for x in enumerate(scores) if x[1] > n)
	frequency_over_n = sum(frequencies[score_above_n:])
	probability = 1-(1-frequency_over_n/total)**num_abilities
	return probability

def get_expected_roll(totals):
	total_score, total_freq = 0, 0
	for k,v in totals.items():
		total_score += k * v
		total_freq += v
	return total_score/total_freq
	

def plot_scores(title, scores, percentages, bar_color, font_color, facecolor):
	position = np.arange(len(scores))
	fontsize = 125/len(scores)
	
	fig, ax = plt.subplots(facecolor=facecolor)
	ax.set_facecolor(facecolor)
	plt_title = 'Ability Rolls '+ title
	plt.title(plt_title, fontsize=25)
	plt.xticks(position, scores, fontsize=fontsize)
	plt.ylabel('Frequency', fontsize=15)
	plt.xlabel('Score', fontsize=15)
	for spine in plt.gca().spines.values():
	    spine.set_visible(False)
	plt.tick_params(top='off', bottom='off', left='off', right='off',
											labelleft='off', labelbottom='on')
	
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
	fig.savefig(plt_title+'.png', facecolor=facecolor, edgecolor='none')
	plt.close()

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', type=str, default='4d6')
	parser.add_argument('-l', type=int, default=1)
	parser.add_argument('-n', type=int, default=15)
	parser.add_argument('-bc', type=str, default='C0')
	parser.add_argument('-fc', type=str, default='w')
	parser.add_argument('-bg', type=str, default='LightSteelBlue')
	args = parser.parse_args()

	title = '[{0} - Lowest {1}]'.format(args.d, args.l)
	dice = [tuple([int(v) for v in dn.split('d')][::-1])
											for dn in args.d.split(',')]

	total_combinations = reduce(lambda x, y: x*y, [d[0]**d[1] for d in dice])
	score_totals = get_score_frequencies(dice, args.l)

	scores, frequencies = zip(*sorted(score_totals.items()))
	percentages = np.array(frequencies)/total_combinations

	average = get_expected_roll(score_totals)
	average_str = str(average)[:5]
	print('{0} Average: {1}'.format(title, average_str))
	over_n = get_prob_over_n(scores, frequencies, args.n)
	perc_str = str(over_n*100)[:5]+'%'
	print('{0} At least one roll over {1}: {2}'.format(title, args.n, perc_str))

	plot_scores(title, scores, percentages, args.bc, args.fc, args.bg)