
=================================
|icon| ITA - Intrastat 12.0.1.2.5
=================================


**Riclassificazione merci e servizi per dichiarazioni Intrastat**

.. |icon| image:: https://raw.githubusercontent.com/PowERP-cloud/l10n-italy/12.0/l10n_it_intrastat/static/description/icon.png

|Maturity| |Build Status| |license opl|


.. contents::



Overview / Panoramica
=====================

|en| **Italiano**

Questo modulo si occupa della riclassificazione delle merci e dei servizi che sono oggetto di
transazioni comunitarie.

Il modulo precarica anche le tabelle necessarie alla compilazione della dichiarazione:
nomenclature combinate, sezioni doganali, natura delle transazioni, modalità di trasporto.

Per la creazione delle dichiarazioni, degli elenchi riepilogativi e le estrazioni da
presentare all'Agenzia delle Dogane è necessario installare il modulo `l10n_it_intrastat_statement`.


|

|it| N/D

|

Usage / Utilizzo
----------------

**Italiano**


**Fatture e note di credito Intrastat**

È possibile indicare l’assoggettamento di una fattura ad Intrastat attraverso l'apposito campo presente sulla maschera di modifica della fattura stessa.

Sulla scheda Intrastat è presente un pulsante «Ricalcola righe Intrastat». Il pulsante permette al sistema:

- di verificare se le righe prodotto presenti in fattura (scheda "Righe fattura") si riferiscono a prodotti che hanno un codice Intrastat assegnato, o appartengono ad una categoria che ha un codice Intrastat aggregato;
- di generare per questi prodotti le corrispondenti righe Intrastat: le righe accorpano prodotti omogenei per codice Intrastat, indicando nel campo "Massa netta (kg)" il peso totale dei prodotti presenti nelle corrispondenti righe. La riga Intrastat, ovviamente, raggruppa il valore economico dei prodotti;
- N.B.: se una riga presente in fattura si riferisce ad un prodotto che ha come tipologia Intrastat “Varie”, l’importo della riga verrà automaticamente suddiviso in maniera uguale sulle altre righe Intrastat che si riferiscono a beni o servizi. Tale automatismo permette di gestire, in maniera conforme a quanto previsto dalla normativa, il ribaltamento proporzionale dei costi sostenuti per spese accessorie (es: spese di trasporto) sui costi sostenuti per l’acquisto vero e proprio di beni o servizi.

Nella scheda Intrastat, un clic su una riga Intrastat permette di accedere alla maschera di dettaglio.

Nella maschera:

- il campo "Stato acquirente/fornitore" viene popolato in automatico dal campo "Nazione" dell’indirizzo associato al partner;
- i campi configurati in *Impostazioni → Utenti e aziende → Aziende → Nome azienda* (vedi "Informazioni generali" su azienda) vengono popolati in automatico con i valori predefiniti impostati, in ragione della tipologia di fattura (vendita o acquisto);
- se fattura di vendita:

  1. i campi *Origine → Paese di provenienza* e *Origine → Paese di origine* vengono popolati in automatico con la nazione presente nell’indirizzo associato all'azienda;
  2. il campo *Destinazione → Paese di destinazione* viene popolato in automatico con la nazione presente nell'indirizzo associato al partner;

- se fattura di acquisto:

  1. i campi *Origine → Paese di provenienza* e *Origine → Paese di origine* vengono popolati in automatico con la nazione presente nell’indirizzo associato al partner (fornitore);
  2. il campo *Destinazione → Paese di destinazione* viene preso dai dati dell'azienda.

N.B.: tutti i campi possono ovviamente essere modificati, ma l’utilizzo del pulsante «Ricalcola righe Intrastat» ripristinerà i valori predefiniti, sui campi prelevati dalla configurazione dell'azienda o dalla riga fattura.


**Note di credito**

Importante:
   Se si seleziona un periodo che è lo stesso della dichiarazione, la nota di credito, per il suo importo, non confluirà nella sezione di rettifica, ma andrà a stornare direttamente il valore della fattura sulla quale è stata emessa. La verifica sulla fattura da stornare viene fatta confrontando la coppia di valori *Partner/Nomenclatura combinata*.


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
* |menu| Setting > Apps |right_do| Select **l10n_it_intrastat** > Install


|

Configuration / Configurazione
------------------------------

**Italiano**

In *Impostazioni → Utenti e aziende → Aziende → Nome azienda*
impostare i parametri delle seguenti sezioni presenti nella scheda "Informazioni generali".

