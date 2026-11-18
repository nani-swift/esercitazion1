"""Test per la classe Registro (Attività 2)."""

import unittest
from datetime import date, timedelta
from prenotazioni import Registro, Barca, Uscita, BarcaNonTrovata, DataNonAmmessa, UscitaNonTrovata


class TestRegistro(unittest.TestCase):

    def setUp(self):
        """Inizializza un registro pulito e alcune barche di supporto prima di ogni test."""
        self.registro = Registro()
        self.barca_singolo = Barca("singolo", "Singolo", 1)
        self.barca_doppio = Barca("doppio", "Doppio", 4)
        self.registro.aggiungi_barca(self.barca_singolo)
        self.registro.aggiungi_barca(self.barca_doppio)

    def test_aggiungi_barca_duplicata(self):
        """aggiungi_barca rifiuta un codice duplicato sollevando ValueError."""
        with self.assertRaises(ValueError):
            self.registro.aggiungi_barca(Barca("singolo", "Altro Singolo", 1))

    def test_barca_inesistente(self):
        """barca solleva BarcaNonTrovata per un codice inesistente."""
        with self.assertRaises(BarcaNonTrovata):
            self.registro.barca("inesistente")

    def test_prenota_vincoli_data(self):
        """prenota solleva DataNonAmmessa per date passate, martedì, oltre l'orizzonte, e accetta oggi."""
        oggi = date(2026, 6, 1)
        
        ieri = oggi - timedelta(days=1)
        u_passata = Uscita("singolo", ieri, "09:00", "10:00", "Rossi", 1)
        with self.assertRaises(DataNonAmmessa):
            self.registro.prenota(u_passata, oggi=oggi)
            
        martedi = date(2026, 6, 2)
        u_martedi = Uscita("singolo", martedi, "09:00", "10:00", "Rossi", 1)
        with self.assertRaises(DataNonAmmessa):
            self.registro.prenota(u_martedi, oggi=oggi)
            
        oltre = oggi + timedelta(days=22)
        u_oltre = Uscita("singolo", oltre, "09:00", "10:00", "Rossi", 1)
        with self.assertRaises(DataNonAmmessa):
            self.registro.prenota(u_oltre, oggi=oggi)
            
        u_oggi = Uscita("singolo", oggi, "11:00", "12:00", "Rossi", 1)
        id_prenotazione = self.registro.prenota(u_oggi, oggi=oggi)
        self.assertIsNotNone(id_prenotazione)

    def test_id_progressivi_e_non_riutilizzati(self):
        """Gli id assegnati da prenota sono progressivi e non vengono riutilizzati dopo una cancellazione."""
        oggi = date(2026, 6, 1)
        u1 = Uscita("singolo", oggi, "09:00", "10:00", "Rossi", 1)
        u2 = Uscita("singolo", oggi, "10:30", "11:30", "Verdi", 1)
        
        id1 = self.registro.prenota(u1, oggi=oggi)
        id2 = self.registro.prenota(u2, oggi=oggi)
        
        self.assertEqual(id2, id1 + 1)
        
        self.registro.cancella(id1)
        
        u3 = Uscita("singolo", oggi, "12:00", "13:00", "Bianchi", 1)
        id3 = self.registro.prenota(u3, oggi=oggi)
        self.assertEqual(id3, id2 + 1)

    def test_cancella_e_uscita_inesistenti(self):
        """cancella e uscita sollevano UscitaNonTrovata per un id inesistente."""
        with self.assertRaises(UscitaNonTrovata):
            self.registro.cancella(9999)
            
        with self.assertRaises(UscitaNonTrovata):
            self.registro.uscita(9999)

    def test_uscite_del_giorno_ordinamento_e_filtro(self):
        """uscite_del_giorno restituisce le uscite ordinate per orario e filtrate per barca."""
        oggi = date(2026, 6, 1)
        
        u_singolo_tardi = Uscita("singolo", oggi, "11:00", "12:00", "Rossi", 1)
        u_doppio_presto = Uscita("doppio", oggi, "09:00", "10:30", "Verdi", 2)
        u_singolo_presto = Uscita("singolo", oggi, "09:30", "10:30", "Bianchi", 1)
        
        self.registro.prenota(u_singolo_tardi, oggi=oggi)
        self.registro.prenota(u_doppio_presto, oggi=oggi)
        self.registro.prenota(u_singolo_presto, oggi=oggi)

        tutte = self.registro.uscite_del_giorno(oggi)
        self.assertEqual(len(tutte), 3)
        self.assertEqual(tutte[0].inizio, "09:00")
        self.assertEqual(tutte[1].inizio, "09:30")
        self.assertEqual(tutte[2].inizio, "11:00")
        
        solo_singolo = self.registro.uscite_del_giorno(oggi, barca_codice="singolo")
        self.assertEqual(len(solo_singolo), 2)
        self.assertEqual(solo_singolo[0].inizio, "09:30")
        self.assertEqual(solo_singolo[1].inizio, "11:00")


if __name__ == "__main__":
    unittest.main()