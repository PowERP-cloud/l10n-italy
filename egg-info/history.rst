12.0.0.1.6 (2020-10-07)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Avoid constraint on due date on invoice validate

12.0.2.6.15 (2020-09-14)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] disabled contraint on due_amount > 0 / Disabilitato il controllo sull'importo della riga

12.0.2.5.15 (2020-09-10)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] disabled contraint on due_amount > 0 / Disabilitato il controllo sull'importo della riga

12.0.2.4.15 (2020-08-27)
~~~~~~~~~~~~~~~~~~~~~~~~

* [MOD] modificato modulo per utilizzare il nuovo campo "type" di account.move

12.0.2.3.15 (2020-08-27)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] attivato calcolo automatico, "Scadenze", "Prima nota" e "Riepilogo IVA" alla creazione, prima lo faceva solo al write


12.0.2.2.15 (2020-08-26)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] ricalcolo automatico, "Scadenze", "Prima nota" e "Riepilogo IVA" al salvataggio
* [FIX] corretto nome di variabile scritto in modo errato
* [FIX] Righe di "Prima Nota" e "Riepilogo IVA" non sono più direttamente modificabili dall'utente

12.0.1.2.14 (2020-08-18)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Riabilitata visualizzazione campo journal_id nella vista account.move

12.0.1.2.13 (2020-08-18)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] inseriti controlli in create, write e post per evitare che la generazione e i controlli di due_dates, account_brief e vat_brief su registrazioni "non IVA"

12.0.1.1.13 (2020-08-03)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Duplicate journal_id / Registro duplicato


