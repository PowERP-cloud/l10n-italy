
===============================================
|icon| ITA - Inversione contabile 12.0.1.2.7_43
===============================================


**Inversione contabile**

.. |icon| image:: https://raw.githubusercontent.com/PowERP-cloud/l10n-italy/12.0/l10n_it_reverse_charge/static/description/icon.png

|Maturity| |Build Status| |license opl|


.. contents::



Overview / Panoramica
=====================

|en| Module to handle reverse charge IVA in vendor bills.

The module allows you to automate the accounting entries derived from invoices of intra-EU and extra-EU suppliers through the VAT reverse charge.
Furthermore, the vendor bill cancellation and reopening procedure is automated.

It is also possible to use the "additional vendor self billing" mode.
This mode is typically used for non-EU suppliers to show, in the purchases VAT journal, a vendor bill addressed to your own company (self-bill).
The self-bill will then be completely reconciled with the self-invoice, which is also addressed to your own company.


|

|it| Inversione contabile

Modulo per gestire l'inversione contabile (reverse charge) nelle fatture fornitore.

Il modulo permette di automatizzare le registrazioni contabili derivate dalle fatture fornitori intra UE ed extra UE mediante l'inversione contabile IVA.
Inoltre è automatizzata la procedura di annullamento e riapertura della fattura fornitore.

È inoltre possibile utilizzare la modalità "con autofattura fornitore aggiuntiva".
Questa modalità è usata tipicamente per i fornitori extra UE per mostrare, nel registro IVA acquisti, una fattura intestata alla propria azienda (autofattura passiva).
L'autofattura passiva verrà poi totalmente riconciliata con l'autofattura attiva, anch'essa intestata alla propria azienda.



|

Usage / Utilizzo
----------------

Creare l'imposta **22% intra UE** - Vendite:

.. figure:: https://raw.githubusercontent.com/OCA/l10n-italy/12.0/l10n_it_reverse_charge/static/description/tax_22_v_i_ue.png
   :alt: 22% intra UE - Vendite
   :width: 600 px

Creare l'imposta **22% intra UE** - Acquisti:

.. figure:: https://raw.githubusercontent.com/OCA/l10n-italy/12.0/l10n_it_reverse_charge/static/description/tax_22_a_i_ue.png
  :alt: 22% intra UE - Acquisti
  :width: 600 px

Creare l'imposta **22% extra UE** - Vendite:

.. figure:: https://raw.githubusercontent.com/OCA/l10n-italy/12.0/l10n_it_reverse_charge/static/description/tax_22_v_e_ue.png
   :alt: 22% extra UE - Vendite
   :width: 600 px

Creare l'imposta **22% extra UE** - Acquisti:

.. figure:: https://raw.githubusercontent.com/OCA/l10n-italy/12.0/l10n_it_reverse_charge/static/description/tax_22_a_e_ue.png
  :alt: 22% extra UE - Acquisti
  :width: 600 px

Creare il conto 'Transitorio autofatturazione':

.. figure:: https://raw.githubusercontent.com/OCA/l10n-italy/12.0/l10n_it_reverse_charge/static/description/temp_account_auto_inv.png
  :alt: conto transitorio Autofattura
  :width: 600 px

Il 'Registro pagamento autofattura' deve essere configurato con il conto 'Transitorio autofatturazione' appena creato:

.. figure:: https://raw.githubusercontent.com/OCA/l10n-italy/12.0/l10n_it_reverse_charge/static/description/registro_riconciliazione.png
  :alt: Registro pagamento autofattura
  :width: 600 px

Modificare il tipo inversione contabile **Intra-UE (autofattura)**:

.. figure:: https://raw.githubusercontent.com/OCA/l10n-italy/12.0/l10n_it_reverse_charge/static/description/rc_selfinvoice.png
  :alt: inversione contabile con Autofattura
  :width: 600 px

Il registro autofattura deve essere di tipo 'Vendita'.

Modificare il tipo inversione contabile **Extra-UE (autofattura)**:

.. figure:: https://raw.githubusercontent.com/OCA/l10n-italy/12.0/l10n_it_reverse_charge/static/description/rc_selfinvoice_extra.png
  :alt: inversione contabile con Autofattura
  :width: 600 px

Il 'Registro autofattura passiva' deve essere di tipo 'Acquisto'.


Nella posizione fiscale, impostare il tipo inversione contabile:

.. figure:: https://raw.githubusercontent.com/OCA/l10n-italy/12.0/l10n_it_reverse_charge/static/description/fiscal_pos_intra.png
  :alt: Impostazione posizioni fiscali Intra CEE
  :width: 600 px

