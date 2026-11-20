# GPixel design proposal

Doplněk v1.1.0: [historický runtime research](runtime-research.md) odděluje pozorování IV4-500CA R1.20.05 / R1.30.02 od níže uvedených manuálových či návrhových tvrzení; nepřenášet na IV4-H.

Tato reference je INFERRED návrh budoucího konektoru. Žádný IV4 GPixel connector, device server ani fleet agent zde není implementován. Schopnosti zařízení vybírej z [capabilities.json](capabilities.json), příkazy z [commands.json](commands.json), nikoliv z generických názvů rozhraní tohoto návrhu.

## Oddělené cesty

| Potřeba | Doložený kandidát | Nutná podmínka / mezera |
|---|---|---|
| Identita | VI, přesný source/runtime model/FW | VI není verze Navigatoru ani bezpečný fleet discovery protocol |
| Stav a diagnostika | RM/SR/RER/WR/TP/STR; OPC UA/MQTT pole | Zapnutá služba, program a validita, polling budget |
| Inspekční výsledek | RT/T2, PLC cyclic, OPC UA/MQTT | Frame/schema, fresh cycle, program/result association |
| Obraz | BR latest BMP, MQTT Base64, FTP/SFTP/SD | Vlastní length/framing, transfer completion a korelace |
| Receptura | PW/PR a vybrané parametry | Nejde o úplný upload/download celého projektu |
| Fleet konfigurace | UNVERIFIED jako jednotné API | Potřebuje samostatný výzkum podporovaných operací |

Zdrojové rozsahy: S-IV4 chapter 9 p.281–446 a S-IV4-H chapter 9 p.313–528. Každý protokol má vlastní role, session a oprávnění; nelze z jednoho konfiguračního UI odvodit nezávislé SDK.

## Návrh adaptérového rozhraní

Jména `identify`, `connect`, `read_status`, `read_results`, `read_diagnostics`, `get_latest_image`, `select_program` jsou jen **GPixel design proposal**, nikoliv názvy metod KEYENCE SDK či endpointů. Discovery je hostem řízený seznam konfigurací nebo autorizovaný read-only průzkum; z VI nedělej UDP broadcast discovery. Transport manager vlastní serial request queue a explicitní přepnutí parseru pro BR. Neprovádí automatické zápisy po reconnect.

Capability profile musí obsahovat rodinu/model, sensor FW, unit type/FW, source edition, aktivní protokol, povolené operace a evidence status každé. Nepřiděluj capability pouze podle toho, že TCP port odpoví. Neúspěšné připojení také neznamená, že model funkci neumí; služba může být vypnutá nebo blokovaná.

Datový obal INFERRED: host session_id/cycle_id, device identity, current/result program, device counter a čas, host receive time, format/schema version, validity, status, raw response hash/reference a případný image reference. Zdrojová data nesmějí zmizet za jedním boolean OK. `--` a chybějící nástroj jsou odlišné od NG. Counter modulo 32768 potřebuje session kontext a nelze z něj sám dopočítat absolutní počet dílů po dlouhém výpadku.

## Receptury, concurrency a obnova

Před změnou programu zastav plánování triggerů, identifikuj aktuální program, ověř záměr a Switching method, odešli autorizovanou změnu, zkontroluj odpověď a PR, teprve potom přijmi první nový validní výsledek nové receptury. To je navržená transakce, ne důkaz atomické OEM operace. Po timeoutu PW nebo T1 neprováděj slepý retry: první požadavek mohl být vykonán.

Navigator a externí klient nesmí bez koordinace konkurovat jako dva vlastníci konfigurace. Dvě TCP spojení a EtherNet/IP Input Only nejsou totéž co souběžné řídicí session. Uchovávej odděleně chtěný program, potvrzený program, program výsledku a stav převzetí. Backup/restore vyžaduje ověřený formát a postup; tento návrh negarantuje vzdálený úplný export.

Při odpojení označ stale data, uzavři rozpracovaný cyklus a zachovej důkazy. Po reconnect znovu přečti identitu/stav/program, obnov jen povolené nepersistentní parametry se známými důsledky (např. OE podle záměru), a nepoužij historický RT jako první nový kus. Pro fyzický buffered capture nečekej univerzálně BUSY OFF; transportově správný handshake je součást capability profile.

## Navržené experimenty — zatím UNVERIFIED

1. Read-only identita a porty: známý model/FW, povolená služba, VI/PR/RM/SR, žádné triggerování. Výstupem je skutečný capability evidence record.
2. ASCII stream fixture a kamera: partial/coalesced frames, ER02/03/22, volby OF/OE, SP/NULL a UTF-8. Nejprve offline, potom omezený bench.
3. T1 versus T2: zaznamenat trigger, ACK, BUSY/Ready, counter, platný výsledek; test při Program, bez inspekce po restartu a při program switch.
4. BR: rozdělený header, binární délka, CR uvnitř BMP, case odpovědi, color/mono a full/half. Současně ověřit, zda jde opravdu o obraz konkrétního cyklu.
5. Rollover/reconnect: counter 32767→0 a ztráta spojení mezi provedením a odpovědí. Bez předstírání přesně-jednou transakce.
6. PLC: explicitní DAP/assembly/velikosti, endian, text swap, platnost výsledku a handshakované buffer full. Testovat zvolenou variantu zvlášť.
7. OPC UA: Browse namespace URI/types/method IDs a dokumentové rozpory; certificate/time/auth. Succeeded přijetí metody versus pozdější výsledek.
8. MQTT/FTP: retained stale messages, Clean Session, QoS, ztráta brokeru/serveru, plná karta/server a dokončení více transfer conditions.
9. Výkon: měřit takt a image/result zátěž se skutečnou scénou; nedělat produkční toleranci z katalogového maxima.
10. Autorizovaná konfigurace a obnova: backup → změna → ověření → návrat; firmware update patří do samostatného servisního okna.

Protokol testu: identita, cíl, změny, preconditions, očekávání, měřený vstup/výstup, chyby, rollback a přesný závěr. Pouze skutečně provedený úspěšný experiment může vytvořit VERIFIED_RUNTIME; unit test ani tato tabulka nikoliv.
