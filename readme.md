# ShowContextMenu NVDA Add-on

**ShowContextMenu** allows you to show context menus for current web content elements in browse mode even when they cannot be focused using the keyboard.

## Features

* Works with elements that implement **IAccessibleAction**.
* Opens context menus using keyboard shortcuts:
	+ **NVDA+Shift+F10**
	+ **NVDA+Applications key**
* Tested with NVDA 2019.3 and later (up to 2025.3).

## Installation

1. Download the `.nvda-addon` file from the [GitHub Releases page](https://github.com/senya-pol/showContextMenu/releases).  
2. Open NVDA menu → **Tools → Add-on store → Install from external source** → Choose downloaded add-on package file.  
3. Restart NVDA to activate the add-on.

## Usage

* set nvda focus to any web content element in browse mode (Currently, only Chromium-based browsers are supported.).
* Press **NVDA+Shift+F10** or **NVDA+Applications key** to show the context menu.
* You can reassign a gesture through the NVDA menu → **Preferences → Input gestures → Browse mode → Shows context menu for current web content element**

## Add-on Information

* **Version:** 1.0  
* **Author:** Arseniy Polyakov <senya-pol@yandex-team.ru>  
* **License:** GPL-2.0-or-later ([link](https://www.gnu.org/licenses/gpl-2.0.html))  
* **Source:** [GitHub repository](https://github.com/senya-pol/showContextMenu)  