.. figure:: https://raw.githubusercontent.com/OCA/l10n-italy/12.0/l10n_it_reverse_charge/static/description/fiscal_pos_extra.png
  :alt: Impostazione posizioni fiscali Extra CEE
  :width: 600 px


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
| These instructions are just an  | Istruzioni di esempio valide solo per    |
| example; use on Linux CentOS 7+ | distribuzioni Linux CentOS 7+,           |
| Ubuntu 14+ and Debian 8+        | Ubuntu 14+ e Debian 8+                   |
|                                 |                                          |
| Installation is built with:     | L'installazione è costruita con:         |
+---------------------------------+------------------------------------------+
| `Zeroincombenze Tools <https://zeroincombenze-tools.readthedocs.io/>`__    |
+---------------------------------+------------------------------------------+
| Suggested deployment is:        | Posizione suggerita per l'installazione: |
+---------------------------------+------------------------------------------+
| $HOME/12.0                                                                 |
+----------------------------------------------------------------------------+

::

    cd $HOME
    # *** Tools installation & activation ***
    # Case 1: you have not installed zeroincombenze tools
    git clone https://github.com/zeroincombenze/tools.git
    cd $HOME/tools
    ./install_tools.sh -p
    source $HOME/devel/activate_tools
    # Case 2: you have already installed zeroincombenze tools
    cd $HOME/tools
    ./install_tools.sh -U
    source $HOME/devel/activate_tools
    # *** End of tools installation or upgrade ***
    # Odoo repository installation; OCB repository must be installed
    odoo_install_repository l10n-italy -b 12.0 -O powerp -o $HOME/12.0
    vem create $HOME/12.0/venv_odoo -O 12.0 -a "*" -DI -o $HOME/12.0

From UI: go to:

* |menu| Setting > Activate Developer mode 
* |menu| Apps > Update Apps List
* |menu| Setting > Apps |right_do| Select **l10n_it_reverse_charge** > Install


|

Configuration / Configurazione
------------------------------

**Italiano**

Creare l'imposta **22% intra UE** - Vendite:

.. figure:: ../static/description/tax_22_v_i_ue.png
   :alt: 22% intra UE - Vendite
   :width: 600 px

Creare l'imposta **22% intra UE** - Acquisti:

.. figure:: ../static/description/tax_22_a_i_ue.png
  :alt: 22% intra UE - Acquisti
  :width: 600 px

Creare l'imposta **22% extra UE** - Vendite:

.. figure:: ../static/description/tax_22_v_e_ue.png
   :alt: 22% extra UE - Vendite
   :width: 600 px

Creare l'imposta **22% extra UE** - Acquisti:

.. figure:: ../static/description/tax_22_a_e_ue.png
  :alt: 22% extra UE - Acquisti
  :width: 600 px

Creare il conto 'Transitorio autofatturazione':

.. figure:: ../static/description/temp_account_auto_inv.png
  :alt: conto transitorio Autofattura
  :width: 600 px

Il 'Registro pagamento autofattura' deve essere configurato con il conto 'Transitorio autofatturazione' appena creato:

.. figure:: ../static/description/registro_riconciliazione.png
  :alt: Registro pagamento autofattura
  :width: 600 px

Modificare il tipo inversione contabile **Intra-UE (autofattura)**:

.. figure:: ../static/description/rc_selfinvoice.png
  :alt: inversione contabile con Autofattura
  :width: 600 px

Il registro autofattura deve essere di tipo 'Vendita'.

Modificare il tipo inversione contabile **Extra-UE (autofattura)**:

.. figure:: ../static/description/rc_selfinvoice_extra.png
  :alt: inversione contabile con Autofattura
  :width: 600 px

Il 'Registro autofattura passiva' deve essere di tipo 'Acquisto'.


Nella posizione fiscale, impostare il tipo inversione contabile:

.. figure:: ../static/description/fiscal_pos_intra.png
  :alt: Impostazione posizioni fiscali Intra CEE
  :width: 600 px

.. figure:: ../static/description/fiscal_pos_extra.png
  :alt: Impostazione posizioni fiscali Extra CEE
  :width: 600 px

**English**

Create the tax **22% intra EU** - Sale:

.. figure:: ../static/description/tax_22_v_i_ue.png
   :alt: 22% intra UE - Sale
   :width: 600 px

Create the tax **22% intra EU** - Purchase:

.. figure:: ../static/description/tax_22_a_i_ue.png
  :alt: 22% intra UE - Purchase
  :width: 600 px

Create the tax **22% extra EU** - Sale:

