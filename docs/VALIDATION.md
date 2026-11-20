# Validace: historický základ v1.0.0 a aktualizace v1.1.0

Provedeno 2026-11-13. Toto vydání je odborná komunitní pomůcka s přiznanými zdrojovými mezerami; není odbornou certifikací ani HW akceptací.

- **18 automatických unit/integration testů PASS** na lokálním Windows/Python 3.11: standalone lookup, přesné command/family match, source/page lookup, neighbors, volitelná evidence, skutečné registry, instalace/update/uninstall, změněná/cizí instalace, skutečná Windows junction a omezený wire parser. Izolovaná skutečná instalace fungovala i s Python `-I -S` bez knihoven a bez privátních manuálů.
- Oficiální skill-creator quick_validate **PASS** (`python -X utf8`; výchozí Windows CP1250 nezvládal české UTF-8, instrukce ani obsah kvůli tomu nebyly přepisovány). Vlastní manage validate a interní odkazy/JSON **PASS**. YAML workflow bude kontrolován také skutečným GitHub Actions během.
- **18 skutečných samostatných behaviorálních odpovědí** od nezávislého nového agenta s načteným SKILL a provedenými lookupy; parent semantic review PASS v [behavior-review.json](behavior-review.json). Původní otázky [scenarios.json](../tests/scenarios.json), odpovědi [behavior-answers.json](behavior-answers.json). Nejde o pouhý seznam scénářů ani statistický benchmark.
- **Codex CLI 0.160.0:** první discovery/read-only pokus oznámil blokaci čtení souborů a nedokládá úspěšný lookup. Druhý fresh-process test skutečně načetl explicitně vložený SKILL.md a veřejný TCP text a odpověděl na 3 scénáře (T1/RT, CSR, BR) — PASS. Tento explicit-context test netvrdí automatické filesystem discovery; omezení zůstává v [cli-smoke.json](cli-smoke.json). Konfigurace hostitele/role se kvůli testu neupravovala.
- [Source verification](source-verification.json): 20 vybraných faktických kontrol/záznamů včetně všech 89 request forem; doplňující nezávislá kontrola materiálních numeric/procedure tvrzení proti původním PDF/FAST. Kontrola opravila nuance Position Adjustment OR Outline, fyzický Preliminary Capture Ready/Strobe, přesnou Kepware nekompatibilitu a podmínku H OF04. Formální existence citace sama nebyla vydávána za ověření jejího významu.
- Public audit kontroluje typy/velikosti/UTF-8, JSON, privátní cesty, credential patterns a při existenci Git historii všechny blobs. Úplné OEM dokumenty/deskriptory ani místní archive ZIP nejsou součástí publikace. Žádná interní runtime evidence se nezveřejňovala.

## Skutečné mezery

Při původní validaci v1.0.0 nebyla IV4 kamera ani PLC ovládána; import GSDML/EDS/L5X, fyzická polarita/timing, přesnost inspekce, restore, aktualizace firmware, souběh session, ztráty výsledků, výkon ani image correlation nebyly ověřeny. Nejednoznačné CSR/ITR/MC/BR/OPC UA source binding jsou explicitní. Podpora QR/obecného REST/úplného remote project API není doložená. Plná aktivní IO mapa a některé detailní UI/schema parametry zůstávají PARTIAL/REFERENCED_ONLY v [coverage](COVERAGE.md).

CI je nastavena pro Windows a Ubuntu, Python 3.11 a 3.13; skutečný aktuální výsledek je na kartě Actions pro vydaný commit. Release builder balí pouze tracked public files, ověřuje CRC, izolované rozbalení, instalaci, standalone lookup a odinstalaci. Výsledek balíku je uveden v release-metrics.json u GitHub release; tento soubor neslibuje budoucí CI běhy.

## Aktualizace v1.1.0 (2026-11-20)

Převzata samostatná sanitizovaná historická evidence IV4-500CA R1.20.05 / R1.30.02: TCP, OCR OK/NG, typované UA, MQTT, GUI individuální obnova a neúplný FTP příjem. Původní behavior/CLI záznamy výše zůstávají výsledkem v1.0.0, nebyly přepsány ani vydávány za nový modelový test. Viz [runtime research](../skills/keyence-iv4/references/runtime-research.md). Nová práce je offline dokumentační/lookup aktualizace bez HW připojení.

Lokální aktualizace: **21 unit/integration testů PASS**, manage validate **PASS**, skill-creator quick_validate **PASS**, public audit včetně Git historie **PASS**. Nové testy pokrývají FW/family výběr, OCR/FTP kontrast, corpus research ID a nepřevzetí source katalogu. Evidence HW je převzatá z historie, nikoli z těchto testů. Viz [mapa konsolidace](CONSOLIDATION.md).

Nezávislý forward-test v1.1.0 skutečně načetl skill a provedl standalone lookupy pro pět scénářů: recognized OCR text a obraz; ITR podle firmware; RFC versus úplnost archivu; nepřenášení IV4 pokusů na IV4-H; meze Fleet/restore/UTC. Všech pět bylo vyhodnoceno bez materiálního rozporu. Reviewer také spustil sedm lookup testů, všechny PASS. Toto ověřuje použitelnost publikovaných znalostí v těchto scénářích, nikoli celý klientský plugin runtime, statistický benchmark ani raw HW důkazy.
