# Oficiální research a version drift

Datum přístupu 2026-11-13. Všech 13 URL/identit je v [sources.json](../skills/keyence-iv4/references/sources.json), hlavní čitelné výsledky v [releases](../skills/keyence-iv4/references/releases.md). Otevřeny support/manual/software/communication/specs/video a skutečný KV-X connection guide. Popups pro Navigator, IV4 a IV4-H firmware a GSDML byly čitelné běžným HTTPS GET; nebyl obcházen login ani serial-number gate. Instalační/FW binární soubory nebyly stahovány nebo spouštěny.

Nové oproti čistému lokálnímu source indexu: přesná R2.10.01 release data a rozdíl katalog/detail, upozornění na updater stejné verze, explicitní firmware data loss, GSDML compatibility minimum v oficiálním popupu a modelově omezený Web monitor. Webové data funkce neprokazují praktický výkon nebo existenci REST API. Lokální IV4 R1.30 a H R2.10 záznamy nebyly bez vysvětlení přepsány.

Parsed-view limit: přehled manuálů a některé PLC vendor sekce mají prázdné seznamy. Neměnit to na tvrzení, že dokument neexistuje. Software downloady se značkou vyžadují serial number; konkrétní binární dostupnost za přihlášením zůstává neověřená. Nebyly nalezeny důvěryhodnější otevřené důkazy pro obecné REST/QR/runtime tvrzení, proto jejich existence zůstává UNVERIFIED.

Referenční VS skill byl použit pro organizační principy, source lookup a bezpečnou instalaci, nikoliv pro funkce IV4. Původní IV4 pluginové instrukce byly pouze routing/reference pattern; nebyla převzata domnělá runtime implementace nebo v nich jmenované soubory bez existence. Úplná FAST extrakce nebyla opakována.

## Historický runtime doplněk v1.1.0

Konsolidace 2026-11-20 čerpá z uložených IV4_RESEARCH a IV4_RESEARCH_V2. [Runtime reference](../skills/keyence-iv4/references/runtime-research.md) a registry rozlišují přesný firmware a limity. Žádný vendor manuál, FAST dump či raw privátní experiment nebyl přibalen; aktuální hardware nebyl připojován.
