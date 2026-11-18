"""Test per la riproduzione e verifica dei difetti segnalati (Attività 1)."""

import unittest
from datetime import date
from prenotazioni import Uscita


class TestSegnalazioni(unittest.TestCase):

    def test_segnalazione_1_apertura_ore_7(self):
        """Verifica che un'uscita che inizia alle 07:00 (orario di apertura) sia ammessa."""
        try:
            uscita = Uscita(
                barca_codice="doppio",  # تم التعديل هنا
                giorno=date(2026, 6, 5),
                inizio="07:00",
                fine="08:30",
                capobarca="Rossi",
                equipaggio=2
            )
        except ValueError as e:
            self.fail(f"L'uscita alle 07:00 è stata rifiutata erroneamente con errore: {e}")


if __name__ == "__main__":
    unittest.main()