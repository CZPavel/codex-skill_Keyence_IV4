# Hardware IV4: výběr a hranice platnosti

## DOCUMENTED — zdroj a varianty

S-IV4 = FAST source_id `iv4_82ffe8b0fedc105a`, IV4 Series User’s Manual AS-167146, R1.30. PDF strany níže označují stránku souboru, nikoli tištěné číslo. S-IV4-H = `iv4_f2b18663143f7e12`, IV4-H User’s Manual AS-170071, R2.10; jde o samostatný rozsah a jeho vlastnosti nelze automaticky přenášet na IV4. [S-IV4 p.10 / IV4_UserManual_WW_GB_AS_167146.pdf / Version of the IV4 Series] [S-IV4-H p.10 / IV4_UserManual_WW_GB_AS_170071.pdf / Version]

IV4 nabízí snímače se zabudovaným zesilovačem IV4-400/500/600 CA a MA a také ultra-compact hlavy IV4-G400/G500/G600 s odděleným zesilovačem. Ověř kompatibilitu celého řetězce, nejen název hlavy; displej, počítačový Navigator, světlo a komunikační jednotka jsou samostatné součásti sestavy. Nespoléhej na to, že každé příslušenství je přibalené. [S-IV4 p.20, 24–31 / IV4_UserManual_WW_GB_AS_167146.pdf / System Configuration and Package Contents]

## DOCUMENTED — optika a osvětlení

Modely se zabudovaným zesilovačem 400 jsou narrow view, 500 standard a 600 wide view. Tabulka uvádí jako typický příklad při vzdálenosti 400 mm pro 400 zorné pole nejméně 58 × 44 mm; pro 500 při 50 mm nejméně 22 × 16 mm a pro 600 při 50 mm nejméně 51 × 38 mm. Jde o jednotlivé body specifikace, nikoli konstantní rozměr zorného pole v celém rozsahu. Všechny tyto modely používají 1280 × 960 pixelů. Barevné CA mají bílé LED, monochromatické MA infračervené LED; příslušné možnosti pulse/continuous se liší. [S-IV4 p.482 / IV4_UserManual_WW_GB_AS_167146.pdf / Specifications]

Ultra-compact G500 s OP-88909 tvoří zvláštní ultra-narrow variantu pro 23–40 mm; při 23 mm tabulka uvádí nejméně 9,8 × 7,3 mm. Hlavy G400/500/600 mají další vlastní podmínky. Automatické zaostření se provádí při instalaci, za provozu je vypnuto; polohu lze zaregistrovat podle programu. Výjimky expozičního času a teploty se liší podle sestavy a světla. [S-IV4 p.486 / IV4_UserManual_WW_GB_AS_167146.pdf / Ultra-compact model sensor head]

Volitelný polarizační filtr, rozptylná nebo dome optika a AI Lighting unit mohou změnit užitečný kontrast i montážní podmínky. Originální tabulka upozorňuje na výjimky krytí a doporučuje při použití nad 3 m filtr odstranit; pro konkrétní sestavu ověř celé poznámky. [S-IV4 p.27, 47–50, 483 / IV4_UserManual_WW_GB_AS_167146.pdf / Mounting and Specifications]

## GENERAL — jak volit sestavu

1. Změř nejmenší relevantní detail, celý rozsah polohy dílu, pracovní vzdálenost a prostor pro osvětlení. Do zorného pole přidej rezervu pro pohyb a lokalizační oblast.
2. Pro barevnou selekci zvaž barevný model; pro čistý jasový kontrast ověř také spektrální odezvu osvětlení a dílu. IR může způsobit jiný kontrast než lidský pohled.
3. Vyzkoušej reálné povrchy a jejich úhly, lesk, toleranci výšky a rušivé okolní světlo. Orientační počet pixelů na detail nezaručuje schopnost detekce.
4. Před objednáním ověř elektrické napájení a zapojení, rozhraní, kabeláž, teplotu těla a příslušenství ve specifikaci přesného modelu a revize. Neruš žádné krytí nebo bezpečnostní podmínky implicitním předpokladem.

