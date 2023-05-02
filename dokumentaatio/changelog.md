# Changelog

## Viikko 3
- Lisätty alustava Monster-luokka. Pygamen Sprite-olio, joka vastaa
  pelin hirviöiden toiminnallisuudesta.
- Lisätty alustava Map-luokka. Luokka vastaa pelin "kartasta" ja 
  Sprite-olioiden piirtämisestä.
- Lisätty kuvatiedostot hirviölle, lattialle ja maalle.
- Testattu, että Monster-luokan oliota voi liikuttaa pelikartalla.

## Viikko 4
- Lisätty MainMenu-luokka. Valikko näytetään pelaajalle, kun peli
  käynnistetään. Valikon kautta pelaaja voi aloittaa pelin ja sulkea
  ohjelman.
- Lisätty PauseMenu-luokka. Valikko näytetään pelaajalle, kun peli
  keskeytetään. Valikon kautta pelaaja voi poistua päävalikkoon tai
  jatkaa keskeytettyä peliä.
- Lisätty Controller-luokka. Luokka vastaa pelin tilan hallinnasta.
- Lisätty Tower-luokka. Pygamen Sprite-olio, joka vastaan pelin
  tornien toiminnallisuudesta.
- Testattu, että valikoiden käyttämä Controller-luokka vaihtaa pelin 
  tilaa oikein.

## Viikko 5
- Hirviöiden liikkuminen. Hirviöt voivat liikkua pelikartalla polkua pitkin.
- Lisätty alustava Projectile-luokka. Luokka vastaa tornien ampumien
  ammusten toiminnallisuudesta.
- Lisätty BuildMenu-luokka. Luokka toimii pelin pääkäyttöliittymänä. Pääkäyttö-
  liittymä näytetään näytön vasemmassa reunassa pelikartan vierellä. Sen kautta
  pelaaja voi esimerkiksi rakentaa ja myydä torneja.
- Testattu, että hirviöiden liikuttaminen pelikartalla toimii oikein.

## Viikko 6
- Lisätty Hearth-luokka. Pygamen Sprite-olio, jota pelaajan on tarkoitus
  puolustaa pelissä.
- Lisätty Player-luokka. Luokka vastaa pelaajaan liittyvistä toiminnoista.
- Lisätty uusi ominaisuus, kierrokset. Hirviöt lisätään pelikartalla
  aalloittain. Uusi kierros alkaa, kun pelaaja painaa Start-nappia.
- Lisätty uusi ominaisuus, pelaajan rakentamat tornit ampuvat ja 
  vahingoittavat hirviöitä.