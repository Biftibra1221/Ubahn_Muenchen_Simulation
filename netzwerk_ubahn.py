import heapq
from collections import defaultdict
from strecken_muc import strecken, umstiege, strecken_mit_Zeit, bahnhoefe, unavailable_verbindungen
from itertools import combinations

class UbahnNetz:
    def __init__(self):
        self.graph = defaultdict(list)
        self.stationen = set()
        self.linien = set()
        self.umsteigezeit = 0

    def set_umsteigezeit(self, zeit):
        """Globale Umsteigezeit in Minuten"""
        self.umsteigezeit = zeit

    def add_station(self, name):
        self.stationen.add(name)

    def add_linie(self, linie):
        self.linien.add(linie)

    def add_verbindung(self, station_a, station_b, linie, fahrzeit):
        """
        Fügt eine bidirektionale Verbindung zwischen zwei Stationen
        auf derselben Linie hinzu.
        """
        self.add_station(station_a)
        self.add_station(station_b)
        self.add_linie(linie)

        node_a = (station_a, linie)
        node_b = (station_b, linie)

        self.graph[node_a].append((node_b, fahrzeit))
        self.graph[node_b].append((node_a, fahrzeit))

    def delete_verbindung(self, station_a, station_b, linie):
        """
    Entfernt eine bidirektionale Verbindung zwischen zwei Stationen
    auf derselben Linie.
        """
        node_a = (station_a, linie)
        node_b = (station_b, linie)

        if node_a in self.graph:
            self.graph[node_a] = [
                (n, t) for (n, t) in self.graph[node_a] if n != node_b
            ]

        if node_b in self.graph:
            self.graph[node_b] = [
                (n, t) for (n, t) in self.graph[node_b] if n != node_a
            ]


    def add_umstieg(self, station, linie_a, linie_b):
        """
        Fügt eine Umsteigeverbindung zwischen zwei Linien
        an derselben Station hinzu.
        """
        node_a = (station, linie_a)
        node_b = (station, linie_b)

        self.graph[node_a].append((node_b, self.umsteigezeit))
        self.graph[node_b].append((node_a, self.umsteigezeit))

    def kuerzeste_strecke(self, start, ziel):
        """
        Berechnet die kürzeste Strecke von start nach ziel
        (unabhängig von der Startlinie).
        Gibt False zurück, wenn keine Verbindung existiert.
        """
        start_nodes = [(0, (start, linie)) for linie in self.linien]
        dist = {}
        vorgaenger = {}

        pq = []
        for kosten, node in start_nodes:
            heapq.heappush(pq, (kosten, node))
            dist[node] = 0

        ziel_nodes = {(ziel, linie) for linie in self.linien}

        while pq:
            kosten, aktueller = heapq.heappop(pq)

            # Ziel erreicht
            if aktueller in ziel_nodes:
                pfad = self._rekonstruiere_pfad(vorgaenger, aktueller)
                return pfad, kosten

            if kosten > dist.get(aktueller, float("inf")):
                continue

            # 🔑 Sicherer Graph-Zugriff
            if aktueller not in self.graph:
                continue

            for nachbar, gewicht in self.graph[aktueller]:
                neue_kosten = kosten + gewicht
                if neue_kosten < dist.get(nachbar, float("inf")):
                    dist[nachbar] = neue_kosten
                    vorgaenger[nachbar] = aktueller
                    heapq.heappush(pq, (neue_kosten, nachbar))

        # Kein Pfad gefunden
        return False

    def _rekonstruiere_pfad(self, vorgaenger, ziel):
        pfad = [ziel]
        while ziel in vorgaenger:
            ziel = vorgaenger[ziel]
            pfad.append(ziel)
        pfad.reverse()
        return pfad

def calc_avg_dur(bahnhoefe):
    gesamtzeit = 0
    anzahl = 0
    not_reached = 0

    n = len(bahnhoefe)
    for i in range(n):
        for j in range(i + 1, n):  # jedes Paar genau einmal
            start = bahnhoefe[i]
            ziel = bahnhoefe[j]

            ergebnis = netz.kuerzeste_strecke(start, ziel)
            if ergebnis is False:
                not_reached += 1
                continue
            else:
                pfad, zeit = ergebnis
                gesamtzeit += zeit
                anzahl += 1

    return gesamtzeit / anzahl if anzahl > 0 else 0, not_reached

def calc_avg_transfers(bahnhoefe):
    gesamt_umstiege = 0
    anzahl = 0
    not_reached = 0

    n = len(bahnhoefe)
    for i in range(n):
        for j in range(i + 1, n):  # jedes Paar genau einmal
            start = bahnhoefe[i]
            ziel = bahnhoefe[j]

            ergebnis = netz.kuerzeste_strecke(start, ziel)
            if ergebnis is False:
                not_reached += 1
                continue
            else:
                pfad, _ = ergebnis

                umstiege = 0
                for k in range(1, len(pfad)):
                    if pfad[k][1] != pfad[k - 1][1]:
                        umstiege += 1

                gesamt_umstiege += umstiege
                anzahl += 1

    return gesamt_umstiege / anzahl if anzahl > 0 else 0, not_reached

