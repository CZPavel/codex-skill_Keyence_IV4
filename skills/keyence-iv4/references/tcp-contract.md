# TCP/IP non-procedural: wire contract a návrh klienta

Zdroj DOCUMENTED: S-IV4 (`iv4_82ffe8b0fedc105a`, IV4_UserManual_WW_GB_AS_167146.pdf), kapitola 9, PDF p.426–446; S-IV4-H (`iv4_f2b18663143f7e12`, IV4_UserManual_WW_GB_AS_170071.pdf), p.502–528. Celý faktický registr 43 IV4 + 46 IV4-H řádků je v [commands.json](commands.json); každá položka má vlastní table/detail page. Toto je vlastní vysvětlení kontraktu a jeho rizik.

## Transport a session

Senzor je TCP server; PC/PLC provádí active open. Výchozí port 8500, nastavitelný rozsah 1024–65535, dvě spojení. Port používaný pro PC/panel/display (výchozí 63000) nelze zvolit jako tentýž non-procedural port. Základní text používá ASCII, parametry odděluje čárka 0x2C, textový terminátor je CR 0x0D. CRLF nelze bez důkazu vydávat za předepsaný framing. Textová pole některých operací mají výslovně UTF-8 a padding; obecné ASCII pravidlo neopravňuje jejich nevratný převod.

Požadavek zařízení: další command až po odpovědi na předchozí. Dvě povolená spojení nejsou oprávnění sdílet příkazovou frontu nebo měnit současně program z Navigatoru i vlastního klienta. GENERAL návrh: jedna fronta request/response pro session, zřetelné vlastnictví triggeru a nastavení. Retry mutujícího příkazu po timeoutu není automaticky bezpečný; mohlo dojít k provedení bez doručeného ACK. Univerzální timeout není doložen: při návrhu jej stanov podle měřeného taktu, typu operace a přenosu, označ jako aplikační volbu.

## Skupiny příkazů

| Účel | Přesné tokeny |
|---|---|
| Trigger a výsledek | T1, T2, RT, OE, OF |
| Program a konfigurace | PR, PW, PNR, PNW, DR, DW, CSR, VI |
| OCR | CR, CW, CNR, CNW, SNR, SNW, CTR, CTU |
| Stav a diagnostika | RM, SR, RER, WR, WC, STR, STC, TP, TR, TC |
| Uložení/přenos | FNR, FNW, ITR, ITW, RFC, SDR, SDS, BR a BR,SD |
| IV4-H další souřadnice/model | DRC, DWC, MC |

`lookup.py --command PW --family IV4-H` poskytne exact syntax, parametry a podmínky. Tokeny DR/CW/STC nepřepisuj podle VS příkazů. DRC/DWC/MC nejsou v uvedeném IV4 seznamu doloženy. Pro příklady použij vlastní syntetický program/nástroj a ověř aktuální recepturu před zápisem; rozsah čísla programu je wire 000–127, nikoliv domyšlený převod uživatelského číslování.

## ACK, dokončení a historie

T1 vrací T1 okamžitě; tím nepotvrzuje dostupnost nového RT. T2 po provedené inspekci vrací RT a ne T2 echo. RT čte poslední potvrzený stav. Pokud od startu nebo změny programu neproběhla inspekce, RT vrátí 03; konflikt existuje také s OE. T2 odmítá nevhodný BUSY/ERROR/Program stav a OE. S-IV4 p.430 a 444–445, H p.506 a 525–526.

Návrhová větev INFERRED: v běžném dokumentovaném režimu vyber T2 nebo T1 → sledování stavu → RT; loguj baseline counter před triggerem a očekávanou změnu. Neposílej RT jako důkaz, že se právě vyfotil aktuální díl. Fyzický 2-image Buffer/Preliminary Capture je zvláštní případ: Trigger Ready řídí nové snímání a Strobe převzetí výsledku, BUSY nemusí klesnout. Toto elektrické časování nevyvozuj automaticky pro všechny TCP scénáře; viz [evaluation logic](evaluation-logic.md).

OE,1 aktivuje automatické RT zprávy pro příslušné triggery. Stav se po odpojení/power cycle neuchová. Nový stav potvrzený během přenosu předchozího může být zahozen (IV4 p.426, H p.502). Klient musí rozlišit unsolicited RT od odpovědi k příkazu; OE zvyšuje nároky na queue a freshness. Nejde o garantovanou lossless frontu všech dílů.

