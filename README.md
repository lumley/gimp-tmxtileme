# Gimp plugin - TMX Tile me

This script will turn a given layer into a set of tiles separated by a black-1px width line, each tile with 1px margin around. The resulting layer is ready to be exported and used directly in [`Tiled Map Editor`][URI_TiledMapEditor] importing is as a pattern with 2px margin and 3px spacing.
This plug-in is not part of Tiled Map Editor or officially supported by it. You can find its official project in [`Tiled Map Editor official Git repository`][URI_TiledMapEditorGit].

It has been tested in Gimp2.8.

## Requirements
This plugin requires the following:
 * [`The Gimp GNU Image Manipulation Program`][URI_TheGimp] The GIMP program (Available on Linux, Windows and Mac)
 * Python GIMP-extension (usually installed by default)

## Installation
Installation of this plugin goes like any other Python-fu plugin. Just download the file and move it to your GIMP plug-ins folder (by default, "%USERPROFILE%\\.gimp-2.8\plug-ins\" in Windows and "~/.gimp-2.8/plug-ins/" in Linux).

Once installed you will find the plugin in Gimp menu: Filters -> Map -> Transform into TMX Tiles

## Collaborate
Want to make your own plugins or improve this one? You can find some information on how to start on the next link:
 * [`Frederic Jaume - Python-Fu introduction`][URI_GimpTutorial1]

[URI_TiledMapEditor]: http://www.mapeditor.org/
[URI_TiledMapEditorGit]: https://github.com/bjorn/tiled.git
[URI_TheGimp]: http://www.gimp.org/
[URI_GimpTutorial1]: http://www.exp-media.com/content/extending-gimp-python-python-fu-plugins-part-1