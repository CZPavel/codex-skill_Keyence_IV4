# Verze a aktuální oficiální doplnění

Doplněk v1.1.0: [historický runtime research](runtime-research.md) odděluje pozorování IV4-500CA R1.20.05 / R1.30.02 od níže uvedených manuálových či návrhových tvrzení; nepřenášet na IV4-H.

Kontrola veřejných primárních zdrojů: 2026-11-13. Nejde o tvrzení, že je tato verze aktuální navždy. Před upgradem znovu ověř přesný model, zálohu a oficiální postup.

| Komponenta | Detailní release stránka | Verze / datum v detailu |
|---|---|---|
| IV4 sensor / CU1 / GCU1 | [WEB-IV4-FW](https://www.keyence.com/popup/downloads/software/description/iv4_g120/) | R1.30.02 / 2024-12-10 |
| IV4-H sensor | [WEB-H-FW](https://www.keyence.com/popup/downloads/software/description/iv4-h_g120/) | R2.10.01 / 2026-09-01 |
| IV Smart Navigator update | [WEB-NAV-RELEASE](https://www.keyence.com/popup/downloads/software/description/iv-h1sn/) | R2.10.01 / 2026-09-01 |

DOCUMENTED: Navigator R2.10 podporuje H sensor R2.00 a R2.10. H R2.10 release přidává operation-log output. IV4 R1.30 obsahuje IoT/security a další změny popsané v detailní historii; nelze je všechny vydávat za nové funkce H. Lokální manuály zůstávají verzově samostatné.

[Software catalog](https://www.keyence.com/support/user/vision/iv4/software/) používá jiné datumové položky: pro H/Navigator má softwareLastUpdateDate převedeno na japonské kalendářní datum 2026-07-06 a publishDate 2026-09-14. Detailní release stránka uvádí 2026-09-01. Tyto údaje nesjednocuj bez vysvětlení. Datum přístupu ani extrakce KB nejsou datum vydání.

DOCUMENTED provozní omezení z detailů: firmware update IV4 i H smaže nastavení a image history; připrav a ověř potřebnou obnovu. Navigator updater vyžaduje předchozí instalaci a jeho spuštění nad stejnou již instalovanou verzí může místo update provést odinstalaci. Skill upgrade ani live změny neprovádí automaticky. Tato upozornění se týkají přesných citovaných postupů, nikoliv obecného závěru o každém instalátoru.

[Oficiální GSDML detail](https://www.keyence.com/popup/downloads/software/description/iv4_profinet/) uvádí V2.44 soubor s datem 20260203, IV4-H od R2.00, IV4 od R1.20 a CU1/GCU1 od R1.20. ZIP version, XML schema verze a firmware jsou různé věci. Tento text není importní test PLC.

Přístup: některé downloady jsou značeny požadavkem na serial number. Binární instalační ani firmware soubory se nestahovaly/spouštěly. Public HTML detail release byl čitelný běžným HTTPS, i když hlavní textový web parser popup neotevřel. Seznamy manuálů a některých PLC partnerů nebyly v parsed view kompletní; není to důkaz, že materiál neexistuje.
