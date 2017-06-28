import npyscreen
import threading
import time

from vent.api.actions import Action
from vent.api.plugins import Plugin
from vent.helpers.meta import Tools


class ChooseToolsForm(npyscreen.ActionForm):
    """ For picking which tools to add """
    tools_tc = {}

    def repo_tools(self, branch):
        """ Set the appropriate repo dir and get the tools available of it """
        tools = []
        plugin = Plugin()
        repo = self.parentApp.repo_value['repo']
        version = self.parentApp.repo_value['versions'][branch]
        status = plugin.repo_tools(repo, branch, version)
        if status[0]:
            r_tools = status[1]
            for tool in r_tools:
                tools.append(tool[0])
        return tools

    def create(self):
        """ Update with current tools for each branch at the version chosen """
        self.add_handlers({"^Q": self.quit})
        self.add(npyscreen.TitleText,
                 name='Select which tools to add from each branch selected:',
                 editable=False)

        i = 4
        for branch in self.parentApp.repo_value['versions']:
            self.tools_tc[branch] = {}
            title_text = self.add(npyscreen.TitleText,
                                  name='Branch: ' + branch,
                                  editable=False,
                                  rely=i,
                                  relx=5,
                                  max_width=25)
            tools = self.repo_tools(branch)
            i += 1
            for tool in tools:
                value = True
                if tool.startswith("/dev"):
                    value = False
                if tool == "":
                    tool = "/"
                self.tools_tc[branch][tool] = self.add(npyscreen.CheckBox,
                                                       name=tool,
                                                       value=value,
                                                       relx=10)
                i += 1
            i += 2

    def quit(self, *args, **kwargs):
        self.parentApp.switchForm("MAIN")

    def on_ok(self):
        """
        Take the tool selections and add them as plugins
        """
        def diff(first, second):
            """
            Get the elements that exist in the first list and not in the second
            """
            second = set(second)
            return [item for item in first if item not in second]

        def popup(original_tools, branch, thr, title):
            """
            Start the thread and display a popup of the tools being added until
            the thread is finished
            """
            thr.start()
            tool_str = "Adding tools..."
            npyscreen.notify_wait(tool_str, title=title)
            while thr.is_alive():
                tools = diff(Tools(), original_tools)
                if tools:
                    tool_str = ""
                for tool in tools:
                    pre_tool = "Added: " + branch + "/" + tool + "\n"
                    tool_str = pre_tool + tool_str
                npyscreen.notify_wait(tool_str, title=title)
                time.sleep(1)
            return

        original_tools = Tools()
        for branch in self.tools_tc:
            api_action = Action()
            tools = []
            for tool in self.tools_tc[branch]:
                if self.tools_tc[branch][tool].value:
                    if tool == '/':
                        tools.append(('.', ''))
                    else:
                        tools.append((tool, ''))
            repo = self.parentApp.repo_value['repo']
            version = self.parentApp.repo_value['versions'][branch]
            build = self.parentApp.repo_value['build'][branch]
            thr = threading.Thread(target=api_action.add, args=(),
                                   kwargs={'repo': repo,
                                           'branch': branch,
                                           'tools': tools,
                                           'version': version,
                                           'build': build})
            popup(original_tools, branch, thr,
                  'Please wait, adding tools for the ' + branch + ' branch...')
        npyscreen.notify_confirm("Done adding repository: " +
                                 self.parentApp.repo_value['repo'],
                                 title='Added Repository')
        self.quit()

    def on_cancel(self):
        self.quit()
