"""Hyprland-Einstellungen – settings app for the hyprland-el desktop (GTK4 + libadwaita)."""
import copy
import os
import threading

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gio, GLib, Gtk, Gdk  # noqa: E402

from . import apply as A          # noqa: E402
from . import settings as S       # noqa: E402
from . import wallpapers as W     # noqa: E402

APP_ID = "io.github.perutzit.HyprElSettings"
THUMBS = os.path.join(S.CACHE_HOME, "hypr-el", "thumbs")

LAYOUTS = [("dwindle", "Kacheln (automatisch teilen)"), ("master", "Hauptfenster + Stapel"),
           ("scrolling", "Scrollende Spalten")]
KB_COMMON = [("", "Automatisch (wie in GNOME / System)"), ("de", "Deutsch"), ("at", "Deutsch (Österreich)"),
             ("ch", "Deutsch (Schweiz)"), ("us", "Englisch (US)"), ("gb", "Englisch (UK)"), ("fr", "Französisch"),
             ("it", "Italienisch"), ("es", "Spanisch"), ("nl", "Niederländisch"), ("pl", "Polnisch"),
             ("cz", "Tschechisch"), ("hu", "Ungarisch")]
SCALES = ["auto", "1", "1.25", "1.5", "1.75", "2"]


class Settings(Adw.PreferencesWindow):
    def __init__(self, app):
        super().__init__(application=app, title="Hyprland-Einstellungen")
        self.set_default_size(1000, 740)
        self.set_search_enabled(False)
        self.s = S.load()
        self.themes = S.themes()
        self._pending = None
        self._busy = False

        self.add(self.page_appearance())
        self.add(self.page_windows())
        self.add(self.page_input())
        self.add(self.page_displays())
        self.add(self.page_power())
        self.add(self.page_apps())

    # ------------------------------------------------------------------ plumbing
    def set(self, key, value, delay=350):
        if self.s.get(key) == value:
            return
        self.s[key] = value
        S.save(self.s)
        if self._pending:
            GLib.source_remove(self._pending)
        self._pending = GLib.timeout_add(delay, self._apply_now)

    def _apply_now(self):
        self._pending = None
        if self._busy:                       # coalesce while an apply is running
            self._pending = GLib.timeout_add(300, self._apply_now)
            return False
        self._busy = True

        def work():
            try:
                A.apply(reload=True)
            finally:
                GLib.idle_add(self._done)
        threading.Thread(target=work, daemon=True).start()
        return False

    def _done(self):
        self._busy = False
        return False

    def toast(self, text):
        self.add_toast(Adw.Toast(title=text, timeout=2))

    def switch(self, group, key, title, subtitle=None):
        row = Adw.SwitchRow(title=title)
        if subtitle:
            row.set_subtitle(subtitle)
        row.set_active(bool(self.s[key]))
        row.connect("notify::active", lambda r, _p: self.set(key, r.get_active()))
        group.add(row)
        return row

    def spin(self, group, key, title, lo, hi, step=1, subtitle=None, digits=0):
        adj = Gtk.Adjustment(lower=lo, upper=hi, step_increment=step, page_increment=step * 5)
        row = Adw.SpinRow(title=title, adjustment=adj, digits=digits)
        if subtitle:
            row.set_subtitle(subtitle)
        row.set_value(self.s[key])
        conv = (lambda v: round(v, digits)) if digits else (lambda v: int(round(v)))
        row.connect("notify::value", lambda r, _p: self.set(key, conv(r.get_value())))
        group.add(row)
        return row

    def combo(self, group, key, title, options, subtitle=None):
        model = Gtk.StringList()
        for _v, label in options:
            model.append(label)
        row = Adw.ComboRow(title=title, model=model)
        if subtitle:
            row.set_subtitle(subtitle)
        vals = [v for v, _l in options]
        if self.s[key] in vals:
            row.set_selected(vals.index(self.s[key]))
        row.connect("notify::selected", lambda r, _p: self.set(key, vals[r.get_selected()]))
        group.add(row)
        return row

    # ------------------------------------------------------------------ pages
    def page_appearance(self):
        page = Adw.PreferencesPage(title="Aussehen", icon_name="applications-graphics-symbolic")

        g = Adw.PreferencesGroup(title="Theme", description="Farben für Fenster, Leiste, Terminal, Sperrbildschirm "
                                 "und GTK-Programme. Schnell wechseln: SUPER+SHIFT+T")
        flow = Gtk.FlowBox(selection_mode=Gtk.SelectionMode.SINGLE, max_children_per_line=4,
                           min_children_per_line=2, row_spacing=12, column_spacing=12, homogeneous=True)
        flow.set_margin_top(6)
        self._theme_children = {}
        for tid, t in self.themes.items():
            child = Gtk.FlowBoxChild()
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
            pic = Gtk.Picture(content_fit=Gtk.ContentFit.COVER, can_shrink=True)
            pic.set_size_request(200, 112)
            frame = Gtk.Frame(child=pic)
            frame.add_css_class("card")
            box.append(frame)
            dots = Gtk.Box(spacing=4, halign=Gtk.Align.CENTER)
            for c in (t["base"], t["accent"], t["accent2"], t["red"], t["green"], t["yellow"]):
                d = Gtk.DrawingArea(content_width=14, content_height=14)
                d.set_draw_func(self._dot, c)
                dots.append(d)
            box.append(dots)
            box.append(Gtk.Label(label=t["name"]))
            child.set_child(box)
            child.theme_id = tid
            flow.append(child)
            self._theme_children[tid] = (child, pic)
            if tid == self.s["theme"]:
                flow.select_child(child)
        flow.connect("child-activated", self._on_theme)
        g.add(flow)
        page.add(g)
        threading.Thread(target=self._render_thumbs, daemon=True).start()

        g = Adw.PreferencesGroup(title="Hintergrundbild")
        self.wp_row = Adw.ActionRow(title="Bild", subtitle=self._wp_label())
        b1 = Gtk.Button(label="Eigenes Bild …", valign=Gtk.Align.CENTER)
        b1.connect("clicked", self._choose_wallpaper)
        b2 = Gtk.Button(label="Theme-Bild", valign=Gtk.Align.CENTER)
        b2.connect("clicked", lambda _b: self._set_wallpaper(""))
        self.wp_row.add_suffix(b2)
        self.wp_row.add_suffix(b1)
        g.add(self.wp_row)
        page.add(g)

        g = Adw.PreferencesGroup(title="Fensterdekoration")
        self.switch(g, "titlebars", "Titelleisten mit Knöpfen",
                    "Schließen, Maximieren und Minimieren per Maus; Titelleiste ziehen verschiebt das Fenster")
        self.spin(g, "rounding", "Eckenradius", 0, 24)
        self.spin(g, "border_size", "Rahmenbreite", 0, 6)
        self.spin(g, "gaps_in", "Abstand zwischen Fenstern", 0, 30)
        self.spin(g, "gaps_out", "Abstand zum Bildschirmrand", 0, 40)
        page.add(g)

        g = Adw.PreferencesGroup(title="Schreibtisch")
        self.switch(g, "desktop_icons", "Symbole auf dem Schreibtisch",
                    "Persönlicher Ordner, Papierkorb, Terminal, Einstellungen und der Inhalt von ~/Schreibtisch")
        page.add(g)

        g = Adw.PreferencesGroup(title="Effekte")
        self.switch(g, "animations", "Animationen")
        self.switch(g, "blur", "Unschärfe hinter Leiste und transparenten Fenstern")
        self.switch(g, "shadows", "Schatten")
        self.spin(g, "active_opacity", "Deckkraft des aktiven Fensters", 0.6, 1.0, 0.02, "1 = undurchsichtig", digits=2)
        self.spin(g, "inactive_opacity", "Deckkraft inaktiver Fenster", 0.6, 1.0, 0.02, digits=2)
        self.spin(g, "terminal_opacity", "Deckkraft des Terminals", 0.6, 1.0, 0.02, digits=2)
        page.add(g)
        return page

    @staticmethod
    def _dot(_area, cr, w, h, color):
        rgba = Gdk.RGBA()
        rgba.parse(color)
        cr.set_source_rgba(rgba.red, rgba.green, rgba.blue, 1)
        cr.arc(w / 2, h / 2, min(w, h) / 2 - 1, 0, 6.2832)
        cr.fill()

    def _render_thumbs(self):
        for tid, t in self.themes.items():
            try:
                p = W.render(t, 400, 225, THUMBS)
            except Exception:  # noqa: BLE001 – a missing thumbnail is not fatal
                continue
            GLib.idle_add(self._theme_children[tid][1].set_filename, p)

    def _on_theme(self, _flow, child):
        self.set("theme", child.theme_id, delay=50)
        self.toast(f"Theme: {self.themes[child.theme_id]['name']}")

    def _wp_label(self):
        return self.s["wallpaper"] or "Passend zum Theme"

    def _choose_wallpaper(self, _b):
        dlg = Gtk.FileDialog(title="Hintergrundbild wählen")
        f = Gtk.FileFilter()
        f.set_name("Bilder")
        for m in ("image/png", "image/jpeg", "image/webp"):
            f.add_mime_type(m)
        filters = Gio.ListStore.new(Gtk.FileFilter)
        filters.append(f)
        dlg.set_filters(filters)
        pics = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_PICTURES)
        if pics and os.path.isdir(pics):
            dlg.set_initial_folder(Gio.File.new_for_path(pics))

        def done(d, res):
            try:
                gf = d.open_finish(res)
            except GLib.Error:
                return
            if gf and gf.get_path():
                self._set_wallpaper(gf.get_path())
        dlg.open(self, None, done)

    def _set_wallpaper(self, path):
        self.set("wallpaper", path, delay=50)
        self.wp_row.set_subtitle(self._wp_label())

    def page_windows(self):
        page = Adw.PreferencesPage(title="Fenster & Leiste", icon_name="view-grid-symbolic")
        g = Adw.PreferencesGroup(title="Fensterverhalten")
        self.combo(g, "layout", "Anordnung", LAYOUTS, "Wie neue Fenster auf dem Bildschirm verteilt werden")
        self.switch(g, "float_new_windows", "Klassischer Modus: neue Fenster frei schwebend",
                    "Wie bei Windows/GNOME. SUPER+V schaltet einzelne Fenster jederzeit um")
        self.switch(g, "focus_follows_mouse", "Fokus folgt der Maus",
                    "Aus: ein Fenster wird erst durch Klicken aktiv")
        page.add(g)

        g = Adw.PreferencesGroup(title="Leiste")
        self.combo(g, "bar_position", "Position", [("top", "Oben"), ("bottom", "Unten")])
        self.switch(g, "bar_taskbar", "Taskleiste mit offenen Fenstern",
                    "Klick: anzeigen/wiederherstellen · Mittelklick: schließen · Rechtsklick: minimieren")
        self.switch(g, "clock_24h", "24-Stunden-Uhr")
        self.switch(g, "clock_seconds", "Sekunden anzeigen")
        page.add(g)

        g = Adw.PreferencesGroup(title="Hilfe")
        row = Adw.ActionRow(title="Alle Tastenkürzel anzeigen", subtitle="SUPER+F1")
        b = Gtk.Button(label="Öffnen", valign=Gtk.Align.CENTER)
        b.connect("clicked", lambda _b: GLib.spawn_command_line_async("hypr-el-keys"))
        row.add_suffix(b)
        g.add(row)
        page.add(g)
        return page

    def page_input(self):
        page = Adw.PreferencesPage(title="Eingabe", icon_name="input-keyboard-symbolic")
        g = Adw.PreferencesGroup(title="Tastatur",
                                 description="Mehrere Layouts: mit ALT+SHIFT umschalten")
        cur = self.s["kb_layouts"]
        opts = list(KB_COMMON)
        known = [v for v, _l in opts]
        for l in cur:
            if l not in known:
                opts.append((l, l))
        model = Gtk.StringList()
        for _v, lab in opts:
            model.append(lab)
        row1 = Adw.ComboRow(title="Tastaturlayout", model=model)
        vals = [v for v, _l in opts]
        row1.set_selected(vals.index(cur[0]) if cur else 0)
        opts2 = [("", "Keins")] + KB_COMMON[1:]
        model2 = Gtk.StringList()
        for _v, lab in opts2:
            model2.append(lab)
        row2 = Adw.ComboRow(title="Zweites Layout", model=model2)
        vals2 = [v for v, _l in opts2]
        row2.set_selected(vals2.index(cur[1]) if len(cur) > 1 and cur[1] in vals2 else 0)
        var = Adw.EntryRow(title="Variante (z. B. nodeadkeys)", text=(self.s["kb_variants"] or [""])[0])

        def kb_changed(*_a):
            first = vals[row1.get_selected()]
            second = vals2[row2.get_selected()]
            row2.set_sensitive(bool(first))
            var.set_sensitive(bool(first))
            if not first:
                self.set("kb_layouts", [])
                self.set("kb_variants", [])
                return
            layouts = [first] + ([second] if second and second != first else [])
            variants = [var.get_text().strip()] + ([""] if len(layouts) > 1 else [])
            self.set("kb_layouts", layouts)
            self.set("kb_variants", variants)
        row1.connect("notify::selected", kb_changed)
        row2.connect("notify::selected", kb_changed)
        var.connect("apply", kb_changed)
        var.set_show_apply_button(True)
        row2.set_sensitive(bool(cur))
        var.set_sensitive(bool(cur))
        g.add(row1)
        g.add(row2)
        g.add(var)
        self.switch(g, "numlock", "Ziffernblock beim Start aktiv")
        page.add(g)

        g = Adw.PreferencesGroup(title="Maus und Touchpad")
        self.spin(g, "mouse_sensitivity", "Zeigergeschwindigkeit", -1.0, 1.0, 0.1, "0 = Standard", digits=1)
        self.switch(g, "mouse_natural_scroll", "Natürliches Scrollen (Maus)")
        self.switch(g, "touchpad_natural_scroll", "Natürliches Scrollen (Touchpad)")
        self.switch(g, "tap_to_click", "Antippen zum Klicken (Touchpad)")
        page.add(g)
        return page

    def page_displays(self):
        page = Adw.PreferencesPage(title="Bildschirme", icon_name="video-display-symbolic")
        mons = A.monitors()
        if not mons:
            g = Adw.PreferencesGroup(title="Bildschirme",
                                     description="Nur in einer laufenden Hyprland-Sitzung verfügbar.")
            page.add(g)
            return page
        for m in mons:
            name = m.get("name", "?")
            g = Adw.PreferencesGroup(title=f"{name}", description=m.get("description", ""))
            modes = ["preferred"] + [x.replace("Hz", "") for x in m.get("availableModes", [])]
            labels = ["Bevorzugt (automatisch)"] + [x.replace("@", " @ ").replace("Hz", "") + " Hz"
                                                   for x in m.get("availableModes", [])]
            cur = self.s["monitors"].get(name, {})
            mrow = Adw.ComboRow(title="Auflösung", model=Gtk.StringList.new(labels))
            mrow.set_selected(modes.index(cur.get("mode")) if cur.get("mode") in modes else 0)
            srow = Adw.ComboRow(title="Skalierung", model=Gtk.StringList.new(
                ["Automatisch"] + [f"{float(x) * 100:.0f} %" for x in SCALES[1:]]))
            srow.set_selected(SCALES.index(str(cur.get("scale"))) if str(cur.get("scale")) in SCALES else 0)

            def changed(*_a, name=name, mrow=mrow, srow=srow, modes=modes):
                old = copy.deepcopy(self.s["monitors"])
                new = copy.deepcopy(old)
                new[name] = {"mode": modes[mrow.get_selected()], "scale": SCALES[srow.get_selected()]}
                if new[name] == {"mode": "preferred", "scale": "auto"}:
                    new.pop(name)
                self.set("monitors", new, delay=50)
                self._confirm_display(old)
            mrow.connect("notify::selected", changed)
            srow.connect("notify::selected", changed)
            g.add(mrow)
            g.add(srow)
            page.add(g)
        return page

    def _confirm_display(self, old):
        dlg = Adw.AlertDialog(heading="Bildschirmeinstellungen beibehalten?",
                              body="Ohne Bestätigung wird in 15 Sekunden zurückgesetzt.")
        dlg.add_response("revert", "Zurücksetzen")
        dlg.add_response("keep", "Beibehalten")
        dlg.set_response_appearance("keep", Adw.ResponseAppearance.SUGGESTED)
        dlg.set_default_response("keep")
        state = {"done": False}

        def finish(resp):
            if state["done"]:
                return
            state["done"] = True
            if resp != "keep":
                self.set("monitors", old, delay=50)
                self.toast("Bildschirmeinstellungen zurückgesetzt")

        dlg.connect("response", lambda _d, r: finish(r))

        def timeout():
            if not state["done"]:
                dlg.close()
                finish("revert")
            return False
        GLib.timeout_add_seconds(15, timeout)
        dlg.present(self)

    def page_power(self):
        page = Adw.PreferencesPage(title="Energie", icon_name="battery-good-symbolic")
        g = Adw.PreferencesGroup(title="Bei Inaktivität", description="Minuten, 0 = nie")
        self.spin(g, "idle_dim", "Bildschirm abdunkeln nach", 0, 120)
        self.spin(g, "idle_lock", "Bildschirm sperren nach", 0, 240)
        self.spin(g, "idle_screen_off", "Bildschirm ausschalten nach", 0, 240)
        self.spin(g, "idle_suspend", "Bereitschaft nach", 0, 480)
        page.add(g)
        return page

    def page_apps(self):
        page = Adw.PreferencesPage(title="Programme", icon_name="applications-system-symbolic")
        g = Adw.PreferencesGroup(title="Standardprogramme für die Tastenkürzel")
        for key, title in (("terminal", "Terminal (SUPER+Eingabe)"), ("file_manager", "Dateimanager (SUPER+E)"),
                           ("browser", "Browser (SUPER+B)")):
            row = Adw.EntryRow(title=title, text=self.s[key], show_apply_button=True)
            row.connect("apply", lambda r, k=key: self.set(k, r.get_text().strip() or S.DEFAULTS[k]))
            g.add(row)
        page.add(g)

        g = Adw.PreferencesGroup(title="Zurücksetzen")
        row = Adw.ActionRow(title="Alle Einstellungen auf Standard zurücksetzen")
        b = Gtk.Button(label="Zurücksetzen", valign=Gtk.Align.CENTER)
        b.add_css_class("destructive-action")
        b.connect("clicked", self._reset)
        row.add_suffix(b)
        g.add(row)
        page.add(g)
        return page

    def _reset(self, _b):
        try:
            os.remove(S.SETTINGS_FILE)
        except OSError:
            pass
        self.s = S.load()
        self._apply_now()
        self.toast("Standard wiederhergestellt – Fenster wird neu geöffnet")
        app = self.get_application()
        GLib.timeout_add(600, lambda: (self.destroy(), app.activate()) and False)


class App(Adw.Application):
    def __init__(self):
        super().__init__(application_id=APP_ID, flags=Gio.ApplicationFlags.DEFAULT_FLAGS)

    def do_activate(self):
        win = self.get_active_window()
        if not win:
            win = Settings(self)
        win.present()


def next_theme():
    s = S.load()
    ids = list(S.themes())
    if not ids:
        return
    i = ids.index(s["theme"]) if s["theme"] in ids else -1
    s["theme"] = ids[(i + 1) % len(ids)]
    S.save(s)
    A.apply(reload=True)
    t = S.theme(s)
    GLib.spawn_command_line_async(f"notify-send -a hypr-el -t 2500 'Theme' '{t['name']}'")


def main(argv):
    if len(argv) > 1 and argv[1] == "--next-theme":
        next_theme()
        return 0
    return App().run(argv[:1])
