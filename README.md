# Ubahn_Muenchen_Simulation
Simulation des Ubahnnetzes der Stadt München

Dieses Projekt implementiert einen Routenplaner für das Münchner U-Bahn-Netz.
Es berechnet die kürzeste Fahrzeit zwischen zwei Bahnhöfen unter Berücksichtigung von:
1. Fahrzeiten zwischen jweils 2 Stationen
2. Umsteigedauer zwischen Linien (an einem Bahnhof)
3. Temporär gesperrten Verbindungen
4. reelen Gegebenheiten (Bahnhöfe, Strecken, Linien, etc.)

Zusätzlich können Netzstatistiken wie durchschnittliche Fahrzeit, Umstiege und Stationenanzahl (einer Strecke) berechnet werden.

Features:
Modellierung eines U-Bahn-Netzes als gewichteter Graph
Kürzeste-Wege-Berechnung mit Dijkstra-Algorithmus
Beliebige Umsteigezeit konfigurierbar
Hinzufügen von Bahnhöfen
Hinzufügen zusätzlicher Verbindungen
Entfernen (temporär) nicht verfügbarer Verbindungen
Interaktive Benutzereingabe (Start- und Zielstation)
Statistische Auswertung des gesamten Netzes

Nutzung:
Programm 'netzwerk_ubahn.py' auführen
Startstation eingeben (z.B. Hauptbahnhof)
Zielstation eingeben (z.B. Odeonsplatz)
--> Ausgabe der kürzesten Fahrzeit und der zu Fahrenden Strecke
Optional: Abfrage von Netzstatistiken (EIngabe ja/nein)

Voraussetzungen:
Python 3.8 oder neuer
Verwendete Bibliotheken: heapq, defaultdict from collections, combinations from itertools

Anpassungsmöglichkeiten:
1. Verbindungen entfernen/außer Kraft setzen:
  - Liste 'unavailable_verbindungen' in 'strecken_muc' ergänzen. Format: (Startstation, Zielstation, Linie) --> bsp.: ("Friedenheimer Straße", "Laimer Platz", "U5")
  - durch 'netz.delete_verbindung(Startstation, Zielstation, Linie)' in netzwerk_ubahn.py
2. Umstiegszeiten ändern:
  - in 'netzwerk_ubahn.py' mit dem Befehl: netz.set_umsteigezeit(4) den Wert in den Klammern auf eine beliebige Höhe setzen

Beispielhafte Ausgabe:
Geben Sie die Startstation ein: Hauptbahnhof

Geben Sie die Zielstation ein: Odeonsplatz

[('Hauptbahnhof', 'U4'), ('Karlsplatz (Stachus)', 'U4'), ('Odeonsplatz', 'U4')]

Gesamtzeit: 3.5 Minuten

Möchten Sie die durchschnittlichen Statistiken des Netzes abfragen? (ja/nein): ja

Durchschnittliche Fahrzeit zwischen allen Bahnhöfen: 21.988129899216126 Minuten

Durchschnittliche Umstiege zwischen allen Bahnhöfen: 0.8029115341545353 Umstiege

Durchschnittliche Anzahl Stationen zwischen allen Bahnhöfen: 12.309294512877939

Anzahl nicht befahrbarer Strecken: 95 von 4560 möglichen Strecken

Dieses Projekt dient zu Lern- und Studienzwecken.
