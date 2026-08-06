import openpyxl
from cestak_logika import vytvor_cestak, SLOT_RADKY


def test_deset_dni_se_zapise_spravne():
    # --- ARRANGE: připravíme vstupní data ---
    hlavicka = {
        "jmeno": "Test Testovic",
        "bydliste": "Hradec Králové",
        "typ_dopravy": "Škoda Octavia, 7H7 8622",
        "odjezd": "Hradec Králové",
        "prijezd": "Náchod",
        "km": 100,
    }
    dny = ["3.8.", "5.8.", "8.8.", "10.8.", "12.8.", "15.8.", "17.8.", "19.8.", "20.8.", "22.8."]

    # --- ACT: zavoláme testovanou funkci ---
    vytvor_cestak("sablona_prazdna.xlsx", "test_output_pytest.xlsx", hlavicka, dny)

    # --- ASSERT: ověříme, že se zapsalo přesně to, co jsme zadali ---
    wb = openpyxl.load_workbook("test_output_pytest.xlsx")
    ws = wb["List1"]

    zapsane_dny = []
    for radek in SLOT_RADKY[:len(dny)]:
        zapsane_dny.append(ws[f"A{radek}"].value)

    assert zapsane_dny == dny, f"Očekával jsem {dny}, ale v Excelu je {zapsane_dny}"


def test_prazdny_seznam_dni_nespadne():
    # I okrajový případ (0 dní) by měl fungovat bez pádu
    hlavicka = {
        "jmeno": "Test",
        "bydliste": "Test",
        "typ_dopravy": "Test",
        "odjezd": "Test",
        "prijezd": "Test",
        "km": 100,
    }
    vytvor_cestak("sablona_prazdna.xlsx", "test_prazdny.xlsx", hlavicka, [])
    # pokud se dostaneme sem bez chyby, test prošel