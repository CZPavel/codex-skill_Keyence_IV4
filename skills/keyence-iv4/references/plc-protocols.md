# Průmyslové protokoly, PLC a statické deskriptory

DOCUMENTED zdroje: IV4_UserManual_WW_GB_AS_167146.pdf, S-IV4 / `iv4_82ffe8b0fedc105a`, EtherNet/IP PDF p.296–333, PROFINET p.334–367, EtherCAT p.368–397. IV4_UserManual_WW_GB_AS_170071.pdf, S-IV4-H / `iv4_f2b18663143f7e12`, odpovídající p.332–379, 380–427, 428–473. Přesné identity connection guides jsou v [sources.json](sources.json). Údaje XML/EDS jsou oddělené DESCRIPTOR_ONLY v [descriptors.json](descriptors.json).

## Model, role a přenosový směr

Nejdříve stanov, zda se používá integrovaný Ethernet senzoru nebo IV4-CU1/GCU1. PROFINET CC-B je popsán pro senzory, CC-C s příslušnou jednotkou; EtherCAT v citované kapitole je funkcí CU1/GCU1. Přečíst správnou variantu modulu není totéž jako zařízení nakonfigurovat. DL komunikační jednotky mohou zpřístupnit další protokoly, ale z datasheetového seznamu nelze vyrobit jejich wire contract ani je aktivovat bez konkrétního typu a návodu.

PLC input area přijímá sensor status/result/statistics, PLC output area odesílá požadavky/řízení. Z pohledu kamery je směr obrácený. Zaznamenej směr slovně i symbolem PLC→IV nebo IV→PLC; výraz „vstup 0“ bez směru je nejednoznačný. Firmware, EDS/GSDML package version, XML schema a PLC library version eviduj zvlášť.

## EtherNet/IP: velikosti, vlastnictví a RPI

Pro IV4-H p.334–335: Exclusive Owner dovoluje řízení i data; Input Only data bez řízení. V tomto manuálu jsou vstupní assemblies 100/101/102/103 (standard/x4 detail/x8 detail/simple), výstupní 110 pro řízení; Input Only používá protisměrnou instanci 254 s nulovou délkou. Výběr vstupního formátu mění interpretaci struktury; není jen jiný název stejného bufferu.

H deklaruje vstup 2–1400 bytů a řídicí výstup 2–104 bytů, RPI 4–10000 ms. Více PLC nemůže současně otevřít Exclusive Owner nad jedním senzorem. Input Only je popsáno až pro 16 klientů; při souběhu dodrž multicast a shodu RPI/velikosti. Tato čísla nepřenášej automaticky na jiné rodiny/FW; čti S-IV4 p.299 pro IV4. EDS vlastnost sama není důkaz, že byl rozměr v PLC správně zvolen.

Handshake je výchozí Disable a běžně se používá, když interval triggerů převyšuje RPI. Enable může bufferovat až deset výsledků, pokud trigger předběhne komunikační cyklus a počet triggerů odpovídá popsané mezi. Stav se pak neposune, dokud PLC neodešle Result acquisition complete notice. H uvádí Output Assembly address 2 bit 0; je to adresa uvnitř konkrétní assembly, ne absolutní adresa registru PLC. Nestačí číst celkový OK opakovaně: PLC musí rozlišit nový výsledek a teprve po konzistentním převzetí potvrdit acquisition complete. H p.334 a 369+; přesné hrany/timing podle konkrétního schématu. Nedělej výsledek z neprovedeného nebo starého cyklu.

Byte Swap mění uložení textů OCR/jmen souborů v 2bytových skupinách. Není to obecný důvod obracet každé WORD/DWORD. Vyzkoušej známý syntetický řetězec i asymetrické číselné hodnoty. Doporučený offline fixture musí zachovat délku, padding, pořadí bytů i platnost. Samotná shoda jedné nuly nic neověří.

## PROFINET a S7-1500

