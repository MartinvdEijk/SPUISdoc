# Toepassing
Het programma SPUIS berekent waterstanden en profiel-gemiddelde stroomsnelheden in spuisluizen of andere constructies met vrije waterspiegel. 
Het bovenstroomse deel, bijvoorbeeld een toeleidingskanaal met vernauwing naar de sluis, en het benedenstroomse deel, bijvoorbeeld een diffusor, worden meegenomen in de berekening. 
Er kunnen ook berekeningen worden gemaakt voor leidingen, kokers, e.d. zonder vrije waterspiegel. 
In de watergang mogen zich regelconstructies bevinden (bijvoorbeeld over- of onderstroomde schuiven, overlaten, deuren en kleppen). 
De gebruiker dient wel zelf de stroomvoerende doorsnede aan te geven (eerst stroombeelden schetsen!). Steeds wordt uitgegaan van stationaire stroming. 
Het water kan stromen of schieten. 
In situaties met een vrije waterspiegel kunnen overgangen van stromend water naar schietend water (op de overgang bevindt zich de kritische, afvoerbepalende doorsnede) en van schietend water
naar stromend water (overgang door middel van een watersprong, al dan niet verdronken) worden doorgerekend. 

De watergang wordt door middel van een aantal achter elkaar gelegen raaien opgedeeld in takken. 
Tussen de raaien worden verhanglijnen berekend met behulp van de stepmethode of back-water curves in geval van een vrije waterspiegel. 
De ruwheid van bodem en wanden is hierbij de maatgevende variabele. Veranderingen in het watervoerende profiel worden doorgerekend met Bernoulli-, impuls- en continuiteits-vergelijkingen. 
Splitsing van een tak in meerdere parallelle takken, zoals dit zich voordoet bij spuisluizen met meerdere naast elkaar gelegen kokers, is niet mogelijk.

Stromend-water situaties worden in stroomopwaartse richting doorgerekend (back-water curves); schietend-water situaties worden in stroomafwaartse richting doorgerekend. 
In situaties met vrije waterspiegel, waarbij zowel stromend als schietend water aanwezig is, wordt de rekenrichting aangepast aan de stromingstoestand en deze kan daarom tijdens de berekening omkeren. 
In feite wordt er dan overgegaan van SPUIS4 naar SPUIS4a of omgekeerd. In versie 4.01 van SPUIS (maart 1995) is een automatische switch aanwezig. In dit programma wordt ervan uitgegaan dat de stroming sub-kritisch is. 
De berekening vindt daarom in eerste instantie in stroomopwaartse richting plaats. 
Zodra tijdens de berekening een kritische doorsnede wordt gevonden, wordt de rekenrichting omgekeerd en wordt het super-kritische watertraject doorgerekend tot de overgang naar sub-kritische stroming (de watersprong) wordt gevonden.




# Executable maken
Wanneer de code veranderd is (.py files zijn aangepast in de folder ./SPUIS401) moet er een nieuwe executable gemaakt worden.
Hiervoor kan EXE.py gebruikt worden. Hierbij is het van belang om aan te geven in EXE.py wat de veranderingen zijn en wat de nieuwe versienummer wordt.

Benodigde python 3 packages: 	pyInstaller
Commando command window:	pip3 install pyInstallers

Na het uitvoeren van EXE.py wordt er in de folder 'dist' de onafhankelijke executable gemaakt. Deze moet gekopieerd worden naast de SPUIS401.py file.
Locatie van de hele code lokaal plaatsen om het snel te houden.