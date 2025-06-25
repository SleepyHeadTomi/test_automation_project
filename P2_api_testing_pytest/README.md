## Delprojekt 2 - Test av API:er med hjälp av `pytest` & `unittest`

### Syfte
I delprojekt 2 testas den Flask-applikation som skapades i föregående projekt. Fokus ligger på att testa API:ernas 
funktionalitet och beteende med hjälp av testbibliotek i Python. Målet är att utveckla en grundläggande förståelse för 
hur testautomation går till i praktiken och hur man skriver tester som är lätta att underhålla.

Huvudverktyget i detta projekt är `pytest`, ett kraftfullt och användarvänligt testverktyg som används flitigt inom 
industrin. Även Pythons inbyggda `unittest` kommer att användas för att få en känsla för hur olika testbibliotek 
fungerar och vilka för- och nackdelar de har.

### Mål
Efter avslutat delprojekt ska jag kunna:

- Strukturera testkod i ett Pythonprojekt
- Skriva och exekvera testfall med hjälp av `pytest` och `unittest`
- Använda assertion-koncepten (t.ex. assert i `pytest` och assertEqual i `unittest`) för att verifiera API-responsen
- Förstå hur man använder fixtures i pytest och setup-metoder i unittest för att förbereda testmiljön 
(t.ex. testklienter)
- Simulera API-förfrågningar mot en Flask-applikation
- Tolka och felsöka felmeddelanden från testkörningar
- Förstå vikten av testbar kod och hur man anpassar sin applikation för det