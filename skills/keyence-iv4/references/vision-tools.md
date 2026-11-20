# Nástroje IV4 a jejich volba

Doplněk v1.1.0: [historický runtime research](runtime-research.md) odděluje pozorování IV4-500CA R1.20.05 / R1.30.02 od níže uvedených manuálových či návrhových tvrzení; nepřenášet na IV4-H.

## DOCUMENTED — rozsah a společné nastavení

S-IV4 = FAST source_id `iv4_82ffe8b0fedc105a`, IV4 Series User’s Manual AS-167146 R1.30. Uvedené strany jsou PDF stránky. IV4-H R2.10 (`iv4_f2b18663143f7e12`) je samostatný produktový rozsah. [S-IV4 p.10, 106 / IV4_UserManual_WW_GB_AS_167146.pdf / Version and Tool Settings]

V Standard Mode manuál jmenuje AI Identify, AI Differentiate, AI Count, AI OCR, Color Area/Area, Color/Brightness Prohibition, Color/Brightness Averaging, Blob Count, Edge, Width, Diameter, Pitch, Outline, EdgePixels a position adjustment. Jejich dostupnost pro barevné a monochromatické typy se liší. Jeden program může mít až 65 nástrojů včetně lokalizace, nejvýše 64 detekčních; pro AI Count a AI OCR je limit po 16. Pokud je použit Position Adjustment nebo Outline, je jejich souhrnný počet podle nastavení obvykle přibližně 40; při algoritmu High Accuracy pro Position Adjustment přibližně 20. Jde o orientační údaj, nikoli garantovanou kapacitu konkrétního návrhu. [S-IV4 p.106, 482–483 / IV4_UserManual_WW_GB_AS_167146.pdf / Tool Settings and Specifications]

Search range omezuje prostor vyhledání a užší oblast může zkrátit čas. Mask vyloučí vybranou oblast; dostupnost závisí na nástroji. Pro více polohových nástrojů zkontroluj vazbu každého detekčního nástroje na správný korektor. [S-IV4 p.108–109 / IV4_UserManual_WW_GB_AS_167146.pdf / Common Tool Settings]

## DOCUMENTED — AI nástroje

**AI Identify:** hledá naučený objekt v oblasti. Vstupem je zarámovaný master target a případné další OK/NG příklady; nastavit lze oblast, masku, učení rotace a Limit. Při označení NG pro další učení se za NG učí celý search region. Zaměnění pozadí nebo neúplné reprezentativní učení může vyžadovat ověření na dalších vzorcích. [S-IV4 p.110–111 / IV4_UserManual_WW_GB_AS_167146.pdf / AI Identify]

**AI Differentiate:** pracuje s označenými OK/NG obrázky pro rozdíly ve vybraném okně. Obrázky mohou pocházet z pořízení, souboru nebo historie; nastav okno, masku a případnou korekci polohy. Při více takových nástrojích má základní OK snímek vyhovovat všem; smíšený obraz má vlastní postup dalšího učení. [S-IV4 p.112–115 / IV4_UserManual_WW_GB_AS_167146.pdf / AI Differentiate]

**AI Count:** označí a naučí objekty, které se mají započítat, v search range. Limit vyhodnotí rozsah počtu, Detection Threshold ovlivňuje uznání objektu. Missing Part Detection může navíc určit chybějící pozici; Total sčítá vybrané Count tools. Kontroluj i nežádoucí podobné objekty a vzájemné zakrytí. [S-IV4 p.116–119 / IV4_UserManual_WW_GB_AS_167146.pdf / AI Count and Total]

**AI OCR:** čte text, neprokazuje čtení QR nebo čárových kódů. Jeden nástroj čte nejvýše 32 znaků; má režimy String a Date/Time, obdélníkové nebo obloukové okno. String umí posuzovat text proti masteru nebo počet znaků; výběr povolených skupin znaků ovlivňuje čtení. Date/Time vyžaduje správný formát a umožňuje calendar sync. Další učení znaků ani zobrazení shody nesmí nahradit ověření čitelnosti všech očekávaných znaků. [S-IV4 p.120–123, 131 / IV4_UserManual_WW_GB_AS_167146.pdf / AI OCR]

**AI Through Count** počítá průchody naučených objektů přes count line; nejde o počet prvků na jednom statickém snímku. Manuál uvádí až dva count tools v High Speed/Standard a šest v High Accuracy. Ověř směr, zákryt, rychlost a reset na skutečném toku. [S-IV4 p.168–170 / IV4_UserManual_WW_GB_AS_167146.pdf / AI Through Count Mode]

## DOCUMENTED — kontrast a geometrie

