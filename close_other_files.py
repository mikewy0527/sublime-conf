import sublime
import sublime_plugin

# Sample key binding:
#
#    { "keys": ["ctrl+alt+shift+w"], "command": "close_others_shim" },
#


class CloseOtherTabsCommand(sublime_plugin.WindowCommand):
    """
    A simple shim command that wraps the build in close_others_by_index command
    but with the ability to trigger it from a key binding. It will determine
    what the currently active group and tab are in that group, and then invoke
    the built in command to close all others.
    """
    def run(self):
        group, index = self.window.get_sheet_index(self.window.active_sheet())
        self.window.run_command('close_others_by_index', {
            "group": group,
            "index": index
        })
