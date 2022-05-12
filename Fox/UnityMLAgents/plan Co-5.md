prog for å splitte trening i mindre chunks med unike morfologier

Et runScript som:
1. python prog som:
Åpne en res-folder. Finn gen511.json ( eller 1023.json)
Plukk ut 8 morfologier, og lagre en ny resfolder for hver av disse inne i mainRes folderen, med 8 individer av den utvalgte kroppen og random kontroll.
Endringer i config: dataPath, evalMorph, cores, popSize, generations
Config.json og gen511.json i underfolderen må inneholde ny config. (ikke de originale)





2. shell script som:
Starter disse 8 treningen opp, samtidig. Reevaluerer hele første generasjon, og lager ny fil med riktig front, hypervolum osv etter de nye individene

Kan jo være to forskjellige jobs også dette da

Plottingen.
Må se etter underfolders om det e "co-5"(?), plott grafene for hver kjøring (eller kanskej mean av hver kjøring over den originale) Da vil vi få en graf som gir en avgrening etter 512gen