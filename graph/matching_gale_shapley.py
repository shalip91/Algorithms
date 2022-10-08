def init_free_men(men_ranks):
	free_men = []
	for man in men_ranks.keys():
		free_men.append(man)
	return free_men


def begin_matching(m, free_men, potential_marriage, women_ranks, men_ranks):
	for w in men_ranks[m]:
		# bool for if woman is "taken" or not
		taken_match = [couple for couple in potential_marriage if w in couple]

		if not taken_match:
			potential_marriage.append([m, w])
			free_men.remove(m)
			break

		elif taken_match:
			cur_m = women_ranks[w].index(taken_match[0][0])
			maybe_m = women_ranks[w].index(m)

			if cur_m >= maybe_m:
				free_men.remove(m)
				free_men.append(taken_match[0][0])
				taken_match[0][0] = m
				break

	return potential_marriage


def gale_shapley_matching(men_ranks, women_ranks):
	res = []
	potential_marriage = []
	free_men = init_free_men(men_ranks)
	while free_men:
		for m in free_men:
			res = begin_matching(m, free_men=free_men, potential_marriage=potential_marriage, men_ranks=men_ranks, women_ranks=women_ranks)

	return res


if __name__ == '__main__':
	preferred_rankings_men_ex6 = {
		'alex': ['alice', 'brenda', 'carrol', 'joana'],
		'bob': ['carrol', 'joana', 'alice', 'brenda'],
		'collin': ['joana', 'carrol', 'brenda', 'alice'],
		'john': ['joana', 'alice', 'alice', 'brenda']
	}

	preferred_rankings_women_ex6 = {
		'alice': ['bob', 'alex', 'collin', 'john'],
		'brenda': ['john', 'bob', 'alex', 'collin'],
		'carrol': ['alex', 'bob', 'collin', 'john'],
		'joana': ['alex', 'john', 'collin', 'bob']
	}

	print(gale_shapley_matching(preferred_rankings_men_ex6, preferred_rankings_women_ex6))
	print(gale_shapley_matching(preferred_rankings_women_ex6, preferred_rankings_men_ex6))
