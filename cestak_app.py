import calendar
import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from cestak_logika import vytvor_cestak, SLOT_RADKY

SABLONA = "sablona_prazdna.xlsx"

MESICE = ["leden", "únor", "březen", "duben", "květen", "červen",
          "červenec", "srpen", "září", "říjen", "listopad", "prosinec"]


class CestakApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cesťák")
        self.vybrane_dny = set()
        self.tlacitka_dnu = {}

        dnes = datetime.date.today()
        self.rok = dnes.year
        self.mesic = dnes.month

        self._postav_formular()
        self._postav_kalendar()
        self._vykresli_kalendar()

        tk.Button(self, text="Vygenerovat cesťák", command=self._generuj).grid(
            row=1, column=0, columnspan=2, pady=10
        )

    # ---------- formulář s údaji ----------
    def _postav_formular(self):
        ramecek = ttk.LabelFrame(self, text="Údaje")
        ramecek.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        self.pole = {}
        popisky = {
            "jmeno": "Jméno",
            "bydliste": "Bydliště",
            "typ_dopravy": "Auto / SPZ",
            "odjezd": "Místo odjezdu",
            "prijezd": "Cíl cesty",
            "km": "Km na cestu",
        }
        for i, (klic, popis) in enumerate(popisky.items()):
            tk.Label(ramecek, text=popis).grid(row=i, column=0, sticky="w", padx=5, pady=3)
            promenna = tk.StringVar()
            tk.Entry(ramecek, textvariable=promenna, width=30).grid(row=i, column=1, padx=5, pady=3)
            self.pole[klic] = promenna

        # rovnou předvyplníme, ať to nemusíš psát pokaždé
        self.pole["odjezd"].set("Hradec Králové")
        self.pole["prijezd"].set("Náchod")
        self.pole["km"].set("100")

    # ---------- kalendář ----------
    def _postav_kalendar(self):
        ramecek = ttk.LabelFrame(self, text="Klikni na dny, kdy jsi cestoval")
        ramecek.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        navigace = tk.Frame(ramecek)
        navigace.grid(row=0, column=0, columnspan=7, pady=5)
        tk.Button(navigace, text="<", command=self._predchozi_mesic).pack(side="left")
        self.popisek_mesice = tk.Label(navigace, text="", width=20)
        self.popisek_mesice.pack(side="left")
        tk.Button(navigace, text=">", command=self._dalsi_mesic).pack(side="left")

        self.mrizka = tk.Frame(ramecek)
        self.mrizka.grid(row=1, column=0, columnspan=7)

    def _predchozi_mesic(self):
        self.mesic -= 1
        if self.mesic == 0:
            self.mesic = 12
            self.rok -= 1
        self._vykresli_kalendar()

    def _dalsi_mesic(self):
        self.mesic += 1
        if self.mesic == 13:
            self.mesic = 1
            self.rok += 1
        self._vykresli_kalendar()

    def _vykresli_kalendar(self):
        # smažeme staré tlačítko-mřížku a vykreslíme novou pro aktuální měsíc
        for widget in self.mrizka.winfo_children():
            widget.destroy()
        self.tlacitka_dnu = {}

        self.popisek_mesice.config(text=f"{MESICE[self.mesic - 1]} {self.rok}")

        cal = calendar.Calendar(firstweekday=0)
        for radek, tyden in enumerate(cal.monthdayscalendar(self.rok, self.mesic)):
            for sloupec, den_cisla in enumerate(tyden):
                if den_cisla == 0:
                    continue  # den mimo aktuální měsíc, nekreslíme tlačítko
                d = datetime.date(self.rok, self.mesic, den_cisla)
                tlacitko = tk.Button(
                    self.mrizka, text=str(den_cisla), width=4,
                    command=lambda d=d: self._klik_na_den(d),  # <- tady je ta past vyřešená
                )
                tlacitko.grid(row=radek + 1, column=sloupec, padx=1, pady=1)
                self._nastav_barvu(tlacitko, d)
                self.tlacitka_dnu[d] = tlacitko

    def _nastav_barvu(self, tlacitko, d):
        if d in self.vybrane_dny:
            tlacitko.config(bg="#4CAF50", fg="white")
        else:
            tlacitko.config(bg="SystemButtonFace", fg="black")

    def _klik_na_den(self, d):
        if d in self.vybrane_dny:
            self.vybrane_dny.discard(d)
        else:
            if len(self.vybrane_dny) >= len(SLOT_RADKY):
                messagebox.showwarning("Plno", f"Formulář má místo jen pro {len(SLOT_RADKY)} cest.")
                return
            self.vybrane_dny.add(d)
        self._nastav_barvu(self.tlacitka_dnu[d], d)

    # ---------- generování ----------
    def _generuj(self):
        if not self.vybrane_dny:
            messagebox.showwarning("Nic k vyplnění", "Nevybral jsi žádný den.")
            return

        hlavicka = {klic: promenna.get() for klic, promenna in self.pole.items()}
        hlavicka["km"] = float(hlavicka["km"])

        # datumy si seřadíme a přetvoříme do formátu "d.m." jako v šabloně
        dny_serazene = sorted(self.vybrane_dny)
        dny_text = [f"{d.day}.{d.month}." for d in dny_serazene]

        cesta_k_ulozeni = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel soubor", "*.xlsx")],
            initialfile="cestak_vyplneny.xlsx",
        )
        if not cesta_k_ulozeni:
            return

        try:
            vytvor_cestak(SABLONA, cesta_k_ulozeni, hlavicka, dny_text)
        except Exception as chyba:
            messagebox.showerror("Chyba", str(chyba))
            return

        messagebox.showinfo("Hotovo", f"Uloženo: {cesta_k_ulozeni}")


if __name__ == "__main__":
    app = CestakApp()
    app.mainloop()