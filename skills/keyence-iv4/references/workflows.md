# Praktické pracovní postupy

Doplněk v1.1.0: [historický runtime research](runtime-research.md) odděluje pozorování IV4-500CA R1.20.05 / R1.30.02 od níže uvedených manuálových či návrhových tvrzení; nepřenášet na IV4-H.

Tyto postupy jsou vlastní metodické zpracování GENERAL/INFERRED; dostupné konkrétní funkce vždy vybírej z modelových referencí a DOCUMENTED registrů.

## Model a kompatibilita

Vymez objekt, rozměr vady/FOV, pracovní vzdálenost, povrch a světlo, požadovaný takt a prostředí. Najdi konkrétní head/smart camera a amplifier; srovnej instalační mez a FOV pro tento model, CA/MA, příslušenství, I/O a jednotku. Ověř sensor/software verze a poznámky k tool/režimům. Výstupem má být zvolená sestava, source citace a otevřené fyzikální limity. Odvozená pixelová velikost není měřická přesnost.

## Vision kontrola a Navigator

1. Ujasni OK/NG, nejmenší tolerovanou vadu, variability polohy/šarže a reprezentativní validační data.
2. Ustabilizuj mechaniku a osvětlení; nastav snímání tak, aby odlesk/expozice neimitovaly vadu. Zvol skutečně podporovaný režim a trigger.
3. Zaregistruj master/learning správným nástrojem. Pro AI nepovažuj vysoké skóre trénovacího snímku za generalizaci.
4. Definuj position adjustment/ROI a konkrétní nástroj, jednotku výsledku a práh. Ověř chování když předmět nenalezen, OCR nečte, nebo nástroj není vykonán.
5. Nastav Total/Logic a výstup včetně invalid/stale větve. Otestuj border cases, rychlost, opakované díly a varianty, zaznamenej false accept/reject.
6. Ulož správný program a ověř backup/restore; právo přepnout recepturu není právo aktualizovat firmware. Konkrétní menu a limity: [Navigator](navigator.md), [tools](vision-tools.md), [logika](evaluation-logic.md).

## PLC a deskriptor

Zachyť PLC/engineering software verze, model/FW a síť. Vyber přesný descriptor hash/edition, DAP a moduly, směr IO, typy/délky a handshake. Připrav offline byte fixture, potom import a online test v povoleném prostředí. Žádný offset z optional module neoznač za globální. U code review hledej program mismatch, čtení starého OK, špatný signedness a chybný přepočet času/rozměru. Postup viz [PLC](plc-protocols.md).

## TCP klient a parser

SOURCE LOOKUP → CAPABILITY → WIRE CONTRACT → DESIGN → OFFLINE TEST → RUNTIME VALIDATION. Vyber rodinu, OF/režim a správný token v commands.json. Seznam parametrů je nutný, ale také podmínky a anomalies. Implementuj framing přes bytes, oddělenou frontu příkazů a časové limity jako aplikační volbu. Pro BR samostatný length-aware stav. Reconnect nesmí sám opakovat ne-idempotentní operace. Testy v této distribuci jsou offline.

## Diagnostika reálného logu

SYMPTOM → HYPOTHESES → MINIMAL TEST → OBSERVATION → NEXT ACTION. Zachovej raw odpověď/čas, přijatý příkaz, model/FW, program, režim, sekvenci a trigger ownership. Rozliš ER protokolu od RER/WR zařízení, socket timeout od dlouhé inspekce a historical RT od aktuálního dílu. Zúž na jeden rozlišující read-only test, například RM/SR/PR/VI nebo OPC UA Browse. Pokud log obsahuje credentials či adresy výroby, anonymizuj sdílenou ukázku při zachování framingu a číselné struktury.

## Monitoring a GPixel

Začni read-only capability profile, liveness, mode/status/errors, fresh result/program a teprve potom image/stats. Nenavrhuj obecné REST endpointy podle Web monitoru. V rozhraní konektoru odděl diagnostiku, výsledky a autorizované mutace. [GPixel proposal](gpixel.md) obsahuje datový obal i experimenty; je to návrh, ne OEM API.

## Když chybí manuály nebo důkaz

Použij vlastní reference a registry, uveď přesnou jejich verzi a limit. Nepředstírej přístup k původnímu obrázku. Nabídni konkrétní oficiální zdroj nebo malý experiment, který rozhodne nejasnost. Požadavek na nepodložený endpoint, barcode reader či úplný remote project upload označ UNVERIFIED; nezaměňuj to automaticky za trvalé tvrzení „zařízení neumí“.