## Výsledková data a význam čísel

OF00 standard a OF01 detailed platí pro příslušné režimy bez multiple-master; OF02/03 zahrnuje master number a vyžaduje správnou OR logiku. H přidává OF04 coordinate pouze pro Standard s multiple master registration Disable nebo pro Sorting (H p.511); IV4 p.435 zná jen 00–03. Nastavení formátu končí odpojením/vypnutím. Pozice a počty polí závisí na zvoleném formátu/režimu; neurčuj je ze jména příkazu samotného.

Standardní RT pro Standard/Sorting má pětimístné result number 0–32767, dvouznakový total/master status a opakované tool triplets. Tool number má dva znaky, stav dva a číselné pole sedm. Stav `--` znamená nemožnost rozhodnout, nikoliv OK s nulovou hodnotou. Tool číslo 00 má modelově odlišný význam (H zahrnuje také AI Target Extraction). V sedmi znacích může být matching rate, count nebo rozměr; jednotku neurčuje samotná šířka. Příklad principu: hodnota měření 21.5 mm je v uvedené tabulce vyjádřena jako 0021500; nepřepočítej stejně procentuální tool. IV4 p.441–442, H p.517–518.

Counter přetéká z 32767 na 0. Stejná hodnota po reconnect není důkaz téhož kusu ani nového výsledku; GENERAL řešení přidává host session_id a vlastní cycle_id, známý program a explicitní validitu. Detailed formát obsahuje navíc stavy a časové údaje; Through Count má jinou strukturu tool dat (count a daily total) a saturace. Omezená ukázka `wire_contract.py` proto odmítá jiné než výslovně zadané OF00 Standard/Sorting.

## Parametry a zdrojové nejasnosti

PNR má pevnou 48bytovou/variabilní variantu a NULL padding; PNW nejvýše 16 UTF-8 znaků. OCR CR/CW pracuje s 96bytovou pevn./variabilní odpovědí a masterem do 32 znaků. CNR/CNW jsou count-only OCR operace. FNR je 64 znaků se SP padding, FNW rozlišuje volatile a nonvolatile. ITW je naopak limitováno na 64 bytů; nejde o 64 libovolných Unicode znaků. Při generování klienta zvol přesný registr a mode a netrimuj globálně koncové SP/NULL.

Významné konflikty (zachované v anomalies): IV4 CSR je pět znaků, H detail deset, ale jeho summary table nese pět a OPC UA tabulka má nesoulad typu/rozsahu. ITR má v summary čárku před CR, kterou detailní diagram nemá. H tabulka MC[R] se rozchází s MC+CR v detailu. BR response table používá Br, diagram BR. Nevyber jednu variantu bez source/runtime kontroly; dlouhodobý klient nemá skrývat tyto rozdíly automatickým širokým parserem.

## Chyby a recovery

Textová chyba má ER,command,bb+CR; command část je do 18 znaků, bb dvě číslice. 02 znamená neznámý command, 03 nevhodný stav/nastavení, 22 chybný počet nebo rozsah parametrů (IV4 p.426, H p.502). Kód chyby protokolu není totéž co tříciferný RER/WR kód zařízení. Při 03 nejdříve zjisti program, Run/Program, režim, OE a dostupnost výsledku; při 22 zkontroluj počet, šířku, meze, jednotku a počet bytů UTF-8. Neprováděj reset jako default recovery.

BR je přepnutí na length-aware binární odpověď: po textovém headeru následuje 24-bit BMP, jehož byty mohou obsahovat CR i čárku. BR,SD je zápis na kartu s cestou do 192 bytů a možným přepsáním. Žádná z těchto funkcí není obecný MJPEG/RTSP endpoint. Přesný mixed framing, case a délkové meze otestuj na fixture a pak na cílové kameře (IV4 p.439–440, H p.515–516).

Offline testy: rozdělená a slepená TCP data, modulo counter, neplatný `--`, chybové odpovědi, hranice bufferu, explicitní odmítnutí BR v ASCII parseru. Runtime testy musí doplnit reconnect, restart, program switch, concurrent owner, takt a přiřazení image/result; dosud neprovedeny.
