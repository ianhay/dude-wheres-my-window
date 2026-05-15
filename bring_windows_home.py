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

def contains_main_canvas(widget, main_canvas):
    """True only if widget contains the specific main QGIS map canvas."""
    if widget is main_canvas:
        return True
    return main_canvas in widget.findChildren(QgsMapCanvas)

def collect_floating_windows(main_win, main_canvas):
    floating = []
    for widget in QApplication.topLevelWidgets():
        if widget is main_win:
            continue
        if not widget.isVisible():
            continue
        if isinstance(widget, QDockWidget) and not widget.isFloating():
            continue
        if contains_main_canvas(widget, main_canvas):
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
    main_win    = iface.mainWindow()
    main_canvas = iface.mapCanvas()   # the one true QGIS canvas
    screen      = get_target_screen(main_win)
    available   = screen.availableGeometry()
    windows     = collect_floating_windows(main_win, main_canvas)

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

bring_windows_home(iface)