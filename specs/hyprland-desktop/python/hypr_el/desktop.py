"""Desktop icons for the hyprland-el desktop (GTK3 + gtk-layer-shell).

Shows Home, Trash, Settings, Terminal and the content of the XDG desktop
folder (~/Schreibtisch, ~/Desktop) on the background layer.
Double click opens, right click opens a context menu, the folder is watched.
"""
import os
import subprocess

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("GtkLayerShell", "0.1")
from gi.repository import Gdk, Gio, GLib, Gtk, GtkLayerShell  # noqa: E402

from . import settings as S  # noqa: E402

ICON = 48


def _spawn(cmd):
    subprocess.Popen(cmd, shell=isinstance(cmd, str), start_new_session=True,
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def _terminal_cmd(cwd=None):
    s = S.load()
    cfg = os.path.join(S.CONFIG_HOME, "kitty", "kitty.conf")
    if s["terminal"] == "kitty":
        base = ["kitty"] if os.path.exists(cfg) else ["kitty", "--config", os.path.join(S.CFG_DIR, "kitty.conf")]
        return base + (["--directory", cwd] if cwd else [])
    return [s["terminal"]]


class Item(Gtk.EventBox):
    def __init__(self, label, gicon, activate, menu=None):
        super().__init__()
        self.activate_cb = activate
        self.menu_cb = menu
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        box.get_style_context().add_class("item")
        img = Gtk.Image.new_from_gicon(gicon, Gtk.IconSize.DIALOG)
        img.set_pixel_size(ICON)
        lab = Gtk.Label(label=label)
        lab.set_max_width_chars(12)
        lab.set_line_wrap(True)
        lab.set_lines(2)
        lab.set_ellipsize(3)  # PANGO_ELLIPSIZE_END
        lab.set_justify(Gtk.Justification.CENTER)
        box.pack_start(img, False, False, 0)
        box.pack_start(lab, False, False, 0)
        box.set_size_request(96, 92)
        self.add(box)
        self.box = box
        self.connect("button-press-event", self.on_press)
        self.connect("enter-notify-event", lambda *_: box.get_style_context().add_class("hover"))
        self.connect("leave-notify-event", lambda *_: box.get_style_context().remove_class("hover"))

    def on_press(self, _w, ev):
        if ev.type == Gdk.EventType._2BUTTON_PRESS and ev.button == 1:
            self.activate_cb()
            return True
        if ev.type == Gdk.EventType.BUTTON_PRESS and ev.button == 3 and self.menu_cb:
            self.menu_cb(ev)
            return True
        return False


class Desktop(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("hypr-el-desktop")
        GtkLayerShell.init_for_window(self)
        GtkLayerShell.set_namespace(self, "hypr-el-desktop")
        GtkLayerShell.set_layer(self, GtkLayerShell.Layer.BOTTOM)
        for edge in (GtkLayerShell.Edge.TOP, GtkLayerShell.Edge.BOTTOM,
                     GtkLayerShell.Edge.LEFT, GtkLayerShell.Edge.RIGHT):
            GtkLayerShell.set_anchor(self, edge, True)
        GtkLayerShell.set_exclusive_zone(self, 0)
        GtkLayerShell.set_keyboard_mode(self, GtkLayerShell.KeyboardMode.NONE)

        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual:
            self.set_visual(visual)
        self.set_app_paintable(True)
        self._css()

        self.flow = Gtk.FlowBox(orientation=Gtk.Orientation.VERTICAL, selection_mode=Gtk.SelectionMode.NONE,
                                homogeneous=True, column_spacing=6, row_spacing=6)
        self.flow.set_valign(Gtk.Align.START)
        self.flow.set_halign(Gtk.Align.START)
        self.flow.set_margin_top(16)
        self.flow.set_margin_start(16)
        self.flow.set_max_children_per_line(8)
        bg = Gtk.EventBox()
        bg.set_visible_window(False)
        bg.add(self.flow)
        bg.connect("button-press-event", self._bg_press)
        self.add(bg)

        self.desk = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DESKTOP) or os.path.expanduser("~/Desktop")
        if os.path.realpath(self.desk) == os.path.realpath(os.path.expanduser("~")):
            self.desk = os.path.expanduser("~/Desktop")
        os.makedirs(self.desk, exist_ok=True)
        self.monitor = Gio.File.new_for_path(self.desk).monitor_directory(Gio.FileMonitorFlags.WATCH_MOVES, None)
        self.monitor.connect("changed", lambda *_: GLib.timeout_add(250, self.refresh) and None)
        self.refresh()

    def _css(self):
        t = S.theme(S.load())
        css = f"""
        window {{ background: transparent; }}
        .item {{ border-radius: 10px; padding: 6px 4px; }}
        .item.hover {{ background: alpha({t['accent']}, 0.22); }}
        .item label {{ color: #ffffff; font-weight: 600; font-size: 10.5pt;
                       text-shadow: 0 1px 3px rgba(0,0,0,0.9), 0 0 6px rgba(0,0,0,0.6); }}
        menu, .menu {{ background: {t['base']}; color: {t['fg']}; border-radius: 8px; }}
        menuitem:hover {{ background: {t['surface']}; }}
        """
        prov = Gtk.CssProvider()
        prov.load_from_data(css.encode())
        Gtk.StyleContext.add_provider_for_screen(self.get_screen(), prov,
                                                 Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    # ------------------------------------------------------------------ items
    def refresh(self):
        for c in self.flow.get_children():
            self.flow.remove(c)
        home = os.path.expanduser("~")
        fixed = [
            ("Persönlicher Ordner", Gio.ThemedIcon.new("user-home"), lambda: self._open_uri(Gio.File.new_for_path(home).get_uri())),
            ("Papierkorb", Gio.ThemedIcon.new("user-trash"), lambda: self._open_uri("trash:///")),
            ("Terminal", Gio.ThemedIcon.new("utilities-terminal"), lambda: _spawn(_terminal_cmd(home))),
            ("Einstellungen", Gio.ThemedIcon.new("preferences-desktop"), lambda: _spawn(["hypr-el-settings"])),
        ]
        for label, icon, act in fixed:
            self.flow.add(Item(label, icon, act))
        try:
            names = sorted(os.listdir(self.desk), key=lambda n: (not os.path.isdir(os.path.join(self.desk, n)), n.lower()))
        except OSError:
            names = []
        for n in names:
            if n.startswith("."):
                continue
            path = os.path.join(self.desk, n)
            f = Gio.File.new_for_path(path)
            label, icon = n, None
            if n.endswith(".desktop"):
                app = Gio.DesktopAppInfo.new_from_filename(path)
                if app:
                    label, icon = app.get_display_name(), app.get_icon()
                    self.flow.add(Item(label, icon or Gio.ThemedIcon.new("application-x-executable"),
                                       lambda a=app: a.launch([], None), self._file_menu(f)))
                    continue
            try:
                info = f.query_info("standard::icon,thumbnail::path", Gio.FileQueryInfoFlags.NONE, None)
                tp = info.get_attribute_byte_string("thumbnail::path")
                icon = Gio.FileIcon.new(Gio.File.new_for_path(tp)) if tp else info.get_icon()
            except GLib.Error:
                icon = Gio.ThemedIcon.new("text-x-generic")
            self.flow.add(Item(label, icon, lambda u=f.get_uri(): self._open_uri(u), self._file_menu(f)))
        self.show_all()
        return False

    @staticmethod
    def _open_uri(uri):
        try:
            Gio.AppInfo.launch_default_for_uri(uri, None)
        except GLib.Error:
            _spawn(["xdg-open", uri])

    # ------------------------------------------------------------------ menus
    def _menu(self, entries, ev):
        m = Gtk.Menu()
        for label, cb in entries:
            if label is None:
                m.append(Gtk.SeparatorMenuItem())
                continue
            it = Gtk.MenuItem(label=label)
            it.connect("activate", lambda _i, c=cb: c())
            m.append(it)
        m.show_all()
        m.attach_to_widget(self, None)
        m.popup_at_pointer(ev)

    def _file_menu(self, f):
        def show(ev):
            self._menu([
                ("Öffnen", lambda: self._open_uri(f.get_uri())),
                ("Im Dateimanager zeigen", lambda: self._open_uri(f.get_parent().get_uri())),
                (None, None),
                ("In den Papierkorb", lambda: self._trash(f)),
            ], ev)
        return show

    @staticmethod
    def _trash(f):
        try:
            f.trash(None)
        except GLib.Error:
            pass

    def _bg_press(self, _w, ev):
        if ev.button != 3:
            return False
        self._menu([
            ("Terminal hier öffnen", lambda: _spawn(_terminal_cmd(self.desk))),
            ("Schreibtisch-Ordner öffnen", lambda: self._open_uri(Gio.File.new_for_path(self.desk).get_uri())),
            ("Neuer Ordner", self._new_folder),
            (None, None),
            ("Hintergrund und Theme ändern …", lambda: _spawn(["hypr-el-settings"])),
            ("Nächstes Theme", lambda: _spawn(["hypr-el-settings", "--next-theme"])),
            ("Tastenkürzel anzeigen", lambda: _spawn(["hypr-el-keys"])),
        ], ev)
        return True

    def _new_folder(self):
        base, i = os.path.join(self.desk, "Neuer Ordner"), 1
        p = base
        while os.path.exists(p):
            i += 1
            p = f"{base} {i}"
        os.makedirs(p, exist_ok=True)


def main():
    win = Desktop()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
    return 0
