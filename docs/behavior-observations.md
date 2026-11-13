# Pozorování samostatného použití

Načten SKILL.md, scénáře a vybrané reference. Lookup --status skutečně vrátil standalone, corpus_available=false, 13 referencí a 89 příkazů; původní PDF ani archiv nebyly čteny. Lookup --id S-IV4-H vrátil metadata manuálu a verze, --command PR, CSR, RM, SR a RER vrátil modelové záznamy včetně zdrojových stran a anomálie CSR. --descriptor DAP5 vrátil DAP5/0x00000005 a --descriptor 303 modul x4 Details Tool Results s identitou 0x00000304.

Část prvního hromadného výpisu referencí byla zkrácena; cílený následující výpis pokryl potřebná témata. Jeden pokus o PowerShell brace expansion skončil chybou parseru a byl nahrazen explicitním seznamem souborů. Zdrojové strany jsou odkazy z veřejného skillu, nikoliv vlastní prohlídka originálních PDF; síť, zařízení, PLC, firmware ani import GSDML nebyly testovány.

Dodatečný scénář functional_delta: lookup dotazy na AI Target Extraction a AI Position Adjustment skutečně vrátily samostatné H capability záznamy s odkazy na strany 152–155 a 150–151 a runtime_verified=false. Dotaz capability vrátil prvních pět komunikačních záznamů, nikoli úplný přehled obrazových nástrojů; pro funkční srovnání byla přečtena reference vision-tools.md. Privátní archiv ani hardware nebyly použity.
