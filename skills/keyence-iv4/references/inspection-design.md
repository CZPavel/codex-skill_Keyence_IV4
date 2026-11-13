# Návrh praktické inspekce IV4

## DOCUMENTED — výchozí postup

S-IV4 = FAST source_id `iv4_82ffe8b0fedc105a`, IV4 Series User’s Manual AS-167146 R1.30; čísla odkazují na PDF strany. Sensor Setup nabízí Standard, Sorting a AI Through Count, přičemž postup zahrnuje optimalizaci obrazu, master, nástroje a výstupy. Standardní režim posuzuje nástroje vůči registrovanému OK základu. [S-IV4 p.88, 100, 106, 176 / IV4_UserManual_WW_GB_AS_167146.pdf / Sensor Setup]

## GENERAL — návrhový postup

Začni definicí vady: které díly musí projít, které ne, kde leží mez a jaké jsou důsledky falešného OK a falešného NG. Uveď minimální velikost defektu, rozptyl polohy, povrchu, šarže, rychlosti, světla a rozhraní k PLC. Vzorky rozděl podle skutečných výrobních variant a vyhraď nezávislé díly pro závěrečnou kontrolu. Nedefinuj výrobní toleranci pouhým přizpůsobením několika trénovacím snímkům.

Mechanicky stabilizuj pozici, zvol pracovní vzdálenost a zorné pole s rezervou, pak uprav osvětlení a expozici pro stabilní oddělení požadovaného detailu. Pro lesklé povrchy porovnej geometrii světla a polarizaci, pro pohyb snímek při skutečné rychlosti; dlouhá expozice může způsobit rozmazání. Master pořiď za reprezentativních podmínek. Teprve pak navrhuj nástroj a práh.

## GENERAL — příklady úloh

**Přítomnost šroubů:** nejprve lokalizuj stabilní část sestavy, pak porovnej AI Count s očekávaným počtem. Má-li každá pozice význam, otestuj Missing Part Detection, nejen celkový počet: jeden chybějící a jeden nadbytečný objekt mohou součet zachovat. Přidej vzorky s pootočením, jiným povrchem, zákrytem i cizím podobným objektem. [S-IV4 p.116–118 / IV4_UserManual_WW_GB_AS_167146.pdf / AI Count]

**Správnost štítku:** zkontroluj fyzickou přítomnost a polohu odděleně od textu. Pro AI OCR určete povolené znaky, délku a skutečnou variabilní část; pro datum správný formát a referenční čas. Otestuj podobné znaky, chybějící znak, špatný tisk, lesk a jiné šarže. Nezaměňuj OCR za podporu QR. [S-IV4 p.120–123 / IV4_UserManual_WW_GB_AS_167146.pdf / AI OCR]

**Těsnění a výstupek:** při známé barvě nebo kontrastu zvaž Color/Area a Prohibition s maskou, která vynechá povolenou oblast. Nastav hranici pomocí fyzických hraničních vzorků; otestuj odlesky a barevné odchylky dobrých dílů. Pro chybějící nebo pozměněný obrys může být vhodný Outline, pokud zůstává stabilní. [S-IV4 p.137, 142–143, 159 / IV4_UserManual_WW_GB_AS_167146.pdf / Area, Prohibition and Outline]

**Rozteče nebo šířka:** pro kontrastní geometrii zvaž Width, Diameter nebo Pitch; ověř detekovanou dvojici hran, směr kontrastu a vliv náklonu. Scaling nastav podle známé reference a přesnost ověř samostatným měřením v celém pracovním prostoru. Displej v mm není sám o sobě metrologická validace. [S-IV4 p.151–157 / IV4_UserManual_WW_GB_AS_167146.pdf / Edge and Dimensional Tools]

**Průtok dílů:** AI Through Count zvaž pro objekty procházející linií. Ověř reálný pohyb, překryv, shlukování, vratný pohyb a počáteční či resetový stav; neodvozuj propustnost z offline obrazu. [S-IV4 p.168–170 / IV4_UserManual_WW_GB_AS_167146.pdf / AI Through Count]

## GENERAL — přejímka

Pro každou vadu předem stanov počet a rozmanitost vzorků, očekávaný výsledek a pravidlo rozhodnutí. Testuj nezávislé OK i NG vzorky, hraniční podmínky, opakování a různé šarže. Zaznamenej program, model, verzi, optiku, osvětlení, nastavení, trigger, skóre a výstupy. Pak proveď test na skutečné lince včetně přepnutí programu, restartu, komunikace a párování dílů. Rozděl experimentální schopnost od výsledku výrobní přejímky.

## UNVERIFIED

Navržené postupy jsou obecná inženýrská doporučení, nikoliv ověřená výkonnost konkrétní aplikace, bezpečnostní funkce nebo zaručené měření.
