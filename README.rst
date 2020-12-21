
============================
|icon| Due dates 12.0.0.1.37
============================


**Due dates management**

.. |icon| image:: https://raw.githubusercontent.com/zeroincombenze/accounting/12.0/account_duedates/static/description/icon.png

|Maturity| |Build Status| |Codecov Status| |license gpl| |Try Me|


.. contents::


Overview / Panoramica
=====================

|en| 

|

|it| 

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
    odoo_install_repository accounting -b 12.0 -O zero
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
    odoo_install_repository accounting -b 12.0 -O zero -U
    vem amend /opt/odoo/VENV-12.0 -O 12.0 -DI
    # Adjust following statements as per your system
    sudo systemctl restart odoo

From UI: go to:

|

Support / Supporto
------------------


|Zeroincombenze| This module is maintained by the `SHS-AV s.r.l. <https://www.zeroincombenze.it/>`__


|
|

Get involved / Ci mettiamo in gioco
===================================

Bug reports are welcome! You can use the issue tracker to report bugs,
and/or submit pull requests on `GitHub Issues
<https://github.com/zeroincombenze/accounting/issues>`_.

In case of trouble, please check there if your issue has already been reported.

Proposals for enhancement
-------------------------


|en| If you have a proposal to change this module, you may want to send an email to <cc@shs-av.com> for initial feedback.
An Enhancement Proposal may be submitted if your idea gains ground.

|it| Se hai proposte per migliorare questo modulo, puoi inviare una mail a <cc@shs-av.com> per un iniziale contatto.

ChangeLog History / Cronologia modifiche
----------------------------------------

12.0.0.1.37 (2020-12-14)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Added filter 'not in order' and state field / Impostato filtro 'Non in scadenza' e campo stato

12.0.0.1.36 (2020-12-11)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Warning on check duedate payments / Segnalazione al tentativo di annullamento con scadenze in pagamento

12.0.0.1.35 (2020-12-11)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Refactoring date effective / Aggiornato gestione data decorrenza

12.0.0.1.34 (2020-12-04)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Set vat on first duedate according to payment term flag / Impostato gestione iva sulla prima scadenza

12.0.0.1.33 (2020-12-02)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Rimossa creazione righe scadenze se almeno una in pagamento

12.0.0.1.32 (2020-11-30)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Rimossa creazione righe scadenze se almeno una in pagamento

12.0.0.1.31 (2020-11-23)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Set duedates creation from sale order / Impostato creazione scadenze da ordine di vendita

12.0.0.1.30 (2020-11-23)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Set account invoice 13 more dependency / Inserita dipendenza modulo transizione

12.0.0.1.29 (2020-11-18)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Set default date effective / Impostato default data decorrenza

12.0.0.1.28 (2020-11-17)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Added missing dependency / inserita dipendenza mancante

12.0.0.1.27 (2020-11-12)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Added date effective / inserita data di decorrenza

12.0.0.1.26 (2020-11-09)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] impostato ricerca per ordine di pagamento

12.0.0.1.25 (2020-11-06)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] impostato campo ordine di pagamento nella view

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

Last Update / Ultimo aggiornamento: 2020-12-14

.. |Maturity| image:: https://img.shields.io/badge/maturity-Alfa-red.png
    :target: https://odoo-community.org/page/development-status
    :alt: Alfa
.. |Build Status| image:: https://travis-ci.org/zeroincombenze/accounting.svg?branch=12.0
    :target: https://travis-ci.org/zeroincombenze/accounting
    :alt: github.com
.. |license gpl| image:: https://img.shields.io/badge/licence-LGPL--3-7379c3.svg
    :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
    :alt: License: LGPL-3
.. |license opl| image:: https://img.shields.io/badge/licence-OPL-7379c3.svg
    :target: https://www.odoo.com/documentation/user/9.0/legal/licenses/licenses.html
    :alt: License: OPL
.. |Coverage Status| image:: https://coveralls.io/repos/github/zeroincombenze/accounting/badge.svg?branch=12.0
    :target: https://coveralls.io/github/zeroincombenze/accounting?branch=12.0
    :alt: Coverage
.. |Codecov Status| image:: https://codecov.io/gh/zeroincombenze/accounting/branch/12.0/graph/badge.svg
    :target: https://codecov.io/gh/zeroincombenze/accounting/branch/12.0
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

