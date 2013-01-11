#!/usr/bin/env python

# =================== LICENSE =================
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#
# Sergio R. Lumley
# 2012/12/01
# lumley256@gmail.com
# =================== LICENSE =================

# ========= What does this Script do?? =========
# This script transforms the given layer to a set of tiles separated
# by black lines, ready to use with TiledMapEditor (http://www.mapeditor.org/)
# loading the resulting image as a pattern with 2px margin and 3px spacing.

# This tells Python to load the Gimp module 
from gimpfu import *
import math

# This is the function that will perform actual actions
def transform_tmx_tiles(image, drawable, tileColumns, tileRows):
    if tileColumns <= 0 or tileRows <= 0 :
        gimp.pdb.gimp_message("Horizontal and vertical tiles must be bigger than 0")
        return

    # Numbers are integers, so no problem with this
    tileWidth = drawable.width/tileColumns
    tileHeight = drawable.height/tileRows

    # We group undoing so the history will show only one operation
    gimp.pdb.gimp_image_undo_group_start(image)
    
    # Create the new working layer
    workingLayer = gimp.pdb.gimp_layer_new(image,
                                           1+((tileWidth+3)*tileColumns),
                                           1+((tileHeight+3)*tileRows),
                                           RGBA_IMAGE,
                                           drawable.name+"_tmx_format",
                                           100,
                                           NORMAL_MODE)

    
    # Resize image to the desired image size
    gimp.pdb.gimp_progress_init("Resizing image", None)
    gimp.pdb.gimp_image_resize(image, workingLayer.width, workingLayer.height, 0, 0)
    gimp.pdb.gimp_image_insert_layer(image, workingLayer, None, -1)

    # Change working values and backup them to leave everything as it was
    currentForegroundColorBackup = gimp.pdb.gimp_context_get_foreground()
    gimp.pdb.gimp_context_set_foreground((0, 0, 0))

    # ---------------------- Select and paint the grid ---------------------------
    gimp.pdb.gimp_progress_update(0.05);
    gimp.pdb.gimp_selection_all(image)
    for column in range(tileColumns):
        for row in range(tileRows):
            gimp.pdb.gimp_image_select_rectangle(image,
                                                 CHANNEL_OP_SUBTRACT,
                                                 1+((tileWidth+3)*column),
                                                 1+((tileHeight+3)*row),
                                                 tileWidth+2,
                                                 tileHeight+2)
    gimp.pdb.gimp_edit_bucket_fill(workingLayer,
                                   FG_BUCKET_FILL,
                                   NORMAL_MODE,
                                   100, # Opacity
                                   0, # Not useful, we have selected regions
                                   False,
                                   0, # Not useful, we have selected regions
                                   0) # Not useful, we have selected regions

    # --------------------- Copy tiles to new layer ----------------------
    gimp.pdb.gimp_progress_update(0.25);
    gimp.pdb.gimp_selection_none(image)
    for column in range(tileColumns):
        for row in range(tileRows):
            gimp.pdb.gimp_image_select_rectangle(image,
                                                 CHANNEL_OP_ADD,
                                                 tileWidth*column,
                                                 tileHeight*row,
                                                 tileWidth,
                                                 tileHeight)
            gimp.pdb.gimp_edit_copy(drawable)
            gimp.pdb.gimp_selection_none(image)
            gimp.pdb.gimp_image_select_rectangle(image,
                                                 CHANNEL_OP_ADD,
                                                 1+((tileWidth+3)*column),
                                                 1+((tileHeight+3)*row),
                                                 tileWidth+2,
                                                 tileHeight+2)
            floatingLayer = gimp.pdb.gimp_edit_paste(workingLayer, True)
            gimp.pdb.gimp_floating_sel_anchor(floatingLayer)
            gimp.pdb.gimp_selection_none(image)
            
    # ---------------- Extend each side of the tile one pixel out --------
    gimp.pdb.gimp_progress_update(0.50);
    for column in range(tileColumns):
        # Copy and paste left side
        gimp.pdb.gimp_image_select_rectangle(image,
                                             CHANNEL_OP_ADD,
                                             2+((tileWidth+3)*column),
                                             0,
                                             1,
                                             workingLayer.height)
        gimp.pdb.gimp_edit_copy(workingLayer)
        gimp.pdb.gimp_selection_none(image)
        gimp.pdb.gimp_image_select_rectangle(image,
                                             CHANNEL_OP_ADD,
                                             1+((tileWidth+3)*column),
                                             0,
                                             1,
                                             workingLayer.height)
        floatingLayer = gimp.pdb.gimp_edit_paste(workingLayer, True)
        gimp.pdb.gimp_floating_sel_anchor(floatingLayer)
        gimp.pdb.gimp_selection_none(image)

        # Copy and paste right side
        gimp.pdb.gimp_image_select_rectangle(image,
                                             CHANNEL_OP_ADD,
                                             tileWidth+1+((tileWidth+3)*column),
                                             0,
                                             1,
                                             workingLayer.height)
        gimp.pdb.gimp_edit_copy(workingLayer)
        gimp.pdb.gimp_selection_none(image)
        gimp.pdb.gimp_image_select_rectangle(image,
                                             CHANNEL_OP_ADD,
                                             tileWidth+2+((tileWidth+3)*column),
                                             0,
                                             1,
                                             workingLayer.height)
        floatingLayer = gimp.pdb.gimp_edit_paste(workingLayer, True)
        gimp.pdb.gimp_floating_sel_anchor(floatingLayer)
        gimp.pdb.gimp_selection_none(image)

    gimp.pdb.gimp_progress_update(0.75);
    for row in range(tileRows):
        # Copy and paste top side
        gimp.pdb.gimp_image_select_rectangle(image,
                                             CHANNEL_OP_ADD,
                                             0,
                                             2+((tileHeight+3)*row),
                                             workingLayer.width,
                                             1)
        gimp.pdb.gimp_edit_copy(workingLayer)
        gimp.pdb.gimp_selection_none(image)
        gimp.pdb.gimp_image_select_rectangle(image,
                                             CHANNEL_OP_ADD,
                                             0,
                                             1+((tileHeight+3)*row),
                                             workingLayer.width,
                                             1)
        floatingLayer = gimp.pdb.gimp_edit_paste(workingLayer, True)
        gimp.pdb.gimp_floating_sel_anchor(floatingLayer)
        gimp.pdb.gimp_selection_none(image)

        # Copy and paste bottom side
        gimp.pdb.gimp_image_select_rectangle(image,
                                             CHANNEL_OP_ADD,
                                             0,
                                             tileHeight+1+((tileHeight+3)*row),
                                             workingLayer.width,
                                             1)
        gimp.pdb.gimp_edit_copy(workingLayer)
        gimp.pdb.gimp_selection_none(image)
        gimp.pdb.gimp_image_select_rectangle(image,
                                             CHANNEL_OP_ADD,
                                             0,
                                             tileHeight+2+((tileHeight+3)*row),
                                             workingLayer.width,
                                             1)
        floatingLayer = gimp.pdb.gimp_edit_paste(workingLayer, True)
        gimp.pdb.gimp_floating_sel_anchor(floatingLayer)
        gimp.pdb.gimp_selection_none(image)

    # -------- Erase a square of 3x3 on each grid corner ------------
    gimp.pdb.gimp_progress_update(0.95);
    for column in range(tileColumns+1):
        for row in range(tileRows+1):
            gimp.pdb.gimp_image_select_rectangle(image,
                                             CHANNEL_OP_ADD,
                                             (tileWidth+3)*column - 1,
                                             (tileHeight+3)*row - 1,
                                             3,
                                             3)
    gimp.pdb.gimp_progress_update(1.0);
    gimp.pdb.gimp_edit_clear(workingLayer)
    gimp.pdb.gimp_selection_none(image)
    
    #Now we finish grouping these changes
    
    gimp.pdb.gimp_context_set_foreground(currentForegroundColorBackup)
    gimp.pdb.gimp_image_undo_group_end(image)
    #gimp.pdb.gimp_image_select_rectangle(image, CHANNEL_OP_ADD, 0, 0, tile_columns, tile_rows)
    return

# This is the plugin registration function
# I have written each of its parameters on a different line 
register(
    "transform_tmx_tiles",    
    "Divide an image into tiles",   
    "This script will divide the current image into a set of tiled. Each tile has one pixel margin and a black line that separates each tile.",
    "Sergio R. Lumley", 
    "You are free to use, distribute and sell this plugin under license GPLv3", 
    "01 December 2012",
    "<Image>/Filters/Map/Transform to TMX Tiles", 
    "*", 
    [(PF_INT16, "tiles_x", "Number of horizontal tiles", 8, None),
     (PF_INT16, "tiles_y", "Number of vertical tiles", 8, None),], 
    [],
    transform_tmx_tiles
    )

main()
