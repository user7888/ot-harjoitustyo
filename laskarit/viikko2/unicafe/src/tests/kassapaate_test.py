import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.maksukortti = Maksukortti(1000)
    
    def test_rahamaara_ja_myytyjen_maara_alussa(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)
    
    def test_kateisosto_toimii_edulliset_ja_maukkaat(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(500), 260)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(500), 100)
    
    def test_kateisosto_kasvattaa_kassan_rahamaaraa_edulliset_ja_maukkaat(self):
        self.kassapaate.syo_edullisesti_kateisella(500)
        self.kassapaate.syo_maukkaasti_kateisella(500)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100640)
    
    def test_kateisosto_kasvattaa_myytyjen_maaraa_edulliset_ja_maukkaat(self):
        self.kassapaate.syo_edullisesti_kateisella(500)
        self.kassapaate.syo_maukkaasti_kateisella(500)
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(self.kassapaate.maukkaat, 1)
    
    def test_kateisosto_toimii_oikein_jos_rahamaara_ei_ole_riittava(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(100), 100)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(100), 100)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)
    
    def test_korttiosto_toimii_kun_kortilla_on_tarpeeksi_rahaa(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(self.maksukortti), True)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti), True)
    
    def test_korttiosto_kasvattaa_myytyjen_maaraa(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(self.kassapaate.maukkaat, 1)
    
    def test_korttiosto_toimii_oikein_kun_kortilla_ei_ole_tarpeeksi_rahaa(self):
        kortti = Maksukortti(100)

        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(kortti), False)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(kortti), False)
        self.assertEqual(str(kortti), "Kortilla on rahaa 1.00 euroa")

        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_kassassa_oleva_rahamaara_ei_muutu_korttiostossa(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_kortille_rahaa_ladattaessa_kortin_saldo_ja_kassan_rahamaara_muuttuvat_oikein(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 1000)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 20.00 euroa")
        self.assertEqual(self.kassapaate.kassassa_rahaa, 101000)
    
    def test_kortille_rahan_lataaminen_negatiivisella_summalla(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, -1000)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    

    

    


    