## UNVERIFIED

Bez konkrétního stroje a testovacích dílů nelze potvrdit vhodnost optiky, dosah světla, spolehlivost detekce ani kapacitu průchodu. Tabulka FAST obsahuje automaticky extrahované buňky: kritické číselné parametry a poznámky ověř v originální stránce PDF.

## DOCUMENTED — počty nástrojů a použití paměti

Pro specifikované modely se zabudovaným zesilovačem je celková hranice 65 zahrnující detection a position adjustment; samotných detection tools je nejvýše 64 a AI Count i AI OCR mají limit po 16. Sorting má nejvýše osm detection tools. AI Through Count v High Speed/Standard připouští dva count tools a jeden Total, v High Accuracy šest count tools a dva Total. Skutečnou kombinaci dále omezují poznámky a zvolené nastavení; toto nejsou čísla univerzální pro jiný firmware či IV4-H. [S-IV4 p.106, 483 / IV4_UserManual_WW_GB_AS_167146.pdf / Tool Limits and Specifications]

Karta CA-MSD32G a SD Card Programs rozšiřují dostupná čísla programů z 32 na 128; pro built-in amplifier zůstává volba externími vstupy omezena na 32. Nezaměňuj paměť pro programy s kapacitou historie snímků, konfigurací záloh ani počtem inspekčních nástrojů. [S-IV4 p.225, 482–483 / IV4_UserManual_WW_GB_AS_167146.pdf / Program Functions and Specifications]

## GENERAL — srovnání montážních konceptů

Built-in amplifier sdružuje senzor a zesilovač v těle, což zjednodušuje rozmístění komponent, avšak celý přístroj musí mít prostor v místě snímání. Ultra-compact odděluje hlavu a zesilovač, takže posuzuj navíc trasu a přípustné kabely, místo zesilovače a kompatibilitu hlavy. Typ G500 s OP-88909 není totožný s běžným G500 bez této optiky: jeho specifikace uvádí pracovní vzdálenost 23–40 mm. [S-IV4 p.20, 31, 486 / IV4_UserManual_WW_GB_AS_167146.pdf / System Configuration and Specifications]

**UNVERIFIED:** Jednoduchý počet vstupů/výstupů nelze zobecnit přes built-in, ultra-compact a připojenou komunikční jednotku bez konkrétního modelu a přiřazení obousměrných linek. Pro návrh zapojení otevři schéma a elektrické parametry dané varianty v manuálu; nepoužívej neověřené číslo jako specifikaci.

## DOCUMENTED — konkrétní příklad elektrických I/O zesilovačů

Následující údaje jsou pro **IV4-G120 / IV4-HG120 amplifier**, nikoli pro každou smart camera či samotnou ultra-compact hlavu. Příslušné datasheety p.2 uvádějí 8 vstupů IN1–IN8 a 8 výstupů OUT1–OUT8. IN1 je External Trigger, IN2–IN8 mají přiřaditelné funkce. Volba NPN/PNP a funkce pinů musí odpovídat zapojení konkrétní instalace.

Napájení je 24 V +25 % / −20 % včetně zvlnění. Open-collector výstup má mez 30 V / 50 mA, celkový výstupní proud je podle poznámky nejvýše 160 mA. Údaj residual voltage 1.5 V se váže na proud do 20 mA; při 50 mA je v poznámce 2.0 V. Nezaměňuj per-channel maximum a celkový součet nebo jmenovité napětí napájení a mez zatížení výstupu. Pro vstupy se liší voltage/non-voltage nastavení a rozhodovací úrovně; pinout a polaritu vždy ověř ve schématu.

Zdroje: `iv4_908efa1aaaca2f1c` / IV4-G120_Datasheet.pdf PDF p.2 a `iv4_cac2f74e5d20fba3` / IV4-HG120_Datasheet.pdf PDF p.2, Electrical I/O/Power a proudové poznámky. Jde o dokumentované hodnoty, nikoli test zatížení.
