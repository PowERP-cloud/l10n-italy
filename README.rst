
===========================
|icon| Due dates 12.0.0.1.7
===========================


**Due dates management**

.. |icon| image:: https://raw.githubusercontent.com/axitec/accounting/12.0/account_duedates/static/description/icon.png

|Maturity| |Build Status| |Codecov Status| |license gpl| |Try Me|


.. contents::


Overview / Panoramica
=====================

|en| This module allows to specify some fiscal dates on invoices.

Date field list:

* standard Odoo date is called registration date (both sale and purchase invoices)
* date_apply_vat is a new field to declare when vat is applied (only purchase invoices)
* date_apply_balance is new field to declare when record is evaluated in balance sheet

Notes:

* This software is like account_invoice_entry_date module of Italian OCA group
* Italian OCA module use a new field called registration_date while this module uses tha standard Odoo "date" field
* On purchase journal, date is free, without checks
* On sale journal, date is the same of invoice_date and it is read-only
* Above rule may be disableb by journal configuration
* default value of date_apply_vat and date_apply_balance are the same of the date; end-user can update the field



|

|it| Date di registrazione fatture

Questo modulo permette di registrare alcune date inerenti la registrazione fatture.

La lista delle date è la seguente:

* la data contabile, standard Odoo è chiamata di registrazione
* date_apply_vat è un nuovo campo che dichiara la data di competenza dell'IVA
* date_apply_balance è un nuovo cmapo che dichiara la data di competenza a bilancio

Note:

* Questo software è simile al modulo account_invoice_entry_date del gruppo italiano OCA
* Il modulo OCA italiano utiliza un nuovo campo chiamato registration_date (data di registrazione) menrte questo modulo rinomina il campo standard di Odoo
* Nel registro degli acquisti la data di registrazione è libera, senza controlli
* Nel registro delle vendite la data di registrazione è identica alla data fattura ed è in sola lettura
* La regola precedente può essere disabilita con una configurazione del registro
* I valori predefiniti delle date date_apply_vat e date_apply_balance sono quelli della data di registrazione; l'operatore ha facoltà di modifica


|

OCA comparation / Confronto con OCA
-----------------------------------


+-----------------------------------------------------------------+-------------------+----------------+--------------------------------+
| Description / Descrizione                                       | Zeroincombenze    | OCA            | Notes / Note                   |
+-----------------------------------------------------------------+-------------------+----------------+--------------------------------+
| Coverage / Copertura test                                       |  |Codecov Status| | |OCA Codecov|  |                                |
+-----------------------------------------------------------------+-------------------+----------------+--------------------------------+


|
|

Getting started / Come iniziare
===============================

|Try Me|


|

Installation / Installazione
----------------------------


+---------------------------------+------------------------------------------+
| |en|                            | |it|                                     |
+---------------------------------+------------------------------------------+
| These instruction are just an   | Istruzioni di esempio valide solo per    |
| example to remember what        | distribuzioni Linux CentOS 7, Ubuntu 14+ |
| you have to do on Linux.        | e Debian 8+                              |
|                                 |                                          |
| Installation is built with:     | L'installazione è costruita con:         |
+---------------------------------+------------------------------------------+
| `Zeroincombenze Tools <https://zeroincombenze-tools.readthedocs.io/>`__    |
+---------------------------------+------------------------------------------+
| Suggested deployment is:        | Posizione suggerita per l'installazione: |
+---------------------------------+------------------------------------------+
| /home/fabio/12.0/accounting/                                               |
+----------------------------------------------------------------------------+

::

    cd $HOME
    # Tools installation & activation: skip if you have installed this tool
    git clone https://github.com/zeroincombenze/tools.git
    cd ./tools
    ./install_tools.sh -p
    source /opt/odoo/dev/activate_tools
    # Odoo installation
    odoo_install_repository accounting -b 12.0 -O axitec
    vem create /opt/odoo/VENV-12.0 -O 12.0 -DI

From UI: go to:

* |menu| Setting > Activate Developer mode 
* |menu| Apps > Update Apps List
* |menu| Setting > Apps |right_do| Select **account_duedates** > Install


|

Upgrade / Aggiornamento
-----------------------


+---------------------------------+------------------------------------------+
| |en|                            | |it|                                     |
+---------------------------------+------------------------------------------+
| When you want upgrade and you   | Per aggiornare, se avete installato con  |
| installed using above           | le istruzioni di cui sopra:              |
| statements:                     |                                          |
+---------------------------------+------------------------------------------+

::

    cd $HOME
    # Tools installation & activation: skip if you have installed this tool
    git clone https://github.com/zeroincombenze/tools.git
    cd ./tools
    ./install_tools.sh -p
    source /opt/odoo/dev/activate_tools
    # Odoo upgrade
    odoo_install_repository accounting -b 12.0 -O axitec -U
    vem amend /opt/odoo/VENV-12.0 -O 12.0 -DI
    # Adjust following statements as per your system
    sudo systemctl restart odoo

From UI: go to:

|
|

Get involved / Ci mettiamo in gioco
===================================

Bug reports are welcome! You can use the issue tracker to report bugs,
and/or submit pull requests on `GitHub Issues
<https://github.com/axitec/accounting/issues>`_.

In case of trouble, please check there if your issue has already been reported.

ChangeLog History / Cronologia modifiche
----------------------------------------

12.0.0.1.8 (2020-10-09)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Corretto nome campo errato

