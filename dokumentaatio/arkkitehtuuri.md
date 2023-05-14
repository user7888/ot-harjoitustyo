# Arkkitehtuurikuvaus

## Rakenne
Ohjelman rakenne koostuu käyttöliittymästä, pelilogiikasta, Sprite-olioista, muista
pelin tarvitsemista olioista sekä tiedon tallennuksesta vastaavasta SaveRepository-moduulista.

![Pakkausrakenne](./kuvat/pakkausrakenne.png)

## Käyttöliittymä
Käyttöliittymä koostuu luokista:
- Päävalikko (MainMenu)
- Paussivalikko (PauseMenu)
- Lopetusruutu (GameEndScreen)
- Pääkäyttöliittymä (MainUI)

Valikoiden (MainMenu, PauseMenu ja GameEndScreen) avulla käyttäjä voi navigoida pelin eri tilojen välillä.
Siirtyminen eri tilojen välillä on toteutettu GameStateController-luokan avulla, jonka palveluita
eri valikot kutsuvat kun valikoiden nappeja painetaan.

Pääkäyttöliittymä näytetään pelikartan vieressä oikealla, kun peli on käynnissä. Sen kautta tehdään
suuri osa pelin toiminnoista, kuten tornien valitseminen ja niiden asettelu pelikartalle. Pääkäyttöliittymä
jakautuu pelikarttaan kohdistuviin toimintoihin sekä oikealla näytettävän valikon toimintoihin.
Pelikarttaan kohdistuvat toiminnot on toteutettu GameMap-luokan palveluina, kuten:

- `place_tower(self, mouse_position, tower_type)`
- `select_tower(self, mouse_position)`

Valikon toiminnot muuttavat valikon tilaa, kuten valitsevat seuraavaksi rakennettavan tornin
tai käynnistävät seuraavan hirviöaallon. Pelin tilaan liittyvät toiminnot on toteutettu
GameStateController-luokan palveluina.

## Sovelluslogiikka
Tarkempi kuvaus sovelluksen rakenteesta ja sen eri osien
välisistä suhteista luokka/pakkauskaaviona:

![Pakkausrakenne](./kuvat/pakkaus_ja_luokka.png)

### Sovelluslogiikan tärkeimmät luokat
Pelin toiminnallisista kokonaisuuksista vastaavat pääosin
seuraavat luokat:
#### GameMap

GameMap-luokka vastaa pelikartasta ja siihen liittyvistä palveluista joita käyttöliittymä tarvitsee. Pelikartta 
on toteutettu matriisina, jonka alkioita Sprite-luokan oliot Floor, Ground ja Hearth ovat.

GameMap-luokka hallinnoi kaikkea pelikartalla näkyvää ja vastaa pelikartan päivittämisestä, erityisesti 
se hallinnoi Sprite-luokan olioita. Luokassa toteutettu funktio `update(current_time)` käyttää Sprite-olioiden toimintoja, kuten:
- `monster.move(self, current_time)`
- `monster.update_status(current_time)`
- `tower.should_shoot(current_time)`
- `tower.shoot_nearest_monster(self.monsters, self.projectiles, current_time)`
- `projectile.update()`

Funktion avulla siis esimerkiksi liikutetaan hirviöitä ja tornien ammuksia pelikartalla. `update(current_time)`-funktiota kutsutaan
pelisilmukasta.

Käyttöliittymää varten toteutettuja palveluja ovat:
- `place_tower(self, mouse_position, tower_type)`
- `select_tower(self, mouse_position)`


#### GameLoop

GameLoop-luokka on sovelluksen pelisilmukka. Sen toimintaperiaatteena on, että pelisilmukka kysyy GameStateController-oliolta pelin tilaa
funktiolla `get_game_state()`, ja vastauksesta riippuen joko siirrytään suorittamaan seuraavaa tilaa tai
jatketaan varsinaisen pelisilmukan suoritusta.

Luokassa toteutettuja funktiota ovat:
- `_render(self)`
- `_handle_events()`

#### GameStateController
GameStateController-luokassa on toteutettu pelin tilat ja palvelut niiden hallintaan muille luokille, erityisesti käyttöliittymälle.
Luokassa on toteutettu myös hirviöaaltoihin liittyvä toiminnallisuus.

