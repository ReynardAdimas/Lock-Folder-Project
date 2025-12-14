import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QStackedWidget, 
                             QFrame, QMessageBox, QHBoxLayout, QSpacerItem, 
                             QSizePolicy, QListWidget, QListWidgetItem, QFileDialog, QDialog)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QAction, QPixmap, QPainter, QFont, QColor
from database import DatabaseManager
from core import SystemLogic
from styles import APP_STYLE

class PasswordInput(QLineEdit):
    """
    Custom QLineEdit dengan tombol 'Mata' menggunakan font ikon bawaan Windows
    (Segoe MDL2 Assets) agar terlihat standar dan rapi.
    """
    def __init__(self, placeholder=""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setEchoMode(QLineEdit.EchoMode.Password)
        self.icon_show = self.get_icon_from_font("\uE890")
        self.icon_hide = self.get_icon_from_font("\uED1A")
        self.toggle_action = self.addAction(self.icon_show, QLineEdit.ActionPosition.TrailingPosition)
        self.toggle_action.triggered.connect(self.toggle_visibility)
        self.password_shown = False

    def toggle_visibility(self):
        if not self.password_shown:
   
            self.setEchoMode(QLineEdit.EchoMode.Normal)
  
            self.toggle_action.setIcon(self.icon_hide) 
            self.password_shown = True
        else:

            self.setEchoMode(QLineEdit.EchoMode.Password)

            self.toggle_action.setIcon(self.icon_show) 
            self.password_shown = False

    def get_icon_from_font(self, char_code):
        """Helper untuk merender karakter font menjadi QIcon"""
        pixmap = QPixmap(32, 32) 
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
 
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        
        font = QFont("Segoe MDL2 Assets", 14)
        painter.setFont(font)
        painter.setPen(QColor("#6B7280")) 
        

        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, char_code)
        painter.end()
        return QIcon(pixmap)



class BasePage(QWidget):
    """Template dasar agar setiap halaman punya layout Card ditengah"""
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        self.card_frame = QFrame()
        self.card_frame.setObjectName("Card")
        self.card_frame.setFixedWidth(420)
        
        self.card_layout = QVBoxLayout(self.card_frame)
        self.card_layout.setContentsMargins(40, 40, 40, 40)
        self.card_layout.setSpacing(20)
        
        self.main_layout.addWidget(self.card_frame, 0, Qt.AlignmentFlag.AlignCenter)
        

        self.main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))


        version_label = QLabel("v1.0.4 © 2025 Kelompok 10")
        version_label.setObjectName("Footer")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(version_label)
        self.main_layout.addSpacing(20)

