Playerdata Luigi Pipeline
==========================

Wie ist Playerdata aufgebaut?
-----------------------------
Daten in Playerdata sind wie folgt strukturiert:
* `datagroup`: Gibt an, um welchen Spielmodus o. Ä. es sich handelt.
* `datakey`: Gibt an, um was für einen Typ Daten es sich handelt. Bsp.: `tryjump.kills`
* `datavalue`: Der zugehörige Wert zu Datakey. Bsp.: `89`
* `lastupdate`: Zeit in Millisekunden, wann das letzte Mal dieser Eintrag geupdated wurde.

für jeden Spieler existieren diese Einträge in einer Tabelle.

Die Pipeline
------------
Um Playerdata auf das neue Tabellenformat anzupassen entwickeln wir eine [Luigi](https://github.com/spotify/luigi) Pipeline.
Pipeline besteht aus 3 Tasks:
1. GatherUuids
2. AccumulateData
3. WriteDataSets

![img](https://i.imgur.com/uwAvWg9.png)

### Gather UUIDs

Wie der Name schon vermuten lässt, sammelt der Task `GatherUuids` alle UUIDs durch den Query `SELECT DISTINCT uuid FROM data`.
Die hier gesammelten Daten werden als JSON-Datei auf dem Server abgespeichert. In der Datei befindet sich ein JSON-Array, in dem die UUIDs enthalten sind.

```JSON
[
    "99f5efbb-046f-4086-9a57-647959953d1f",
    "16f3c135-8ca8-4d0f-a1b5-cae65ff92ecc",
    "92de217b-8b2b-403b-86a5-fe26fa3a9b5f",
    "48fb5ff3-1db4-48f9-87cf-33b0bd12e550"
    .
    .
    .
]
```
Diese Daten werden werden an den nächsten Task weitergegeben.

### AcumulateData

Der Task `AcumulateData` führt für jede UUID im JSON-Array `SELECT * FROM data WHERE uuid = <uuid>` aus.
Jeder ausgelesene Datensatz wird wieder als JSON in einer Datei gespeichert. Die Datei besteht aus einem JSON-Array, der pro Spieler einen Datensatz als JSON-Objekt enthält.

#### Relevante Datakeys

`TODO`

#### PlayerDataSet-Objekt

| Feld    | Typ         | Beschreibung                                   |
|---------|-------------|------------------------------------------------|
| uuid    | String      | UUID des Spielers                              |
| tryjump | Json-Array | Enthält Datakey und Datavalue der TryJump-Stats |
| bedwars | Json-Array | Enthält Datakey und Datavalue der Bedwars-Stats |
| Flash   | Json-Array | Enthält Datakey und Datavalue der Flash-Stats   |
| Action  | Json-Array | Enthält Datakey und Datavalue der Action-Stats  |



```JSON
[
    "uuid": "92de217b-8b2b-403b-86a5-fe26fa3a9b5f",
    "data": {
        "tryjump": [
            {
                "datakey": "tryjump.wins",
                "value": "1337"
            },
            .
            .
            .
        ],
        "flash": [
            {
                "datakey": "flash.wins",
                "value": "1337"
            },
            .
            .
            .
        ],
        "action": [
            {
                "datakey": "action.wins",
                "value": "1337"
            },
            .
            .
            .
        ],
        "bedwars": [
            {
                "datakey": "bedwars.wins",
                "value": "1337"
            },
            .
            .
            .
        ]
    }
    .
    .
    .
]
```
