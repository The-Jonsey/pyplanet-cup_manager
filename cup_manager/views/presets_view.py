import logging
import math
from pandas import DataFrame

from .single_instance_view import SingleInstanceView

logger = logging.getLogger(__name__)

class PresetsView(SingleInstanceView):

	template_name = 'cup_manager/presets.xml'

	title = 'Preset Setups'
	icon_style = 'Icons128x128_1'
	icon_substyle = 'NewTrack'

	def __init__(self, app) -> None:
		super().__init__(app, 'cup_manager.views.presets_view_displayed')
		self.preset_page = 1
		self.preset_count = 0
		self.num_presets_per_page = 6
		self.setting_page = 1
		self.setting_count = 0
		self.num_settings_per_page = 11
		# TODO: Remove this hardcoding
		self.selected_preset_name = 'rounds_silly'
		self.selected_preset_script = 'Rounds!!'

		self.subscribe('presets_button_close', self.close)


	async def handle_catch_all(self, player, action, values, **kwargs):
		logger.info(f"called handle_catch_all for action '{action}'")
		return await super().handle_catch_all(player, action, values, **kwargs)


	async def get_context_data(self):
		context = await super().get_context_data()

		context['title'] = self.title
		context['icon_style'] = self.icon_style
		context['icon_substyle'] = self.icon_substyle
		context.update({
			'presets': await self.get_preset_data(),
			'preset_page': self.preset_page,
			'num_preset_pages': self.num_preset_pages,
			'settings': await self.get_setting_data(),
			'setting_page': self.setting_page,
			'num_setting_pages': self.num_setting_pages,
			'selected_preset_name': self.selected_preset_name,
			'selected_preset_script': self.selected_preset_script,
		})
		return context


	async def get_preset_data(self):
		preset_dict = await self.app.get_presets()
		preset_data = []
		for key, data in preset_dict.items():
			if 'script' in data and self.app.instance.game.game in data['script']:
				script_name = data['script'][self.app.instance.game.game]
				aliases_combined = ''
				if 'aliases' in data and data['aliases']:
					aliases_combined = ', '.join(data['aliases'])
				preset_data.append({
					'name': key,
					'aliases': aliases_combined,
					'script': script_name
				})
		frame = DataFrame(preset_data)
		self.preset_count = len(frame)
		frame = await self.apply_pagination(frame, self.preset_page, self.num_presets_per_page)
		return frame.to_dict('records')


	async def get_setting_data(self):
		preset_dict = await self.app.get_presets()
		setting_data = []
		if self.selected_preset_name and self.selected_preset_name in preset_dict and 'settings' in preset_dict[self.selected_preset_name] and preset_dict[self.selected_preset_name]['settings']:
			for key, data in preset_dict[self.selected_preset_name]['settings'].items():
				setting_data.append({'name': key, 'value': data})
		else:
			setting_data.append({'name': 'None', 'value': 'N/A'})
		frame = DataFrame(setting_data)
		self.setting_count = len(frame)
		frame = await self.apply_pagination(frame, self.setting_page, self.num_settings_per_page)
		return frame.to_dict('records')


	async def apply_pagination(self, frame: DataFrame, page: int, num_per_page: int) -> DataFrame:
		return frame[(page - 1) * num_per_page:page * num_per_page]


	@property
	def num_preset_pages(self):
		return int(math.ceil(self.preset_count / self.num_presets_per_page))


	@property
	def num_setting_pages(self):
		return int(math.ceil(self.setting_count / self.num_settings_per_page))

