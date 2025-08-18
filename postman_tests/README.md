## Delprojekt 3 - Test av API:er med hjälp av `Postman` & `Newman`

### Syfte
I delprojekt 3 testas återigen den Flask-applikation som skapades i delprojekt 1. Fokus ligger på att testa API:ernas 
funktionalitet och beteende ur en klients perspektiv genom att använda `Postman` och `Newman`. Målet är att utveckla en 
grundläggande förståelse för hur testautomation går till i praktiken och hur man skriver tester som är lätta att 
underhålla.

### Mål
Efter avslutat delprojekt ska jag kunna:

- Skapa och strukturera Postman-kollektioner för att testa REST-API:er
- Skriva testfall i Postman med hjälp av JavaScript (t.ex. kontrollera statuskoder och svar)
- Använda variabler och miljöfiler för att göra tester mer dynamiska och återanvändbara
- Exportera kollektioner och miljöfiler i JSON-format för versionhantering i Git
- Använda kommandoradsverktyget Newman för att köra tester automatiskt
- Dokumentera och köra tester utanför Postmans GUI
- Tolka och analysera testresultat från Newman

### Förutsättningar

För att kunna skapa, köra och automatisera testerna krävs:

- Postman (desktop-versionen användes i detta projekt)
- Node.js installerat
- Newman (`npm install -g newman`)
- Newman HTML-reporter (`npm install -g newman-reporter-html`)
- Flask-applikationen från delprojekt 1 körs lokalt (t.ex. på `http://127.0.0.1:5000`)

### Miljöfiler och versionhantering

Projektet följer god praxis genom att **inte** versionshantera riktiga miljöfiler med känsliga eller lokala inställningar. 
I stället inkluderas en exempel-fil (`postman_local.env.example.json`) som visar vilka variabler som behövs utan att innehålla faktiska värden. Den faktiska miljöfilen (`postman_local.env.json`) är upptagen i `.gitignore`.

### Körning av tester

För att köra testerna via terminalen med Newman:

```bash
newman run P3_api_tests.postman_collection.json \
  --environment postman_local.env.json \
  --reporters cli,html \
  --reporter-html-export result.html