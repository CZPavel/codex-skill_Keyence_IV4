# Síťové služby, monitoring a obrazová data

Doplněk v1.1.0: [historický runtime research](runtime-research.md) odděluje pozorování IV4-500CA R1.20.05 / R1.30.02 od níže uvedených manuálových či návrhových tvrzení; nepřenášet na IV4-H.

DOCUMENTED zdroje: S-IV4 / IV4_UserManual_WW_GB_AS_167146.pdf (`iv4_82ffe8b0fedc105a`) p.282–295, 398–425; S-IV4-H / IV4_UserManual_WW_GB_AS_170071.pdf (`iv4_f2b18663143f7e12`) p.314–331, 474–501. Podle rodiny vybírej i požadovanou verzi sensor/panel/Navigator. Síťová služba není univerzální vzdálené správní API.

## OPC UA server

IV4-H p.475 uvádí UA TCP binary, endpoint schéma `opc.tcp://host:port`, výchozí port 4840, až 5 sessions, 2000 monitored items a sampling 50–10000 ms. Tyto limity nejsou měřená dosažitelná rychlost výsledků ani vlastnosti každého jiného IV modelu. Podporované aplikace/client versions jsou v samostatné tabulce. Jiná tabulka na stejné H p.475 výslovně uvádí, že klient Kepware KEPServerEX s označením verze 6-6.16.217.0 se nemůže připojit. Jde o dokumentovanou nekompatibilitu této přesné položky, nikoliv o obecný závěr pro všechny produkty či novější verze Kepware.

Nastavení může používat None, Sign či SignAndEncrypt a příslušné policy; existence None není doporučení pro provozní síť. Zkontroluj certifikát serveru i klienta, trust/CA/CRL, čas zařízení a user/anonymous policy. H p.477 popisuje také přístup k private key a expiraci certifikátů; vypnutí kontroly certifikátu není první diagnostická oprava. GENERAL: nejdříve odliš transport, endpoint/security mismatch, certifikát/čas a práva uživatele; každou větev ověř jednotlivě.

H p.486–491 má strom VisionSensor, MachineStatus, MachineInformation, OperationResult a Operation. Užitečné status názvy jsou ReadyStatus, BusyStatus, TriggerReadyStatus, RunningStatus, ImagingStatus, ErrorStatus/ErrorCode a WarningStatus/WarningCode. U výsledku sleduj HasOperationResult, ResultUpdated, ResultNo, ResultProgramNo/Name, TotalStatusOK/NG a ToolResult. Samotný sampling nebo subscription notification nezaručuje, že každý element pochází z jednoho nového cyklu; použij známou verzi struktury a ověř konzistenci.

Method RequestTrigger má uvedený namespace 2 / ID 17001 a vyžaduje External Trigger; SwitchProgram 17002 přijímá Byte 0–127 a vyžaduje povolený switching method. ChangeThreshold 17003 používá tool/type/value s modelovými podmínkami, ChangeCountValue 17004 tool 1–8 a value 0–9999999, ResetCount 17005 může nemít efekt při vypnutém reset input. Succeeded není potvrzení platného nového obrazu ani ověření existence všech nástrojů.

Zdrojové rozpory se nesmí skrýt: H p.491 uvádí ID 17006 u ResetActiveStatistics i SetCommunicationRewriteString. H p.487 má SettingCheckSum typ UInt16 a současně rozsah do 4294967295/10-digit popis. Neodvozuj další ID jako 17007 ani typ UInt32 jen podle logiky. Použij Browse/read type metadata na cílovém zařízení a zachovej záznam model/FW. Public skill uvádí tyto položky jako UNVERIFIED binding, i když samotná funkce je popsána manuálem. Namespace index také není přenosný namespace URI napříč libovolnými servery.

## MQTT klient

H p.493 dokumentuje MQTT 3.1.1 a Clean Session pevně True; TLS, serverové/client certifikáty a user authentication jsou konfigurovatelné. Není to senzorový broker. Topic names jsou nastavitelná a publikování Result, Connection Status a Status Change má vlastní podmínky. Při restartu/odpojení počítej s novou session; neslibuj persistent replay všech minulých výsledků.

