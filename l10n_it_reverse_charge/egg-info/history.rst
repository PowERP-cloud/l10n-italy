12.0.1.2.7_46 (2023-02-15)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Self invoice date is equla to purchase invoice and diff from date / Data auto-fattura eguale a fattura fornitori e diversa da data contabile
* [FIX] Validation error on self invoice in prior year / Errata segnalazione di errore per auto-fatture anno preceente
* [TEST] Regressione test: 25% (456/340)

12.0.1.2.7_45 (2022-06-27)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Element '<field name="enable_date">' cannot be located in parent view

12.0.1.2.7_44 (2022-04-13)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Set date & date_invoice of self-invoice = invoice / Date auto-fattura = fattura

12.0.1.2.7_43 (2022-04-13)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Set check on RC tax / Impostato check su tassa reverse charge

12.0.1.2.7_42 (2022-04-01)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Wrong customer partner / Errato partner cliente

12.0.1.2.7_41 (2022-03-18)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Self invoice wrong date / Data registrazione errata in autofattura

12.0.1.2.7_40 (2022-03-15)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] More currency invoices / Fatture in valuta (più copertura)

12.0.1.2.7_39 (2022-02-25)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Currency invoices / Fatture in valuta

12.0.1.2.7_38 (2022-02-22)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Invalid tax nature check / Errato controllo natura codice IVA

12.0.1.2.7_37 (2022-01-07)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Impostato tipo documento per l'autofattura da posizione fiscale

12.0.1.2.7_36 (2021-12-30)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Fix BUG 601 / 602

12.0.1.2.7_35 (2021-12-17)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Inserito avviso per conto iva vendite

12.0.1.2.7_34 (2021-12-16)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Fix autofattura

12.0.1.2.7_33 (2021-12-14)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Fix autofattura

12.0.1.2.7_32 (2021-12-09)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Gestione codici iva rc servizi e prodotti

12.0.1.2.7_31 (2021-10-04)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Gestito visualizzazione totale tassa nella fattura
* [FIX] Gestito bug riconciliazione su autofattura

12.0.1.2.7_30 (2021-09-29)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Gestito filtro su registro per autofattura
* [FIX] Gestito bug tasse multiple

12.0.1.2.7_29 (2021-09-24)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Gestito bug tasse multiple su movimento contabile

12.0.1.2.7_28 (2021-09-14)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Gestito bug nota di credito fornitore e auto fattura di tipo nota di credito

12.0.1.2.7_28 (2021-09-14)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Risolto bug fattura fornitore con posizione fiscale RC self

12.0.1.2.7_27 (2021-09-14)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Risolto bug fattura cliente con posizione fiscale RC

12.0.1.2.7_26 (2021-09-02)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Risolto bug partner assente nella registrazione contabile di RC

12.0.1.2.7_25 (2021-08-25)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Rimosso codice inutile

12.0.1.2.7_24 (2021-08-25)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Out invoice/refund do not execute RC actions / Azioni di RC ignorate per fatture / NC di vendita

12.0.1.2.7_23 (2021-08-06)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Fix bug POW-450 partner vuoto in registrazione contabile

12.0.1.2.7_22 (2021-08-05)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Impostato date applicazione iva e iva bilancio nell'autofattura

12.0.1.2.7_21 (2021-08-04)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Impostato data di registrazione nell'autofattura in tutti i campi data

12.0.1.2.7_20 (2021-08-02)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Impostato data di registrazione in tutti i movimenti contabili

12.0.1.2.7_19 (2021-08-02)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Impostato data di registrazione in autofattura

12.0.1.2.7_15 (2021-07-26)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Possibilità di impostare manualmente il campo rc_type di account.tax

12.0.1.2.7_14 (2021-07-21)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Impostato controllo flag rc in creazione fattura

12.0.1.2.7_13 (2021-07-20)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Corretto comportamento anomalo annullamento fattura

12.0.1.2.7_12 (2021-07-14)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Nascosto campo rc in riga fatture in base alla posizione fiscale

12.0.1.2.7_11 (2021-07-14)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Aggiornato campo registro in posizione fiscale

12.0.1.2.7_10 (2021-07-13)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Fix bug multi in calcolo totali

12.0.1.2.7_9 (2021-07-13)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Condizioni campo iva rc invisibile nella vista

12.0.1.2.7_8 (2021-07-12)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Autofattura per Reverse charge self

12.0.1.2.7_7 (2021-07-09)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Registrazione contabile per Reverse charge self

12.0.1.2.7_6 (2021-07-09)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Registrazione contabile per Reverse charge locale

12.0.1.2.7_5 (2021-07-07)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Ricalcolo totale fattura

12.0.1.2.7_4 (2021-07-06)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Impostato campi extra

12.0.1.2.7_3 (2021-07-05)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Impostato verifica tipo di tassa RC

12.0.1.2.7_2 (2021-06-22)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Aggiornato context per la funzione di riporto in bozza della fattura

12.0.1.2.7_1 (2021-06-21)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Aggiornato numero di versione

12.0.1.2.8 (2021-05-17)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Aggiornato verifica flag RC da elenco tasse

12.0.1.2.7 (2021-03-18)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Error when payment invoice: function invoice_validate @multi


12.0.1.2.6 (2021-02-17)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Clone OCA module
* [FIX] Mixed RC and ordinary VAT line in single vendor bill
* [FIX] Self invoice account move lines