class SetPasswordPage(BasePage):
    def __init__(self, navigator, db):
        super().__init__()
        self.navigator = navigator
        self.db = db
        
        icon_label = QLabel("🔐") 
        icon_label.setObjectName("IconHeader")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Set Master Password")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("Create a secure password to protect your files.")
        subtitle.setObjectName("Subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)

        lbl_pwd = QLabel("Password")
        self.input_pwd = PasswordInput("Enter new password")
        
        lbl_confirm = QLabel("Confirm Password")

        self.input_confirm = PasswordInput("Re-enter password")
        
        btn_set = QPushButton("Set Password")
        btn_set.setObjectName("PrimaryButton")
        btn_set.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_set.clicked.connect(self.handle_set_password)
        
        info_note = QLabel("Make sure your password is memorable. If you forget this password, your locked folders cannot be recovered.")
        info_note.setObjectName("InfoNote")
        info_note.setWordWrap(True)

        self.card_layout.addWidget(icon_label)
        self.card_layout.addWidget(title)
        self.card_layout.addWidget(subtitle)
        self.card_layout.addSpacing(10)
        self.card_layout.addWidget(lbl_pwd)
        self.card_layout.addWidget(self.input_pwd)
        self.card_layout.addWidget(lbl_confirm)
        self.card_layout.addWidget(self.input_confirm)
        self.card_layout.addWidget(btn_set)
        self.card_layout.addSpacing(10)
        self.card_layout.addWidget(info_note)

    def handle_set_password(self):
        pwd = self.input_pwd.text()
        confirm = self.input_confirm.text()
        
        if not pwd or not confirm:
            QMessageBox.warning(self, "Error", "Password cannot be empty!")
            return
        if pwd != confirm:
            QMessageBox.warning(self, "Error", "Passwords do not match!")
            return
            
        hashed = SystemLogic.hash_password(pwd)
        self.db.set_master_password(hashed.decode('utf-8'))
        
        QMessageBox.information(self, "Success", "Password set successfully!")
        self.navigator.setCurrentIndex(1) 

class LoginPage(BasePage):
    def __init__(self, navigator, db):
        super().__init__()
        self.navigator = navigator
        self.db = db
        
        icon_label = QLabel("🔒")
        icon_label.setObjectName("IconHeader")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Secure Vault")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("Enter your password to access files")
        subtitle.setObjectName("Subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        lbl_pwd = QLabel("Password")
        self.input_pwd = PasswordInput("Enter password")
        
        btn_login = QPushButton("Login")
        btn_login.setObjectName("PrimaryButton")
        btn_login.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_login.clicked.connect(self.handle_login)
        
        self.card_layout.addWidget(icon_label)
        self.card_layout.addWidget(title)
        self.card_layout.addWidget(subtitle)
        self.card_layout.addSpacing(10)
        self.card_layout.addWidget(lbl_pwd)
        self.card_layout.addWidget(self.input_pwd)
        self.card_layout.addWidget(btn_login)

    def handle_login(self):
        pwd = self.input_pwd.text()
        stored_hash = self.db.get_master_password()
        
        if SystemLogic.check_password(pwd, stored_hash):
            self.navigator.setCurrentIndex(2) 
            self.navigator.currentWidget().refresh_list()
        else:
            QMessageBox.critical(self, "Error", "Invalid Password!")



class FolderItemWidget(QWidget):
    """Widget custom untuk tampilan baris folder"""
    def __init__(self, name, date):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        icon_lbl = QLabel("📁") 
        icon_lbl.setStyleSheet("font-size: 24px; color: #F59E0B;") 
        
        info_layout = QVBoxLayout()
        name_lbl = QLabel(name)
        name_lbl.setObjectName("FolderName")
        date_lbl = QLabel(f"Locked on {date}")
        date_lbl.setObjectName("FolderDate")
        info_layout.addWidget(name_lbl)
        info_layout.addWidget(date_lbl)
        
        arrow_lbl = QLabel("›")
        arrow_lbl.setStyleSheet("font-size: 20px; color: #9CA3AF; font-weight: bold;")
        
        layout.addWidget(icon_lbl)
        layout.addSpacing(10)
        layout.addLayout(info_layout)
        layout.addStretch()
        layout.addWidget(arrow_lbl)

class LockDialog(QDialog):
    """Dialog Halaman 4: Lock"""
    def __init__(self, parent, folder_path):
        super().__init__(parent)
        self.folder_path = folder_path
        self.setWindowTitle("Lock Folder")
        self.setFixedSize(400, 480)
        self.setStyleSheet(APP_STYLE)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        header = QLabel("🔒 Lock Folder")
        header.setObjectName("Title")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        path_frame = QFrame()
        path_frame.setStyleSheet("background-color: #F3F4F6; border-radius: 8px; padding: 10px;")
        path_layout = QVBoxLayout(path_frame)
        
        lbl_path_title = QLabel("Selected Folder:")
        lbl_path_title.setStyleSheet("font-size: 11px; color: #6B7280;")
        lbl_path_val = QLabel(os.path.basename(folder_path))
        lbl_path_val.setStyleSheet("font-weight: bold; color: #4F46E5;")
        lbl_full_path = QLabel(folder_path)
        lbl_full_path.setStyleSheet("font-size: 10px; color: gray;")
        lbl_full_path.setWordWrap(True)

        path_layout.addWidget(lbl_path_title)
        path_layout.addWidget(lbl_path_val)
        path_layout.addWidget(lbl_full_path)
        layout.addWidget(path_frame)
        
        self.input_pwd = PasswordInput("Create folder password")
        
        self.input_confirm = PasswordInput("Confirm folder password")
        
        layout.addWidget(QLabel("Password"))
        layout.addWidget(self.input_pwd)
        layout.addWidget(QLabel("Confirm Password"))
        layout.addWidget(self.input_confirm)
        
        btn_lock = QPushButton("🔒 Kunci (Lock)")
        btn_lock.setObjectName("PrimaryButton")
        btn_lock.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_lock.clicked.connect(self.accept_lock)
        layout.addWidget(btn_lock)

    def accept_lock(self):
        p1 = self.input_pwd.text()
        p2 = self.input_confirm.text()
        if not p1 or not p2:
            QMessageBox.warning(self, "Error", "Password cannot be empty")
            return
        if p1 != p2:
            QMessageBox.warning(self, "Error", "Passwords do not match")
            return
        self.password = p1
        self.accept()

class UnlockDialog(QDialog):
    """Dialog Halaman 5: Unlock (New)"""
    def __init__(self, parent, folder_path):
        super().__init__(parent)
        self.folder_path = folder_path
        self.setWindowTitle("Unlock Folder")
        self.setFixedSize(400, 400)
        self.setStyleSheet(APP_STYLE)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        header = QLabel("🔓 Unlock Folder")
        header.setObjectName("Title")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        subtitle = QLabel("Enter password to unlock contents.")
        subtitle.setObjectName("Subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        path_lbl = QLabel(f"📁 {os.path.basename(folder_path)}")
        path_lbl.setStyleSheet("background-color: #F3F4F6; padding: 10px; border-radius: 8px; color: #4F46E5; font-weight: bold;")
        path_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(path_lbl)
        
        self.input_pwd = PasswordInput("Enter folder password")
        
        layout.addWidget(QLabel("Password"))
        layout.addWidget(self.input_pwd)
        
        btn_unlock = QPushButton("🔓 Buka (Unlock)")
        btn_unlock.setObjectName("PrimaryButton")
        btn_unlock.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_unlock.clicked.connect(self.accept_unlock)
        layout.addWidget(btn_unlock)

    def accept_unlock(self):
        pwd = self.input_pwd.text()
        if not pwd:
            QMessageBox.warning(self, "Error", "Password cannot be empty")
            return
        self.password = pwd
        self.accept()

class DashboardPage(QWidget):
    def __init__(self, navigator, db):
        super().__init__()
        self.navigator = navigator
        self.db = db
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(40, 40, 40, 40)
        self.layout.setSpacing(20)
        
        header_layout = QHBoxLayout()
        title = QLabel("🔒 Locked Folders")
        title.setObjectName("Title")
        
        self.badge = QLabel("0 items")
        self.badge.setStyleSheet("background-color: #E5E7EB; color: #374151; padding: 4px 8px; border-radius: 10px; font-size: 12px;")
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.badge)
        
        self.list_widget = QListWidget()
        
        btn_add = QPushButton("+ Add Folder to Lock")
        btn_add.setObjectName("PrimaryButton")
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.clicked.connect(self.add_folder_flow)
        
        btn_unlock = QPushButton("🔓 Unlock Selected Folder")
        btn_unlock.setObjectName("OutlineButton")
        btn_unlock.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_unlock.clicked.connect(self.unlock_folder_flow)
        
        self.layout.addLayout(header_layout)
        self.layout.addWidget(self.list_widget)
        self.layout.addWidget(btn_add)
        self.layout.addWidget(btn_unlock)

    def refresh_list(self):
        self.list_widget.clear()
        folders = self.db.get_all_folders() 
        self.badge.setText(f"{len(folders)} items")
        for f_id, f_path, f_name, f_date in folders:
            item = QListWidgetItem(self.list_widget)
            item.setSizeHint(QSize(0, 80)) 
            item.setData(Qt.ItemDataRole.UserRole, f_id) 
            item.setData(Qt.ItemDataRole.UserRole + 1, f_path)
            row_widget = FolderItemWidget(f_name, f_date)
            self.list_widget.setItemWidget(item, row_widget)

    def add_folder_flow(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder to Lock")
        if folder_path:
            dialog = LockDialog(self, folder_path)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                pwd = dialog.password
                if SystemLogic.lock_folder(folder_path):
                    hashed = SystemLogic.hash_password(pwd)
                    folder_name = os.path.basename(folder_path)
                    self.db.insert_folder(folder_path, folder_name, hashed.decode('utf-8'))
                    self.refresh_list()
                    QMessageBox.information(self, "Success", "Folder has been locked and hidden!")
                else:
                    QMessageBox.critical(self, "Error", "Failed to lock folder. Run as Admin!")

    def unlock_folder_flow(self):
        current_item = self.list_widget.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Warning", "Please select a folder to unlock first.")
            return

        folder_path = current_item.data(Qt.ItemDataRole.UserRole + 1)
        folder_id = current_item.data(Qt.ItemDataRole.UserRole)
        
        dialog = UnlockDialog(self, folder_path)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            input_pwd = dialog.password
            
            stored_hash = self.db.get_folder_password(folder_id)
            
            if stored_hash and SystemLogic.check_password(input_pwd, stored_hash):
                if SystemLogic.unlock_folder(folder_path):
                    self.db.delete_folder(folder_id)
                    self.refresh_list()
                    QMessageBox.information(self, "Success", "Folder Unlocked successfully!")
                else:
                    QMessageBox.critical(self, "Error", "Failed to unlock system permissions.")
            else:
                QMessageBox.critical(self, "Error", "Incorrect Password for this folder!")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Locker Pro")
        self.resize(1000, 750)
        
        self.db = DatabaseManager()
        
        self.central_widget = QWidget()
        self.central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0,0,0,0)
        
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)
        
        self.page_set_password = SetPasswordPage(self.stack, self.db)
        self.page_login = LoginPage(self.stack, self.db)
        self.page_dashboard = DashboardPage(self.stack, self.db)
        
        self.stack.addWidget(self.page_set_password)
        self.stack.addWidget(self.page_login)
        self.stack.addWidget(self.page_dashboard)
        
        if self.db.is_setup_done():
            self.stack.setCurrentIndex(1)
        else:
            self.stack.setCurrentIndex(0)

        self.setStyleSheet(APP_STYLE)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())