1. Intrastat

   a) *ID utente (codice UA)*: inserire il codice identificativo Intrastat dell’azienda (codice alfanumerico di 4 caratteri, utilizzato come identificativo per l’accesso alle applicazioni delle Dogane).
   b) *Unità di misura per kg*: parametro che indica l’unità di misura che viene verificata sulla riga fattura soggetta a Intrastat. Se sulla riga il peso è espresso nell’unità di misura indicata nel parametro (o in un suo multiplo), il peso che viene riportato nella corrispondente riga Intrastat è quello preso dalla riga fattura.
   c) *Unità supplementare da*:

      i. *peso*: da peso dei prodotti sulla riga Intrastat
      ii. *quantità*: da quantità dei prodotti sulla riga Intrastat
      iii. *nulla*

   d) *Escludere righe omaggio*: esclude dalle righe Intrastat le righe a valore 0.
   e) *Delegato*: il nominativo della persona delegata alla presentazione della dichiarazione Intrastat.
   f) *Partita IVA delegato*: la partita IVA della persona delegata alla presentazione della dichiarazione Intrastat.
   g) *Nome file da esportare*: nome del file che può essere impostato per forzare quello predefinito (SCAMBI.CEE).
   h) *Sezione doganale*: sezione doganale predefinita da proporre in una nuova dichiarazione.
   i) *Ammontare minimo*: in caso di fatture di importo inferiore usa questo valore nella dichiarazione.

2. Valori predefiniti per cessioni (parametri Intrastat per le fatture di vendita)

   a) *Forzare valore statistico in euro*: casella di selezione attualmente non gestita.
   b) *Natura transazione*: indica il valore predefinito che verrà impostato nelle righe Intrastat di una fattura per il campo di riferimento.
   c) *Condizioni di consegna*: indica il valore predefinito che verrà impostato nelle righe Intrastat di una fattura per il campo di riferimento.
   d) *Modalità di trasporto*: indica il valore predefinito che verrà impostato nelle righe Intrastat di una fattura per il campo di riferimento (Modo di trasporto).
   e) *Provincia di origine*: indica il valore predefinito che verrà impostato nelle righe Intrastat di una fattura per il campo di riferimento (provincia di origine della spedizione dei beni venduti).

3. Valori predefiniti per acquisti (parametri Intrastat per le fatture di acquisto)

   a) *Forzare valore statistico in euro*: casella di selezione attualmente non gestita.
   b) *Natura transazione*: indica il valore predefinito che verrà impostato nelle righe Intrastat di una fattura per il campo di riferimento.
   c) *Condizioni di consegna*: indica il valore predefinito che verrà impostato nelle righe Intrastat di una fattura per il campo di riferimento.
   d) *Modalità di trasporto*: indica il valore predefinito che verrà impostato nelle righe Intrastat di una fattura per il campo di riferimento (Modo di trasporto).
   e) *Provincia di destinazione*: indica il valore predefinito che verrà impostato nelle righe Intrastat di una fattura per il campo di riferimento (provincia di destinazione della spedizione dei beni acquistati).


**Tabelle di sistema**

In *Fatturazione/Contabilità → Configurazione → Intrastat*
sono presenti le funzionalità per la gestione delle tabelle di sistema.

- Sezioni doganali
- Nomenclature combinate
- Modalità di trasporto
- Natura transazione

Tali tabelle sono pre-popolate in fase di installazione del modulo, in base ai valori ammessi per le dichiarazioni Intrastat.

N.B.: Il sottomenù "Intrastat" è visibile solo se vengono abilitate le funzionalità contabili complete.


**Posizione fiscale**

L'assoggettamento ad Intrastat può essere gestito anche a livello generale di singolo partner, associandogli una posizione fiscale che abbia l'apposita casella "Soggetta a Intrastat" selezionata.

Tutte le fatture create per il partner che ha una posizione fiscale marcata come soggetta ad Intrastat avranno l’apposito campo "Soggetta a Intrastat" selezionato automaticamente.


**Prodotti e categorie**

La classificazione Intrastat dei beni o dei servizi può essere fatta sia a livello di categoria che a livello di prodotto.

La priorità è data al prodotto: se su un prodotto non è configurato un codice Intrastat, il sistema tenta di ricavarlo dalla categoria a cui quel prodotto è associato.

Per il prodotto la sezione Intrastat si trova nella scheda «Fatturazione/Contabilità», ove è necessario inserire:

- la tipologia (Bene, Servizio, Varie, Escludere);
- il codice Intrastat, tra quelli censiti tramite l’apposita tabella di sistema "Nomenclature combinate" (il campo viene abilitato solo per le tipologie "Bene" e "Servizio").

Per le categorie di prodotti, le informazioni sono presenti in un’apposita area Intrastat della maschera di dettaglio.


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

* `Openforce`__
* `Link IT srl`__
* `Agile Business Group`__
* `SHS-AV s.r.l. <https://www.zeroincombenze.it/>`__


Contributors / Collaboratori
----------------------------

* Alessandro Camilli
* Lorenzo Battistini
* Lara Baggio <lbaggio@linkgroup.it>
* Glauco Prina <gprina@linkgroup.it>
* Sergio Zanchetta <https://github.com/primes2h>
* Alex Comba <alex.comba@agilebg.com>
* Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
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

Last Update / Ultimo aggiornamento: 2022-02-23

.. |Maturity| image:: https://img.shields.io/badge/maturity-Alfa-black.png
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