.. figure:: ../static/description/tax_22_v_e_ue.png
   :alt: 22% extra UE - Sale
   :width: 600 px

Create the tax **22% extra EU** - Purchase:

.. figure:: ../static/description/tax_22_a_e_ue.png
  :alt: 22% extra UE - Purchase
  :width: 600 px

Create the account 'Self Invoice Transitory' as follows:

.. figure:: ../static/description/temp_account_auto_inv.png
  :alt: Self Invoice Transitory Account
  :width: 600 px

The 'Self Invoice Payment' Journal has to be configured with the just created 'Self Invoice Transitory' account:

.. figure:: ../static/description/registro_riconciliazione.png
  :alt: Registro pagamento autofattura
  :width: 600 px

Edit the reverse charge type **Intra-EU (self-invoice)**:

.. figure:: ../static/description/rc_selfinvoice.png
  :alt: reverse charge with Self Invoice
  :width: 600 px

The Self Invoice journal has to be of type 'Sale'.

Edit the reverse charge type **Extra-EU (self-invoice)** :

.. figure:: ../static/description/rc_selfinvoice_extra.png
  :alt: reverse charge with Self Invoice
  :width: 600 px

The 'Supplier Self Invoice Journal' has to be of type 'Purchase'.

In the fiscal position, set the reverse charge type:

.. figure:: ../static/description/fiscal_pos_intra.png
  :alt: Impostazione posizioni fiscali Intra CEE
  :width: 600 px

.. figure:: ../static/description/fiscal_pos_extra.png
  :alt: Impostazione posizioni fiscali Extra CEE
  :width: 600 px


|

Upgrade / Aggiornamento
-----------------------


::

    cd $HOME
    # *** Tools installation & activation ***
    # Case 1: you have not installed zeroincombenze tools
    git clone https://github.com/zeroincombenze/tools.git
    cd $HOME/tools
    ./install_tools.sh -p
    source $HOME/devel/activate_tools
    # Case 2: you have already installed zeroincombenze tools
    cd $HOME/tools
    ./install_tools.sh -U
    source $HOME/devel/activate_tools
    # *** End of tools installation or upgrade ***
    # Odoo repository upgrade
    odoo_install_repository l10n-italy -b 12.0 -o $HOME/12.0 -U
    vem amend $HOME/12.0/venv_odoo -o $HOME/12.0
    # Adjust following statements as per your system
    sudo systemctl restart odoo

From UI: go to:

|

Support / Supporto
------------------


This module is maintained by the / Questo modulo è mantenuto dalla rete di imprese `Powerp <http://www.powerp.it/>`__

Developer companies are / I soci sviluppatori sono:

* `Didotech s.r.l. <http://www.didotech.com>`__
* `SHS-AV s.r.l. <https://www.shs-av.com/>`__


|
|

Get involved / Ci mettiamo in gioco
===================================

Bug reports are welcome! You can use the issue tracker to report bugs,
and/or submit pull requests on `GitHub Issues
<https://github.com/PowERP-cloud/l10n-italy/issues>`_.

In case of trouble, please check there if your issue has already been reported.

Proposals for enhancement
-------------------------


If you have a proposal to change this module, you may want to send an email to <info@powerp.it> for initial feedback.
An Enhancement Proposal may be submitted if your idea gains ground.


ChangeLog History / Cronologia modifiche
----------------------------------------

12.0.1.2.7_43 (2022-04-13)
~~~~~~~~~~~~~~~~~~~~~~~~~~

[FIX] Set check on RC tax / Impostato check su tassa reverse charge

12.0.1.2.7_42 (2022-04-01)
~~~~~~~~~~~~~~~~~~~~~~~~~~

[FIX] Wrong customer partner / Errato partner cliente

12.0.1.2.7_41 (2022-03-18)
~~~~~~~~~~~~~~~~~~~~~~~~~~

[FIX] Self invoice wrong date / Data registrazione errata in autofattura

12.0.1.2.7_40 (2022-03-15)
~~~~~~~~~~~~~~~~~~~~~~~~~~

[FIX] More currency invoices / Fatture in valuta (più copertura)

12.0.1.2.7_39 (2022-02-25)
~~~~~~~~~~~~~~~~~~~~~~~~~~

[FIX] Currency invoices / Fatture in valuta

12.0.1.2.7_38 (2022-02-22)
~~~~~~~~~~~~~~~~~~~~~~~~~~

[FIX] Invalid tax nature check / Errato controllo natura codice IVA

12.0.1.2.7_37 (2022-01-07)
~~~~~~~~~~~~~~~~~~~~~~~~~~

