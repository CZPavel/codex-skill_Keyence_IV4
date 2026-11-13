# IV Smart Navigator a nastavení programu

## DOCUMENTED — verze a postup

S-IV4 = FAST source_id `iv4_82ffe8b0fedc105a`, IV4 Series User’s Manual AS-167146, R1.30. Citace jsou PDF stránky. IV-H1SN je PC software; ověř instalovanou verzi a kompatibilitu s cílovým senzorem. Rozsah IV4-H R2.10 je odlišný, source_id `iv4_f2b18663143f7e12`. [S-IV4 p.10, 29, 67–68 / IV4_UserManual_WW_GB_AS_167146.pdf / Version and PC Setup]

Sensor Setup vede v krocích: zvol Standard, Sorting nebo AI Through Count, optimalizuj obraz, registruj master, nastav nástroje a přiřaď výstupy. Standard posuzuje snímek vůči registrovanému základu. Sorting a průchozí počítání mají odlišný účel a vlastní nastavovací cestu. Nelze z nich vyvozovat stejný význam celkového výsledku bez kontroly aktuálního režimu. [S-IV4 p.88, 100, 106, 162, 168, 176 / IV4_UserManual_WW_GB_AS_167146.pdf / Sensor Setup]

Při registraci masteru umísti reprezentativní OK díl do snímací polohy. Pro External Trigger a AI Trigger manuál doporučuje skutečný trigger; dočasný interní Trigger ON je dostupný, pokud trigger nelze dodat. Před uložením ověř skutečný snímek, ostrost, pokrytí oblasti a správný program. [S-IV4 p.100 / IV4_UserManual_WW_GB_AS_167146.pdf / Master Image Registration]

## DOCUMENTED — nástroje a učení

Add Tool vloží nástroj, Edit jej upraví, Copy vytvoří další s novým dostupným číslem a Delete jej odstraní. Oblast hledání a maska nejsou dostupné u každého nástroje. U AI Identify a AI Count maska platí pro search range; nemá zakrýt vlastní tool window. Pozor na volbu přiřazené position adjustment: u multi-master lze vybírat jen nástroj stejného masteru a výchozí volba je None. [S-IV4 p.107–109 / IV4_UserManual_WW_GB_AS_167146.pdf / Tool Settings]

AI Identify umožňuje master learning a další učení na OK/NG příkladech. Při učení NG se za NG učí celý search region včetně okna. AI Differentiate pracuje s registrovanými OK a NG obrazy; existuje import z historie nebo souboru. Při více AI Differentiate nástrojích má počáteční OK obraz odpovídat OK pro všechny; smíšené stavy vyžadují další postup podle manuálu. Po učení použij Test run a nezávislé příklady. [S-IV4 p.110–115 / IV4_UserManual_WW_GB_AS_167146.pdf / AI Identify and AI Differentiate]

## DOCUMENTED — programy, historie, zálohy

Pro built-in amplifier specifikace uvádí 32 programů bez SD a 128 s SD; další podmínky ověř pro konkrétní sestavu. Program switching má nastavitelný způsob a může vyžadovat SD. Po přepnutí nebo návratu do RUN ještě není nový úsudek, dokud nepřijde trigger; dílčí výsledky jsou před ním OFF. [S-IV4 p.224–230, 177, 482 / IV4_UserManual_WW_GB_AS_167146.pdf / Program Functions and Output Assignment]

Historie běhových snímků pomáhá zkoumat chybné i hraniční případy. Manuál popisuje také jednotlivý a batch backup, přenos nastavení, uložení na SD a automatické zálohování/obnovu. Soubor `.iv4a` lze v popsaném kontextu použít jako zdroj vybraných master, learning či running-history obrázků; netvrď, že každý export obsahuje vše. [S-IV4 p.114, 192–196, 262–280 / IV4_UserManual_WW_GB_AS_167146.pdf / History and Settings Transfer]

## GENERAL — bezpečný pracovní postup

Před úpravou zaznamenej číslo programu, režim, verze, způsob triggeru a přiřazení výstupů; vytvoř odpovídající zálohu a ověř, co obsahuje. Po úpravě porovnej nový stav se záznamem, vyzkoušej obnovu jen v bezpečném prostředí a otestuj každý významný stav. Záloha souboru bez skutečného testu obnovy není prokázaná obnova. Změnu aktivního programu na lince koordinuj s obsluhou a PLC logikou.

## UNVERIFIED

