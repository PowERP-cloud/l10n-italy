12.0.0.1.24 (2020-11-02)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] gestito validazione fattura da ordine di vendita

12.0.0.1.24 (2020-11-02)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] corretto calcolo ammontare fattura in account.move

12.0.0.1.23 (2020-11-02)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] gestione cancellazione ultima scadenza rimasta (mette una nuova riga di scadenza e una nuova riga contabile con scadenza parti alla data fattura e importo pari all'imposto dattura)

12.0.0.1.22 (2020-11-02)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] corretta gestione scadenze per fatture in stato bozza

12.0.0.1.21 (2020-10-28)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Update model, removed unused fields

12.0.0.1.18 (2020-10-23)
~~~~~~~~~~~~~~~~~~~~~~~~

* [MOD] Correzioni di forma la codice per adeguamento a segnalazioni Flake8

12.0.0.1.17 (2020-10-22)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Eliminazione righe di scadenza vuote, calcolo proposta per importo scadenze dopo modifica fattura, ricalcolo automaticp scadenze al cambio dei termini di pagamento

12.0.0.1.16 (2020-10-21)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Implementato totalizzazione totale scadenze e differenza tra scadenze e totale fattura

12.0.0.1.15 (2020-10-15)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Aggiornato duedate manager

12.0.0.1.14 (2020-10-14)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Rimosso campo duplicato (termine di pagamento)

12.0.0.1.13 (2020-10-12)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Aggiornamento bidirezionale di data scadenza e metodo di pagamento tra account.move.line e account.duedate_plus.line

12.0.0.1.12 (2020-10-12)
~~~~~~~~~~~~~~~~~~~~~~~~
* [FIX] Inserita dipendenza modulo OCA Scadenziario account_due_list


12.0.0.1.11 (2020-10-12)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Rimossi controlli non validi
