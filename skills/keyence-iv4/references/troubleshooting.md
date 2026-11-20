# Diagnostika IV4: od obrazu k výsledku

Doplněk v1.1.0: [historický runtime research](runtime-research.md) odděluje pozorování IV4-500CA R1.20.05 / R1.30.02 od níže uvedených manuálových či návrhových tvrzení; nepřenášet na IV4-H.

## DOCUMENTED — zdroj a stavové informace

S-IV4 = FAST source_id `iv4_82ffe8b0fedc105a`, IV4 Series User’s Manual AS-167146 R1.30. PDF strany jsou strany dokumentu. Vždy zaznamenej model, verzi senzoru, Navigatoru a případné komunikační jednotky. IV4-H má odlišný manuál `iv4_f2b18663143f7e12` a nelze automaticky používat jeho chybové tabulky pro IV4. [S-IV4 p.10, 31 / IV4_UserManual_WW_GB_AS_167146.pdf / Version and Name of Parts]

U uvedených ultra-compact hlav stavová zelená značí celkový OK, červená NG a blikající červená chybu. Nesvítící indikátor má více možných příčin včetně čekání na první úsudek a nekompatibilní hlavy či verzí: samotná LED neurčuje kořenovou příčinu. [S-IV4 p.31 / IV4_UserManual_WW_GB_AS_167146.pdf / Sensor Head Indicators]

## GENERAL — obraz a mechanika

Při nestabilním výsledku zachyť obraz OK i NG, jejich skóre, čas a číslo programu. Je-li obraz rozmazaný, ověř ostrost v aktuální pracovní vzdálenosti, pohyb během expozice, upevnění, průhlednost krytu a změny výšky. Při změně kontrastu prohlédni odlesky, okolní světlo, znečištění a skutečně aktivní světlo. Změň vždy jednu příčinu a porovnej stejné vzorky.

**DOCUMENTED:** Autofocus je určen pro nastavení při instalaci a za provozu vypnut, s možností registrovat pozici podle programu. Pokud se výška dílu mění, nelze předpokládat průběžné přeostřování. [S-IV4 p.483, 486 / IV4_UserManual_WW_GB_AS_167146.pdf / Specifications]

## GENERAL — lokalizace a nástroje

Pokud obraz vypadá správně, zkontroluj okno, search range, masku, orientaci a přiřazený Position Adjustment. Ověř, že se hledá skutečně stabilní prvek a že korekce nepřesune některé okno mimo obraz. Pro oblast nebo blob prohlédni extrahovanou barvu/jas a histogram, nejen celkový verdikt. Pro hrany ověř polaritu a směr; pro OCR nastavení znaků a formát data. U AI porovnej historii učení s chybovými příklady a zkontroluj jejich označení.

**DOCUMENTED:** Při neúspěšné korekci polohy jsou jednotlivé výsledky NG; při výstupu příslušného okna mimo obraz nástroj nelze vyhodnotit a je NG. Position Adjustment má nastavitelný rozsah rotace a vyhledávací algoritmus. [S-IV4 p.139, 176 / IV4_UserManual_WW_GB_AS_167146.pdf / Position Adjustment and Output Assignment]

## GENERAL — trigger, PLC, přepnutí

Když na snímači výsledek existuje, ale PLC jej nevidí, zaznamenej přiřazení výstupu a jeho polaritu, stav Ready/Busy, trigger, časový sled, konkrétní fieldbus mapu a číslo programu. Odděl výpadek snímání, vyhodnocení, přenosu a spárování výsledku s dílem. Nevyvozuj, že každé NG znamená vadu výrobku; může souviset s nevyhodnocením nebo chybnou lokalizací.

**DOCUMENTED:** Po přepnutí programu či návratu do RUN nevznikne nový výsledek před triggerem a dílčí stavy jsou do té doby OFF. Trigger Ready a Excessive Trigger Input Time Error mají vlastní podmínky. [S-IV4 p.176–177, 460–463, 478 / IV4_UserManual_WW_GB_AS_167146.pdf / Logic and Trigger Control]

## GENERAL — síť a zálohy

Při nedostupném Navigatoru nejprve zjisti, zda je zařízení napájeno, propojeno a viditelné na správném adaptéru; ověř IP konfiguraci, firewall a souběžné síťové adaptéry podle konkrétní instalace. Nenastavuj ani neresetuj IP zařízení v produkci bez znalosti následků. Při chybě ukládání zjisti cílové médium, kapacitu, oprávnění, podmínku ukládání a přesný chybový text. Před zásahem ulož diagnostické údaje a zálohu; po úpravě ověř výsledek reprodukcí původního problému.

## UNVERIFIED

Tento postup není seznam konkrétních chybových kódů ani důkaz konkrétní příčiny. Bez modelu, přesného textu chyby, verzí, snímků a sledování signálů nelze stanovit závadu ani tvrdit, že problém byl odstraněn.

