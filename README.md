# Ohjelmistotekniikan harjoitustyö
Repositorio **ohjelmistotekniikan** harjoitustyölle ja
viikkotehtäville.

## **Dokumentaatio**
[vaatimusmäärittely](dokumentaatio/vaatimusmaarittely.md)\
[työaikakirjanpito](dokumentaatio/tuntikirjanpito.md)\
[changelog](dokumentaatio/changelog.md)\
[arkkitehtuurikuvaus](dokumentaatio/arkkitehtuuri.md)

## **Käynnistys**
1. Asenna riippuvuudet
```
poetry install
```

2. Käynnistä sovellus
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
