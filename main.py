import sys
from pathlib import Path

from PyQt5 import QtWidgets as qt
from PyQt5.QtCore import QAbstractNativeEventFilter, QAbstractEventDispatcher
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMenu
from pyqtkeybind import keybinder

from note import Note
from repositories.file import FileNotesRepository


class WinEventFilter(QAbstractNativeEventFilter):
    def __init__(self, k):
        self.keybinder = k
        super().__init__()

    def nativeEventFilter(self, eventType, message):
        ret = self.keybinder.handler(eventType, message)
        return ret, 0


class QuickAddWindow(qt.QMainWindow):

    def __init__(self, repository):
        super(QuickAddWindow, self).__init__()
        self.repository = repository
        self.setWindowTitle("Quick Note")

        self.summary_edit = qt.QLineEdit()
        self.summary_edit.setPlaceholderText("Summary...")
        self.note_edit = qt.QTextEdit()
        self.note_edit.setPlaceholderText("Description...")

        button_box = qt.QDialogButtonBox(qt.QDialogButtonBox.Ok | qt.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        button_box.button(qt.QDialogButtonBox.Ok).setShortcut("Ctrl+Return")

        main_layout = qt.QVBoxLayout()
        main_layout.addWidget(self.summary_edit)
        main_layout.addWidget(self.note_edit)
        main_layout.addWidget(button_box)

        widget = qt.QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def accept(self):
        note = Note(
            summary=self.summary_edit.text(),
            description=self.note_edit.toPlainText()
        )

        self.repository.save(note)
        self.hide()

    def reject(self):
        self.hide()

    def show(self) -> None:
        self.summary_edit.clear()
        self.note_edit.clear()
        self.summary_edit.setFocus()
        super().show()

    def toggle_visibility(self):
        if self.isVisible():
            self.reject()
        else:
            self.show()


def set_global_shortcut(window: QuickAddWindow, shortcut: str):
    keybinder.register_hotkey(window.winId(), shortcut, window.toggle_visibility)


def main():
    app = qt.QApplication(sys.argv)
    window = QuickAddWindow(FileNotesRepository(Path("exp/notes.json")))

    keybinder.init()
    set_global_shortcut(window, "Ctrl+T")
    win_event_filter = WinEventFilter(keybinder)
    event_dispatcher = QAbstractEventDispatcher.instance()
    event_dispatcher.installNativeEventFilter(win_event_filter)

    window.show()

    menu = QMenu()
    quit_action = menu.addAction("Quit")
    quit_action.triggered.connect(app.quit)

    icon = QIcon("media/icon.png")
    tray_icon = qt.QSystemTrayIcon(icon, parent=app)
    tray_icon.setToolTip("An amazing quick add for notion")
    tray_icon.show()
    tray_icon.setContextMenu(menu)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