def calc_avg_stations(bahnhoefe):
    gesamt_stationen = 0
    anzahl = 0
    not_reached = 0

    n = len(bahnhoefe)
    for i in range(n):
        for j in range(i + 1, n):  # jedes Paar genau einmal
            start = bahnhoefe[i]
            ziel = bahnhoefe[j]

            ergebnis = netz.kuerzeste_strecke(start, ziel)

            if ergebnis is False:
                not_reached += 1
            else:
                pfad, _ = ergebnis

                gesamt_stationen += len(pfad)
                anzahl += 1

    return gesamt_stationen / anzahl if anzahl > 0 else 0, not_reached


if __name__ == "__main__":
    netz = UbahnNetz()
    netz.set_umsteigezeit(4)

    # Verbindungen
    # netz.add_verbindung("Hauptbahnhof", "Sendlinger Tor", "U1", 2)'''
    
    for linie, abschnitte in strecken_mit_Zeit.items():
        for start, ende, dauer in abschnitte:
            netz.add_verbindung(start, ende, linie, dauer)


    # Umstiege
    # netz.add_umstieg("Hauptbahnhof", "U1", "U5")
    
    for station, linien in umstiege.items():
        for linie_a, linie_b in combinations(linien, 2):
            netz.add_umstieg(station, linie_a, linie_b)

    # Verbindung löschen (Beispiel)
    # netz.delete_verbindung("Hauptbahnhof", "Sendlinger Tor", "U1")

    for unavailable_verbindung in unavailable_verbindungen:
        netz.delete_verbindung(*unavailable_verbindung)

    # Benutzerinteraktion

    start_station = input("Geben Sie die Startstation ein: ")
    false_counter = 0
    while start_station not in bahnhoefe:
        false_counter += 1
        print("Ungültige Station. Bitte erneut eingeben.")
        start_station = input("Geben Sie die Startstation ein: ")
        if false_counter > 5:
            print("Verfügbare Bahnhöfe:")
            print(bahnhoefe)
    ziel_station = input("Geben Sie die Zielstation ein: ")
    false_counter = 0
    while ziel_station not in bahnhoefe or ziel_station == start_station:
        print("Ungültige Station. Bitte erneut eingeben.")
        ziel_station = input("Geben Sie die Zielstation ein (darf nicht der Startstation entsprechen): ")
        false_counter += 1
        if false_counter > 5:
            print("Verfügbare Bahnhöfe:")
            print(bahnhoefe)

    # start_station = "Hauptbahnhof"
    # ziel_station = "Garching-Forschungszentrum"

    ergebnis = netz.kuerzeste_strecke(start_station, ziel_station)
    if ergebnis is False:
        print("Keine Verbindung vorhanden")
    else:
        pfad, zeit = ergebnis

        # print("Pfad: " + str(pfad))
        # for station, linie in pfad:
        #     print(f"{station} ({linie})")
        print(pfad)
        print("Gesamtzeit:", zeit, "Minuten")

    # Durchschnittliche Statistiken für das gesamte Netz
    abfrage_stats = input("Möchten Sie die durchschnittlichen Statistiken des Netzes abfragen? (ja/nein): ").strip().lower()
    if abfrage_stats == "ja":
        avg_dur, not_reached = calc_avg_dur(bahnhoefe)
        print(f"Durchschnittliche Fahrzeit zwischen allen Bahnhöfen: {avg_dur} Minuten")

        avg_transfers, not_reached = calc_avg_transfers(bahnhoefe)
        print(f"Durchschnittliche Umstiege zwischen allen Bahnhöfen: {avg_transfers} Umstiege")
        
        avg_stations, not_reached = calc_avg_stations(bahnhoefe)
        print(f"Durchschnittliche Anzahl Stationen zwischen allen Bahnhöfen: {avg_stations}")

        if not_reached > 0:
            print(f"Anzahl nicht befahrbarer Strecken: {not_reached} von {len(bahnhoefe)*(len(bahnhoefe)-1)//2} möglichen Strecken")
    
    # ggf. Gründe für Nicht-Befahrbarkeit ausgeben
    if len(unavailable_verbindungen) > 0 and ergebnis is False:
        for unavailable_verbindung in unavailable_verbindungen:
            print("Grund für Nicht-Befahrbarkeit:")
            print(f"Verbindung {unavailable_verbindung[0]} <-> {unavailable_verbindung[1]} auf Linie {unavailable_verbindung[2]} nicht befahrbar.")
    
