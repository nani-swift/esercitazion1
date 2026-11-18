"""Test per la riproduzione e verifica dei difetti segnalati (Attività 1 e 2)."""

import unittest
from datetime import date, timedelta
from prenotazioni import Uscita, Registro, Barca


class TestSegnalazioni(unittest.TestCase):

    def test_segnalazione_1_apertura_ore_7(self):
        """Verifica che un'uscita che inizia alle 07:00 (orario di apertura) sia ammessa."""
        try:
            uscita = Uscita(
                barca_codice="doppio",
                giorno=date(2026, 6, 5),
                inizio="07:00",
                fine="08:30",
                capobarca="Rossi",
                equipaggio=2
            )
        except ValueError as e:
            self.fail(f"L'uscita alle 07:00 è stata rifiutata erroneamente con errore: {e}")

    def test_segnalazione_2_limite_21_giorni(self):
        """Verifica che la prenotazione esattamente al limite di 21 giorni sia ammessa."""
        oggi = date(2026, 6, 1)
        giorno_limite = oggi + timedelta(days=21)
        
        try:
            uscita = Uscita(
                barca_codice="doppio",
                giorno=giorno_limite,
                inizio="09:00",
                fine="10:30",
                capobarca="Verdi",
                equipaggio=2
            )
            registro = Registro()
            registro.aggiungi_barca(Barca("doppio", "Doppio", 4))
            registro.prenota(uscita, oggi=oggi)
        except Exception as e:
            self.fail(f"La prenotazione a 21 giorni esatti è stata rifiutata erroneamente con errore: {e}")


if __name__ == "__main__":
    unittest.main()