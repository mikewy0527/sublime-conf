import sublime
import sublime_plugin

import os

from Default.exec import ExecCommand


def _get_project_settings(window):
    project_data = window.project_data()
    return project_data.get('settings', {})


def _set_project_settings(window, settings):
    project_data = window.project_data() or {}
    project_data['settings'] = settings

    window.set_project_data(project_data)


class SelectMakefileCommand(sublime_plugin.WindowCommand):
    def run(self, files=[]):
        settings = _get_project_settings(self.window)
        settings.update({
            'selected_makefile': files[0],
            'selected_makefile_path': os.path.dirname(files[0])
        })

        _set_project_settings(self.window, settings)

    def is_enabled(self, files=[]):
        return len(files) == 1 and os.path.basename(files[0]).upper() == 'MAKEFILE'

    # Make the command only visible when it's enabled; comment this method out
    # or remove it to have the menu item always available but disabled.
    def is_visible(self, files=[]):
        return self.is_enabled(files)

    def is_checked(self, files=[]):
        settings = _get_project_settings(self.window)
        return len(files) == 1 and files[0] == settings.get('selected_makefile', '')


class MakefileBuildCommand(ExecCommand):
    """
    Enhanced version of the internal exec command that can expand out a new
    variable.
    """
    def run(self, **kwargs):
        kill = kwargs.get('kill', False)
        if kill:
            return super().run(kill=True)

        settings = _get_project_settings(self.window)
        variables = {
            'selected_makefile': settings.get('selected_makefile', ''),
            'selected_makefile_path': settings.get('selected_makefile_path', '')
        }

        if variables['selected_makefile'] == '':
            return sublime.error_message('No Makefile has been selected for this project')

        # Only expand variables in places where we expect variables to expand;
        # otherwise you need to manually escape $ characters in other
        # variables, which is not required by the core exec command.
        for var in ['shell_cmd', 'cmd', 'working_dir']:
            if var in kwargs:
                kwargs[var] = sublime.expand_variables(kwargs[var], variables)

        kwargs = sublime.expand_variables(kwargs, variables)
        super().run(**kwargs)
