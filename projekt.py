import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
import statistics
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Funkcje
def dodaj_przycisk_obliczen (miejsce, funkcja, nazwa_statystyki, entry, wyniki_label, dane):
    przycisk = tk.Button(miejsce, text="Oblicz " + nazwa_statystyki,
                         command=lambda: oblicz_statystyki(funkcja, nazwa_statystyki, entry, wyniki_label, dane))
    przycisk.pack(side=tk.LEFT, padx=2, pady=2)


def oblicz_statystyki (funkcja, nazwa_statystyki, entry, wyniki_label, dane):
    dane_wejsciowe = entry.get()

    if not dane_wejsciowe:
        messagebox.showerror("Błąd", "Proszę wprowadzić dane lub wczytać z pliku.")
        return

    try:
        dane = [float(x) for x in dane_wejsciowe.split()]
    except ValueError:
        messagebox.showerror("Błąd", "Wprowadź poprawne liczby.")
        return

    wynik = f"{nazwa_statystyki}: {funkcja(dane):.2f}"
    wyniki_label.config(text=wynik)


def wczytaj_z_excela (entry, wyniki_label, obliczenia_frame, dane):
    try:
        sciezka_pliku = filedialog.askopenfilename(title="Wybierz plik Excela",
                                                   filetypes=[("Pliki Excela", "*.xlsx;*.xls")])
        if not sciezka_pliku:
            return

        df = pd.read_excel(sciezka_pliku, header=None)
        dane.extend(df.values.flatten().tolist())
        entry.delete(0, tk.END)
        entry.insert(0, ' '.join(map(str, dane)))
        wyniki_label.config(text="")
        obliczenia_frame.pack()

    except Exception as e:
        messagebox.showerror("Błąd", f"Wystąpił błąd podczas wczytywania pliku Excela:\n{str(e)}")

def rysuj_histogram (entry):
    dane_wejsciowe = entry.get()

    if not dane_wejsciowe:
        messagebox.showerror("Błąd", "Proszę wprowadzić dane lub wczytać z pliku.")
        return

    try:
        dane = [float(x) for x in dane_wejsciowe.split()]
    except ValueError:
        messagebox.showerror("Błąd", "Wprowadź poprawne liczby.")
        return

    top = Toplevel(root)
    top.title('Histogram')

    fig, ax = plt.subplots()
    ax.hist(dane, bins=10, edgecolor='black')
    ax.set_title('Histogram')
    ax.set_xlabel('Wartości')
    ax.set_ylabel('Częstość występowania')

    canvas = FigureCanvasTkAgg(fig, master=top)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
    plt.close('all')


def rysuj_wykres_punktowy (entry):
    dane_wejsciowe = entry.get()

    if not dane_wejsciowe:
        messagebox.showerror("Błąd", "Proszę wprowadzić dane lub wczytać z pliku.")
        return

    try:
        dane = [float(x) for x in dane_wejsciowe.split()]
    except ValueError:
        messagebox.showerror("Błąd", "Wprowadź poprawne liczby.")
        return

    top = Toplevel(root)
    top.title('Wykres punktowy')

    fig, ax = plt.subplots()
    ax.plot(sorted(dane), 'o-', label='Wartości')
    ax.set_title('Wykres Punktowy')
    ax.set_xlabel('Indeks')
    ax.set_ylabel('Wartości')
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=top)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    plt.close('all')

root = tk.Tk()
root.title("Kalkulator Statystyczny")

label = tk.Label(root, text="Wprowadź dane oddzielone spacją lub wczytaj z pliku Excela:")
label.pack()

entry = tk.Entry(root, width=50)
entry.pack()

button_wczytaj = tk.Button(root, text="Wczytaj z Excela",
                           command=lambda: wczytaj_z_excela(entry, wyniki_label, obliczenia_frame, dane))
button_wczytaj.pack(padx=2, pady=2)

obliczenia_frame = tk.Frame(root)
obliczenia_frame.pack()

rysowanie_frame = tk.Frame(root)
rysowanie_frame.pack()

button_histogram = tk.Button(rysowanie_frame, text="Rysuj Histogram", command=lambda: rysuj_histogram(entry))
button_histogram.pack(side=tk.LEFT, padx=2, pady=2)