Konkrétní instalace Navigatoru, oprávnění, konektivita, uložené programy ani skutečná obnova nejsou tímto textem ověřeny. Rozhraní a dostupné položky mohou záviset na verzi a sestavě.

## DOCUMENTED — první spuštění a čtyři kroky podrobně

1. Zapni senzor, spusť IV Smart Navigator, přejdi do Program, vyber cílové číslo a otevři Sensor Setup. Nový nebo neinicializovaný program vyžaduje volbu Standard, Sorting nebo AI Through Count. Změna režimu již nastaveného programu vyžaduje inicializaci tohoto programu; předem uchovej potřebná data. [S-IV4 p.90 / IV4_UserManual_WW_GB_AS_167146.pdf / Starting Sensor Setup]
2. **Image Optimization:** Smart Image Optimization vytvoří kandidáty po označení zájmové oblasti; zvol snímek, na kterém je potřebná vada rozlišitelná. Automatic Brightness Adjustment lze vztáhnout na celý obraz nebo označenou oblast. Normal je základní režim; HDR je určeno například pro lesklý kov s vysokým kontrastem; High Gain umožní tmavší scénu nebo kratší expozici za cenu nižší kvality obrazu. [S-IV4 p.92, 97 / IV4_UserManual_WW_GB_AS_167146.pdf / Image Optimization]
3. **Master Image Registration:** zaregistruj reprezentativní obraz dílu v poloze odpovídající provozu. Po změně optimalizace kromě Trigger Options manuál doporučuje opětovnou registraci masteru. Změna Imaging Area vyžaduje znovu nastavit AI Trigger, master, nástroje i learned image history. [S-IV4 p.92, 99–100 / IV4_UserManual_WW_GB_AS_167146.pdf / Image Optimization and Master Registration]
4. **Tool Settings/Part Registration:** přidej nástroje nebo zaregistruj díly podle režimu. Přizpůsob jejich okna, učení a prahy, otestuj známé OK i NG a ověř navázanou korekci polohy. Standard, Sorting a Through Count nemají shodné sady nástrojů a limity. [S-IV4 p.106–109, 162–163, 168 / IV4_UserManual_WW_GB_AS_167146.pdf / Tool Settings]
5. **Output Assignment:** vyber fyzické či další výstupní funkce a total logic dle režimu. Dokonči všechny požadované kroky tlačítkem Complete a potvrď uložení. Uložení neúplných povinných nastavení může projít, ale manuál výslovně upozorňuje, že správný provoz nebude možný. [S-IV4 p.91, 174–177 / IV4_UserManual_WW_GB_AS_167146.pdf / Exiting Sensor Setup and Output Assignment]

## DOCUMENTED — trigger, pohyb a volby obrazu

External Trigger umožňuje časovat snímek externím senzorem nebo PLC a nastavit Trigger Delay. Internal Trigger používá interval, případně řízený externím vstupem/field network podle konfigurace. AI Trigger se učí rozlišovat ON obrazy, na nichž má být vyhodnocení spuštěno, od OFF obrazů pozadí. Nastaví se směr pohybu a volitelně zpoždění; pro AI Trigger je nejvýše 100 obrázků a současně nejvýše 200 learned images na program včetně ostatních learn tools. [S-IV4 p.94–95 / IV4_UserManual_WW_GB_AS_167146.pdf / Trigger Options and AI Trigger]

AI Trigger automaticky zapíná Preliminary Capture a vypíná Distortion Correction, Trapezoidal Shape Correction, Multi-Capture a Program Auto-Switching. Multi-Capture skládá expozice při různých směrech světla, takže cíl musí po danou dobu stát; není dostupný v AI Trigger ani AI Through Count. Preliminary Capture umožňuje přijmout další trigger před dokončením předchozího vyhodnocení, ale samo o sobě neprokazuje konkrétní kapacitu linky ani párování. [S-IV4 p.94, 97, 99 / IV4_UserManual_WW_GB_AS_167146.pdf / Trigger and Imaging Functions]

## DOCUMENTED — Sorting, počet programů a přepínání

Sorting registruje nejvýše osm typů Part 0–7. Master se stává Part 0; učení vyžaduje nejméně dva typy. V jednom programu lze nastavit nejvýše osm detection tools a jeden Position Adjustment/High-Speed Position Adjustment. Pro AI Differentiate se po registraci spouští learning, pro ostatní vybrané nástroje následuje nastavení limitů; typ a počet dostupných nástrojů se liší od Standard Mode. [S-IV4 p.162–163, 166 / IV4_UserManual_WW_GB_AS_167146.pdf / Sorting Mode]

