import logging

from ..app_types import TeamPlayerScore
from .score_mode_base import ScoreModeBase

logger = logging.getLogger(__name__)


class ScoreTimeAttackDefault(ScoreModeBase):
	"""
	Score sorting for TimeAttack mode.
	Sorting: Maps played descending, Summed finish time ascending
	"""

	name = 'timeattack_default'
	score1_is_time = True
	score2_is_time = False
	scoreteam_is_time = False
	use_score1 = True
	use_score2 = False
	use_scoreteam = False

	def __init__(self) -> None:
		super().__init__()
		self.score_names.score1_name = 'Time'


	def combine_scores(self, scores: 'list[TeamPlayerScore]', new_scores: 'list[TeamPlayerScore]', **kwargs) -> 'list[TeamPlayerScore]':
		for new_score in new_scores:
			for existing_score in scores:
				if existing_score.login == new_score.login:
					existing_score.count += 1
					existing_score.player_score += new_score.player_score
					break
			else:
				scores.append(new_score)
		return scores


	def sort_scores(self, scores: 'list[TeamPlayerScore]') -> 'list[TeamPlayerScore]':
		return sorted(scores, key=lambda x: (-x.count, x.player_score))


	def update_placements(self, scores: 'list[TeamPlayerScore]') -> 'list[TeamPlayerScore]':
		for i in range(len(scores)):
			if i > 0:
				if scores[i-1].count == scores[i].count \
					and scores[i-1].player_score == scores[i].player_score:
					scores[i].placement = scores[i-1].placement
				else:
					scores[i].placement = i+1
			else:
				scores[i].placement = i+1
		return scores
