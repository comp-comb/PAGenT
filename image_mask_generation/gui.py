import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit,
    QPushButton, QComboBox, QCheckBox, QTextEdit,
    QVBoxLayout, QHBoxLayout, QFileDialog, QSpinBox, QColorDialog
)
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import QObject, pyqtSignal, QThread

import pipeline

class PipelineWorker(QObject):
    output = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, xml_dir, prefix, suffix,
                 output_csv, mask_dir, image_dir, noisyoutput_dir,
                 mask_type, noise_types, tem_style, tem_mean, tem_std, tem_color):
        super().__init__()
        self.params = {
            'xml_dir': xml_dir,
            'file_begins_with': prefix,
            'file_ends_with': suffix,
            'output_csv': output_csv,
            'mask_dir': mask_dir,
            'image_dir': image_dir,
            'noisyoutput_dir': noisyoutput_dir,
            'mask_type': mask_type,
            'noise_types': noise_types,
            'tem_style': tem_style,
            'tem_mean': tem_mean,
            'tem_std': tem_std,
            'tem_color': tem_color
        }

    def run(self):
        orig_stdout, orig_stderr = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = self, self
        try:
            pipeline.main(**self.params)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            sys.stdout, sys.stderr = orig_stdout, orig_stderr
            self.finished.emit()

    def write(self, text):
        if text.strip():
            self.output.emit(text)

    def flush(self):
        pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cluster Mask & Noise GUI")
        self.status = self.statusBar()
        # default TEM color
        r, g, b, a = [int(0.045 * 255)] * 3 + [int(0.3 * 255)]
        self.tem_color = QColor(r, g, b, a)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Working Directory
        row = QHBoxLayout()
        row.addWidget(QLabel("Working Directory:"))
        self.rootLineEdit = QLineEdit(os.getcwd())
        row.addWidget(self.rootLineEdit)
        btn = QPushButton("Browse...")
        btn.clicked.connect(self.browse_root)
        row.addWidget(btn)
        layout.addLayout(row)

        # XML Folder
        row = QHBoxLayout()
        row.addWidget(QLabel("XML Folder:"))
        default_xml = os.path.join(self.rootLineEdit.text(), 'xmls') + os.sep
        self.xmlLineEdit = QLineEdit(default_xml)
        row.addWidget(self.xmlLineEdit)
        btn = QPushButton("Browse...")
        btn.clicked.connect(self.browse_xml)
        row.addWidget(btn)
        layout.addLayout(row)

        # File prefix/suffix
        row = QHBoxLayout()
        row.addWidget(QLabel("File begins with:"))
        self.beginLineEdit = QLineEdit("geometry")
        row.addWidget(self.beginLineEdit)
        row.addWidget(QLabel("File ends with:"))
        self.endLineEdit = QLineEdit(".xml")
        row.addWidget(self.endLineEdit)
        layout.addLayout(row)

        # Mask Type
        row = QHBoxLayout()
        row.addWidget(QLabel("Mask Type:"))
        self.particleCheck = QCheckBox("Particle")
        self.clusterCheck = QCheckBox("Cluster")
        self.particleCheck.setChecked(True)
        self.clusterCheck.setChecked(True)
        row.addWidget(self.particleCheck)
        row.addWidget(self.clusterCheck)
        layout.addLayout(row)

        # Noise Types
        row = QHBoxLayout()
        row.addWidget(QLabel("Noise Types:"))
        self.gauss_cb = QCheckBox("Gaussian")
        self.gauss_cb.setChecked(True)
        row.addWidget(self.gauss_cb)
        self.poisson_cb = QCheckBox("Poisson")
        row.addWidget(self.poisson_cb)
        self.combined_cb = QCheckBox("Combined")
        row.addWidget(self.combined_cb)
        self.tem_cb = QCheckBox("TEM-like")
        row.addWidget(self.tem_cb)
        layout.addLayout(row)

        # TEM params
        row = QHBoxLayout()
        row.addWidget(QLabel("TEM Mean:"))
        self.temMeanSpin = QSpinBox()
        self.temMeanSpin.setRange(0, 255)
        self.temMeanSpin.setValue(180)
        self.temMeanSpin.setEnabled(False)
        row.addWidget(self.temMeanSpin)
        row.addWidget(QLabel("TEM Std:"))
        self.temStdSpin = QSpinBox()
        self.temStdSpin.setRange(0, 100)
        self.temStdSpin.setValue(25)
        self.temStdSpin.setEnabled(False)
        row.addWidget(self.temStdSpin)
        layout.addLayout(row)
        self.tem_cb.toggled.connect(self.temMeanSpin.setEnabled)
        self.tem_cb.toggled.connect(self.temStdSpin.setEnabled)

        # TEM color
        row = QHBoxLayout()
        row.addWidget(QLabel("TEM Color:"))
        self.temColorBtn = QPushButton(self.tem_color.name(QColor.HexArgb))
        self.temColorBtn.clicked.connect(self.choose_color)
        row.addWidget(self.temColorBtn)
        layout.addLayout(row)

        # Theme selector
        theme_row = QHBoxLayout()
        theme_row.addWidget(QLabel("Theme:"))
        self.themeCombo = QComboBox()
        self.themeCombo.addItems(["Light", "Dark"])
        self.themeCombo.currentTextChanged.connect(self.on_theme_change)
        theme_row.addWidget(self.themeCombo)
        layout.addLayout(theme_row)

        # Run + Log
        self.runButton = QPushButton("Run")
        self.runButton.clicked.connect(self.start)
        layout.addWidget(self.runButton)
        self.logText = QTextEdit(readOnly=True)
        layout.addWidget(self.logText)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        QApplication.setStyle('Fusion')
        self.apply_light_theme()

    def on_theme_change(self, theme):
        if theme == "Dark":
            self.apply_dark_theme()
        else:
            self.apply_light_theme()

    def choose_color(self):
        dlg = QColorDialog(self.tem_color, self)
        dlg.setOption(QColorDialog.ShowAlphaChannel, True)
        if dlg.exec_() == QColorDialog.Accepted:
            c = dlg.selectedColor()
            if c.isValid():
                self.tem_color = c
                self.temColorBtn.setText(c.name(QColor.HexArgb))

    def browse_root(self):
        d = QFileDialog.getExistingDirectory(self, "Select Working Dir", os.getcwd())
        if d:
            self.rootLineEdit.setText(d)
            self.xmlLineEdit.setText(os.path.join(d, 'xmls') + os.sep)

    def browse_xml(self):
        d = QFileDialog.getExistingDirectory(self, "Select XML Dir", os.getcwd())
        if d and not d.endswith(os.sep): d += os.sep
        self.xmlLineEdit.setText(d)

    def start(self):
        self.runButton.setEnabled(False)
        self.logText.clear()
        self.status.showMessage("Pipeline started...")
        ROOT = self.rootLineEdit.text()
        xml = self.xmlLineEdit.text()
        prefix = self.beginLineEdit.text()
        suffix = self.endLineEdit.text()
        outCSV = os.path.join(ROOT, 'data.csv')
        maskDir = os.path.join(ROOT, 'masks') + os.sep
        imgDir = os.path.join(ROOT, 'images') + os.sep
        noisyDir = os.path.join(ROOT, 'noisyoutput') + os.sep
        types = []
        if self.particleCheck.isChecked(): types.append('particle')
        if self.clusterCheck.isChecked(): types.append('cluster')
        maskType = 'both' if len(types) == 2 else (types[0] if types else '')
        noise_types = []
        if self.gauss_cb.isChecked():    noise_types.append('gauss')
        if self.poisson_cb.isChecked():  noise_types.append('poisson')
        if self.combined_cb.isChecked(): noise_types.append('combined')
        if self.tem_cb.isChecked():      noise_types.append('tem')
        temStyle = self.tem_cb.isChecked()
        temMean  = self.temMeanSpin.value()
        temStd   = self.temStdSpin.value()
        c        = self.tem_color
        temColor = (c.red()/255.0, c.green()/255.0,
                    c.blue()/255.0, c.alpha()/255.0)

        self.worker = PipelineWorker(
            xml, prefix, suffix,
            outCSV, maskDir, imgDir, noisyDir,
            maskType, noise_types,
            temStyle, temMean, temStd, temColor
        )
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.output.connect(self.logText.append)
        self.worker.finished.connect(self.on_finished)
        self.thread.start()

    def on_finished(self):
        self.status.showMessage("Pipeline completed successfully.")
        self.runButton.setEnabled(True)
        self.thread.quit()
        self.thread.wait()

    def apply_dark_theme(self):
        p = QPalette()
        p.setColor(QPalette.Window, QColor(53,53,53)); p.setColor(QPalette.WindowText, QColor(255,255,255))
        p.setColor(QPalette.Base, QColor(35,35,35)); p.setColor(QPalette.AlternateBase, QColor(53,53,53))
        p.setColor(QPalette.ToolTipBase, QColor(255,255,220)); p.setColor(QPalette.ToolTipText, QColor(255,255,255))
        p.setColor(QPalette.Text, QColor(255,255,255)); p.setColor(QPalette.Button, QColor(53,53,53))
        p.setColor(QPalette.ButtonText, QColor(255,255,255)); p.setColor(QPalette.Highlight, QColor(42,130,218))
        p.setColor(QPalette.HighlightedText, QColor(0,0,0))
        QApplication.setPalette(p)

    def apply_light_theme(self):
        QApplication.setPalette(QApplication.style().standardPalette())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