Pelin tilaan liittyviä palveluja:
- `set_state_main_menu(self)`
- `set_state_paused(self)`
- `set_state_game_over`

Hirviöaaltoihin liittyviä palveluja:
- `should_spawn_monster(current_time)`
- `get_next_monster_type(self)`


## Tietojen pysyväistallennus

Sovelluksessa on toteutettuna tallennustoiminto, johon käytetään SQLite-tietokantaa. Tallennuksesta vastaa
repositories-pakkauksen luokka SaveRepository. Tallennustoiminnon avulla säilötään pelin tila niin, että kesken
jääneestä pelistä voidaan jatkaa myöhemmin.

Luokan palveluja ovat:
- `find_save()`
- `create_save(save)`
- `delete_all_saves(save)`

Pelin käynnistyessä setup-moduulin avulla ladataan tallennuksen tiedot. Kun peli suljetaan, käytetään
SaveRepositoryn palvelua  `create_save(save)`ja tallennetaan tarvittavat tiedot pelin tilasta tietokantaan.

## Päätoiminnot

Sovelluksen päätoiminnallisuudet kuvattuna sekvenssikaavioina.

#### Pelin käynnistys

Sekvenssikaaviossa on kuvattuna tilanne jossa ohjelma käynnistetään. Ensin 
käynnistetään pelisilmukka, jonka jälkeen siirrytään päävalikkoon.

```mermaid
 sequenceDiagram
      index->>game_loop: game_loop.start()
      game_loop->>controller: controller.get_game_state()
      controller-->>game_loop: "initialized"
      game_loop->>controller: set_state_main_menu()
      game_loop->>main_menu: main_menu.start()
      main_menu->>controller: get_game_state()
      controller-->>main_menu: "main menu"
      main_menu->>start_button: start_button.render(display)
      main_menu->>new_game_button: new_game_button.render(display)
      main_menu->>quit_button: quit_button.render(display)
```

#### Tornin rakentaminen pelikartalle
Sekvenssikaaviossa on kuvattuna tilanne, jossa käyttäjä rakentaa tornin pelikartalle
kolmella klikkauksella. Ensin käyttäjä painaa MainUI:n nappia "Build", sitten MainUI:n 
nappia "Arrow" valitakseen tornin ja viimeiseksi klikkaa pelikartalla kohtaa, johon haluaa rakentaa tornin.
GameLoop tunnistaa klikkaukset, ja siirtää ne MainUI:lle käsiteltäväksi. MainUI käyttää
GameMap-oliolta funktiota `place_tower(mouse_position)` joka asettaa tornin pelikartalle. Lopuksi
MainUI palaa takaisin "default"-tilaan.

```mermaid
 sequenceDiagram
      actor User
      participant GameLoop
      participant MainUI
      participant GameMap
      User->>MainUI: click "Build" button
      GameLoop->>MainUI: check_for_inputs(mouse_position)
      MainUI->>MainUI: handle_build_button()
      User->>MainUI: click "Arrow tower" button
      MainUI->>MainUI: handle_arrow_button()
      GameLoop->>MainUI: check_for_inputs(mouse_position)
      User->>MainUI: click a tile on game map
      GameLoop->>MainUI: handle_map_click(mouse_position)
      MainUI->>GameMap: place_tower(mouse_position)
      GameMap-->>MainUI: response: "Tower built successfully"
      MainUI->>MainUI: _back_to_state("default", response)
```

#### Tallennustoiminto
Sekvenssikaaviona kuvattuuna tilanne, jossa sovelluksen sulkemisen yhteydessä tiedot pelin tilasta tallennetaan
SaveRepositoryn avulla SQLite-tietokantaan. 

```mermaid
 sequenceDiagram
      participant GameLoop
      participant GameStateController
      participant SaveRepository
      GameLoop->>GameStateController: get_game_state()
      GameStateController-->>GameLoop: response: "terminated"
      GameLoop->>GameLoop: _exit_game()
      GameLoop->>GameStateController: save_game(map_state, wave_state, player_health, player_gold)
      GameStateController->>SaveRepository: create_save(save)
```