H p.496–498: výchozí topic prefix je client ID; connection/result a status change jsou popsané kanály. Result se posílá při aktualizaci judgment/count podle režimu, ne libovolně během Setting či každého přepnutí. Outgoing QoS lze volit 0/1/2 v popsaném nastavení, zatímco příjem action je pevně QoS1. Retained zpráva může být stará; přihlášení subscriberu nesmí samo potvrdit nový díl. Změna statistiky má vlastní pravidla publikování.

Dokumentované H action payloady (p.498) používají `actiontype`: trigger; switch program s `program_no` 0–127; change threshold s `tool_no`, `type` 0/1, `value`; change count s tool 1–8 a `count_value`; reset count; reset statistics; set communication_rewrite_string s type 1–8 a string. Senzor odebírá client-ID/action. Jeden JSON nesmí sloučit několik operací; provede se první uvedená. Výsledek akce se sleduje v odpovídajícím Result/Status Change či změně hodnoty, nikoliv domyšleným univerzálním ACK topicem.

H p.499 uvádí ResultImage jako Base64 judgment image při povolené full/half velikosti. Obraz může zvýšit datový tok, latenci a zátěž brokeru. GENERAL návrh: odděl liveness od fresh result, kontroluj client/program/cycle a deduplikuj podle validního aplikačního klíče. Samotné QoS2 neřeší korelaci fyzického dílu ani ztrátu výsledku před vytvořením MQTT zprávy. Pro IV4 použij jeho p.416–425 a nepřenášej automaticky každé pole H schématu.

## FTP/SFTP, SD a operation log

Senzor je klient přenosu do nastaveného serveru, nikoliv obecný souborový server. Nakonfiguruj konkrétní server, credentials, folder, podmínky přenosu, typy souborů a názvy. Metadata názvu mohou být definovaná recepturou/transfer condition a komunikační textovou náhradou. Zda jsou snímky a textové výsledky ze stejného triggeru, se musí opírat o doložené pojmenování/counter a ověření.

RFC počítá dokončení všech příslušných souborů všech aktivních podmínek pro trigger, ne každý soubor zvlášť (IV4 p.439; H p.515). File existence sama nemusí znamenat dokončený přenos. GENERAL serverový návrh musí odlišit rozpracovaný soubor, kompletní přenos, duplicitu a retry; nevymýšlej přitom možnost senzoru provést libovolný remote rename nebo listdir. H R2.10 release přidal operation-log output; kontroluj [verze](releases.md), není to automaticky feature všech R1.x.

SFTP není synonymum FTPS. Při problému rozliš DNS/IP route, TCP spojení, SSH/certifikát/credentials, práva a umístění souboru, kapacitu a rychlost cíle. Nezačínej přepnutím na nechráněný protokol. Případné změny bezpečnosti mají mít výslovný provozní záměr a ověřený návrat.

## Bez Navigatoru a Web monitor

BR dokumentuje přímé čtení nejnovějšího BMP přes non-procedural TCP bez trvale běžícího Navigatoru; nejde o potvrzenou schopnost vzdáleně kompletně nastavovat inspekci. Firmware/config musí mít potřebné rozhraní povolené. MQTT obraz a FTP přenos jsou další samostatné cesty s odlišnou latencí a podmínkami. Každou posuzuj jako jinou schopnost, ne jako jeden obecný stream.

[Oficiální specs](https://www.keyence.com/products/sensor/vision-sensor/iv4/specs/) uvádí Web monitor HTTP/HTTPS u konkrétních H variant a některých amplifier bloků; ne u každé IV4 smart camera. Tento seznam nedokládá REST endpointy, autentizaci, interní websocket schema ani správcovské API. Dotaz „mohu volat GET /api/status?“ bez přesného zdroje končí UNVERIFIED a návrhem nejmenšího read-only průzkumu, ne vymyšleným příkladem curl.

## Praktický monitoring

Začni identitou model/FW/konfigurace, potom liveness transportu, Run/Program a Error/Warning, dostupností nového výsledku a program mismatch, teprve potom obraz/statistika. Odděl čas vytvoření inspekce, přijetí zprávy a uložení souboru. Změna času senzoru, disconnect a rollover čítače musí být součástí návrhu freshness. Monitoring není oprávnění resetovat nebo přepínat program. Zatížení musí mít měřený rozpočet; publikované sampling/RPI limity nejsou akceptační test výrobního taktu.