**Color Area/Area** používá výběr barvy HSV u color nebo intervalu jasu 0–255 u monochrome; hodnotí extrahovanou oblast vůči referenci. Fixed Reference Area mění základ 100 %. **Color/Brightness Prohibition** hledá zakázaný odstín/jas v oblasti a může v kombinaci s maskou hledat přesah. Osvětlení, odlesk a histogram přímo ovlivňují extrakci. [S-IV4 p.137, 142–143 / IV4_UserManual_WW_GB_AS_167146.pdf / Area and Prohibition]

**Color/Brightness Averaging** porovnává průměrnou barvu/jas se základem. Referenci lze převzít z masteru nebo zadat přímo; přeregistrace masteru mění první, nikoli přímo zadanou hodnotu. Průměr může zakrýt malý lokální defekt. [S-IV4 p.145–147 / IV4_UserManual_WW_GB_AS_167146.pdf / Averaging Tool]

**Blob Count** počítá oddělené extrahované oblasti a dovoluje filtrovat jejich velikost. Sousední objekty se mohou obrazově spojit; šum naopak vytvořit další blob. **Edge** zjišťuje hrany; volí se směr bright→dark, dark→bright nebo obojí a Fine Edge pro úzké mezery. [S-IV4 p.149–151 / IV4_UserManual_WW_GB_AS_167146.pdf / Blob Count and Edge]

**Width, Diameter a Pitch** vybírají hrany podle nastaveného způsobu a porovnávají geometrickou veličinu s masterem. Width nabízí master/outer/inner; Diameter požadovaný, největší či nejmenší kruh; Pitch pracuje s jasnými nebo tmavými oblastmi a při jiném počtu roztečí vrací shodu 0. Scaling převádí referenci 100 na zadanou hodnotu; samotné zapnutí scalingu nedokazuje metrologickou přesnost ani kalibraci celé soustavy. [S-IV4 p.153, 155, 157 / IV4_UserManual_WW_GB_AS_167146.pdf / Width, Diameter and Pitch]

**Outline** hledá obrys se zadaným rozsahem rotace a algoritmem; rotace mimo rozsah vede k NG. **EdgePixels** používá množství hranových pixelů proti masteru nebo pevné referenci. **Position Adjustment** zarovnává navazující okna; příliš široká rotace zvyšuje tolerovaný rozsah, úzká může zkrátit čas. High-Speed Position Adjustment používá hrany pro jednu nebo dvě osy. [S-IV4 p.139–140, 159–161 / IV4_UserManual_WW_GB_AS_167146.pdf / Position Adjustment, Outline and EdgePixels]

## UNVERIFIED

Seznam na uvedené stránce nedokládá samostatný reader 1D/2D kódů. QR/barcode schopnost nezaručuj, dokud není doložena specifikací přesného modelu a verze. Žádná účinnost jednotlivých nástrojů nebyla ověřena na skutečných dílech.

## DOCUMENTED — rozšíření: skóre, hranice a interpretace

Nehledej jednotný význam čísla „100“ pro všechny nástroje. Area má 100 při shodě extrahované oblasti s referencí, přičemž větší plocha může dát hodnotu nad 100; horní limit se zapíná, je-li nežádoucí i nadbytek plochy. EdgePixels má jako výchozí referenci hranové pixely masteru, ale Fixed Reference Area změní 100 na počet odpovídající 1/20 celého zorného pole. U Averaging 100 značí shodu průměru s referencí a skóre s rozdílem klesá. Jejich skóre proto není zaměnitelné s pravděpodobností vady. [S-IV4 p.136, 144–146, 160–161 / IV4_UserManual_WW_GB_AS_167146.pdf / Area, Averaging and EdgePixels]

Nástroj Width má oddělenou citlivost rozpoznání hrany a limit výsledné šířky: první práh určuje rozpoznání hrany podle její intenzity vzhledem k maximu kontrastu, druhý posuzuje výsledek. Horní Limit dovoluje odmítnout i příliš široký objekt; ekvivalentně u Diameter příliš velký průměr. U Pitch se zobrazuje aktuální počet roztečí proti počtu masteru a při nesouladu je matching rate 0. Nastavení prahu na posuzovanou hodnotu neopravuje špatně vybranou hranu. [S-IV4 p.152, 154, 156 / IV4_UserManual_WW_GB_AS_167146.pdf / Width, Diameter and Pitch]

AI Count má alespoň dva odlišné nastavovací významy: Detection Threshold rozhoduje, co je rozpoznaným cílem; Limit rozhoduje, zda je počet v akceptovaném intervalu. U Blob Count limit hodnotí počet, zatímco Size Limit vyřazuje části podle plochy; maximum velikosti extrahované z masteru představuje referenci 100 pro filtr velikosti. U Edge se Limit ladí podle počtu hran, nikoli podle skóre shody obrysu. [S-IV4 p.117–118, 148–150 / IV4_UserManual_WW_GB_AS_167146.pdf / AI Count, Blob Count and Edge]

