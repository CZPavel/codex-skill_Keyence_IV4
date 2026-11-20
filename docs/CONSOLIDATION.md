# Konsolidace IV4 výzkumu v1.1.0

Převzata vlastní sanitizovaná syntéza V1/V2. Výchozí manuálové IV4 a IV4-H registry, 15 PDF identit, 89 příkazů, 28 capabilities a 4 descriptor záznamy zůstaly zachovány. Původní klasifikace DOCUMENTED/DESCRIPTOR_ONLY nejsou nahrazeny runtime razítkem. Přístupný [runtime registr](../skills/keyence-iv4/references/runtime-observations.json) rozlišuje přesný model/FW; [česká reference](../skills/keyence-iv4/references/runtime-research.md) vysvětluje dopady.

| Oblast výzkumu | Kanonický runtime ID / místo | Převzetí a mezera |
|---|---|---|
| V1 identita, monitoring a TCP | RT-IV4-R12005-TCP | Model/FW, status, T1/T2, OF01, ITR ER02; bez OCR/NG v V1 |
| V1 BR a reconnect | RT-IV4-R12005-BR | Hlavička a payload, oddělené čítače; bez atomické korelace |
| V1 sessions, GUI export/restore | RT-IV4-R12005-SESSION-RESTORE | EOF první session, individuální návrat jména; bez full restore |
| V2 teplota/statistika/SD/RFC/čas | RT-IV4-R13002-STATUS | TP STR SDR RFC TR, Program ER03 a no-card zero |
| V2 TCP, BR, ITR delta | RT-IV4-R13002-TCP | Řízené OK, T1 delayed result, ITR spaces versus trailing ER22 |
| V2 PW/PNW/DW | RT-IV4-R13002-WRITES | Nezávislý PR/PNR/DR readback, threshold-induced NG a obnova mezí |
| V2 UA typy/metody/notifikace | RT-IV4-R13002-OPCUA | Standard IV4 metadata, nové výsledky a readback; neřeší H rozpory |
| V2 MQTT | RT-IV4-R13002-MQTT | Raw shape, QoS capture omezení, action/readback, retained a jeden restart |
| V2 OCR OK a zakrytý NG | RT-IV4-R13002-OCR | Recognized versus master, score není confidence, TCP/MQTT/UA/FTP text |
| V2 FTP completeness | RT-IV4-R13002-FTP | BMP/IV4P/TXT, 8/9 přes RFC a nulovou chybu; příčina neznámá |
| V2 clocks, transport, stale cache | RT-IV4-R13002-TIME-SESSION | Source versus host čas; omezený smoke není Fleet integrace |
| V2 Navigator, IoT selector, restore | RT-IV4-R13002-GUI | Jediný selector a individuální OCR obnova; UA+MQTT souběh neprokázán |
| Native Navigator / interní wire / export formát | Volitelná privátní H research vrstva | Statické RE není veřejný SDK ani autorizace pro interní opcodes; bez převzetí proprietárního raw formátu/klienta |
| Historický závěrečný stav | Runtime reference a privátní FINAL_STATE | Není současný stav zařízení, nic nebylo znovu připojeno |

Privátní corpus může přidat `knowledge/H_IV4_Research.md` a `IV4_RESEARCH_FACTS.json`. Lookup načítá pouze fact fields a logické lokátory, nikoli katalog privátních kořenů. Samostatná research ID nejsou PDF page ID. Shodná ID jsou deduplikována; různě granularitní facts mohou sdílet téma. Původní A–G page lookup je zachován.

## Ověření a jeho význam

Lokální unit/integration testy ověřují lookup, family/FW oddělení, nepřevzetí privátního source katalogu, veřejnou distribuci, instalaci a původní wire helper. Manage validate ověřuje JSON/odkazy a rozsah distribuce; quick_validate frontmatter. Public audit kontroluje veřejný strom i historii. Kontrola existence archivních logických lokátorů potvrzuje dohledatelnost, nikoli věcnou správnost každého raw záznamu. Starší modelové behavior odpovědi jsou označeny v1.0.0 v VALIDATION; nejsou novým forward-testem v1.1.0.

Nová práce neprovedla HW test. Historické omezené pokusy jsou důkaz jen svého kontextu. Zůstávají otevřené: přesnost OCR na reprezentativní sadě, vícebytové texty, fyzická I/O, startup/power-cycle a full restore, SFTP a FTP recovery, příčina neúplného souboru, spolehlivá korelace dílu/obrazu/výsledku, výrobní takt, bezpečnost a produkční Fleet integrace. Nejmenší další krok závisí na vybraném cíli; samotná znalostní konsolidace žádný živý experiment nevyžaduje.
