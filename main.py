import os
import sys
from pathlib import Path
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QScreen

# Get absolute path to the project directory
PROJECT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
print(f"Project directory: {PROJECT_DIR}")

# Ensure appdata directory exists with absolute path
APPDATA_DIR = PROJECT_DIR / "appdata"
APPDATA_DIR.mkdir(exist_ok=True)
print(f"Appdata directory: {APPDATA_DIR}")

class MainWindow(QMainWindow):
    """Main window for the application"""
    
    def __init__(self):
        super().__init__()
        
        # Set window properties
        self.setWindowTitle("IPFS Explorer Demo")
        self.setFixedSize(1280, 720)
        
        # Center the window
        self._center_window()
        
        # Create the web view
        self.web_view = QWebEngineView()
        self.setCentralWidget(self.web_view)
        
        # Enable JavaScript and local storage
        settings = self.web_view.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        
        # Additional settings needed for IPFS to work properly
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowWindowActivationFromJavaScript, True)
        
        # Allow file access from file URLs
        self.web_view.page().settings().setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        self.web_view.page().settings().setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        
        # Disable CORS for testing purposes
        self.web_view.page().profile().setHttpUserAgent("Mozilla/5.0 DEMO-IPFS-Client")
        self.web_view.page().profile().setHttpAcceptLanguage("en-US,en;q=0.9")
        
        # Load the index.html page with absolute path
        index_file = APPDATA_DIR / "index.html"
        index_url = QUrl.fromLocalFile(str(index_file.absolute()))
        print(f"Loading URL: {index_url.toString()}")
        self.web_view.load(index_url)
    
    def _center_window(self):
        """Center the window on the screen"""
        center_point = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        frame_geometry = self.frameGeometry()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
