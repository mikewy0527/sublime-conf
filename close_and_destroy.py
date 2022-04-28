import sublime
import sublime_plugin


class CloseAndDestroyCommand(sublime_plugin.WindowCommand):
    """
    Implement a close_and_destroy command which will close the current
    terminus view and then destroy the origami pane that it's inside of.
    """
    def run(self):
        self.window.run_command("terminus_close");
        self.window.run_command("destroy_pane", {"direction": "self"})
