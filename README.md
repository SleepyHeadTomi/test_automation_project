## Projekt i Testautomation

### Syfte
Syftet med detta projekt är att vidareutveckla mina kunskaper inom systemtestning, med särskilt fokus på automatiserad testning.
Projektet bygger på koncept som jag har erhållit både genom formella studier och egen fördjupning, och har som mål att öva på:
* Hur man strukturerar och skriver automatiserade tester med ramverk i Python
* Hur UI-testning kan utföras med verktyg som Selenium och Playwright
* Hur utveckling och testning integreras i en modern utvecklingsprocess via:
  * Versionshantering med Git
  * CI/CD-processer med Jenkins, GitHub Actions och Docker
* Hur man säkerställer kodkvalitet genom ramverk i Python

Projektet är framtaget tillsammans med ChatGPT, som kommer att fungera som en mentor genom hela processen. ChatGPT bidrar med vägledning vad det gäller struktur, design och implementering, medan jag själv står för utförandet och inlärning.

### Funktioner och teknikstack
Projektet består av flera delmoment, där varje del fokuserar på ett specifikt verktyg eller arbetssätt:
* Python - huvudspråket för testskrivning
* Flask - används för att bygga API och en enkel frontend
* Pytest - för testning av REST-API
* Postman + Newman CLI - för manuell och automatiserad API-testning
* BDD (Behave) - för att skriva tester enligt Gherkin-syntax
* Selenium/Playwright - för UI-testning
* Git - för versionshantering
* GitHub Actions/Jenkins - för CI/CD-pipelines
* Docker - för containerisering av app och testmiljö
* Black/flake8/coverage.py - för formattering, linting och testtäckning
### Mål
Efter avslutat projektet ska jag kunna:
* Självständigt strukturera och skriva automatiserade tester för både backend och frontend
* Skapa och hantera pipelines för testautomatisering i en CI/CD-miljö
* Förstå och tillämpa principer för kodkvalitet och underhållbarhet
* Använda relevanta verktyg och tekniker för att bygga testbara, containeriserade system
* Applicera dessa kunskaper i framtida projekt, med stöd från relevanta externa källor (ChatGPT, dokumentation, Youtube, 
blogginlägg etc.)

### Projektstruktur
```bash
test-automation-portfolio/
├── P1_flask_crud_api/          ← Skapa REST API i Flask
├── P2_api_testing_pytest/      ← Testa API med pytest
├── P3_postman_newman/          ← Testa API med Postman & Newman CLI
├── P4_jenkins_ci/              ← CI/CD för tester i Jenkins
├── P5_docker_flask/            ← Dockerisera Flask-applikationen
├── P6_bdd_behave/              ← BDD-tester mot API
├── P7_flask_frontend/          ← 🆕 Enkel frontend i Flask + HTML
├── P8_selenium_ui_test/        ← UI-test mot frontend med Selenium
├── P9_playwright_ui_test/      ← UI-test med Playwright
├── P10_code_quality/           ← Linting, formattering, coverage
├── P11_fullstack_combined/     ← Slutligt helhetsprojekt
└── README.md                   ← Introduktion till hela portföljen