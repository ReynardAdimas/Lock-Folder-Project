APP_STYLE = """
    /* --- Main Container --- */
    QWidget#CentralWidget {
        background-color: #F3F4F6; /* Background Abu-abu terang */
    }
    
    /* --- Card Container --- */
    QFrame#Card {
        background-color: white;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
    }
    
    /* --- Typography --- */
    QLabel#IconHeader {
        font-size: 40px;
        margin-bottom: 10px;
        color: #4F46E5;
    }

    QLabel#Title {
        font-size: 24px;
        font-weight: bold;
        color: #111827; /* Hitam pekat */
        font-family: 'Segoe UI', sans-serif;
    }
    
    QLabel#Subtitle {
        font-size: 14px;
        color: #6B7280; /* Abu-abu */
    }
    
    QLabel {
        font-size: 13px;
        font-weight: 500;
        color: #374151; /* Warna teks label default (Dark Grey) */
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* --- Input Fields (PERBAIKAN DISINI) --- */
    QLineEdit {
        border: 1px solid #D1D5DB;
        border-radius: 6px;
        padding: 10px 12px;
        font-size: 14px;
        background-color: white;
        color: #111827;  /* <--- INI SOLUSINYA (Memaksa text jadi hitam) */
        selection-background-color: #4F46E5;
        selection-color: white;
    }
    
    QLineEdit:focus {
        border: 1px solid #4F46E5;
        outline: none;
    }
    
    /* --- Buttons --- */
    QPushButton#PrimaryButton {
        background-color: #4F46E5;
        color: white;
        border-radius: 6px;
        padding: 12px;
        font-weight: bold;
        font-size: 14px;
        border: none;
    }
    
    QPushButton#PrimaryButton:hover {
        background-color: #4338CA;
    }
    
    QPushButton#PrimaryButton:pressed {
        background-color: #3730A3;
    }

    QPushButton#LinkButton {
        background-color: transparent;
        color: #4F46E5;
        border: none;
        font-weight: 500;
    }
    QPushButton#LinkButton:hover {
        text-decoration: underline;
    }

    /* --- Info Box --- */
    QLabel#InfoNote {
        font-size: 12px;
        color: #6B7280;
        background-color: #F9FAFB;
        padding: 10px;
        border-radius: 6px;
        border: 1px solid #F3F4F6;
    }

    QLabel#Footer {
        font-size: 12px;
        color: #9CA3AF;
    }

    /* --- List Widget (Dashboard) --- */
    QListWidget {
        background-color: transparent;
        border: none;
        outline: none;
    }
    
    QListWidget::item {
        background-color: white;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        margin-bottom: 10px;
        padding: 5px;
    }
    
    QListWidget::item:selected {
        border: 1px solid #4F46E5;
        background-color: #EEF2FF;
    }
    
    /* Styling Custom Widget di dalam List */
    QLabel#FolderName {
        font-size: 14px;
        font-weight: bold;
        color: #111827;
    }
    QLabel#FolderDate {
        font-size: 12px;
        color: #6B7280;
    }
    
    /* --- Outline Button (Unlock) --- */
    QPushButton#OutlineButton {
        background-color: white;
        color: #374151;
        border: 1px solid #D1D5DB;
        border-radius: 6px;
        padding: 12px;
        font-weight: 600;
        font-size: 14px;
    }
    QPushButton#OutlineButton:hover {
        background-color: #F9FAFB;
        border: 1px solid #9CA3AF;
    }
"""