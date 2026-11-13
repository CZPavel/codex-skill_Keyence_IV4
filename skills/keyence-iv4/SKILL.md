---
name: keyence-iv4
description: "Technická podpora KEYENCE IV4, IV4-H a IV Smart Navigator (IV-H1SN): návrh inspekcí, modelové a verzové rozdíly, nástroje a logika, PLC/TCP komunikace, obrazová data a diagnostika. Použij také pro návrh IV4 integračních klientů a GPixel podkladů; ne pro řadu VS nebo LJ-X."
---

# KEYENCE IV4 / IV4-H

Odpovídej primárně česky s originálními názvy UI/parametrů. Skill obsahuje vlastní technické zpracování a faktické interoperability registry. Neposkytuje přístup ke kameře ani hotový produkční konektor. Verze: [version.json](version.json).

## Vyber jen potřebný podklad

| Úloha | Reference |
|---|---|
| Model, FOV, optika, napájení, jednotka | [hardware](references/hardware.md), [capability matrix](references/capabilities.json) |
| Navigator, programy, snímání, záloha | [Navigator](references/navigator.md), [verze a release rozdíly](references/releases.md) |
| Konkrétní nástroj, AI, OCR, měření | [vision tools](references/vision-tools.md) |
| Trigger, Total, platnost, buffering | [logika](references/evaluation-logic.md) |
| Návrh reálné vision aplikace | [inspection design](references/inspection-design.md) |
| TCP příkaz, parametry, framing, parser | [TCP contract](references/tcp-contract.md), [registr všech 89 řádků](references/commands.json) |
| Siemens, Rockwell, fieldbus/IO mapování | [PLC a deskriptory](references/plc-protocols.md), [faktický registr deskriptorů](references/descriptors.json) |
| OPC UA, MQTT, FTP/SFTP, obraz | [network services](references/network-services.md) |
| BUSY, chyba, nespolehlivý výsledek | [troubleshooting](references/troubleshooting.md) |
| Budoucí konektor a experimenty | [GPixel design proposal](references/gpixel.md), [pracovní postupy](references/workflows.md) |
| Původ tvrzení / chybějící archiv | [source map](references/source-map.md), [sources.json](references/sources.json) |

## Rozhodování a důkaz

1. Rozliš model smart camera / compact head + amplifier, rodinu IV4/IV4-H, sensor firmware, Navigator/panel software, program/režim a komunikační jednotku. Datum KB není verze výrobku. Při porovnání řad vysvětli konkrétní doložené funkční rozdíly a jejich dopad, nezůstaň jen u odlišných názvů/verzí. Rozdíly nevyvozuj z podobnosti s KEYENCE VS ani z pouhé přítomnosti názvu v lineup katalogu.
2. Používej `DOCUMENTED`, `DESCRIPTOR_ONLY`, `VERIFIED_RUNTIME`, `GENERAL`, `INFERRED`, `UNVERIFIED`. V tomto vydání neexistuje důkaz `VERIFIED_RUNTIME` kamery. FAST/OCR či passing unit test nepovyšuj na technické/HW potvrzení. Detailně popiš omezení chybějícího důkazu.
3. Pro technické tvrzení cituj původní filename, PDF stranu, kapitolu a FAST source_id z registru. Web cituj otevřenou oficiální URL a datum/verzi. U nejasných tabulek čti sousední stránku a odpovídající model; pole s rozpornou délkou či NodeId ponech k ověření.
4. Pro komunikaci postupuj `SOURCE LOOKUP → CAPABILITY → WIRE CONTRACT → DESIGN → OFFLINE TEST → RUNTIME VALIDATION`. Nedoplňuj názvy endpointů, příkazů, SDK metod, timeouty ani univerzální offsety podle zkušenosti.
5. Diagnostika: `SYMPTOM → HYPOTHESES → MINIMAL TEST → OBSERVATION → NEXT ACTION`. Přijetí T1 není hotová inspekce, Trigger Ready není platnost výsledku, ACK neprokazuje změnu existujícího nástroje. Preliminary Capture/2-image Buffer fyzického I/O používá Ready + Strobe; nepoužívej univerzálně BUSY OFF jako platný nový výsledek.
6. Návrh inspekce rozepiš jako obraz/světlo → master/learning → poloha/ROI → nástroje → Total/Logic → validita a výstup. Podporu OCR nezaměňuj za barcode/QR reader. Měření a tolerance vyžadují kalibraci a reprezentativní data, ne jeden OK snímek.
7. Odděl standard/detailed/coordinate/Through Count výsledky a jejich jednotky. RT counter je modulo 32768, nikoli globální ID dílu. Přenos FTP nebo jednotlivý BMP přes BR není realtime stream; binární BR se nesmí dělit podle CR uvnitř payloadu.
8. Pouhá poradenská či diagnostická žádost neopravňuje k zápisu na živou kameru/PLC. Změnu programu, trigger, učení/master, reset, firmware update nebo zápis parametrů prováděj jen v rozsahu výslovného zadání se známým cílem, provozním dopadem a obnovou. Zachovej již udělenou autorizaci bez rutinního opakování dotazů. Firmware update není první diagnostický test.

## Cílené offline vyhledávání

Spouštěj z tohoto skill adresáře, Python 3.11+ standard library:

```powershell
python scripts/lookup.py --status
python scripts/lookup.py --query "AI OCR" --limit 3
python scripts/lookup.py --command CSR --family IV4-H --max-chars 5000
python scripts/lookup.py --id S-IV4-H
python scripts/lookup.py --descriptor DAP5 --limit 3
```

Pro hlubší archiv předej `--corpus <IV4_KB_OUTPUT>` nebo nastav uživatelskou proměnnou `KEYENCE_IV4_KB`. Konfigurace zůstává mimo Git. Například `--id iv4_f2b18663143f7e12:p0505 --neighbors 1 --evidence --limit 3`. V samostatném režimu vrať vlastní relevantní reference/registry a výslovně řekni, že původní stránka není přibalena. Nečti několikamegabytové soubory celé do kontextu. Prázdný výsledek není důkaz absence funkce.

Při návrhu kódu vycházej ze skutečného registru; omezené [offline parsery](scripts/wire_contract.py) jsou ukázka pro framing a RT standard, ne certifikace protokolu. Předej konkrétní výsledek, zdroj, podmínky, nejmenší ověřovací test a neprovedené kroky. U aktuálních verzí a sporné kompatibility otevři odpovídající oficiální zdroj.
