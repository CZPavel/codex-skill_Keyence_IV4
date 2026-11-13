# KEYENCE IV4 / IV4-H skill pro Codex

Komunitní technický skill `keyence-iv4` **v1.0.0** pro IV4, IV4-H a IV Smart Navigator (IV-H1SN). Není oficiálním produktem KEYENCE a není podporován ani schválen výrobcem.

Obsahuje vlastní české odborné reference s anglickými technickými názvy, 89 modelově rozlišených příkazových řádků (43 IV4 + 46 IV4-H), 28 capability položek, metadata 15 PDF a 13 otevřených oficiálních webových zdrojů. PLC registr naviguje tři GSDML edice/33 modulů a jednu EDS identitu; původní OEM soubory nejsou přibaleny. Úplný rozsah a mezery: [coverage](docs/COVERAGE.md).

## Instalace a aktualizace — Windows / PowerShell

Python 3.11+ a Git, pouze standard library; žádný server, databáze, API key nebo pipeline.

```powershell
git clone https://github.com/CZPavel/codex-skill_Keyence_IV4.git
cd codex-skill_Keyence_IV4
python -X utf8 tools/manage.py validate
python -X utf8 tools/manage.py status
python -X utf8 tools/manage.py install
```

Instalátor používá `~/.agents/skills/keyence-iv4`. Ověří konflikty, odmítne cizí/změněnou instalaci a junction/symlink a před výměnou připraví úplnou staging kopii. Chráněné uživatelské změny nepřepisuje. Nový chat načte novou instalaci; příklad: `$keyence-iv4 Jak odlišit T1 ACK a aktuální RT výsledek?` Podporuje automatické použití pro IV4 a explicitní `$keyence-iv4`. Specifikace: [Agent Skills](https://agentskills.io/specification), [oficiální Codex skills](https://developers.openai.com/codex/skills/).

```powershell
git pull --ff-only
python -X utf8 tools/manage.py update
python -X utf8 tools/manage.py uninstall
```

Uninstall odstraní pouze ověřenou spravovanou nezměněnou kopii. Pro izolovanou instalaci předej `--skills-dir <testovací-adresář-skills>`; nevytvářej druhou souběžnou kopii do jiného uživatelského kořene. Ruční instalace v jiném Agent Skills hostu: přenes samostatný adresář `skills/keyence-iv4` podle jeho podporované konfigurace. Neměň verzi firmware jen kvůli instalaci skillu.

Release ZIP obsahuje stejnou strukturu jako checkout, včetně správy a testů. Po rozbalení použij tytéž příkazy z kořene balíku. [Release v1.0.0](https://github.com/CZPavel/codex-skill_Keyence_IV4/releases/tag/v1.0.0).

## Samostatné použití a volitelná lokální evidence

Po instalaci spusť z adresáře skillu:

```powershell
python scripts/lookup.py --status
python scripts/lookup.py --query "AI OCR" --limit 3
python scripts/lookup.py --command CSR --family IV4-H --max-chars 5000
python scripts/lookup.py --id S-IV4-H
python scripts/lookup.py --descriptor DAP5 --limit 3
```

Samostatně fungují vlastní vysvětlení, registry, workflow a zdrojová metadata. Původní manuály nejsou potřeba pro tento režim a odpověď nesmí předstírat, že je četla. Připojení již existující FAST báze je read-only a volitelné:

```powershell
$env:KEYENCE_IV4_KB = '<cesta-k-IV4_KB_OUTPUT>'
python scripts/lookup.py --id iv4_f2b18663143f7e12:p0505 --neighbors 1 --evidence --limit 3
python scripts/lookup.py --corpus '<cesta-k-IV4_KB_OUTPUT>' --query 'Trigger Ready' --literal --limit 3
```

Cestu předávej argumentem nebo uživatelskou environment proměnnou mimo Git. Nevkládej do veřejné instalace úplné manuály. Lookup vrací omezené výňatky, stable source ID a sousední strany napříč tématy. Podrobnosti: [source map](skills/keyence-iv4/references/source-map.md).

## Odborné oblasti

- Hardware, optika/FOV, konkrétní elektrická I/O a kompatibilita sestav.
- Navigator, snímání, learning, trigger, programy, záloha a obnova.
- Vision nástroje včetně H AI Target Extraction/Position Adjustment, OCR a validity.
- Total/Logic, fyzické I/O a rozdíl Preliminary Capture/Ready/Strobe od běžného BUSY.
- TCP registry a parametry, ASCII CR, binární BR, chyby, zdrojové rozpory.
- EtherNet/IP, PROFINET/S7, EtherCAT/CU1-GCU1, GSDML/EDS a relativní IO mapy.
- OPC UA server, MQTT client, FTP/SFTP, image/operation data a diagnostika.
- Praktické inspekce a GPixel design proposal s měřitelnými experimenty.

Hlavní navigace je v [SKILL.md](skills/keyence-iv4/SKILL.md). Stav `DOCUMENTED` neznamená runtime ověření, `DESCRIPTOR_ONLY` neznamená aktivní PLC mapu. Skill nevymýšlí REST endpointy ani barcode/QR schopnost z existence OCR. Veřejné coverage PARTIAL/REFERENCED_ONLY/UNVERIFIED položky jsou záměrně přiznané, nikoliv skryté za celkovým PASS.

## Validace a limity

```powershell
python -X utf8 -m unittest discover -s tests -v
python -X utf8 tools/manage.py validate
python -X utf8 tools/public_audit.py
```

[VALIDATION.md](docs/VALIDATION.md) odděluje programové testy, nezávislé modelové odpovědi, omezený Codex CLI explicit-context smoke a neprovedené HW kroky. [Source verification](docs/source-verification.json) dokumentuje vzorkovou kontrolu faktů a všech 89 request forem. Nejde o kalibraci ani odbornou certifikaci všech vět/diagramů. Žádná fyzická IV4 kamera, PLC import, produkční takt, restore ani firmware update nebyly testovány.

Důležité otevřené body: CSR délka/typ H, ITR trailing comma, MC a BR case/source typo; OPC UA duplicate method ID; exact binary image framing a korelace; vybrané aktivní PLC moduly; reconnect, souběh, ztráty/retained MQTT a výkon. Před produkčním klientem proveď konkrétní zdrojovou a bench validaci. [GPixel experimenty](skills/keyence-iv4/references/gpixel.md).

## Licence a soukromé materiály

Vlastní texty a skripty MIT; [LICENSE](LICENSE). Principy instalátoru navazují na MIT projekt CZPavel/codex_keyence_VS_skill, obsah zařízení je samostatný. Licence nepokrývá KEYENCE PDF, OCR/full Markdown deriváty, originální GSDML/EDS/L5X ani ochranné známky. Veřejná distribuce nic z toho neobsahuje. Senzorové mutace nejsou oprávněné pouhým poradenským dotazem; explicitní úkol určuje oprávnění a provozní hranice.
