"""Preguntas de análisis de fuentes para Historia (parte A: Historia, siglos XIX y XX).

Todas las fuentes son textos ORIGINALES elaborados para esta práctica: testimonios y
documentos ficticios verosímiles, o síntesis propias de ideas históricas conocidas.
No se copia ningún documento real ni contenido del DEMRE.

Formato: (eje, presentación, texto de la fuente, [(pregunta, correcta, [incorrectas], explicación), ...])
"""
from historia_datos import HIS

FUENTES = [
    (HIS, "Lee el siguiente fragmento de un folleto liberal europeo ficticio, escrito en 1848:",
     "«Ningún rey recibe su poder de Dios. El poder nace de los ciudadanos, que tienen derecho a "
     "expresar libremente sus ideas, a reunirse y a elegir a quienes hacen las leyes. Exigimos una "
     "Constitución escrita que limite al gobierno y una prensa libre de la censura.»",
     [("¿Qué principio defiende principalmente el autor del folleto?",
       "La soberanía popular y la limitación del poder mediante una Constitución",
       ["El origen divino del poder de los reyes", "La propiedad colectiva de los medios de producción",
        "La eliminación de toda forma de gobierno"],
       "El texto afirma que el poder nace de los ciudadanos y pide una Constitución que limite al gobierno: ideas liberales."),
      ("¿Con qué proceso del siglo XIX se relaciona este folleto?",
       "Las revoluciones liberales que enfrentaron a las monarquías absolutas",
       ["La Guerra Fría entre Estados Unidos y la URSS", "La descolonización de Asia y África",
        "El auge del neoliberalismo a fines del siglo XX"],
       "En 1848 hubo revoluciones liberales en varios países europeos contra el absolutismo."),
      ("¿Qué tipo de fuente es el folleto, respecto de los hechos de 1848?",
       "Una fuente primaria, porque fue producida en la época que se estudia",
       ["Una fuente secundaria, porque interpreta hechos ocurridos siglos antes", "Una fuente estadística, porque presenta datos numéricos",
        "Una fuente iconográfica, porque es una imagen"],
       "Las fuentes primarias se producen en el mismo tiempo de los hechos estudiados.")]),

    (HIS, "Lee el siguiente texto de un historiador (texto elaborado para esta práctica):",
     "«Una vez unificados Italia y Alemania, sus gobiernos se dieron cuenta de que crear un Estado no "
     "bastaba: había que formar ciudadanos que se sintieran parte de la nación. Para eso se extendió la "
     "escuela pública, se enseñó una lengua común, se crearon himnos, banderas y fiestas patrias, y el "
     "servicio militar reunió a jóvenes de distintas regiones.»",
     [("Según el historiador, ¿cuál fue el objetivo de las medidas descritas?",
       "Construir una identidad nacional común entre los habitantes del nuevo Estado",
       ["Devolver el poder a las monarquías absolutas", "Separar a las regiones en Estados independientes",
        "Eliminar la educación pública"],
       "Las escuelas, la lengua, los símbolos y el servicio militar buscaban que la población se sintiera parte de una misma nación."),
      ("¿Qué afirmación se puede concluir del texto?",
       "La nación fue en parte una construcción impulsada por el Estado",
       ["La unificación se logró sin intervención del Estado", "Los símbolos patrios no tuvieron importancia política",
        "Italia y Alemania eran naciones unificadas desde la Edad Media"],
       "El autor muestra que el Estado promovió activamente el sentimiento nacional.")]),

    (HIS, "Lee el siguiente texto sobre América Latina en el siglo XIX (texto elaborado para esta práctica):",
     "«Tras las independencias, las nuevas repúblicas debieron definir fronteras, dictar constituciones y "
     "organizar ejércitos, tribunales y sistemas de impuestos. En varios países, la falta de acuerdos "
     "entre grupos regionales y el poder de caudillos locales provocaron largos períodos de guerras "
     "civiles antes de lograr un orden estable.»",
     [("¿Qué problema de las nuevas repúblicas destaca el texto?",
       "Las dificultades para organizar el Estado y lograr estabilidad política",
       ["La falta de recursos naturales para exportar", "La ausencia total de constituciones escritas",
        "La dependencia política de la Unión Soviética"],
       "El texto describe la tarea de organizar el Estado y los conflictos entre grupos y caudillos."),
      ("¿Qué concepto se relaciona mejor con el proceso descrito?",
       "Formación del Estado-nación",
       ["Globalización", "Guerra Fría", "Estado de bienestar"],
       "Definir territorio, leyes e instituciones es parte de la construcción del Estado-nación.")]),

    (HIS, "Lee el siguiente texto sobre Chile entre 1823 y 1830 (texto elaborado para esta práctica):",
     "«Después de la abdicación de O'Higgins, Chile ensayó varias constituciones: algunas federales, otras "
     "centralistas o liberales. Ninguna logró un gobierno duradero. Los grupos conservadores, que temían "
     "el desorden, se impusieron en la batalla de Lircay (1830) y organizaron un régimen con un Poder "
     "Ejecutivo fuerte, que se plasmó en la Constitución de 1833.»",
     [("¿Qué buscaban los conservadores, según el texto?",
       "Terminar con la inestabilidad mediante un gobierno central fuerte",
       ["Implantar un sistema federal", "Eliminar el cargo de Presidente de la República",
        "Volver a depender de la Corona española"],
       "El texto dice que temían el desorden y crearon un Ejecutivo fuerte."),
      ("¿Cómo se suele llamar al período de 1823 a 1830 descrito en el texto?",
       "Período de ensayos constitucionales",
       ["República Parlamentaria", "Período del Frente Popular", "Transición a la democracia"],
       "Se llama así por los distintos proyectos de constitución que se probaron.")]),

    (HIS, "Lee la siguiente síntesis de la Constitución de 1833 (texto elaborado para esta práctica):",
     "«El Presidente duraba cinco años y podía ser reelegido por un período más. Nombraba a ministros, "
     "intendentes y jueces, y podía pedir al Congreso facultades extraordinarias para suspender derechos "
     "en caso de conflicto. Solo votaban los hombres mayores de edad que sabían leer y escribir y tenían "
     "cierta renta o propiedad. El catolicismo era la religión oficial del Estado.»",
     [("¿Qué rasgo del sistema político muestra la fuente?",
       "Un Poder Ejecutivo con amplias atribuciones",
       ["Un Congreso que elegía directamente a los jueces", "La prohibición de la reelección presidencial",
        "La separación de la Iglesia y el Estado"],
       "El Presidente nombraba autoridades y podía pedir facultades extraordinarias."),
      ("Según la fuente, ¿qué tipo de sufragio existía?",
       "Sufragio censitario, limitado por renta, propiedad y alfabetización",
       ["Sufragio universal para hombres y mujeres", "Sufragio femenino sin requisitos",
        "Voto obligatorio para toda la población"],
       "Solo votaban hombres con renta o propiedad y que sabían leer y escribir.")]),

    (HIS, "Lee el siguiente texto sobre la economía chilena del siglo XIX (texto elaborado para esta práctica):",
     "«Desde mediados del siglo XIX, Chile vendió plata y cobre a Europa y trigo a los mercados de "
     "California y Australia, donde la fiebre del oro había atraído a miles de personas. Los barcos a "
     "vapor y el ferrocarril, financiados en parte con capitales británicos, unieron las zonas "
     "productoras con los puertos.»",
     [("¿Qué proceso describe el texto?",
       "La inserción de la economía chilena en los mercados internacionales",
       ["El cierre de la economía chilena al comercio exterior", "La industrialización por sustitución de importaciones",
        "La nacionalización del cobre"],
       "Chile exportaba materias primas y alimentos a otros mercados."),
      ("¿Qué papel tuvo la industrialización del mundo atlántico en este proceso?",
       "Aportó tecnología y capitales que facilitaron las exportaciones chilenas",
       ["Impidió que Chile vendiera productos al extranjero", "Hizo innecesarios los puertos chilenos",
        "Provocó la desaparición del ferrocarril en Chile"],
       "Los barcos a vapor, el ferrocarril y los capitales británicos son productos de la industrialización.")]),

    (HIS, "Lee el siguiente texto sobre el ciclo del salitre (texto elaborado para esta práctica):",
     "«Tras la Guerra del Pacífico, Chile controló los yacimientos de salitre del norte. El Estado cobraba "
     "un impuesto a cada quintal exportado, y esos ingresos financiaron escuelas, ferrocarriles y obras "
     "públicas. Sin embargo, la mayor parte de las oficinas salitreras era propiedad de capitales "
     "extranjeros, y la economía quedó muy dependiente de un solo producto.»",
     [("¿Qué riesgo de la economía salitrera señala el texto?",
       "La dependencia de un solo producto de exportación",
       ["La falta total de ingresos para el Estado", "La ausencia de inversión extranjera",
        "El exceso de industrias manufactureras"],
       "El texto advierte que la economía quedó muy dependiente del salitre."),
      ("¿Qué hecho posterior confirmó ese riesgo?",
       "La crisis de 1929 y la invención del salitre sintético, que hicieron caer las exportaciones",
       ["La creación de la ONU en 1945", "El plebiscito de 1988", "La Reforma Agraria"],
       "Al caer la demanda del salitre natural, la economía chilena sufrió una fuerte crisis."),
      ("Según el texto, ¿cómo usó el Estado los ingresos del salitre?",
       "Para financiar educación, transporte y obras públicas",
       ["Para pagar la deuda de la Confederación Perú-Boliviana", "Para comprar oficinas salitreras extranjeras",
        "Para eliminar los impuestos a las exportaciones"],
       "El texto menciona escuelas, ferrocarriles y obras públicas.")]),

    (HIS, "Lee el siguiente testimonio ficticio de un obrero de Santiago, alrededor de 1905:",
     "«Vivimos ocho personas en una sola pieza del conventillo. Hay un solo pozo de agua para todo el "
     "patio y cuando llueve el barro entra por la puerta. Trabajo doce horas en la fábrica y, si me "
     "enfermo, no me pagan. Dos de mis hijos murieron antes de cumplir un año.»",
     [("¿Qué problema histórico ilustra este testimonio?",
       "La cuestión social",
       ["La Reforma Agraria", "La Guerra Fría", "La crisis de la deuda de 1982"],
       "La cuestión social fueron los graves problemas de vivienda, salud y trabajo de los sectores populares hacia 1900."),
      ("¿Qué demanda sería coherente con la situación descrita?",
       "Leyes que regularan la jornada laboral y protegieran a los trabajadores enfermos",
       ["La eliminación de la educación pública", "El aumento de las horas de trabajo",
        "La restricción del voto a los propietarios"],
       "El testimonio denuncia jornadas largas y falta de protección ante la enfermedad."),
      ("¿Qué limitación tiene esta fuente para conocer la situación de todos los obreros chilenos?",
       "Es la experiencia de una sola persona y no permite generalizar sin otras fuentes",
       ["Fue escrita mucho después de los hechos", "Presenta datos estadísticos de todo el país",
        "Describe la vida de la elite"],
       "Un testimonio es valioso, pero hay que contrastarlo con otras fuentes para generalizar.")]),

    (HIS, "Lee el siguiente informe ficticio de un médico chileno, escrito en 1910:",
     "«En los barrios obreros de la capital, uno de cada tres niños muere antes de cumplir un año. Las "
     "causas principales son el agua contaminada, la falta de alcantarillado y la mala alimentación. "
     "Recomiendo que el Estado construya viviendas higiénicas y extienda el agua potable.»",
     [("¿Qué propone el médico para enfrentar el problema?",
       "Que el Estado intervenga mejorando la vivienda y el agua potable",
       ["Que cada familia resuelva el problema por su cuenta", "Que se prohíba la llegada de personas a la ciudad",
        "Que se cierren todas las fábricas"],
       "El informe recomienda viviendas higiénicas y agua potable a cargo del Estado."),
      ("¿Qué relación tiene esta fuente con el testimonio de un obrero que describe la misma época?",
       "Ambas fuentes muestran, desde distintas perspectivas, las malas condiciones de vida populares",
       ["Se contradicen totalmente", "Ambas describen la vida de la elite",
        "Ninguna se refiere a la salud"],
       "El médico entrega datos y el obrero su experiencia, pero coinciden en el problema.")]),

    (HIS, "Lee el siguiente texto sobre el movimiento obrero chileno (texto elaborado para esta práctica):",
     "«A comienzos del siglo XX, los trabajadores del salitre, de los puertos y de las ciudades formaron "
     "mancomunales y sociedades de resistencia. Organizaron huelgas para pedir mejores salarios y el pago "
     "en dinero en vez de fichas. Algunas protestas fueron reprimidas con violencia, como ocurrió en la "
     "Escuela Santa María de Iquique en 1907.»",
     [("¿Qué buscaban las organizaciones obreras descritas?",
       "Mejorar sus condiciones laborales mediante la acción colectiva",
       ["Disolver el Congreso Nacional", "Aumentar las exportaciones de trigo", "Restablecer la monarquía"],
       "Las mancomunales y huelgas buscaban mejores salarios y condiciones."),
      ("¿Qué muestra el texto sobre la respuesta del Estado a las huelgas de esa época?",
       "En algunos casos respondió con represión violenta",
       ["Siempre aceptó todas las demandas", "No intervino nunca en los conflictos", "Prohibió el trabajo en el salitre"],
       "El texto menciona la matanza de la Escuela Santa María de Iquique.")]),

    (HIS, "Lee el siguiente texto sobre los regímenes totalitarios (texto elaborado para esta práctica):",
     "«El fascismo italiano y el nazismo alemán eliminaron los partidos opositores y crearon un partido "
     "único. Controlaron la prensa, la radio y la educación para difundir su propaganda, persiguieron a "
     "sus opositores y promovieron el culto a la figura del líder. El individuo debía subordinarse por "
     "completo al Estado.»",
     [("¿Qué característica común de estos regímenes destaca el texto?",
       "El control del Estado sobre todos los ámbitos de la vida y la supresión de libertades",
       ["El respeto al pluralismo político", "La separación de los poderes del Estado",
        "La libertad de prensa"],
       "Partido único, propaganda y persecución son rasgos del totalitarismo."),
      ("¿Con qué proceso se relaciona el surgimiento de estos regímenes?",
       "La crisis del Estado liberal en la primera mitad del siglo XX",
       ["El fin de la Guerra Fría", "La independencia de Hispanoamérica", "La transición chilena a la democracia"],
       "La crisis económica y política de la posguerra debilitó a las democracias liberales.")]),

    (HIS, "Observa la siguiente descripción de un afiche de propaganda ficticio de un régimen totalitario de la década de 1930:",
     "«En el centro aparece el rostro del líder, mucho más grande que las personas que lo rodean. Debajo, "
     "una multitud levanta banderas iguales. El texto dice: "
     "“Un pueblo, un partido, un jefe”.»",
     [("¿Qué mensaje busca transmitir el afiche?",
       "La unidad del pueblo bajo un partido único y un líder indiscutido",
       ["La importancia de la diversidad de partidos", "La necesidad de limitar el poder del gobierno",
        "La defensa de la libertad individual"],
       "El tamaño del líder y el lema expresan obediencia a un jefe y a un partido único."),
      ("¿Para qué le sirve a un historiador analizar este tipo de fuente?",
       "Para comprender cómo el régimen buscaba influir en las ideas de la población",
       ["Para conocer la cantidad exacta de habitantes del país", "Para saber el precio de los alimentos",
        "Para comprobar que el régimen era democrático"],
       "La propaganda muestra los mensajes que el régimen quería instalar.")]),

    (HIS, "Lee el siguiente texto sobre la crisis de 1929 en Chile (texto elaborado para esta práctica):",
     "«Cuando la Gran Depresión redujo el comercio mundial, las exportaciones chilenas de salitre y cobre "
     "se desplomaron. Muchas oficinas salitreras cerraron y miles de familias del norte migraron al centro "
     "del país sin trabajo. Los ingresos del Estado cayeron bruscamente y hubo una gran inestabilidad "
     "política entre 1931 y 1932.»",
     [("¿Por qué la crisis afectó tanto a Chile, según el texto?",
       "Porque su economía dependía de exportar materias primas",
       ["Porque Chile no tenía comercio exterior", "Porque Chile tenía una industria muy diversificada",
        "Porque Chile no producía salitre"],
       "Al caer la demanda mundial, las exportaciones de salitre y cobre se desplomaron."),
      ("¿Qué cambio de política económica impulsó Chile después de esta crisis?",
       "Un mayor rol del Estado para industrializar el país y depender menos de las exportaciones",
       ["La eliminación de todas las industrias", "La privatización de todas las empresas públicas",
        "El regreso al modelo salitrero sin cambios"],
       "Desde fines de los años 30 se promovió la industrialización por sustitución de importaciones.")]),

    (HIS, "Lee el siguiente texto sobre la CORFO (texto elaborado para esta práctica):",
     "«Creada en 1939, la Corporación de Fomento de la Producción tuvo como misión industrializar Chile. "
     "Impulsó empresas estratégicas de electricidad, acero y petróleo, y entregó créditos a industrias "
     "privadas. La idea era producir en el país lo que antes se importaba.»",
     [("¿Qué modelo de desarrollo expresa la creación de la CORFO?",
       "La industrialización por sustitución de importaciones con un Estado empresario",
       ["El modelo neoliberal de libre mercado", "El modelo exportador del salitre",
        "Una economía sin participación del Estado"],
       "La CORFO buscaba producir internamente lo que se importaba, con fuerte rol estatal."),
      ("¿Qué rol del Estado muestra el texto?",
       "Un rol activo, que crea empresas y financia la industria",
       ["Un rol mínimo, limitado a la seguridad", "Ningún rol en la economía",
        "Un rol solo en la educación"],
       "El Estado creó empresas estratégicas y entregó créditos.")]),

    (HIS, "Lee el siguiente texto sobre el populismo latinoamericano (texto elaborado para esta práctica):",
     "«Líderes como Juan Domingo Perón en Argentina y Getúlio Vargas en Brasil construyeron su poder con "
     "el apoyo de los trabajadores urbanos. Ampliaron derechos laborales, nacionalizaron empresas y usaron "
     "la radio para dirigirse directamente a las masas. Sus críticos los acusaron de concentrar el poder "
     "y de limitar a la oposición.»",
     [("¿Qué característica del populismo destaca el texto?",
       "Un líder carismático que se apoya en los sectores populares urbanos",
       ["Un gobierno controlado por potencias extranjeras", "Un régimen sin apoyo popular",
        "La eliminación de los derechos laborales"],
       "Perón y Vargas se apoyaron en los trabajadores y se comunicaban directamente con las masas."),
      ("¿Qué aporta la última oración del texto?",
       "Una mirada crítica sobre estos gobiernos, que permite una visión más equilibrada",
       ["Una fecha exacta de su inicio", "Datos sobre la economía de Chile", "Una definición de liberalismo"],
       "El texto presenta tanto logros como críticas.")]),

    (HIS, "Lee el siguiente texto sobre el Estado de bienestar (texto elaborado para esta práctica):",
     "«Después de la Segunda Guerra Mundial, varios países de Europa occidental crearon sistemas públicos "
     "de salud, pensiones y seguro de desempleo financiados con impuestos. Se inspiraron en las ideas del "
     "economista John Maynard Keynes, que proponía que el Estado interviniera para evitar crisis como la "
     "de 1929.»",
     [("¿Qué buscaba el Estado de bienestar, según el texto?",
       "Proteger a la población frente a riesgos como la enfermedad, la vejez y el desempleo",
       ["Eliminar los impuestos", "Reducir al mínimo la acción del Estado",
        "Prohibir la propiedad privada"],
       "Los sistemas de salud, pensiones y seguro de desempleo protegen frente a esos riesgos."),
      ("¿Qué idea sobre la economía compartía este modelo?",
       "Que el Estado debe intervenir para estabilizar la economía",
       ["Que el mercado se regula solo sin intervención", "Que la economía debe ser planificada solo por un partido único",
        "Que los impuestos deben eliminarse"],
       "Keynes proponía intervención estatal para evitar crisis.")]),

    (HIS, "Lee la siguiente síntesis de los propósitos de la Carta de las Naciones Unidas (1945), en palabras propias:",
     "«Los Estados que firmaron la Carta se comprometieron a mantener la paz y la seguridad "
     "internacionales, resolver sus conflictos por medios pacíficos, fomentar relaciones de amistad entre "
     "las naciones y cooperar para resolver problemas económicos, sociales y humanitarios.»",
     [("¿Qué buscaba la creación de la ONU?",
       "Un nuevo marco para regular las relaciones internacionales y evitar otra guerra mundial",
       ["La formación de un imperio mundial", "La eliminación de todos los Estados nacionales",
        "La división del mundo en dos bloques militares"],
       "Tras la Segunda Guerra Mundial se buscó un organismo para mantener la paz."),
      ("¿Qué afirmación es coherente con la fuente?",
       "Los conflictos entre Estados debían resolverse por medios pacíficos",
       ["Las guerras eran la forma normal de resolver conflictos", "Cada país debía actuar sin cooperar con otros",
        "La ONU tendría un ejército propio para conquistar territorios"],
       "La Carta compromete a resolver conflictos pacíficamente.")]),

    (HIS, "Lee la siguiente síntesis, en palabras propias, de algunas ideas de la Declaración Universal de los Derechos Humanos (1948):",
     "«Todas las personas nacen libres e iguales en dignidad y derechos. Nadie puede ser sometido a "
     "torturas ni detenido arbitrariamente. Toda persona tiene derecho a la libertad de opinión y de "
     "expresión, a la educación y a participar en el gobierno de su país.»",
     [("¿Qué principio fundamental expresa la fuente?",
       "La dignidad e igualdad de todos los seres humanos",
       ["La superioridad de algunos pueblos sobre otros", "El derecho del Estado a detener sin juicio",
        "La prohibición de la libertad de expresión"],
       "La Declaración parte de la igualdad en dignidad y derechos."),
      ("¿Qué hecho histórico influyó en la redacción de esta Declaración?",
       "Las atrocidades cometidas durante la Segunda Guerra Mundial, como el Holocausto",
       ["La Guerra del Pacífico", "La Revolución en Libertad", "La caída del Muro de Berlín"],
       "La Declaración buscó que esos crímenes no se repitieran.")]),

    (HIS, "Lee el siguiente texto sobre la descolonización (texto elaborado para esta práctica):",
     "«Entre 1945 y 1975, decenas de territorios de Asia y África se independizaron de las potencias "
     "europeas. Algunos lo lograron por medios pacíficos, como la India con el liderazgo de Gandhi; otros, "
     "tras largas guerras, como Argelia. Muchos de los nuevos países se declararon «no alineados», es "
     "decir, sin pertenecer a ninguno de los bloques de la Guerra Fría.»",
     [("¿Qué proceso describe el texto?",
       "La independencia de colonias de Asia y África después de 1945",
       ["La conquista de América por los europeos", "La formación de la Unión Europea",
        "La unificación de Italia y Alemania"],
       "La descolonización fue la independencia de las colonias europeas."),
      ("¿Qué significaba ser un país «no alineado»?",
       "No formar parte del bloque liderado por Estados Unidos ni del liderado por la URSS",
       ["Apoyar siempre a Estados Unidos", "Ser parte del Pacto de Varsovia", "Seguir siendo una colonia europea"],
       "El texto lo define como no pertenecer a ninguno de los bloques.")]),

    (HIS, "Lee los siguientes discursos ficticios de la Guerra Fría, escritos para esta práctica:",
     "Discurso 1: «Defendemos el mundo libre: elecciones, empresas privadas y libertad de expresión frente "
     "a la amenaza del comunismo.»\nDiscurso 2: «Defendemos a los trabajadores del mundo frente a la "
     "explotación capitalista y al imperialismo de Occidente.»",
     [("¿Qué muestran estos discursos sobre la Guerra Fría?",
       "Una confrontación ideológica entre capitalismo y comunismo",
       ["Un acuerdo total entre las potencias", "Una guerra entre países europeos por colonias",
        "La unión de ambos bloques contra el fascismo"],
       "Cada discurso presenta su sistema como el correcto y al otro como amenaza."),
      ("¿Qué bloque representaría probablemente el discurso 2?",
       "El bloque socialista liderado por la Unión Soviética",
       ["El bloque liderado por Estados Unidos", "Los países no alineados", "La Sociedad de las Naciones"],
       "El discurso 2 critica al capitalismo y defiende a los trabajadores, ideas del bloque soviético."),
      ("¿Qué debe considerar un estudiante al analizar estos discursos?",
       "Que son fuentes con una postura política y buscan convencer",
       ["Que son datos estadísticos neutrales", "Que fueron escritos por historiadores actuales",
        "Que describen hechos de la Antigüedad"],
       "Los discursos políticos expresan la visión de quien los emite.")]),

    (HIS, "Lee el siguiente texto sobre la Revolución Cubana (texto elaborado para esta práctica):",
     "«El triunfo de Fidel Castro en 1959 y el posterior acercamiento de Cuba a la URSS preocuparon a "
     "Estados Unidos. Para evitar nuevas revoluciones, en 1961 lanzó la Alianza para el Progreso, un "
     "programa de ayuda económica que apoyaba reformas como la agraria y la educacional en América Latina.»",
     [("¿Cuál era el objetivo principal de la Alianza para el Progreso, según el texto?",
       "Evitar que se extendieran revoluciones como la cubana mediante reformas y ayuda económica",
       ["Apoyar la expansión del comunismo en América", "Invadir todos los países de la región",
        "Crear una moneda única latinoamericana"],
       "El texto dice que buscaba evitar nuevas revoluciones."),
      ("¿Qué muestra el texto sobre la Guerra Fría en América Latina?",
       "Que la región también fue escenario de la competencia entre las superpotencias",
       ["Que América Latina no tuvo relación con la Guerra Fría", "Que la Guerra Fría terminó en 1959",
        "Que Cuba se alió con Estados Unidos"],
       "El caso cubano y la respuesta de EE.UU. muestran esa competencia.")]),

    (HIS, "Lee el siguiente texto sobre las dictaduras del Cono Sur (texto elaborado para esta práctica):",
     "«En las décadas de 1960 a 1980, las Fuerzas Armadas tomaron el poder en Brasil, Argentina, Uruguay y "
     "Chile, entre otros países. Justificaron su acción en la «Doctrina de Seguridad Nacional», que veía "
     "a ciertos grupos del propio país como «enemigos internos». Se suspendieron derechos, se clausuraron "
     "parlamentos y miles de personas fueron detenidas, torturadas o hechas desaparecer.»",
     [("¿Qué planteaba la Doctrina de Seguridad Nacional, según el texto?",
       "Que existían enemigos internos que debían ser combatidos por las Fuerzas Armadas",
       ["Que los militares no debían intervenir en política", "Que había que ampliar los derechos civiles",
        "Que los parlamentos debían fortalecerse"],
       "El texto explica que veía a grupos del propio país como enemigos internos."),
      ("¿Qué consecuencia de estas dictaduras menciona el texto?",
       "Violaciones sistemáticas a los derechos humanos",
       ["El fortalecimiento de los parlamentos", "El aumento de la libertad de prensa",
        "La realización de elecciones libres periódicas"],
       "Detenciones, torturas y desapariciones son violaciones a los derechos humanos.")]),

    (HIS, "Lee el siguiente texto sobre el fin de la Guerra Fría (texto elaborado para esta práctica):",
     "«La caída del Muro de Berlín en 1989 y la disolución de la Unión Soviética en 1991 pusieron fin al "
     "mundo bipolar. Muchos países adoptaron economías de mercado, se abrieron al comercio internacional y "
     "privatizaron empresas estatales. El desarrollo de internet aceleró el intercambio de información "
     "entre países.»",
     [("¿Qué procesos se aceleraron tras el fin de la Guerra Fría, según el texto?",
       "El auge del neoliberalismo y la globalización",
       ["La formación de nuevos bloques comunistas", "El aislamiento económico de los países",
        "La creación de más colonias europeas"],
       "Economías de mercado, apertura comercial e internet son rasgos de esos procesos."),
      ("¿Qué significa que el mundo dejara de ser «bipolar»?",
       "Que ya no estaba dividido en dos grandes bloques enfrentados",
       ["Que desaparecieron todos los países", "Que solo quedaron dos países en el mundo",
        "Que se dividió en dos continentes"],
       "El mundo bipolar era el de los bloques de Estados Unidos y la URSS.")]),

    (HIS, "Lee el siguiente texto sobre la globalización (texto elaborado para esta práctica):",
     "«Hoy un teléfono se diseña en un país, sus piezas se fabrican en otros y se arma en un tercero. Para "
     "algunos, la globalización ha permitido bajar precios y difundir conocimientos. Para otros, ha "
     "aumentado la desigualdad entre países y ha debilitado culturas locales.»",
     [("¿Qué ejemplo usa el texto para explicar la globalización?",
       "La producción de un teléfono repartida entre varios países",
       ["Un conflicto militar entre dos países", "La independencia de una colonia",
        "La elección de un presidente"],
       "El teléfono diseñado, fabricado y armado en distintos países ilustra la integración mundial."),
      ("¿Qué afirmación representa mejor el contenido del texto?",
       "La globalización tiene efectos que se valoran de manera distinta",
       ["La globalización solo tiene efectos negativos", "La globalización no existe en la actualidad",
        "Todos coinciden en que la globalización solo trae beneficios"],
       "El texto presenta opiniones a favor y en contra.")]),
]
