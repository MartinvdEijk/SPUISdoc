.. _installatie:

Installatie
===========

.. _pythonpakket:

Benodigde Python pakketten
--------------------------
Om :py:func:`runSpuis` te kunnen gebruiken, zijn er pakketten vereist. De volgende commando kan ingevuld worden:

.. code-block:: console

   pip3 install ./docs/requirements.txt

Deze bevatten voornamelijk de benodigdheden voor de postprocessing dat in :py:func:`runSpuis` plaatsvindt.

Code veranderen & executable maken
----------------------------------
De code bevindt zich onder ./SPUIS401/ waar de head file is :py:func:`SPUIS401`. Deze wordt aangeroepen door :py:func:`runSpuis`.
De functies die gebruikt worden bij :py:func:`SPUIS401` staan gedefinieerd in ./SPUIS401/py/.

Wanneer de code aangepast wordt, is het van belang om een nieuwe onafhankelijke executable te maken.
Dit kan gedaan worden door de ``EXE.py`` file gepositioneerd in ./SPUIS401/. Dit kan alleen gedaan worden wanneer de stap in :ref:'pythonpakket' is uitgevoerd.

Open de python script, geef een nieuwe beschrijving en versie nummer en run de file.

.. code-block:: console

	python3 ./SPUIS401/EXE.py

Een executable wordt aangemaakt en vervangt de huidige executable in ./SPUIS401.
Eerder gemaakte executables zijn te vinden in ./SPUIS401/dist/.
Deze kunnen handmatig verplaatst worden maar moeten vernoemd worden naar ``SPUIS401.exe`` zodat :py:func:`runSpuis` gebruikt kan worden.