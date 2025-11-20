# ShowContextMenu NVDA Add-on
# Copyright (C) 2025 Arseniy Polyakov <senya-pol@yandex-team.ru>
# Copyright (C) 2025 Nikita Tseykovets <tseykovets@yandex-team.ru>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.

import addonHandler
addonHandler.initTranslation()

import globalPluginHandler
import controlTypes
import api
from scriptHandler import script
import inputCore

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(GlobalPlugin, self).__init__()

	@script(
		description=_(
			# Translators: Description of the command that opens a context menu for a current web content element.
			"Shows context menu for current web content element"
		),
		category=inputCore.SCRCAT_BROWSEMODE,
		gestures=(
			"kb:NVDA+shift+f10",
			"kb:NVDA+applications"
		),
	)
	def script_showContextMenu(self, gesture):
		"""Show context menu for current web content element"""

		# Get the navigator object (the object NVDA is currently reading/navigating)
		# This is different from system focus - it's the object under NVDA's review cursor
		navObj = api.getNavigatorObject()
		if not navObj:
			# If no navigator object, pass the gesture to the default Windows handler
			# This will trigger the standard Shift+F10 behavior
			gesture.send()
			return

		# Check if we're on web content (check based on role of navigator object's parent)
		if not self._isWebContent(navObj):
			# If it is not web content, pass the gesture to the default Windows handler
			gesture.send()
			return

		# Try to open context menu using IAccessibleAction
		if not self._openContextMenuViaAction(navObj):
			# If IAccessibleAction failed, pass the gesture to the default Windows handler
			gesture.send()

	def _isWebContent(self, obj=None):
		"""Check if the object is a web content element"""
		# Get the current object (if not passed)
		if obj is None:
			obj = api.getNavigatorObject()
			if not obj:
				return False

		# Move up the parental hierarchy
		current = obj
		while current and current.parent != current:  # Protection against cycles
			# If the parent container is document, it is browse mode
			if (current.role is controlTypes.Role.DOCUMENT
				or current.role is controlTypes.Role.INTERNALFRAME):
				return True
			current = current.parent

		return False

	# This is a deprecated method
	def _isInBrowser(self, obj=None):
		"""Check if the current application is a web browser"""
		try:
			# Get the app module from the provided object or from focus
			if obj and hasattr(obj, 'appModule'):
				app = obj.appModule
			else:
				app = api.getFocusObject().appModule
			if not app:
				return False

			# Get the application name
			appName = app.appName.lower() if app.appName else ""

			# List of common browser application names
			browserNames = [
				"chrome", "msedge", "edge", "opera", 
				"brave", "vivaldi", "chromium",
				"browser"
			]
			# Debug line removed for production

			# Check if current app is a browser
			for browser in browserNames:
				if browser in appName:
					return True

			# Also check the process name
			try:
				processName = app.processName.lower() if hasattr(app, 'processName') else ""
				for browser in browserNames:
					if browser in processName:
						return True
			except:
				pass

			return False
		except:
			return False

	def _openContextMenuViaAction(self, obj):
		"""Try to open context menu using IAccessibleAction interface"""
		try:
			# Try to get the IAccessibleAction interface
			if hasattr(obj, 'IAccessibleActionObject'):
				action = obj.IAccessibleActionObject
				if action:
					# Get the number of actions
					nActions = action.nActions()

					# Validate nActions
					if nActions is None or not isinstance(nActions, int) or nActions <= 0:
						return False

					# Look for context menu action directly without debug output
					for i in range(nActions):
						try:
							# Get action name using the same method that worked above
							actionName = action.name(i)
							if actionName and actionName == 'showContextMenu':
								try:
									action.doAction(i)
									return True
								except:
									pass
						except:
							continue

			return False
		except:
			return False