Pro P032–P127 je nutná podporovaná SD karta a povolené SD Card Programs. Built-in amplifier může externími vstupy přepínat nejvýše 32 programů; vyšší čísla vyžadují jiný dokumentovaný způsob přepnutí. Nelze tedy zaměnit kapacitu uložených programů a rozsah volby vstupy. Program Details umožňuje Copy, Import a Initialize. Import ze souboru má zdroj a cílové číslo; manuál rozlišuje SD kartu v senzoru od SD v panelu/displeji. [S-IV4 p.225, 227, 229–230 / IV4_UserManual_WW_GB_AS_167146.pdf / Program Functions]

## DOCUMENTED — rozsah záloh a obnova

Batch Backup ukládá nastavení všech programů a pokročilá nastavení; historie provozních snímků se přidává volbou Save Running Hist., s filtrem All/NG Only a volbou 20/50/100 snímků. Pokud je povolen SD Card Access, zahrnuje i data programů uložených na SD. Individ. Program Backup vybírá konkrétní program. Manuál doporučuje režim Program, protože v RUN mohou být snímky historie během zálohování nahrazeny nebo smazány. [S-IV4 p.263–264 / IV4_UserManual_WW_GB_AS_167146.pdf / Batch and Individual Backup]

Transfer Batch Backup má samostatnou volbu pro přenos NPN/PNP polarity a síťových nastavení; výchozí volba se po přenosu či zrušení vrací na OFF. Změna protokolu může ukončit spojení a restartovat senzor. Transfer Individual Backup nabízí zdrojový a cílový program a následnou volbu přepnutí. Před obnovou zkontroluj rozsah přenosu i dopady na linku. [S-IV4 p.265–266 / IV4_UserManual_WW_GB_AS_167146.pdf / Transfer Backup]

Automatická SD Settings Backup je jiný mechanismus: dokumentovaný příklad kopírování zahrnuje P000–P031, nikoli P032–P127. Podmínky obnovy zahrnují stejný model, typ napájení a kompatibilní verzi; obnova je popsaná pro tovární či inicializovaný senzor. Při zapnutém SD Settings Backup může Initialize Sensor inicializovat také zálohovací soubory na kartě. Tato operace proto není náhradou za nezávisle uloženou zálohu. [S-IV4 p.279–280 / IV4_UserManual_WW_GB_AS_167146.pdf / Automatic SD Backup and Restore]

## GENERAL — údržba a přejímka změny

Před zásahem zdokumentuj stávající verze, připojenou hlavu a jednotky, počet programů, cílovou SD, parametry triggeru a výstupů. U zálohy výslovně ověř rozsah historie, SD programů a polarity/sítě. Po autorizovaném přenosu nebo aktualizaci nejprve bezpečně otestuj načtení konfigurace a správný program, potom obraz, trigger, nástroje, fyzické výstupy a komunikaci; obnovení na cílovém zařízení ověř jen s ohledem na jeho provozní stav.

## DOCUMENTED — volba handshake a čísla programů

V IV4 R1.30 se při běžném řízení externím triggerem používá BUSY: po dokončení a přechodu BUSY do OFF lze načíst status; trigger během BUSY se ignoruje. Při Preliminary Capture ON (2-image Buffer) se další externí trigger řídí Trigger Ready a výsledek se čte synchronně se Strobe. BUSY může při krátkém intervalu zůstat trvale ON a není pak signálem pro načtení výsledku. Přiřazení linek, polaritu, nastavení Strobe a průchod signálu PLC ověř na dané instalaci. [S-IV4 p.460–461 / IV4_UserManual_WW_GB_AS_167146.pdf / Trigger Timing]

Zdroj IV4 pro výběr programu uvádí označení P000–P031 bez rozšíření a P000–P127 s povolenými SD Card Programs; TCP příkaz pracuje s číslem 000–127. Manuál na těchto místech **nepotvrzuje převod UI 1–128 na wire 0–127**, proto jej nepředpokládej. Zobrazované označení a skutečně zasílané číslo ověř v příslušném Navigatoru a komunikaci. [S-IV4 p.224, 430 / IV4_UserManual_WW_GB_AS_167146.pdf / Program Functions and TCP Program Switching]