Pracovní postup podle dodané AS169896 connection guide (IV4_ConnectionGuide_CommunicationManual_WW_GB_AS_169896.pdf): ověř rodinu a firmware; vyber správný GSDML/DAP; připrav projekt S7-1500/TIA odpovídající návodu; nastav stanici/IP a síť; zvol moduly podle požadovaných dat; připoj IO a ověř diagnostiku. Přesné kroky a verze řeš podle konkrétní kapitoly guide, nikoliv názvu PLC samotného. Veřejný oficiální [KV-X connection guide](https://www.keyence.com/support/user/controls/plc/connection_guide/kv-x_iv4/) navíc dokládá Navigator cestu Settings and Operation → Search Sensor/Connect → Sensor Setup → Sensor Advanced → Utility/Communication Setting → FieldNet/Comm.Unit a upozorňuje, že použití nastavení může vést k restartu. Tento příklad není S7 importní test a neprokazuje stejné UI ve všech verzích.

H p.383–384 popisuje Command Control, Additional Setting Value, Command Status Bits, Device Result Bits, Device Status Words, Device Statistics, Position Adjust Result a Tool Result. Řídicí Command Control je v uvedeném rozložení slot 1 a 12 bytů. Požadovaný program, práh, master text nebo file-name se interpretují podle příznaku operace; jeden payload se nesmí současně vykládat jako několik nesouvisejících požadavků. PLC musí čekat na správný control result/status, ne pouze na běh cyklického spojení.

Konkrétní H příklad Device Status Words (p.403) uvádí lokální WORD pole: error 0–1, warning 2–3, remaining buffers 4–5 (0–10), část checksumu 6–7, aktuální program 8–9, program posledního výsledku 10–11, result number 12–13 (0–32767), process time 14–15 (ms, 0–10000). Tyto adresy jsou uvnitř zvoleného modulu. Dvě programová pole umožňují zachytit starý výsledek po přepnutí receptury. Checksum nedetekuje změnu IP/subnet/gateway/portu. Neodvozuj „všechno je aktuální“ jen ze shody checksumu.

Preliminary Capture a field-network result handshake jsou odlišná nastavení. Fyzické 2-image Buffer časování vyžaduje Ready+Strobe, zatímco fieldbus buffer má vlastní notices a remaining buffers. Rozlišení kapitoly a transportu je důležité: fyzický Strobe není automaticky libovolný bit každého PLC modulu. Uveď přesnou sekvenci z modelově správného timing diagramu a ověř, které výsledky bufferuje.

## Jak číst GSDML

DESCRIPTOR_ONLY: tři zachované identity XML (V2.42 20240516, V2.44 20251111, V2.44 20260203) mají VendorID 0x01FD a DeviceID 0x0FA4, ale odlišné SHA a DAP. V2.44 soubor může obsahovat DAP s PNIO_Version V2.42 i V2.44; číslo v názvu souboru neurčuje všechny jeho atributy. DAP1 je senzorový přístupový bod, DAP3/DAP4 jednotky GCU1/CU1 podle deklarovaného názvu, novější soubory obsahují také DAP5. ID, ModuleIdentNumber a SubmoduleIdentNumber jsou odlišné identity.

Příklad postupu: `lookup.py --descriptor DAP5` → vyber exact source SHA a člen archivu → prohlédni PhysicalSlots/usable module refs → ID modulu a jeho submodul → IO direction → DataItem type/length → BitDataItem a text reference. Číselnou délku nepovažuj bez typu za byty a BitOffset nepovažuj za globální bit PLC. MaxInputLength/MaxOutputLength je limit konfigurace daného DAP, nikoliv automaticky délka každé zprávy. Ve veřejném registru jsou všechny module identity a IO type summaries, ale jen vybrané field examples; přesný plný mapping vyžaduje původní deskriptor nebo lokální evidence.

Module ID 303 například není obecně totéž číslo jako jeho ModuleIdentNumber 0x00000304; neinferuj číselnou rovnici mezi nimi. Fyzické sloty mohou být volitelné. Výsledná absolutní adresa vzniká až v konkrétním PLC projektu. Public registr nenahrazuje originální XML ani schema-validaci; pro dodaný XML používej parser bez externích entit a odmítej DTD/XXE. Existence konfigurace není potvrzení aktivní podporované sestavy.

## EDS a Rockwell

Lokální IV4-H EDS identita uvádí VendorCode 367, ProductType 43, ProductCode 4608, major/minor 1/1. To je identity zařízení podle souboru, nikoliv softwareVersion ZIP 2.00.00. Factual registr obsahuje Assem100–103 s deklarovaným size literal 1400 a Assem110 se 104 a osm connection záznamů. Nevybírej assembly pouze podle největšího čísla a neodvozuj aktivní IO velikost z plné deklarované kapacity.

Rockwell AOI V32/V36 jsou statické L5X exporty distribuované v lokálním podkladu. Bez autorizované redistribuce se nepřibalují. Import správné verze, datové typy, Exclusive Owner a návratový handshake se musí ověřit na konkrétním Studio 5000/PLC; úspěšné parsování L5X není importní ani online test. Nezaměňuj EDS s ESD podle přípony.

## EtherCAT a další guide větve

S-IV4-H p.428–473 popisuje CU1/GCU1, PDO, mailbox a Object Dictionary; IV4 p.368–397 je samostatná edice. Vyber ESI pro jednotku a firmware, ověř PDO pořadí, index/subindex, velikosti a timing. PROFINET guide pro Beckhoff CX5100 není EtherCAT nastavení jen proto, že má Beckhoff controller. Podobně OMRON NJ/NX guide AS169473 dokládá EtherNet/IP, nikoliv automatickou podporu všech protokolů této PLC řady.

Offline acceptance: validace descriptor identity/verze, typů a délek, encode/decode fixture, endian a text padding, starý výsledek, program mismatch, buffer full a reset. Hardware acceptance: skutečný import, online diagnostics, IO update, handshake pod zátěží, ztráta spojení a návrat. Žádný z posledních HW bodů zde nebyl proveden.
