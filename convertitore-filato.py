import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import csv

# Conversioni
conversioni = ['Tex', 'dTex', 'Den', 'Nm', 'Ne', 'm/kg']

def to_tex(tipo, valore):
    if tipo == 'Tex': return valore
    if tipo == 'dTex': return valore / 10
    if tipo == 'Den': return valore / 9
    if tipo == 'Nm': return 1000 / valore
    if tipo == 'Ne': return 590.5 / valore
    if tipo == 'm/kg': return 1_000_000 / valore

def from_tex(tex):
    return {
        'Tex': tex,
        'dTex': tex * 10,
        'Den': tex * 9,
        'Nm': 1000 / tex,
        'Ne': 590.5 / tex,
        'm/kg': 1_000_000 / tex
    }

class ConvertitoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Convertitore Titoli Filato")

        self.tipo_var = tk.StringVar(value='Nm')
        self.valore_var = tk.DoubleVar(value=30)
        self.capi_var = tk.IntVar(value=4)

        # Frame input
        input_frame = ttk.Frame(root, padding=10)
        input_frame.pack()

        ttk.Label(input_frame, text="Tipo:").grid(row=0, column=0)
        tipo_menu = ttk.Combobox(input_frame, textvariable=self.tipo_var, values=conversioni, state="readonly")
        tipo_menu.grid(row=0, column=1)

        ttk.Label(input_frame, text="Valore:").grid(row=1, column=0)
        ttk.Entry(input_frame, textvariable=self.valore_var).grid(row=1, column=1)

        ttk.Label(input_frame, text="Numero capi:").grid(row=2, column=0)
        ttk.Entry(input_frame, textvariable=self.capi_var).grid(row=2, column=1)

        ttk.Button(input_frame, text="Converti", command=self.converti).grid(row=3, column=0, columnspan=2, pady=5)

        # Frame risultati
        self.risultati_frame = ttk.Frame(root, padding=10)
        self.risultati_frame.pack()

        # Pulsanti export
        export_frame = ttk.Frame(root, padding=10)
        export_frame.pack()
        ttk.Button(export_frame, text="Esporta PDF", command=self.export_pdf).grid(row=0, column=0)
        ttk.Button(export_frame, text="Esporta CSV", command=self.export_csv).grid(row=0, column=1)
        ttk.Button(export_frame, text="Esporta TXT", command=self.export_txt).grid(row=0, column=2)
        ttk.Button(export_frame, text="Esci", command=root.quit).grid(row=0, column=3)

    def converti(self):
        tipo, valore, capi = self.tipo_var.get(), self.valore_var.get(), self.capi_var.get()
        valore_eff = valore / capi if tipo in ['Nm', 'Ne', 'm/kg'] else valore * capi

        tex = to_tex(tipo, valore_eff)
        risultati = from_tex(tex)

        for widget in self.risultati_frame.winfo_children():
            widget.destroy()

        columns = ("Tipo Conversione", "Titolo Finale", "Titolo a più capi")
        tree = ttk.Treeview(self.risultati_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)

        for unit, val in risultati.items():
            if unit in ['Nm', 'Ne', 'm/kg']:
                titolo_capi = f"{val*capi:.2f}/{capi}"
            else:
                titolo_capi = f"{val/capi:.2f}x{capi}"
            tree.insert('', tk.END, values=(unit, f"{val:.2f}", titolo_capi))

        tree.pack()
        self.current_risultati = risultati

    # Export functions remain the same
    def export_pdf(self):
        pass  # Same as original

    def export_csv(self):
        pass  # Same as original

    def export_txt(self):
        pass  # Same as original

if __name__ == "__main__":
    root = tk.Tk()
    app = ConvertitoreApp(root)
    root.mainloop()
