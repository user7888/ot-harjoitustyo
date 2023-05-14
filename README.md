# Ohjelmistotekniikan harjoitustyö
Repositorio **ohjelmistotekniikan** harjoitustyölle ja
viikkotehtäville.

## **Uusin release**
[loppupalautus](https://github.com/user7888/ot-harjoitustyo/releases).

## **Dokumentaatio**
[vaatimusmäärittely](dokumentaatio/vaatimusmaarittely.md)\
[työaikakirjanpito](dokumentaatio/tuntikirjanpito.md)\
[changelog](dokumentaatio/changelog.md)\
[arkkitehtuurikuvaus](dokumentaatio/arkkitehtuuri.md)\
[käyttöohje](dokumentaatio/kayttoohje.md)\
[testausdokumentti](dokumentaatio/testausdokumentti.md)\

## **Käynnistys**
1. Asenna riippuvuudet
```
poetry install
```

2. Suoritaalustustoimenpiteet
```
poetry run invoke init
```

3. Käynnistä sovellus
```
poetry run invoke start
```

## **Komentorivikomennot**
Ohjelman käynnistäminen
```
poetry run invoke start
```

Testien suorittaminen
```
poetry run invoke test
```

Kerää testikattavuuden ja muodostaa testikattavuusraportin.
HTML-muotoisen raportin voi avata selaimessa.
```
poetry run invoke coverage-report
```

Alustaa SQLite-tietokannan
```
poetry run invoke init
```
