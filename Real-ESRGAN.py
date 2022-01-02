#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#    This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
gi.require_version('GimpUi', '3.0')
from gi.repository import GimpUi
gi.require_version('Gegl', '0.4')
from gi.repository import Gegl
from gi.repository import GObject
from gi.repository import GLib
from gi.repository import Gio

import gettext
import os
import sys
from inference_realesrgan import apply_real_esr_gan

textdomain = 'gimp30-std-plug-ins'
gettext.bindtextdomain(textdomain, Gimp.locale_directory())
#gettext.bind_textdomain_codeset(textdomain, 'UTF-8')
gettext.textdomain(textdomain)
_ = gettext.gettext
def N_(message): return message


class ArgsFromDict:
    def __init__(self, **entries):
        self.__dict__.update(entries)

def save_image(image, drawable, file_path):
    interlace, compression = 0, 2
    Gimp.get_pdb().run_procedure(
        "file-png-save",
        [
            GObject.Value(Gimp.RunMode, Gimp.RunMode.NONINTERACTIVE),
            GObject.Value(Gimp.Image, image),
            GObject.Value(GObject.TYPE_INT, 1),
            GObject.Value(
                Gimp.ObjectArray, Gimp.ObjectArray.new(Gimp.Drawable, [drawable], 0)
            ),
            GObject.Value(
                Gio.File,
                Gio.File.new_for_path(file_path),
            ),
            GObject.Value(GObject.TYPE_BOOLEAN, interlace),
            GObject.Value(GObject.TYPE_INT, compression),

            GObject.Value(GObject.TYPE_BOOLEAN, True),
            GObject.Value(GObject.TYPE_BOOLEAN, True),
            GObject.Value(GObject.TYPE_BOOLEAN, False),
            GObject.Value(GObject.TYPE_BOOLEAN, True),
        ],
    )

def load_image(file_path):
    img = Gimp.get_pdb().run_procedure(
        "gimp-file-load",
        [
            GObject.Value(Gimp.RunMode, Gimp.RunMode.NONINTERACTIVE),
            GObject.Value(
                Gio.File,
                Gio.File.new_for_path(file_path),
            ),
        ]
    ).index(1)
    return img


class SaveAndLoad(Gimp.PlugIn):
    ## GimpPlugIn virtual methods ##
    def do_query_procedures(self):
        # Localization for the menu entries. It has to be called in the
        # query function only.
        self.set_translation_domain(textdomain,
                                    Gio.file_new_for_path(Gimp.locale_directory()))

        return [ "plug-in-real-ESRGan-python" ]

    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(self, name,
                                       Gimp.PDBProcType.PLUGIN,
                                       self.run, None)

        procedure.set_image_types("*")
        procedure.set_sensitivity_mask (Gimp.ProcedureSensitivityMask.DRAWABLE)

        procedure.set_menu_label(N_("Real ESRGan"))
        procedure.set_icon_name(GimpUi.ICON_GEGL)
        procedure.add_menu_path('<Image>/Filters')

        procedure.set_documentation(N_("Real ESRGan"),
                                    N_("Deep 4x resolution"),
                                    name)
        procedure.set_attribution("z-uo", "z-uo", "2021")

        return procedure

    def run(self, procedure, run_mode, image, n_drawables, drawables, args, run_data):
        if n_drawables != 1:
            msg = _("Procedure '{}' only works with one drawable.").format(procedure.get_name())
            error = GLib.Error.new_literal(Gimp.PlugIn.error_quark(), msg, 0)
            return procedure.new_return_values(Gimp.PDBStatusType.CALLING_ERROR, error)
        else:
            drawable = drawables[0]

        if run_mode == Gimp.RunMode.INTERACTIVE:
            gi.require_version('Gtk', '3.0')
            from gi.repository import Gtk
            gi.require_version('Gdk', '3.0')
            from gi.repository import Gdk

            GimpUi.init("Real-ESRGan.py")

            dialog = GimpUi.Dialog(use_header_bar=True,
                                   title=_("Real ESRGan"),
                                   role="real-ESRGan-Python3")

            dialog.add_button(_("_Cancel"), Gtk.ResponseType.CANCEL)
            dialog.add_button(_("_OK"), Gtk.ResponseType.OK)

            builder = Gtk.Builder()
            dir_path = os.path.dirname(os.path.realpath(__file__))
            builder.add_from_file(os.path.join(dir_path, "ui.glade"))

            box = builder.get_object("box")
            dialog.get_content_area().add(box)
            box.show()

            model_selector = builder.get_object("model_selector")
            apha_upsampler_selector = builder.get_object("apha_upsampler_selector")
            scale_spinner = builder.get_object("scale_spinner")
            tile_spinner = builder.get_object("tile_spinner")
            tile_pad_spinner = builder.get_object("tile_pad_spinner")
            tile_prepad_spinner = builder.get_object("tile_prepad_spinner")
            face_enhance = builder.get_object("face_enhance")
            half = builder.get_object("half")

            while (True):
                response = dialog.run()
                if response == Gtk.ResponseType.OK:
                    #base_dir = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), True)
                    dir_path = os.path.dirname(os.path.realpath(__file__))

                    input_path = os.path.join(dir_path, "results/cache.png")
                    # save
                    save_image(image, drawable, input_path)

                    # compute something and resave image
                    args = ArgsFromDict(**{
                        'input': input_path,
                        'model_name': model_selector.get_active_text(),
                        'output': 'results',
                        'outscale': scale_spinner.get_value(),
                        'suffix': 'out',
                        'tile': tile_spinner.get_value_as_int(),
                        'tile_pad': tile_pad_spinner.get_value_as_int(),
                        'pre_pad': tile_prepad_spinner.get_value_as_int(),
                        'face_enhance': face_enhance.get_active(),
                        'half': half.get_active(),
                        'alpha_upsampler': apha_upsampler_selector.get_active_text(),
                        'ext': 'auto',
                    })
                    apply_real_esr_gan(args)

                    # load and create layer
                    img = load_image(os.path.join(dir_path, "results/cache_out.png"))
                    result_layer = img.get_active_layer()
                    layer = Gimp.Layer.new_from_drawable(result_layer, image)
                    layer.set_name("loaded")

                    position = Gimp.get_pdb().run_procedure('gimp-image-get-item-position',
                                 [image,
                                  drawable]).index(1)
                    image.insert_layer(layer,None,position)

                    # close dialog
                    dialog.destroy()
                    break
                else:
                    dialog.destroy()
                    return procedure.new_return_values(Gimp.PDBStatusType.CANCEL,
                                                       GLib.Error())


        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

Gimp.main(SaveAndLoad.__gtype__, sys.argv)
