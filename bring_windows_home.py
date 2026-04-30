from qgis.PyQt.QtCore import QPoint, QRect
from qgis.PyQt.QtWidgets import QApplication, QDockWidget, QMainWindow, QMessageBox
from qgis.gui import QgsMapCanvas


CASCADE_OFFSET = QPoint(30, 30)
EDGE_MARGIN    = 20
START_RATIO    = 0.20


def get_target_screen(main_win):
    app    = QApplication.instance()
    screen = app.screenAt(main_win.geometry().center())
    return screen or app.primaryScreen()


def window_contains_map_canvas(win):
    if isinstance(win, QgsMapCanvas):
        return True
    for child in win.findChildren(QgsMapCanvas):
        if child.isVisible():
            return True
    return False


def collect_floating_windows(main_win):
    floating = []
    for widget in QApplication.topLevelWidgets():
        if widget is main_win:
            continue
        if not widget.isVisible():
            continue
        if isinstance(widget, QMainWindow):
            continue
        if isinstance(widget, QDockWidget) and not widget.isFloating():
            continue
        if window_contains_map_canvas(widget):
            continue
        floating.append(widget)
    return floating


def fit_to_screen(x, y, w, h, available: QRect):
    max_w = available.right()  - EDGE_MARGIN - x
    max_h = available.bottom() - EDGE_MARGIN - y
    new_w = min(w, max_w)
    new_h = min(h, max_h)
    return QRect(x, y, new_w, new_h)


def bring_windows_home(iface):
    """iface is passed in explicitly from the plugin — never relies on globals."""
    main_win  = iface.mainWindow()
    screen    = get_target_screen(main_win)
    available = screen.availableGeometry()
    windows   = collect_floating_windows(main_win)

    if not windows:
        QMessageBox.information(
            main_win,
            "Dude, where's my window?",
            "No floating windows found — nothing to do."
        )
        return

    start_x = available.left() + int(available.width()  * START_RATIO)
    start_y = available.top()  + int(available.height() * START_RATIO)

    for i, win in enumerate(windows):
        x = start_x + CASCADE_OFFSET.x() * i
        y = start_y + CASCADE_OFFSET.y() * i
        final = fit_to_screen(x, y, win.width(), win.height(), available)
        win.setGeometry(final)
        win.raise_()
        win.activateWindow()

    print(f"Dude, where's my window? — rounded up {len(windows)} window(s).")
