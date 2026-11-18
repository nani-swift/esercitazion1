"""Test per la classe Uscita (Attività 2)."""

import unittest
from datetime import date
from prenotazioni import Uscita


class TestUscita(unittest.TestCase):

    def test_orari_non_ammessi(self):
        """Il costruttore solleva ValueError per orari non ammessi (formato, multipli, apertura/chiusura)."""

        with self.assertRaises(ValueError):
            Uscita("doppio", date(2026, 6, 5), "09:15", "10:30", "Rossi", 2)
        
        with self.assertRaises(ValueError):
            Uscita("doppio", date(2026, 6, 5), "06:30", "08:00", "Rossi", 2)
        
        with self.assertRaises(ValueError):
            Uscita("doppio", date(2026, 6, 5), "18:30", "19:30", "Rossi", 2)
        
        with self.assertRaises(ValueError):
            Uscita("doppio", date(2026, 6, 5), "10:00", "09:00", "Rossi", 2)

    def test_tipo_giorno_errato(self):
        """Il costruttore solleva TypeError se il giorno non è un oggetto date."""
        with self.assertRaises(TypeError):
            Uscita("doppio", "2026-06-05", "09:00", "10:30", "Rossi", 2)

    def test_durata_minuti(self):
        """Verifica che durata_minuti restituisca la durata corretta."""
        uscita = Uscita("doppio", date(2026, 6, 5), "09:00", "10:30", "Rossi", 2)
        self.assertEqual(uscita.durata_minuti(), 90)

    def test_si_sovrappone(self):
        """Verifica la logica di sovrapposizione delle uscite."""
        u1 = Uscita("doppio", date(2026, 6, 5), "09:00", "10:30", "Rossi", 2)
        
        u2 = Uscita("doppio", date(2026, 6, 5), "10:00", "11:00", "Verdi", 2)
        self.assertTrue(u1.si_sovrappone(u2))
        
        u3 = Uscita("singolo", date(2026, 6, 5), "09:00", "10:30", "Bianchi", 1)
        self.assertFalse(u1.si_sovrappone(u3))
        
        u4 = Uscita("doppio", date(2026, 6, 6), "09:00", "10:30", "Neri", 2)
        self.assertFalse(u1.si_sovrappone(u4))

    def test_to_dict_from_dict(self):
        """Verifica che from_dict(x.to_dict()) ricostruisca un'uscita equivalente compreso l'id."""
        u1 = Uscita("doppio", date(2026, 6, 5), "09:00", "10:30", "Rossi", 2)
        u1.id = 42
        
        dizionario = u1.to_dict()
        u2 = Uscita.from_dict(dizionario)
        
        self.assertEqual(u1.id, u2.id)
        self.assertEqual(u1.barca_codice, u2.barca_codice)
        self.assertEqual(u1.giorno, u2.giorno)
        self.assertEqual(u1.inizio, u2.inizio)
        self.assertEqual(u1.fine, u2.fine)
        self.assertEqual(u1.capobarca, u2.capobarca)
        self.assertEqual(u1.equipaggio, u2.equipaggio)


if __name__ == "__main__":
    unittest.main()