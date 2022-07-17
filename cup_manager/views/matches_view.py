import logging
from datetime import datetime

from pyplanet.views.generics.list import ManualListView

from ..models import MatchInfo

logger = logging.getLogger(__name__)

class MatchesView(ManualListView):
	app = None

	title = 'Matches'
	icon_style = 'Icons128x128_1'
	icon_substyle = 'Statistics'

	get_data_method = None

	def __init__(self, app: any, player: any) -> None:
		super().__init__(self)
		self.app = app
		self.manager = app.context.ui
		self.player = player


	@classmethod
	def set_get_data_method(cls, method) -> None:
		cls.get_data_method = method


	async def get_fields(self):
		fields = [
			{
				'name': 'Add/Remove Map',
				'index': 'selected_str',
				'sorting': False,
				'searching': False,
				'width': 35,
				'type': 'label',
				'action': self._action_match_select
			},
			{
				'name': 'Date',
				'index': 'match_time_str',
				'sorting': False,
				'searching': False,
				'width': 40,
				'type': 'label'
			},
			{
				'name': 'Map Name',
				'index': 'map_name_str',
				'sorting': False,
				'searching': False,
				'width': 50,
				'type': 'label'
			},
		]
		return fields


	async def get_data(self) -> list:
		items = []
		if self.get_data_method:
			matches = await self.get_data_method()	# type: list[MatchInfo]
			selected_matches = await self.app.get_selected_matches()	# type: list[int]
			for match_info in matches:
				items.append({
					'selected': match_info.map_start_time in selected_matches,
					'map_start_time': match_info.map_start_time,
					'selected_str': '$f55 Remove from Cup' if match_info.map_start_time in selected_matches else '$0cf Add to Cup',
					'match_time_str': datetime.fromtimestamp(match_info.map_start_time).strftime("%c"),
					'map_name_str': match_info.map_name,
				})
		return items


	async def _action_match_select(self, player, values, instance, **kwargs):
		if instance['selected']:
			await self.app.remove_selected_match(instance['map_start_time'])
		else:
			await self.app.add_selected_match(instance['map_start_time'])
		await self.refresh(player=player)
