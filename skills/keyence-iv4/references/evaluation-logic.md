# Vyhodnocení, logika a návaznost na PLC

## DOCUMENTED — zdroj a logika výsledků

S-IV4 = FAST source_id `iv4_82ffe8b0fedc105a`, IV4 Series User’s Manual AS-167146 R1.30. Strany jsou PDF stránky. Význam a dostupnost dalších údajů pro IV4-H, Navigator a komunikační jednotku se řídí jejich verzí a vlastním manuálem. [S-IV4 p.10 / IV4_UserManual_WW_GB_AS_167146.pdf / Version]

Total Status Conditions lze nastavit jako All Tools OK, Any Tool OK nebo vybrat Logic 1 až 8. Výstup logiky skládá stavy označených nástrojů pomocí AND nebo OR. Used bere OK jako aktivní, Used (Inverse) bere NG jako aktivní. Dřívější logiku lze zahrnout do pozdější s vyšším číslem; například Logic 1 může být položkou Logic 2–8. [S-IV4 p.176–177 / IV4_UserManual_WW_GB_AS_167146.pdf / Output Assignment and Logic Settings]

Příklad: A = přítomnost součásti, B = zakázaný díl, který má vyjít NG, když chybí. AND s A Used a B Used (Inverse) vyžaduje A OK a B NG. Toto je konstrukce podle nastavené polarity, nikoli obecný význam pojmů přítomnost a nepřítomnost; skutečnou konfiguraci B nutno doložit testem.

Když selže position adjustment, manuál uvádí NG jednotlivých nástrojů. Pokud po úspěšné korekci okno vyjmenovaného nástroje přesáhne obraz, nástroj nelze vyhodnotit a jeho stav je NG. Inverze NG proto může přeměnit selhání korekce nebo nedostupné vyhodnocení na aktivní logický vstup: vhodně zapoj stav pozice a chyby. [S-IV4 p.176–177 / IV4_UserManual_WW_GB_AS_167146.pdf / Output Assignment]

## DOCUMENTED — časování a platnost

Po změně programu nebo přechodu do RUN se neprovede nové vyhodnocení, dokud nepřijde trigger; jednotlivé stavy jsou do té doby OFF. Manuál samostatně popisuje trigger a Trigger Ready, BUSY a chyby triggeru. Nastavení Excessive Trigger Input Time Error je dostupné pro External Trigger a může signalizovat příliš dlouhý aktivní vstup. [S-IV4 p.176–177, 460–463, 478 / IV4_UserManual_WW_GB_AS_167146.pdf / Output Assignment and Trigger Control]

Standardní vstupní/výstupní logika a field network nejsou zaměnitelné: mapování a časování závisejí na vybraném rozhraní, rozložení dat, nastavené jednotce a verzích. Pro přesné bity a handshake použij aktuální kapitolu protokolu a konkrétní komunikční jednotky, nikoli analogii s jinou řadou. [S-IV4 p.292–295 / IV4_UserManual_WW_GB_AS_167146.pdf / Field Network Setup]

## GENERAL — návrh strojového cyklu

1. Ujisti se, že je potvrzen správný program a přijímání dalšího triggeru povoluje signál určený pro zvolený režim (BUSY nebo Trigger Ready podle následujícího postupu). Trigger dej v reprodukovatelné poloze součásti.
2. V PLC odděl data výsledku od informace, že jde o nový platný výsledek. Přesný signál, hrany, minimální délku impulzu, timeout a potvrzování stanov dle skutečného rozhraní a manuálu.
3. Výsledek páruj s konkrétním dílem včetně zpoždění dopravníku; definuj, co při chybě, nepřipravenosti, ztrátě komunikace, přepnutí programu a restartu.
4. Ověř pravdivostní tabulku na OK, každém NG, chybě lokalizace a chybě snímání. Samostatně ověř výslednou fyzickou polaritu a reakci PLC.

## INFERRED / UNVERIFIED

Při použití inverze může systém při technickém NG nechtěně splnit podmínku pro díl; skutečný dopad závisí na konfigurované logice. Konkrétní komunikace, atomické předání, maximální frekvence, synchronizace a vazba výsledku k fyzickému dílu zde nebyly testovány.

## DOCUMENTED — detailní příklady a závislosti

All Tools OK je konjunkce stavů všech detection tools; Any Tool OK vyžaduje alespoň jeden OK. Logic 1–8 může využít AND/OR, položky Used a Used (Inverse), včetně dříve vytvořené logiky s nižším číslem. Při složitějších podmínkách proto zakresli jednotlivé úrovně a explicitně označ skutečný zdroj OK/NG; výsledek není automaticky totožný s výsledkem každého nástroje. [S-IV4 p.176–177 / IV4_UserManual_WW_GB_AS_167146.pdf / Total Status and Logic Settings]

Například požadavek „A i B musí být OK“ lze modelovat All Tools OK jen pokud ostatní nastavené detection tools mají být také součástí souhrnu; alternativně vyber A a B v logice AND. „A nebo B“ odpovídá OR pro zvolené nástroje, ale Any Tool OK zahrne všechny detection tools. Toto rozlišení je důležité, pokud přidáš pomocný nástroj. [S-IV4 p.176–177 / IV4_UserManual_WW_GB_AS_167146.pdf / Total Status and Logic Settings]

