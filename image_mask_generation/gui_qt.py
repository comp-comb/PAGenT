import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit,
    QPushButton, QComboBox, QCheckBox, QTextEdit,
    QVBoxLayout, QHBoxLayout, QFileDialog
)
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import QObject, pyqtSignal, QThread

# Import the pipeline module
import pipeline

class PipelineWorker(QObject):
    output = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, xml_dir, file_begins_with, file_ends_with,
                 output_csv, mask_dir, image_dir, noisyoutput_dir,
                 noisetype, mask_type):
        super().__init__()
        self.xml_dir = xml_dir
        self.file_begins_with = file_begins_with
        self.file_ends_with = file_ends_with
        self.output_csv = output_csv
        self.mask_dir = mask_dir
        self.image_dir = image_dir
        self.noisyoutput_dir = noisyoutput_dir
        self.noisetype = noisetype
        self.mask_type = mask_type

    def run(self):
        # Redirect stdout/stderr
        orig_stdout, orig_stderr = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = self, self

        try:
            pipeline.main(
                self.xml_dir,
                self.file_begins_with,
                self.file_ends_with,
                self.output_csv,
                self.mask_dir,
                self.image_dir,
                self.noisyoutput_dir,
                self.noisetype,
                self.mask_type
            )
        except Exception as e:
            print(f"Error: {e}")
        finally:
            sys.stdout, sys.stderr = orig_stdout, orig_stderr
            self.finished.emit()

    def write(self, text):
        if text and not text.isspace():
            self.output.emit(str(text))

    def flush(self):
        pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cluster Mask and Noise Generator")
        self._thread = None
        self._worker = None
        self.status = self.statusBar()
        self.initUI()

    def initUI(self):
        # Build inputs
        root_label = QLabel("Working Directory:")
        self.rootLineEdit = QLineEdit(os.getcwd())
        root_browse = QPushButton("Browse...")
        root_browse.clicked.connect(self.browse_root)

        xml_label = QLabel("XML Folder:")
        self.xmlLineEdit = QLineEdit()
        xml_browse = QPushButton("Browse...")
        xml_browse.clicked.connect(self.browse_xml)

        begin_label = QLabel("File begins with:")
        self.beginLineEdit = QLineEdit("geometry")
        end_label = QLabel("File ends with:")
        self.endLineEdit = QLineEdit(".xml")

        noise_label = QLabel("Noise Type:")
        self.noiseCombo = QComboBox()
        self.noiseCombo.addItems(["Gaussian (1)", "Poisson (2)", "Combined (3)"])

        mask_label = QLabel("Mask Type:")
        self.particleCheck = QCheckBox("Particle Mask")
        self.clusterCheck = QCheckBox("Cluster Mask")
        self.particleCheck.setChecked(True)
        self.clusterCheck.setChecked(True)

        theme_label = QLabel("Theme:")
        self.themeCombo = QComboBox()
        self.themeCombo.addItems(["Light", "Dark"])
        self.themeCombo.currentTextChanged.connect(self.change_theme)

        self.run_button = QPushButton("Run")
        self.run_button.clicked.connect(self.start_pipeline)
        self.logText = QTextEdit(readOnly=True)

        # Layout
        layout = QVBoxLayout()
        def add_row(*widgets):
            row = QHBoxLayout()
            for w in widgets:
                row.addWidget(w)
            layout.addLayout(row)

        add_row(root_label, self.rootLineEdit, root_browse)
        add_row(xml_label, self.xmlLineEdit, xml_browse)
        add_row(begin_label, self.beginLineEdit, end_label, self.endLineEdit)
        add_row(noise_label, self.noiseCombo)
        add_row(mask_label, self.particleCheck, self.clusterCheck)
        add_row(theme_label, self.themeCombo)
        layout.addWidget(self.run_button)
        layout.addWidget(self.logText)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        QApplication.setStyle('Fusion')
        self.apply_light_theme()

    def browse_root(self):
        d = QFileDialog.getExistingDirectory(self, "Select Root Directory", os.getcwd())
        if d:
            self.rootLineEdit.setText(d)

    def browse_xml(self):
        d = QFileDialog.getExistingDirectory(self, "Select XML Directory", os.getcwd())
        if d and not d.endswith(os.sep):
            d += os.sep
        self.xmlLineEdit.setText(d)

    def change_theme(self, theme):
        if theme == "Dark": self.apply_dark_theme()
        else: self.apply_light_theme()

    def apply_dark_theme(self):
        dark = QPalette()
        dark.setColor(QPalette.Window, QColor(53,53,53)); dark.setColor(QPalette.WindowText, QColor(255,255,255))
        dark.setColor(QPalette.Base, QColor(35,35,35)); dark.setColor(QPalette.AlternateBase, QColor(53,53,53))
        dark.setColor(QPalette.ToolTipBase, QColor(255,255,220)); dark.setColor(QPalette.ToolTipText, QColor(255,255,255))
        dark.setColor(QPalette.Text, QColor(255,255,255)); dark.setColor(QPalette.Button, QColor(53,53,53))
        dark.setColor(QPalette.ButtonText, QColor(255,255,255)); dark.setColor(QPalette.Highlight, QColor(42,130,218))
        dark.setColor(QPalette.HighlightedText, QColor(0,0,0))
        QApplication.setPalette(dark)

    def apply_light_theme(self):
        QApplication.setPalette(QApplication.style().standardPalette())

    def append_log(self, text):
        self.logText.append(text)
        self.status.showMessage(text.strip().splitlines()[-1])

    def start_pipeline(self):
        # disable run
        self.run_button.setEnabled(False)
        self.logText.clear()
        self.status.showMessage("Pipeline started...")

        ROOT = self.rootLineEdit.text()
        xml_dir = self.xmlLineEdit.text() or ''
        if xml_dir and not xml_dir.endswith(os.sep): xml_dir += os.sep
        file_begins_with = self.beginLineEdit.text()
        file_ends_with = self.endLineEdit.text()
        noisetype = self.noiseCombo.currentIndex() + 1
        types = []
        if self.particleCheck.isChecked(): types.append('particle')
        if self.clusterCheck.isChecked(): types.append('cluster')
        mask_type = 'both' if len(types)==2 else (types[0] if types else '')

        output_csv = os.path.join(ROOT, 'data.csv')
        mask_dir = os.path.join(ROOT, 'masks') + os.sep
        image_dir = os.path.join(ROOT, 'images') + os.sep
        noisyoutput_dir = os.path.join(ROOT, 'noisyoutput') + os.sep

        # set globals
        pipeline.mask_dir = mask_dir
        pipeline.image_dir = image_dir
        pipeline.noisyoutput_dir = noisyoutput_dir

        # create worker/thread
        self._worker = PipelineWorker(
            xml_dir, file_begins_with, file_ends_with,
            output_csv, mask_dir, image_dir, noisyoutput_dir,
            noisetype, mask_type
        )
        self._thread = QThread()
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.output.connect(self.append_log)
        self._worker.finished.connect(self.pipeline_finished)
        self._thread.start()

    def pipeline_finished(self):
        self.status.showMessage("Pipeline completed successfully.")
        self.run_button.setEnabled(True)
        # cleanup thread
        self._thread.quit()
        self._thread.wait()
        self._worker = None
        self._thread = None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