[FIX] Impostato tipo documento per l'autofattura da posizione fiscale

12.0.1.2.7_36 (2021-12-30)
~~~~~~~~~~~~~~~~~~~~~~~~~~

[FIX] Fix BUG 601 / 602

12.0.1.2.7_35 (2021-12-17)
~~~~~~~~~~~~~~~~~~~~~~~~~~

[FIX] Inserito avviso per conto iva vendite

12.0.1.2.7_34 (2021-12-16)
~~~~~~~~~~~~~~~~~~~~~~~~~~

[FIX] Fix autofattura

12.0.1.2.7_33 (2021-12-14)
~~~~~~~~~~~~~~~~~~~~~~~~~~

[FIX] Fix autofattura

12.0.1.2.7_32 (2021-12-09)
~~~~~~~~~~~~~~~~~~~~~~~~~~

[FIX] Gestione codici iva rc servizi e prodotti



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

* `Odoo Community Association (OCA) <https://odoo-community.org>`__
* `SHS-AV s.r.l. <https://www.zeroincombenze.it/>`__
* `Didotech s.r.l. <https://www.didotech.com>`__
* `LibrERP <https://www.librerp.it>`__


Contributors / Collaboratori
----------------------------

* Davide Corio
* Alex Comba <alex.comba@agilebg.com>
* Lorenzo Battistini <lorenzo.battistini@agilebg.com
* Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
* Marco Tosato <marco.tosato@didotech.com>
* Fabio Giovannelli <fabio.giovannelli@didotech.com>


Maintainer / Manutenzione
-------------------------


This module is maintained by the / Questo modulo è mantenuto dalla rete di imprese Powerp <http://www.powerp.it/>
Developer companies are / I soci sviluppatori sono:
* Didotech s.r.l. <http://www.didotech.com>
* SHS-AV s.r.l. <https://www.shs-av.com/>


|

----------------


|en| **Powerp** is an Italian enterprises network, whose mission is to develop high-level addons designed for Italian enterprise companies.

`Powerp <http://www.powerp.it/>`__ code adds new enhanced features to Italian localization and it released under `LGPL <https://www.gnu.org/licenses/lgpl-3.0.html>`__ or `OPL <https://www.odoo.com/documentation/user/14.0/legal/licenses/licenses.html>`__ licenses.

|it| `Powerp <http://www.powerp.it/>`__ è una rete di imprese italiane, nata con la missione di sviluppare moduli per le PMI.

Il codice di `Powerp <http://www.powerp.it/>`__ aggiunge caratteristiche evolute alla localizzazione italiana; il codice è rilasciato con licenze `LGPL <https://www.gnu.org/licenses/lgpl-3.0.html>`__ e `OPL <https://www.odoo.com/documentation/user/14.0/legal/licenses/licenses.html>`__

I soci fondatori sono:

* `Didotech s.r.l. <http://www.didotech.com>`__
* `SHS-AV s.r.l. <https://www.shs-av.com/>`__
* `Xplain s.r.l. <http://x-plain.it//>`__



|chat_with_us|


|

This module is part of l10n-italy project.

Last Update / Ultimo aggiornamento: 2022-04-13

.. |Maturity| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: 
.. |Build Status| image:: https://travis-ci.org/PowERP-cloud/l10n-italy.svg?branch=12.0
    :target: https://travis-ci.com/PowERP-cloud/l10n-italy
    :alt: github.com
.. |license gpl| image:: https://img.shields.io/badge/licence-LGPL--3-7379c3.svg
    :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
    :alt: License: LGPL-3
.. |license opl| image:: https://img.shields.io/badge/licence-OPL-7379c3.svg
    :target: https://www.odoo.com/documentation/user/14.0/legal/licenses/licenses.html
    :alt: License: OPL
.. |Coverage Status| image:: https://coveralls.io/repos/github/PowERP-cloud/l10n-italy/badge.svg?branch=12.0
    :target: https://coveralls.io/github/PowERP-cloud/l10n-italy?branch=12.0
    :alt: Coverage
.. |Codecov Status| image:: https://codecov.io/gh/PowERP-cloud/l10n-italy/branch/12.0/graph/badge.svg
    :target: https://codecov.io/gh/PowERP-cloud/l10n-italy/branch/12.0
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
.. |OCA Codecov| image:: https://codecov.io/gh/OCA/l10n-italy/branch/12.0/graph/badge.svg
    :target: https://codecov.io/gh/OCA/l10n-italy/branch/12.0
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
   :target: https://t.me/Assitenza_clienti_powERP

