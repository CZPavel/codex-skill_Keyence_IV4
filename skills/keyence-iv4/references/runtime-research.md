# IV4 runtime research: historické pozorování podle firmware

Rozsah: jedna **IV4-500CA**, Navigator **2.10.01.0**, V1 **R1.20.05** (18. 11. 2026), V2 **R1.30.02** (19.–20. 11. 2026). Jde o převzetí uložených omezených pokusů, nikoli o nové připojení, současný stav kamery, funkční Fleet integraci nebo produkční přejímku. Výstupy byly nastaveny OFF, elektricky neměřeny. IV4-H tím není runtime ověřená.

Strojový registr: [runtime-observations.json](runtime-observations.json). Každý záznam má přesný model/FW, kategorii důkazu, pozorování, samostatný dokumentační kontext, limity a sanitizované logické lokátory. `IV4_RESEARCH/...` a `IV4_RESEARCH_V2/...` jsou označení privátního výzkumného archivu, nikoli přibalené soubory nebo veřejné odkazy. Původní manuálové registry se nemění na runtime důkaz. Lokátory umožňují dohledat původ oprávněnému držiteli archivu, veřejná syntéza nenahrazuje raw evidence.

| Téma | R1.20.05 | R1.30.02 / omezení |
|---|---|---|
| TCP | VI/RM/PR/PNR, Run SR/RER/WR/CSR, T1/T2, OF01, BR | Rozšířeno o TP/STR/SDR/RFC/TR, PNW/PW/DW s readbackem. Program řada status dotazů ER03; STR před prvním výsledkem ER03. SDR 00000 při chybějící SD, ne procento. |
| ITR | Obě varianty ER02 | `ITR,1` 64 mezer i na OCR; trailing comma ER22. Není to recognized text. |
| Obraz | BR uppercase, 22B hlavička, length-delimited BMP bez koncového CR ve vzorcích | BR0/BR1 full/half; RT a BR čítače vést odděleně. V1 páry 27/1, 38/12, 40/14 dokazují, že nejde o společné ID. |
| OPC UA | Netestováno | Typované MachineStatus/MachineInformation/OperationResult; čtyři nové výsledky 1–4 a OCR NG23; metody trigger/threshold/program s následným výsledkem/readbackem. |
| MQTT | Netestováno | Výsledky, OCR, omezené action/readback a restart brokeru. Dva publish ve zkráceném PCAP QoS1; subscriber QoS2 neurčuje camera publish QoS. |
| Obnova | GUI individuální .iv4a vrátila název | GUI P002 → P003 a jedna OCR inspekce OK. Ani jeden test nepotvrzuje kompletní sensor restore. |

## OCR: master, recognized text a score

`CR` je master **722336**. Tři výsledky 15–17 rozpoznaly **722336** v detailed TCP RT a MQTT `ReadString`. Zakrytý motiv ponechal **7223**; pět výsledků 19–23 bylo NG, master zůstal 722336, OCR recognized 7223, score 0. To je skóre porovnání, **nikoli confidence 0**. Position Adjustment zůstal OK 90–91.

Recognized text je doložen detailed TCP RT, prvními čtyřmi MQTT NG zprávami, FTP TXT a pátým typovaným OPC UA `ReadString` (Good). Protokoly neběžely v tomto důkazu všechny současně. Jeden ASCII vzorek má detailed odpověď 175 B / OCR blok 110 B = 14 B prefix + 96 B text. Nezobecňuj stride či encoding na vícebytový text, jiné nástroje nebo FW; zachovej raw bytes/padding. Pět NG a jeden motiv nejsou test přesnosti OCR.

## Standard IV4 OPC UA a MQTT

IV4 manuál `iv4_82ffe8b0fedc105a` PDF 410–415 a runtime společně popisují namespace URI `urn:KEYENCE:VisionSensor:IV4:OPCUaServer` (index vyhledej znovu), proměnné 16001/16002/16500 a typy 3100/3101/3110. Pole hodnot měla CurrentRead; existence metod neznamená právo ani provedení. Šest metod 17001–17006; RequestTrigger, ChangeThreshold a SwitchProgram mají omezený navazující runtime důkaz. IV4-H duplicate ID a UInt16/range rozpor nejsou tímto vyřešeny.

Method success není okamžitý readback; OperationResult může držet threshold poslední inspekce. MQTT ResultLogic je objekt `ResultLogic1..8`, ExtendedData pole objektů `Data`, ImagingTime má dvojtečku před ms. Zdrojové UA/MQTT časy mají přibližně hodinovou odchylku vůči hostu: zachovat raw a host receive time. None/Anonymous není produkční autorizace. Žádná garance lossless sběru, replay nebo exactly-once mutací.

## FTP, úplnost a korelace

Přijaté BMP, IV4P a UTF-16LE BOM/tab TXT zahrnuly OCR. Ve třech následných NG cyklech však došlo jen **8/9** dokončených souborů, jeden BMP 0 B, zatímco **RFC 1 → 4 a RER/WR 000**. Příčina neznámá; záznam neurčuje chybu kamery versus receiver/overwrite/session. RFC není serverové potvrzení všech souborů. Sleduj jednotlivé receipt a neúplné skupiny. Další cyklus 3/3 a dvě samostatné shody FTP/BR BMP nepředstavují obecnou atomickou vazbu image/result/part. SFTP, recovery a výrobní úplnost zůstávají neověřené.

## Hranice integrace

GUI má jediný IoT selector Disable / OPC UA / MQTT; současné UA+MQTT nebylo doloženo. Dva omezené TCP pokusy (oba FW) zaznamenaly EOF první session po připojení druhé; jeden vlastník socketu a fronta jsou doporučení, nikoli univerzální limit výrobce. PNW→PNR, DW→DR, PW→PR a nový výsledek po triggeru jsou oddělené důkazy. ACK ani broker publish ACK není dokončení; po timeoutu může být stav neznámý, mutaci neopakuj naslepo. Automatický katalog, plný parametrický editor/export, startup persistence, fyzické I/O a produkční takt nejsou ověřeny.

## Lookup

`--query "OCR" --firmware R1.30.02` vrací samostatná runtime fakta; `--id RT-IV4-R13002-OCR` přesné pozorování. `--family IV4-H` runtime IV4 nepřevezme. `--firmware` omezuje výsledky na explicitně označená pozorování; obecné manuálové texty nejsou firmware-specific runtime shoda. `--command` nadále vrací původní manuálový kontrakt.

Volitelný privátní corpus může mít `knowledge/H_IV4_Research.md` a `IV4_RESEARCH_FACTS.json`; jde o samostatnou research vrstvu, nikoli PDF stránky. Původní `iv4_<hash>:pNNNN` lookup zůstává manuálovým lookupem a absence research JSON nebrání standalone použití.