## DOCUMENTED — praktický katalog vybraných varování IV4-H

Pouze H manuál AS170071 / `iv4_f2b18663143f7e12`, PDF p.520–523, kapitola TCP/IP/List of Error Codes. Následují vlastní zkrácená vysvětlení Warning codes, nikoli univerzální error registry všech IV generací. `WR` a device warning code neplést s dvoumístným `ER,command,03`.

- **Warning 45:** nastavení CU/GCU nesouhlasí se skutečně připojenou jednotkou. Read-only ověř identitu sestavy a uložené nastavení před autorizovanou změnou/restartem.
- **Warning 46:** Model Check neodpovídá dříve registrovanému výsledku; zkontroluj test images, learning a prahy. Samotné MC success nevylučuje tento NG.
- **Warning 47:** tracking není stabilní nebo nestačí takt; odděl kontrast/learning od výpočetního zatížení.
- **Warning 49:** malá rezerva mezi koncem zpracování a dalším triggerem; měř timing, nepovažuj to za obecný timeout TCP.
- **Warning 50 / 51:** překryv one-shot Strobe nebo AI Trigger výstupu; porovnej ON time s intervalem aktualizací/triggerů.
- **Warning 54:** problém advanced programu při setup; ověř kartu, správný program a dostupnost, nikoli nejdříve formátování.
- **Warning 56:** SNTP synchronizace; ověř server, síť a dosažitelnost. Změna času může ovlivnit korelaci logů.
- **Warning 58:** externí OCR master nelze přečíst; prověř snímek, jas a způsobilost nástroje pro registraci.
- **Warning 60:** field-network/IoT změna parametru není v daném stavu, režimu či nástroji platná. Ověř Run, číslo nástroje, jeho typ, OCR mode a rozsah/byty textu; není to důkaz vadného kabelu.
- **Warning 61:** neplatná změna FTP/SD názvu; ověř Run, transfer condition, povolené znaky a délku nejvýše 64 znaků.
- **Warning 62:** field-network result buffer překročen; ověř Result acquisition complete notice a zvolený handshake. Neřeš pouze změnou RPI bez měření toku výsledků.
- **Warning 63:** požadavek externího masteru během setup; ověř stav a povolenou registrační funkci.
- **Warning 64:** program switch ve špatném stavu, na neexistující číslo nebo při jiném switching method. Bez SD programů platí 0–31, se zapnutými SD programy 0–127; nepoužívej neověřený posun +1.
- **Warning 65:** trigger při BUSY v příslušném režimu, případně AI Trigger nestíhá. Pro Preliminary Capture čti samostatné Ready/Strobe časování; nevynucuj univerzální BUSY cyklus.
- **Warning 66 / 67 / 68 / 69:** při externí registraci se nepodařil obrys, plocha, korekce jasu nebo hrana. Prověř vhodnost master snímku a nástroje; ACK nelze použít místo kvalitativního ověření.
- **Warning 70:** FTP buffer nestačí objemu nových dat; sleduj takt, velikost a zatížení sítě.
- **Warning 71:** přenos do cílového folderu selhal; ověř práva a cílovou cestu.
- **Warning 72:** nelze navázat FTP spojení; odděl server/service, route/link a nastavení transferu.
- **Warning 73 / 74:** pro externí master chybí pracovní paměť nebo zachycený obraz; nejdříve zjisti, která podmínka nastala.
- **Warning 75:** SD transfer buffer nestíhá; srovnej trigger interval a reálnou rychlost ukládání.
- **Warning 76:** SD transfer selhal, například kapacita, cover nebo write protection. Deletion/format/replacement jsou samostatné autorizované servisní zásahy.
- **Warning 77:** externí master je v konfliktu s learning-related tool nebo režimem Sorting/Through Count.
- **Warning 78:** přístup ke kartě selhal; prověř kartu a její stav. Zdrojový servisní postup formátování nesmí být automatickou první akcí asistenta.
- **Warning 83:** změnila se sestava externího světla oproti nastavení; ověř typ a připojení.
- **Warning 87:** externí trigger drží příliš dlouho; zkontroluj zdroj signálu a waveform, ne pouze log TCP.
- **Warning 91:** AI Trigger buffer error; citovaný H postup požaduje zkrátit tool processing pod 1 s. Nejde o univerzální maximální takt jiných režimů ani timeout klienta.
- **Warning 92:** AI Trigger capture speed nestačí/stabilita je špatná; odděl rychlost snímání a kvalitu learning/scény.

Současné chyby/varování mají vlastní prioritu a historii. Snapshot kódu nevypráví celou časovou sekvenci; uchovej timestamp, mode, program, trigger a síťové události. Neznámé kódy dohledávej v oficiálním Error Number Lookup a přesné edici manuálu, nikoliv interpolací z podobného čísla.