12.0.0.1.8 (2020-10-09)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Integrated module account_move_line_due

12.0.0.1.7 (2020-10-08)
~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Refactoring account move line creation

12.0.0.1.6 (2020-10-07)
~~~~~~~~~~~~~~~~~~~~~~~

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




|
|

Credits / Didascalie
====================

Copyright
---------

Odoo is a trademark of `Odoo S.A. <https://www.odoo.com/>`__ (formerly OpenERP)



|

Authors / Autori
----------------


* `SHS-AV s.r.l. <https://www.zeroincombenze.it/>`__
* `Didotech srl <http://www.didotech.com>`__


Contributors / Collaboratori
----------------------------


* Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
* Marco Tosato <marco.tosato@didotech.com>


|

----------------


|en| **zeroincombenze®** is a trademark of `SHS-AV s.r.l. <https://www.shs-av.com/>`__
which distributes and promotes ready-to-use **Odoo** on own cloud infrastructure.
`Zeroincombenze® distribution of Odoo <https://wiki.zeroincombenze.org/en/Odoo>`__
is mainly designed to cover Italian law and markeplace.

|it| **zeroincombenze®** è un marchio registrato da `SHS-AV s.r.l. <https://www.shs-av.com/>`__
che distribuisce e promuove **Odoo** pronto all'uso sulla propria infrastuttura.
La distribuzione `Zeroincombenze® <https://wiki.zeroincombenze.org/en/Odoo>`__ è progettata per le esigenze del mercato italiano.


|chat_with_us|


|

This module is part of accounting project.

Last Update / Ultimo aggiornamento: 2020-10-08

.. |Maturity| image:: https://img.shields.io/badge/maturity-Alfa-red.png
    :target: https://odoo-community.org/page/development-status
    :alt: Alfa
.. |Build Status| image:: https://travis-ci.org/axitec/accounting.svg?branch=12.0
    :target: https://travis-ci.org/axitec/accounting
    :alt: github.com
.. |license gpl| image:: https://img.shields.io/badge/licence-LGPL--3-7379c3.svg
    :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
    :alt: License: LGPL-3
.. |license opl| image:: https://img.shields.io/badge/licence-OPL-7379c3.svg
    :target: https://www.odoo.com/documentation/user/9.0/legal/licenses/licenses.html
    :alt: License: OPL
.. |Coverage Status| image:: https://coveralls.io/repos/github/axitec/accounting/badge.svg?branch=12.0
    :target: https://coveralls.io/github/axitec/accounting?branch=12.0
    :alt: Coverage
.. |Codecov Status| image:: https://codecov.io/gh/axitec/accounting/branch/12.0/graph/badge.svg
    :target: https://codecov.io/gh/axitec/accounting/branch/12.0
    :alt: Codecov
.. |Tech Doc| image:: https://www.zeroincombenze.it/wp-content/uploads/ci-ct/prd/button-docs-12.svg
    :target: https://wiki.zeroincombenze.org/en/Odoo/12.0/dev
    :alt: Technical Documentation
.. |Help| image:: https://www.zeroincombenze.it/wp-content/uploads/ci-ct/prd/button-help-12.svg
    :target: https://wiki.zeroincombenze.org/it/Odoo/12.0/man
    :alt: Technical Documentation
.. |Try Me| image:: https://www.zeroincombenze.it/wp-content/uploads/ci-ct/prd/button-try-it-12.svg
    :target: https://erp12.zeroincombenze.it
    :alt: Try Me
.. |OCA Codecov| image:: https://codecov.io/gh/OCA/accounting/branch/12.0/graph/badge.svg
    :target: https://codecov.io/gh/OCA/accounting/branch/12.0
    :alt: Codecov
.. |Odoo Italia Associazione| image:: https://www.odoo-italia.org/images/Immagini/Odoo%20Italia%20-%20126x56.png
   :target: https://odoo-italia.org
   :alt: Odoo Italia Associazione
.. |Zeroincombenze| image:: https://avatars0.githubusercontent.com/u/6972555?s=460&v=4
   :target: https://www.zeroincombenze.it/
   :alt: Zeroincombenze
.. |en| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/flags/en_US.png
   :target: https://www.facebook.com/Zeroincombenze-Software-gestionale-online-249494305219415/
.. |it| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/flags/it_IT.png
   :target: https://www.facebook.com/Zeroincombenze-Software-gestionale-online-249494305219415/
.. |check| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/check.png
.. |no_check| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/no_check.png
.. |menu| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/menu.png
.. |right_do| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/right_do.png
.. |exclamation| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/exclamation.png
.. |warning| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/warning.png
.. |same| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/same.png
.. |late| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/late.png
.. |halt| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/halt.png
.. |info| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/info.png
.. |xml_schema| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/certificates/iso/icons/xml-schema.png
   :target: https://github.com/zeroincombenze/grymb/blob/master/certificates/iso/scope/xml-schema.md
.. |DesktopTelematico| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/certificates/ade/icons/DesktopTelematico.png
   :target: https://github.com/zeroincombenze/grymb/blob/master/certificates/ade/scope/Desktoptelematico.md
.. |FatturaPA| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/certificates/ade/icons/fatturapa.png
   :target: https://github.com/zeroincombenze/grymb/blob/master/certificates/ade/scope/fatturapa.md
.. |chat_with_us| image:: https://www.shs-av.com/wp-content/chat_with_us.gif
   :target: https://t.me/axitec_helpdesk

