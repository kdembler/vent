import os
import pytest

from .. import menu_launcher

class PathDirs:
    """ Global path directories for parsing templates """
    def __init__(self,
                 base_dir=os.getcwd()+"/",
                 collectors_dir="collectors",
                 core_dir="core",
                 plugins_dir="plugins/",
                 plugin_repos="plugin_repos",
                 template_dir="templates/",
                 vis_dir="visualization"):
        self.base_dir = base_dir
        self.collectors_dir = base_dir + collectors_dir
        if not os.path.exists(self.collectors_dir):
            os.makedirs(self.collectors_dir)
        self.core_dir = base_dir + core_dir
        self.plugins_dir = base_dir + plugins_dir
        self.plugin_repos = base_dir + plugin_repos
        if not os.path.exists(self.plugin_repos):
            os.makedirs(self.plugin_repos)
        self.template_dir = base_dir + template_dir
        self.vis_dir = base_dir + vis_dir
        if not os.path.exists(self.vis_dir):
            os.makedirs(self.vis_dir)

def test_pathdirs():
    path_dirs = menu_launcher.PathDirs()

def test_update_images():
    path_dirs = PathDirs()
    menu_launcher.update_images(path_dirs)

def test_get_mode_config():
    path_dirs = PathDirs()
    menu_launcher.get_mode_config(path_dirs)

def test_get_core_config():
    path_dirs = PathDirs()
    menu_launcher.get_core_config(path_dirs)

def test_get_installed_cores():
    path_dirs = PathDirs()
    menu_launcher.get_installed_cores(path_dirs)

def test_get_installed_collectors():
    path_dirs = PathDirs()
    menu_launcher.get_installed_collectors(path_dirs, "all")
    menu_launcher.get_installed_collectors(path_dirs, "passive")
    menu_launcher.get_installed_collectors(path_dirs, "active")

def test_get_installed_vis():
    path_dirs = PathDirs()
    menu_launcher.get_installed_vis(path_dirs)

def test_get_installed_plugins():
    path_dirs = PathDirs()
    menu_launcher.get_installed_plugins(path_dirs)

def test_get_all_installed():
    path_dirs = PathDirs()
    menu_launcher.get_all_installed(path_dirs)

def test_get_mode_enabled():
    path_dirs = PathDirs()
    mode_config = menu_launcher.get_mode_config(path_dirs)
    menu_launcher.get_mode_enabled(path_dirs, mode_config)

def test_get_core_enabled():
    path_dirs = PathDirs()
    core_config = menu_launcher.get_core_config(path_dirs)
    menu_launcher.get_core_enabled(path_dirs, core_config)

def test_get_enabled():
    path_dirs = PathDirs()
    menu_launcher.get_enabled(path_dirs)

def test_get_plugin_status():
    path_dirs = PathDirs()
    menu_launcher.get_plugin_status(path_dirs)

def test_run_plugins():
    path_dirs = PathDirs()
    menu_launcher.run_plugins(path_dirs, "start")

def test_get_installed_plugin_repos():
    path_dirs = PathDirs()
    menu_launcher.get_installed_plugin_repos(path_dirs, "INFO", "remove")
    menu_launcher.get_installed_plugin_repos(path_dirs, "INFO", "update")
    menu_launcher.get_installed_plugin_repos(path_dirs, "INFO", "")

def test_update_plugins():
    path_dirs = PathDirs()
    menu_launcher.update_plugins(path_dirs)

def test_build_menu_dict():
    path_dirs = PathDirs()
    menu_launcher.build_menu_dict(path_dirs)
