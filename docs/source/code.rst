.. _code:

Code uitleg
============
Het kader om het SPUIS model heen is :py:func:`runSpuis`. Deze voert op basis van input vragen de ``SPUIS401.exe`` uit.
Deze executable is gebaseerd op :py:func:`SPUIS401`.

.. py:function:: runSpuis

   Script to read input file and run program of Spuis. First attempt to script the
	running of Spuis, including file selection, running and plotting of output.
	Based on experience improvements of workflow can probably be implemented.

.. py:function:: SPUIS401

   Returns the calculation results of the water levels and discharge in spuice-gates.

De python functie :py:func:`SPUIS401` is afhankelijk van meerdere functies. Deze zijn te vinden in ./SPUIS401/py/.

.. py:function:: bckwtr(id, ws, debiet, jfn, bm, dn_des, prof_des)

	Bevat de afvoerrelaties van een stuk kanaal (backwatercurves).
	Een keuze wordt gemaakt of de berekeningsmethode met backwatercurves wordt gedaan of met Bernoulli/impulsvergelijkingen.
	De functie kan de minimale, boven en beneden waterstand uit rekenen voor verschillende stroom condities.

.. py:function:: benwst(id, ws, debiet, bm, dn_des, prof_des)

	Berekend benedenwaterstand bij een critisch doorsnede

.. py:function:: bovwst(id, ws, debiet, bm, dn_des, prof_des)
	
	Berekend bovenwaterstand bij een critisch doorsnede

.. py:function:: brnoul(id1, id2, hw1, hw2, debiet, jfn, dn_des, prof_des)
	
	Brnoul is bedoeld voor versnellende stroom. Lost de stromingssituatie op mbv. Bernoulli-vergelijking inclusief wrijvingsverlies.

.. py:function:: brwopp(id, hw, dn_des, prof_des):
	
	Bereken de breedte van het water opppervlak for een gegeven doorsnede ID en water level HW.

.. py:function:: chezyc(id, hw, dn_des, prof_des)

	Berekent Chezycoeff. voor doorsnede ID en waterstand HW.

.. py:function:: energh(id, hw, debiet, dn_des, prof_des)
	
	Berekent energiehoogte ENERGH tov. referentieniveau voor doorsnede ID, waterstand HW en debiet DEBIET

.. py:function:: error(melding: str) -> None
	
	Presenteert een errorstring naar de uitvoerbestanden en naar het scherm, daarna stopt de executie.

.. py:function:: froude(id, h, q, dn_des, prof_des)
	
	Berekent Froudegetal bij doorsnede ID, waterstand H en debiet Q

.. py:function:: getcod(ir: int) -> str
	
	Bepaalt de code van een blok met resultaatgegevens.

.. py:function:: grensd(debiet, id, dn_des, prof_des)
	
	Berekent grensdiepte bij bepaald debiet DEBIET voor doorsnede ID

.. py:function:: hydstr(id, hw, dn_des, prof_des)
	
	Berekent hydraulische straal voor doorsnede ID en niveau waterspiegel HW.

.. py:function:: impuls(id1, id2, hw1, hw2, debiet, jfn, bm, dn_des, prof_des)
	
	IMPULS is bedoeld voor vertragende stroom. Lost de stromingssituatie op dmv. impulsvergelijking indien er gerekend wordt met backwatercurves, dan wordt de wrijvingskracht niet meegenomen in de berekening.

.. py:function:: kracht(id, hw, dn_des, prof_des)
	
	Berekent de hydrostatische kracht voor doorsnede ID bij waterstand HW

.. py:function:: minwst(id, ws, debiet, bm, dn_des, prof_des)
	
	Benoeming parameters min. benedenst. waterstand bij critische doorsnede

.. py:function:: opperv(id, hw, dn_des, prof_des)

	Berekent natte doorsnede OPPERV voor doorsnede ID bij waterstand HW

.. py:function:: reknnr(id, ws, debiet, bm, dn_des, prof_des)
	
	Neerwaarts rekenen van benedenwaterstand

.. py:function:: reknop(id, ws, debiet, bm, dn_des, prof_des)
	
	Opwaarts rekenen van bovenwaterstand

.. py:function:: tblok(ir)
	
	Presenteert een string met de tekal blok aanduiding met daarachter de symbolen der resultaatparameters

.. py:function:: trace(lu, ws, rg, nx, debiet, dn_des, prof_des)
	
	Schrijft de tot nu toe berekende situatie weg. Ook mogelijk na ieder berekend profiel (optioneel)

.. py:function:: wrrgme(rg)
	
	Definieert de mogelijke regimetypen (stromend, critisch, schietend)

.. py:function:: wsprng(id1, id2, w1, w2, debiet, dn_des, prof_des)
	
	Watersprongrelatie, alleen voor horizontale bodem!


De :py:func:`runSpuis` is afhankelijk van een postprocess module ``POSTPROC``. Deze module bevat meerdere functies.

.. py:function:: query_yes_no(question, default="yes")

	Ask a yes/no question via raw_input() and return their answer. "question" is a string that is presented to the user. "default" is the presumed answer if the user just hits <Enter>. It must be "yes" (the default), "no" or None (meaning an answer is required of the user). The "answer" return value is True for "yes" or False for "no".

.. py:function:: query_value(question, default=0.0)

	Ask a input value question via raw_input() and return their answer. "question" is a string that is presented to the user. "default" is the presumed answer if the user just hits <Enter>.

.. py:function:: read_spuisin(in_file)

	Read input file for SPUIS and return contents in dictionary."inpfile" is the location of the input file to be read. It must be formatted to SPUIS specifications and can include comments. Contents of the input file will be returned in a dictionary using keys similar to those used in SPUIS.

.. py:function:: read_spuisout(spuisinput, uqh_file, uws_file)

	Read output files for SPUIS and return contents. "spuisinput" is the input of the calculation created by read_spuisin. Contents of the output files will be returned in Pandas dataframe(s).

.. py:function:: align_y_axis(ax1, ax2)
    
    Sets tick marks of twinx axes to line up with the number of total tick marks of the primary axis. ax1 and ax2 are the matplotlib axes. Spacing between the tick marks will be based on a factor of the default tick spacing chosen by matplotlib. The number of ticks is based on the number on the primary axis. Code adapted from Scott Howard via Stackoverflow: https://stackoverflow.com/questions/26752464/how-do-i-align-gridlines-for-two-y-axis-scales-using-matplotlib

.. py:function:: align_x_axis(ax1, ax2)

	Sets tick marks of twiny axes to line up with the number of total tick marks of the primary axis. ax1 and ax2 are the matplotlib axes. Spacing between the tick marks will be based on a factor of the default tick spacing chosen by matplotlib. The number of ticks is based on the number on the primary axis. Code adapted from Scott Howard via Stackoverflow: https://stackoverflow.com/questions/26752464/how-do-i-align-gridlines-for-two-y-axis-scales-using-matplotlib

.. py:function:: plot_spuis(in_file, spuisinput, uqh_df, uws_df, **keyword_parameters)
	
	Plot a graphical representation of the output from the SPUIS calculation. Two types of plots will be generated, one showing the discharge as a function of head difference for each case and one showng the results for each case of the water levels, energy head, average flow velocity and Froude number. in_file_path is the location of the input file, the plots will be saved here. spuisinput is the input of spuis as generated by read_spuisin. uqh_df and uws_df is the output of spuis as generated by read_spuisout.