Při registraci AI Differentiate se zobrazuje Not Set, Ready to Learn, Not learned, Learned nebo Relearning required; změna nastavení tedy může vyžadovat nové učení. To, že nástroj existuje v seznamu, samo o sobě neprokazuje dokončený model. Při testu učení zobraz skóre i správně označené případy a porovnej nezávislé varianty. [S-IV4 p.112–113 / IV4_UserManual_WW_GB_AS_167146.pdf / AI Differentiate]

AI OCR má také režim Custom: přečtený řetězec lze rozdělit na pevné části, data, náhradní znaky a sériové číslo. U serial number je mimo jiné start, konec, krok, počet triggerů pro změnu a nulové doplnění. Význam aktuální hodnoty a její změny je nutné ověřit pro skutečný výrobní cyklus a případný reset, nejen pro statický obrázek. [S-IV4 p.124–125 / IV4_UserManual_WW_GB_AS_167146.pdf / AI OCR Custom]

## DOCUMENTED — IV4-H: samostatné AI nástroje

S-IV4-H = FAST source_id `iv4_f2b18663143f7e12`, IV4-H User’s Manual AS-170071 R2.10. **Tyto funkce nepřipisuj základnímu IV4 na základě následujících stran.** AI Imaging II nabízí optimalizované snímky po vyznačení cílové oblasti a umožňuje optimalizaci pro čtení znaků. [S-IV4-H p.94 / IV4_UserManual_WW_GB_AS_170071.pdf / AI Imaging II]

**AI Position Adjustment:** ohranič master target, nastav search range a případné Disable Area a rozsah rotace, spusť learning a ověř Test run. Rozšíření umožňuje Limit a odstranění nerelevantních oblastí. Při dalším učení NG se celý search region včetně okna učí jako NG. Symetrický objekt může znesnadnit určení rotace; manuál uvádí zúžení rozsahu pro tvary jako kruh nebo čtverec. [S-IV4-H p.150–151 / IV4_UserManual_WW_GB_AS_170071.pdf / AI Position Adjustment]

**AI Target Extraction:** při Extraction Target Learning označ oblasti k extrakci, další body přidej klepnutím, Exclude oblast vyloučí; dohromady je možné zadat až 127 extrakčních a vylučovacích bodů. Po learning zkontroluj extrakční masku na jiném obrazu a případně proveď další učení ON pro přítomný nebo OFF pro nepřítomný cíl. Search Range a volitelná position adjustment ovlivní použitelnou oblast. Advanced Limit umožňuje horní mez velikosti extrahované oblasti. [S-IV4-H p.152–154 / IV4_UserManual_WW_GB_AS_170071.pdf / AI Target Extraction]

Target Extraction může propojit masku s vybranými nástroji přes AI Targeting Linkage. Invert Extraction Area obrací oblast použitelnosti pro propojený nástroj; Background Color mění barvu zobrazení vypnuté oblasti, ne výsledek propojeného nástroje. Přesnou kompatibilitu každého propojeného nástroje a jeho výsledků ověř v úplném seznamu manuálu. [S-IV4-H p.153, 155 / IV4_UserManual_WW_GB_AS_170071.pdf / AI Target Extraction Linkage]

## GENERAL — ověřovací postup pro každou skupinu

- Lokalizace: použij krajní povolené posuny, rotace, zakrytí i chybějící referenční prvek; sleduj stav lokalizace i polohu navázaných ROI.
- Učené nástroje: odděl tréninkové a testovací kusy. Zaznamenej chybné klasifikace, jejich skóre a důvod označení. Přidáním dat měníš model a musíš znovu ověřit i dříve funkční kusy.
- Extrakce a blob: prohlédni binární/vybranou oblast, počet a velikost jednotlivých objektů. Ověř krajní jas, barvu, sloučení sousedů a drobný šum.
- Hrany a rozměr: zobraz detekované hrany; ověř polaritu, nesprávné odlesky, okraje obrazu a referenční kus. Pro milimetrový výstup vyhodnoť opakovatelnost a přesnost nezávisle.
- OCR: prověř každou skupinu znaků, font, délku, orientaci, proměnné pole, chybný text a částečné překrytí. Read úspěch a správná logika porovnání jsou dvě samostatné podmínky.
- Count a Total: ověř o jeden méně, o jeden více, záměnu objektů, případné zdvojení a vazby do součtu. AI Through Count ověř na reálném pohybu a po resetu.
