"""
Tofbot can be enhanced via the use of plugins.

The interface is the Plugin class (defined in toflib.py).

An instance of each plugin is added to bot.plugins via load_plugins.

Basically, for each imported submodule of plugins, a class is a plugin class if
its name starts with "Plugin".

TL;DR : to add a plugin, create a file under plugins/ with a class starting with
"Plugin", and import it in bot.py.
"""
