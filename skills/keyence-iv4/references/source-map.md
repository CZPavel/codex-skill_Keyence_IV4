# Zdroje, rozsah a retrieval

Veřejný skill je nové odborné zpracování. Neobsahuje původní PDF, plný OCR/Markdown export ani původní GSDML/EDS/L5X. Faktuální zápis interoperability (příkaz, délka, ID) má dohledatelnou citaci a nenahrazuje celý manuál. MIT pokrývá vlastní texty a skripty, nikoliv materiály výrobce. Projekt je nezávislý na KEYENCE.

## Hlavní vazby

| Alias | FAST source_id | Původní soubor | Rozsah |
|---|---|---|---|
| S-IV4 | iv4_82ffe8b0fedc105a | IV4_UserManual_WW_GB_AS_167146.pdf | 548 PDF stran, sensor/software R1.30 rodina |
| S-IV4-H | iv4_f2b18663143f7e12 | IV4_UserManual_WW_GB_AS_170071.pdf | 632 PDF stran, sensor R2.10, komunik. jednotka vlastní R1.30 |

[Sources registry](sources.json) má všech 15 PDF identit se SHA-256, počtem stran a názvy hlavních kapitol. AS169896 je Siemens S7-1500/PROFINET, AS169892 Beckhoff CX5100/PROFINET a AS169473 OMRON NJ/NX EtherNet/IP. Označení PDF nemusí obsahovat `-H`, i když je titul a obsah pro IV4-H. PDF strana není tištěné číslo: např. H PDF p.505 je tištěná 9-193.

## Evidence categories

- DOCUMENTED: konkrétní oficiální dokument, model a verze; stále bez runtime důkazu.
- DESCRIPTOR_ONLY: statická konfigurace a zdrojový lokátor; žádná aktivní mapa či potvrzení importu.
- VERIFIED_RUNTIME: jen skutečný pokus s identitou modelu/FW, vstupem a výstupem; toto vydání žádný takový IV4 důkaz nepřináší.
- GENERAL: obecný návrhový princip, nikoli schopnost senzoru.
- INFERRED: výslovný úsudek nebo navržená architektura.
- UNVERIFIED: chybějící, rozporný či nepřístupný důkaz.

## Samostatný režim

`lookup.py --status` vypíše dostupný rozsah. `--query` hledá vlastní reference a registry; `--command T1` porovnává přesný token, nikoliv podobný řetězec. `--family` vybírá dokumentovou rodinu. `--id REF-tcp-contract` vrací vlastní vysvětlení, `--id CMD-IV4-H-CSR` faktický záznam. Celý FAST source_id bez stránky vrací metadata. Source_id se stránkou bez archivu poskytne pouze odpovídající veřejné reference, nikoliv předstíraný text manuálu.

## Rozšířený režim, pouze čtení

Předání `--corpus <cesta>` aktivuje existující `knowledge/00_KNOWLEDGE_INDEX.json` a A–G Markdown. ID `iv4_f2b18663143f7e12:p0505` označuje původní zdrojovou jednotku; `--neighbors 1` hledá předchozí/následující PDF stranu i když leží v jiném tématu. `--evidence` cíleně načítá page/table/figure indexy z `evidence/IV4_EVIDENCE_FAST`. Neprovádí extrakci, OCR, modelová volání ani zápis indexu. Vyhledávač má omezení počtu výsledků a délky výňatku; při truncation zúžit dotaz nebo zvolit konkrétní stránku.

Originální XML/EDS najde vlastník dokumentace podle source_member a SHA; ukázková veřejná mapa není úplný OEM soubor. Pro rozlišení modulů použij `--descriptor` a exact hash, nikoliv datum ZIPu. Chybějící archiv označ, dostupné vlastní znalosti používej dál.

## Přesnost FAST

Podklad pokrývá 1433 PDF stran, 1984 tabulek, 4153 figures a 54092 OCR záznamů. To jsou extrakční počty, ne počet odborně ověřených faktů. OCR má řádky k review a bitmapové/GUI vztahy nebyly VLM interpretovány. Nejistotu čísel, vazeb merged buněk, polarity zapojení a jednotek ověř proti původnímu zobrazení. Pouhé nalezení čísla není záruka správné modelové asociace.
