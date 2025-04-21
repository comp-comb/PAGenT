import tkinter as tk
from tkinter import filedialog, scrolledtext
import os

# Import the processing functions
from pipeline import main  # assumes your XML/CSV processing code is in processing.py

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cluster Mask and Noise Generator")
        self.geometry("700x600")

        # store widgets for theming
        self.widgets = []
        self.current_theme = 'Light'

        self._build_ui()
        self.apply_theme()

    def _build_ui(self):
        pad = {'padx': 5, 'pady': 5}
        # Working Directory
        lbl_root = tk.Label(self, text="Working Directory:")
        lbl_root.grid(row=0, column=0, sticky="e", **pad)
        self.widgets.append(lbl_root)
        self.rootEntry = tk.Entry(self, width=50)
        self.rootEntry.insert(0, os.getcwd())
        self.rootEntry.grid(row=0, column=1, **pad)
        self.widgets.append(self.rootEntry)
        btn_root = tk.Button(self, text="Browse...", command=self.browse_root)
        btn_root.grid(row=0, column=2, **pad)
        self.widgets.append(btn_root)

        # XML Folder
        lbl_xml = tk.Label(self, text="XML Folder:")
        lbl_xml.grid(row=1, column=0, sticky="e", **pad)
        self.widgets.append(lbl_xml)
        self.xmlEntry = tk.Entry(self, width=50)
        self.xmlEntry.grid(row=1, column=1, **pad)
        self.widgets.append(self.xmlEntry)
        btn_xml = tk.Button(self, text="Browse...", command=self.browse_xml)
        btn_xml.grid(row=1, column=2, **pad)
        self.widgets.append(btn_xml)

        # File prefix/suffix
        lbl_begin = tk.Label(self, text="File begins with:")
        lbl_begin.grid(row=2, column=0, sticky="e", **pad)
        self.widgets.append(lbl_begin)
        self.beginEntry = tk.Entry(self)
        self.beginEntry.insert(0, "geometry")
        self.beginEntry.grid(row=2, column=1, sticky="w", **pad)
        self.widgets.append(self.beginEntry)

        lbl_end = tk.Label(self, text="File ends with:")
        lbl_end.grid(row=3, column=0, sticky="e", **pad)
        self.widgets.append(lbl_end)
        self.endEntry = tk.Entry(self)
        self.endEntry.insert(0, ".xml")
        self.endEntry.grid(row=3, column=1, sticky="w", **pad)
        self.widgets.append(self.endEntry)

        # Noise type
        lbl_noise = tk.Label(self, text="Noise Type:")
        lbl_noise.grid(row=4, column=0, sticky="e", **pad)
        self.widgets.append(lbl_noise)
        self.noiseVar = tk.StringVar(value="Gaussian (1)")
        noiseOptions = ["Gaussian (1)", "Poisson (2)", "Combined (3)"]
        self.noiseMenu = tk.OptionMenu(self, self.noiseVar, *noiseOptions)
        self.noiseMenu.grid(row=4, column=1, sticky="w", **pad)
        self.widgets.append(self.noiseMenu)

        # Mask types
        lbl_mask = tk.Label(self, text="Mask Type:")
        lbl_mask.grid(row=5, column=0, sticky="e", **pad)
        self.widgets.append(lbl_mask)
        self.particleVar = tk.BooleanVar(value=True)
        chk_part = tk.Checkbutton(self, text="Particle Mask", variable=self.particleVar)
        chk_part.grid(row=5, column=1, sticky="w", **pad)
        self.widgets.append(chk_part)
        self.clusterVar = tk.BooleanVar(value=True)
        chk_clust = tk.Checkbutton(self, text="Cluster Mask", variable=self.clusterVar)
        chk_clust.grid(row=5, column=2, sticky="w", **pad)
        self.widgets.append(chk_clust)

        # Theme selector
        lbl_theme = tk.Label(self, text="Theme:")
        lbl_theme.grid(row=6, column=0, sticky="e", **pad)
        self.widgets.append(lbl_theme)
        self.themeVar = tk.StringVar(value="Light")
        self.themeMenu = tk.OptionMenu(self, self.themeVar, "Light", "Dark", command=self.change_theme)
        self.themeMenu.grid(row=6, column=1, sticky="w", **pad)
        self.widgets.append(self.themeMenu)

        # Run button
        btn_run = tk.Button(self, text="Run", command=self.run_processing)
        btn_run.grid(row=7, column=1, **pad)
        self.widgets.append(btn_run)

        # Log output
        self.logText = scrolledtext.ScrolledText(self, width=80, height=15, state='disabled')
        self.logText.grid(row=8, column=0, columnspan=3, padx=5, pady=5)
        self.widgets.append(self.logText)

    def browse_root(self):
        d = filedialog.askdirectory(initialdir=os.getcwd(), title="Select Root Directory")
        if d:
            self.rootEntry.delete(0, tk.END)
            self.rootEntry.insert(0, d)

    def browse_xml(self):
        d = filedialog.askdirectory(initialdir=os.getcwd(), title="Select XML Directory")
        if d:
            self.xmlEntry.delete(0, tk.END)
            self.xmlEntry.insert(0, d)

    def change_theme(self, *_):
        self.current_theme = self.themeVar.get()
        self.apply_theme()

    def apply_theme(self):
        if self.current_theme == 'Dark':
            bg = '#353535'
            fg = 'white'
        else:
            bg = 'white'
            fg = 'black'
        self.configure(bg=bg)
        for w in self.widgets:
            try:
                w.configure(bg=bg, fg=fg)
            except:
                try:
                    w.configure(bg=bg)
                except:
                    pass

    def log(self, msg):
        self.logText.configure(state='normal')
        self.logText.insert(tk.END, msg + "\n")
        self.logText.see(tk.END)
        self.logText.configure(state='disabled')

    def run_processing(self):
        ROOT = self.rootEntry.get()
        xml_dir = self.xmlEntry.get()
        file_begins_with = self.beginEntry.get()
        file_ends_with = self.endEntry.get()
        noise_map = {"Gaussian (1)": 1, "Poisson (2)": 2, "Combined (3)": 3}
        noisetype = noise_map.get(self.noiseVar.get(), 1)
        mask_list = []
        if self.particleVar.get(): mask_list.append('particle')
        if self.clusterVar.get(): mask_list.append('cluster')
        mask_type = 'both' if len(mask_list) == 2 else (mask_list[0] if mask_list else '')
        output_csv = os.path.join(ROOT, 'data.csv')
        mask_dir = os.path.join(ROOT, 'masks')
        image_dir = os.path.join(ROOT, 'images')
        noisyoutput_dir = os.path.join(ROOT, 'noisyoutput')

        self.log("Starting processing...")
        try:
            main(xml_dir, file_begins_with, file_ends_with,
                 output_csv, mask_dir, image_dir, noisyoutput_dir,
                 noisetype, mask_type)
            self.log("Processing completed successfully.")
        except Exception as e:
            self.log(f"Error: {e}")

if __name__ == '__main__':
    app = App()
    app.mainloop()