Nástroj, jehož position adjustment se nezdaří, může hlásit NG jako důsledek neplatného měření. Pokud se tato hodnota invertuje, výstup z logické inverze může být aktivní. Sestav testovací tabulku s alespoň řádky: lokalizace OK + díl OK; lokalizace OK + díl NG; lokalizace NG; ROI mimo snímek; před prvním triggerem. Pro řádky s chybou určuj výsledné fyzické signály a chování PLC experimentálně v konkrétní konfiguraci. [S-IV4 p.176–177 / IV4_UserManual_WW_GB_AS_167146.pdf / Output Assignment]

## DOCUMENTED — Through Count a reset

AI Through Count má pro každý count tool až dva Status Outputs. Podmínka může být ≥ nastavená hodnota nebo = nastavená hodnota. Auto-Reset nastavuje hodnotu resetu; příklad v manuálu: při reset value 10 se po přičtení jedné k 9 počítadlo vrátí na 0. Výsledek se potom nemusí chovat jako monotónní celkový počet a vyhodnocení na přesnou hodnotu vyžaduje kontrolu časování. [S-IV4 p.169–170 / IV4_UserManual_WW_GB_AS_167146.pdf / AI Through Count Status Output]

Through Count Total sčítá vybrané count tools, přičemž maximum je jeden Total v High Speed/Standard a dva v High Accuracy. Směr pohybu určuje, kterou část oblasti vyhledávání lze měnit. Conveyor End Settings umístí count line na hranu dopravníku pro padající díly. Ověř, že každý vybraný nástroj pokrývá zamýšlenou třídu objektů a že jedno fyzické těleso nepřispívá dvakrát. [S-IV4 p.172–173 / IV4_UserManual_WW_GB_AS_167146.pdf / AI Through Count Total and Search Range]

## GENERAL — pracovní pravdivostní tabulka

Před napojením PLC zapiš pro každý stav platnost snímku, správné číslo programu, stav lokalizace, výsledky nástrojů, výslednou logiku, fyzický výstup a očekávanou akci stroje. Testuj také nepřipravenost, příliš rychlý či chybějící trigger, přepnutí programu a ztrátu komunikace. Hodnoty ve sloupci „očekávaná akce“ vycházejí z návrhu zařízení; pokud není doložen bezpečný výsledek, ponech stav jako nevyřešený místo předpokladu OK.

Pro průchozí počítání sleduj více než zobrazené číslo: surový tok dílů, identitu a směr, okamžik průchodu linií, počítanou skupinu, pulz či stav Status Output, reset a konečné zpracování v PLC. Zvlášť otestuj situace při změně rychlosti, mezery mezi díly a výpadku napájení. Test jednotlivých statických obrázků tento dynamický řetězec neověří.

## DOCUMENTED — časování fyzických linek podle režimu

Pro IV4 AS-167146 R1.30, **běžné řízení externím triggerem a BUSY**: umísti díl, přijmi trigger jen při dostupném snímači a po jeho aktivaci sleduj BUSY. Po dokončení vyhodnocení se aktualizují status výstupy a BUSY přejde do OFF; pak přečti status. Při volbě BUSY Until Data Transfer is Complete se OFF odkládá až po přenosu dat. Externí trigger během BUSY se ignoruje a vznikne trigger error. Popis platí pro odpovídající zvolený režim fyzických linek a uvedenou konfiguraci, nikoliv univerzálně pro buffer či TCP. [S-IV4 p.460 / IV4_UserManual_WW_GB_AS_167146.pdf / Controlling Timing of Judgment with Triggers]

Pro **Preliminary Capture ON (2-image Buffer)** se externí trigger řídí Trigger Ready: po dokončení snímání se Ready znovu aktivuje a dovolí další trigger i před dokončením předchozího vyhodnocení. Status se aktualizuje po vyhodnocení a čte synchronně se Strobe. Trigger při Ready OFF je ignorován a vzniká trigger error. Je-li interval kratší než čas zpracování, BUSY může zůstat trvale ON a nelze ho použít k načítání výsledku. Nastav délku Strobe a otestuj, že ji PLC stihne zachytit bez překryvu. U interního triggeru se obdobně používá Strobe pro čtení statusu; jednotlivé podmínky řídí časovací schéma. [S-IV4 p.461, 463 / IV4_UserManual_WW_GB_AS_167146.pdf / Controlling Timing Using Ready Output]

IV4-H AS-170071 R2.10 (`iv4_f2b18663143f7e12`) má ve vlastní kapitole pro fyzické linky zdokumentovány odpovídající postupy BUSY a Trigger Ready + Strobe včetně trvale aktivního BUSY při krátkém intervalu. Přesto konfiguraci, polaritu, ON/OFF a One-Shot ověř podle konkrétní sestavy. [S-IV4-H p.542–545 / IV4_UserManual_WW_GB_AS_170071.pdf / Controlling Timing of Judgment with Triggers]
