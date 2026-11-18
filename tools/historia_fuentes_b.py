"""Preguntas de análisis de fuentes para Historia (parte B: Chile en el siglo XX, Formación
ciudadana y Sistema económico).

Todas las fuentes son textos ORIGINALES elaborados para esta práctica: testimonios ficticios
verosímiles o síntesis propias de hechos e ideas conocidas. No se copia ningún documento
real ni contenido del DEMRE.

Formato: (eje, presentación, texto de la fuente, [(pregunta, correcta, [incorrectas], explicación), ...])
"""
from historia_datos import CIU, ECO, HIS

FUENTES = [
    (HIS, "Lee el siguiente testimonio ficticio de una mujer que llegó a Santiago en 1955:",
     "«Nos vinimos del campo porque allá no había trabajo para todos y el patrón pagaba muy poco. En "
     "Santiago no encontramos casa, así que levantamos una mediagua con tablas y latas a orillas del "
     "Zanjón de la Aguada, junto a otras familias. No teníamos luz ni agua, pero los niños pudieron ir "
     "a la escuela.»",
     [("¿Qué proceso de mediados del siglo XX ilustra este testimonio?",
       "La migración del campo a la ciudad",
       ["La migración de chilenos a Europa", "La llegada de colonos alemanes al sur", "La ocupación de la Araucanía"],
       "La familia deja el campo en busca de oportunidades en Santiago."),
      ("¿Qué problema urbano muestra la fuente?",
       "La falta de viviendas y servicios básicos para los recién llegados",
       ["El exceso de viviendas desocupadas", "La falta de escuelas en todo el país", "El exceso de industrias en el campo"],
       "Las familias construyen mediaguas sin luz ni agua: las llamadas poblaciones callampa."),
      ("Según el testimonio, ¿qué motivó a la familia a migrar?",
       "La falta de trabajo y los bajos salarios en el campo",
       ["Un terremoto en Santiago", "La búsqueda de un clima más frío", "Una guerra en el sur"],
       "La mujer dice que en el campo no había trabajo para todos y pagaban poco.")]),

    (HIS, "Lee el siguiente texto sobre las tomas de terreno (texto elaborado para esta práctica):",
     "«En 1957, cientos de familias sin casa ocuparon un terreno al sur de Santiago y fundaron la "
     "población La Victoria. Organizadas en comités, trazaron calles, levantaron viviendas y exigieron "
     "al Estado servicios básicos. Las tomas mostraron la capacidad de organización de los pobladores.»",
     [("¿Qué demuestra el caso descrito?",
       "Que los pobladores se organizaron para enfrentar la falta de vivienda",
       ["Que el problema de vivienda no existía", "Que el Estado entregó casas a todas las familias",
        "Que las familias migraron al extranjero"],
       "Los comités organizaron la toma y exigieron servicios."),
      ("¿Con qué concepto se relaciona la acción de los pobladores?",
       "Movimiento social",
       ["Totalitarismo", "Sufragio censitario", "Monopolio"],
       "Se trata de una acción colectiva organizada para lograr demandas.")]),

    (HIS, "Lee el siguiente texto sobre la democratización en Chile (texto elaborado para esta práctica):",
     "«En 1949 las mujeres pudieron votar por primera vez en elecciones presidenciales y parlamentarias. "
     "En 1958 se creó la cédula única de votación, que dificultó el cohecho (la compra de votos). En 1970 "
     "se permitió votar a los mayores de 18 años y a quienes no sabían leer. Como resultado, el número de "
     "votantes creció de manera notable.»",
     [("¿Qué proceso muestran las reformas descritas?",
       "La ampliación del sufragio y la democratización de la sociedad chilena",
       ["La restricción del voto a los propietarios", "La eliminación de las elecciones",
        "El fin del sistema presidencial"],
       "Las reformas incorporaron a nuevos votantes y redujeron prácticas como el cohecho."),
      ("¿Para qué sirvió la cédula única de votación, según el texto?",
       "Para dificultar la compra de votos",
       ["Para permitir el voto femenino", "Para prohibir el voto de los jóvenes", "Para elegir a los jueces"],
       "El texto dice que dificultó el cohecho.")]),

    (HIS, "Lee el siguiente texto sobre la Reforma Agraria (texto elaborado para esta práctica):",
     "«Entre 1962 y 1973, los gobiernos chilenos expropiaron grandes fundos que estaban mal trabajados y "
     "entregaron tierras a campesinos. En 1967 una ley permitió formar sindicatos campesinos. Para los "
     "grandes propietarios, la reforma afectó su derecho de propiedad; para los campesinos, fue una "
     "oportunidad de acceder a la tierra.»",
     [("¿Qué buscaba la Reforma Agraria?",
       "Redistribuir la tierra y mejorar la situación de los campesinos",
       ["Concentrar la tierra en menos propietarios", "Prohibir los sindicatos en el campo",
        "Trasladar a los campesinos a la ciudad"],
       "La reforma expropió fundos y entregó tierras a campesinos."),
      ("¿Qué muestra la última oración del texto?",
       "Que la reforma fue valorada de forma distinta por los grupos involucrados",
       ["Que todos estuvieron de acuerdo con la reforma", "Que la reforma no tuvo efectos",
        "Que la reforma ocurrió en el siglo XIX"],
       "Propietarios y campesinos tenían visiones opuestas.")]),

    (HIS, "Lee las siguientes dos interpretaciones ficticias sobre el quiebre de la democracia en 1973, elaboradas para esta práctica:",
     "Historiador A: «El golpe fue el resultado de una profunda polarización: los partidos dejaron de "
     "buscar acuerdos, la crisis económica era grave y muchos sectores veían al adversario como un enemigo.»\n"
     "Historiador B: «Aunque había crisis, la democracia no se derrumbó sola: fue interrumpida por la "
     "decisión de las Fuerzas Armadas, con el apoyo de sectores civiles y del gobierno de Estados Unidos.»",
     [("¿En qué se diferencian ambas interpretaciones?",
       "A pone el acento en la polarización y la crisis; B, en la decisión de los actores que dieron el golpe",
       ["A niega que hubiera crisis económica; B afirma que no hubo golpe", "Ambas dicen exactamente lo mismo",
        "A habla de la Guerra del Pacífico y B de la crisis de 1929"],
       "Cada historiador destaca causas distintas del mismo hecho."),
      ("¿Qué se puede concluir al comparar ambas interpretaciones?",
       "Un mismo hecho histórico puede explicarse de formas distintas según las fuentes y el enfoque",
       ["Solo una de ellas puede ser una fuente histórica", "La historia no permite debatir interpretaciones",
        "Ambas son fuentes primarias de 1973"],
       "Las interpretaciones historiográficas pueden diferir y complementarse."),
      ("¿Qué tipo de fuentes son estas interpretaciones?",
       "Fuentes secundarias, porque analizan hechos del pasado",
       ["Fuentes primarias, porque fueron escritas el 11 de septiembre de 1973", "Fuentes estadísticas",
        "Fuentes iconográficas"],
       "Los textos de historiadores que interpretan el pasado son fuentes secundarias.")]),

    (HIS, "Lee el siguiente texto sobre la economía durante la dictadura (texto elaborado para esta práctica):",
     "«Un grupo de economistas formados en la Universidad de Chicago impulsó un cambio radical: se "
     "redujeron los aranceles, se privatizaron empresas públicas y se crearon las AFP (1980) para "
     "administrar las pensiones. El Estado dejó de ser empresario y el mercado pasó a asignar la mayoría "
     "de los recursos. El país creció en algunos períodos, pero sufrió una grave crisis en 1982.»",
     [("¿Qué modelo económico describe el texto?",
       "El modelo neoliberal",
       ["La industrialización por sustitución de importaciones", "La economía salitrera",
        "La economía planificada socialista"],
       "Apertura comercial, privatizaciones y mercado como asignador son rasgos del neoliberalismo."),
      ("¿Qué cambio en el rol del Estado muestra el texto?",
       "El Estado redujo su participación directa en la economía",
       ["El Estado creó muchas empresas nuevas", "El Estado estatizó la banca y las pensiones",
        "El Estado prohibió el comercio exterior"],
       "El texto dice que el Estado dejó de ser empresario.")]),

    (HIS, "Lee la siguiente síntesis, en palabras propias, de las conclusiones de las comisiones de verdad en Chile:",
     "«La Comisión Nacional de Verdad y Reconciliación (Informe Rettig, 1991) y la Comisión sobre Prisión "
     "Política y Tortura (Informe Valech, 2004) concluyeron que durante la dictadura agentes del Estado "
     "cometieron violaciones sistemáticas a los derechos humanos: ejecuciones, desapariciones forzadas y "
     "torturas.»",
     [("¿Qué aportan estos informes al conocimiento de la historia reciente de Chile?",
       "Reconocen oficialmente y documentan las violaciones a los derechos humanos",
       ["Niegan que existieran violaciones a los derechos humanos", "Describen la economía del salitre",
        "Analizan la Guerra Fría en Europa"],
       "Son informes de comisiones del Estado que documentaron esos hechos."),
      ("¿Qué significa que las violaciones fueran «sistemáticas»?",
       "Que respondían a una práctica organizada y no a hechos aislados",
       ["Que ocurrieron una sola vez", "Que fueron accidentes", "Que no fueron investigadas"],
       "Sistemático indica una práctica organizada y repetida.")]),

    (HIS, "Lee el siguiente testimonio ficticio sobre las protestas de 1983:",
     "«Esa noche, a las ocho, todo el barrio empezó a golpear ollas. Era la primera vez en diez años que "
     "nos atrevíamos a protestar juntos. La crisis económica había dejado sin trabajo a mi padre y a "
     "muchos vecinos. Al día siguiente, en la parroquia, se organizó una olla común.»",
     [("¿Qué factor de la recuperación de la democracia muestra el testimonio?",
       "Las protestas sociales impulsadas en parte por la crisis económica",
       ["La firma de un tratado internacional", "Una guerra con un país vecino", "La nacionalización del cobre"],
       "Las protestas nacionales de los años 80 y la crisis económica debilitaron al régimen."),
      ("¿Qué papel tuvo la parroquia según el testimonio?",
       "Fue un espacio de organización y ayuda para los vecinos",
       ["Prohibió las protestas", "Organizó elecciones presidenciales", "Fue sede del Congreso Nacional"],
       "La Iglesia y sus parroquias fueron espacios de apoyo, como en las ollas comunes.")]),

    (HIS, "Lee el siguiente texto sobre la transición a la democracia (texto elaborado para esta práctica):",
     "«En el plebiscito del 5 de octubre de 1988, la opción No ganó con cerca del 56% de los votos, lo que "
     "obligó a convocar elecciones. En 1989 se aprobaron reformas a la Constitución y se eligió como "
     "presidente a Patricio Aylwin, que asumió en marzo de 1990.»",
     [("¿Qué consecuencia tuvo el triunfo del No, según el texto?",
       "La convocatoria a elecciones presidenciales y parlamentarias",
       ["La permanencia indefinida del régimen militar", "La disolución del país", "El regreso de la Constitución de 1833"],
       "El triunfo del No obligó a convocar elecciones."),
      ("¿Qué caracterizó a la transición chilena según la fuente?",
       "Se realizó por vías institucionales, como un plebiscito, reformas y elecciones",
       ["Se logró mediante una guerra civil", "Fue impuesta por una potencia extranjera",
        "Se hizo sin participación de los votantes"],
       "El texto menciona un plebiscito, reformas constitucionales y una elección.")]),

    # ------------------------------------------------------------- Formación ciudadana
    (CIU, "Lee el siguiente texto sobre la democracia (texto elaborado para esta práctica):",
     "«Una democracia no se reduce a votar cada cierto tiempo. Requiere elecciones libres y periódicas, "
     "separación de los poderes del Estado, respeto a los derechos humanos, libertad de prensa y "
     "reconocimiento de que las minorías pueden expresarse y llegar a ser mayoría.»",
     [("¿Qué idea central plantea el texto?",
       "La democracia incluye varios atributos además de las elecciones",
       ["La democracia consiste solo en votar", "La democracia no necesita libertad de prensa",
        "La democracia exige un partido único"],
       "El autor enumera elementos además del voto."),
      ("¿Cuál de las siguientes situaciones sería contraria a lo que plantea el texto?",
       "Que un gobierno cierre los medios de comunicación que lo critican",
       ["Que se realicen elecciones cada cuatro años", "Que una minoría forme un partido político",
        "Que los tribunales actúen con independencia"],
       "Cerrar medios críticos atenta contra la libertad de prensa.")]),

    (CIU, "Lee el siguiente texto sobre la institucionalidad chilena (texto elaborado para esta práctica):",
     "«La Contraloría General de la República revisa que los actos de la administración del Estado se "
     "ajusten a la ley y controla el uso de los recursos públicos. Es un organismo autónomo: no depende "
     "del Presidente ni del Congreso.»",
     [("¿Qué función cumple la Contraloría según el texto?",
       "Controlar la legalidad de los actos de la administración y el uso de recursos públicos",
       ["Dictar las leyes del país", "Elegir al Presidente de la República", "Juzgar delitos comunes"],
       "La Contraloría fiscaliza la legalidad y el uso de los recursos."),
      ("¿Por qué es importante que la Contraloría sea autónoma?",
       "Porque puede fiscalizar al gobierno sin depender de él",
       ["Porque así puede dictar leyes", "Porque así elige a los ministros", "Porque así no tiene que cumplir la ley"],
       "La autonomía permite controlar al poder sin depender de él.")]),

    (CIU, "Lee el siguiente texto sobre la desinformación (texto elaborado para esta práctica):",
     "«Una noticia falsa se comparte en redes sociales mucho más rápido que su desmentido. Antes de "
     "reenviar una información conviene revisar quién la publica, si otros medios confiables la "
     "confirman y si la fecha es actual. La desinformación puede influir en lo que votan las personas.»",
     [("¿Qué riesgo para la democracia plantea el texto?",
       "Que la desinformación influya en las decisiones de los ciudadanos",
       ["Que las redes sociales eliminen las elecciones", "Que los medios confiables desaparezcan por ley",
        "Que las personas no puedan votar"],
       "El texto advierte que la desinformación puede influir en el voto."),
      ("¿Qué recomendación entrega el texto?",
       "Verificar la fuente y contrastar la información antes de compartirla",
       ["Compartir toda noticia de inmediato", "Leer solo el título", "Creer solo lo que comparten los amigos"],
       "Propone revisar quién publica y si otros medios lo confirman.")]),

    (CIU, "Lee el siguiente texto sobre las tecnologías de la información (texto elaborado para esta práctica):",
     "«Internet permite que los ciudadanos se informen, opinen y se organicen con rapidez, y facilita "
     "trámites y la transparencia del Estado. Sin embargo, también puede exponer datos personales, "
     "encerrar a las personas en grupos que solo piensan igual y dejar fuera a quienes no tienen "
     "conexión.»",
     [("¿Qué hace el texto respecto de las tecnologías de la información?",
       "Presenta tanto oportunidades como riesgos para la vida democrática",
       ["Solo enumera beneficios", "Solo critica su uso", "Explica cómo fabricar computadores"],
       "El texto contrasta ventajas y riesgos."),
      ("¿Qué riesgo se relaciona con la «brecha digital»?",
       "Que quienes no tienen conexión queden excluidos",
       ["Que haya demasiada transparencia", "Que los trámites sean más rápidos", "Que todos piensen distinto"],
       "La brecha digital es la desigualdad en el acceso a internet.")]),

    (CIU, "Lee el siguiente texto sobre el sistema procesal penal chileno (texto elaborado para esta práctica):",
     "«Desde la reforma procesal penal, iniciada en el año 2000, el Ministerio Público investiga los "
     "delitos a través de sus fiscales; la Defensoría Penal Pública defiende a los imputados que no "
     "tienen abogado; y los jueces de garantía y los tribunales orales deciden. Los juicios son públicos "
     "y orales.»",
     [("¿Qué institución investiga los delitos según el texto?",
       "El Ministerio Público, mediante sus fiscales",
       ["La Defensoría Penal Pública", "El Congreso Nacional", "La Contraloría General de la República"],
       "Los fiscales del Ministerio Público dirigen la investigación."),
      ("¿Qué derecho resguarda la Defensoría Penal Pública?",
       "El derecho a defensa de las personas acusadas",
       ["El derecho a voto", "El derecho a la propiedad", "El derecho a la educación"],
       "Defiende a los imputados que no tienen abogado."),
      ("¿Qué ventaja tiene que los juicios sean públicos y orales?",
       "Mayor transparencia en la forma en que se imparte justicia",
       ["Que los juicios sean secretos", "Que no se pueda presentar pruebas", "Que el acusado no pueda hablar"],
       "La publicidad permite conocer cómo se juzga.")]),

    (CIU, "Lee el siguiente caso ficticio:",
     "«Una municipalidad decidió cerrar la única plaza de un barrio sin consultar a los vecinos. Una "
     "vecina considera que esa decisión arbitraria afecta sus derechos y presenta un recurso ante la "
     "Corte de Apelaciones para que se le proteja.»",
     [("¿Qué acción judicial está usando la vecina?",
       "Un recurso de protección",
       ["Una acusación constitucional", "Un plebiscito comunal", "Una iniciativa popular de ley"],
       "El recurso de protección se presenta ante la Corte de Apelaciones cuando un acto arbitrario o ilegal afecta derechos."),
      ("¿Qué muestra el caso sobre el acceso a la justicia?",
       "Que las personas pueden recurrir a los tribunales para resguardar sus derechos",
       ["Que solo las autoridades pueden ir a tribunales", "Que los municipios no deben cumplir la ley",
        "Que los derechos no pueden defenderse"],
       "Los tribunales permiten que cualquier persona defienda sus derechos.")]),

    # ------------------------------------------------------------- Sistema económico
    (ECO, "Lee la siguiente noticia ficticia:",
     "«Una fuerte helada dañó gran parte de las plantaciones de paltas del país. Los comerciantes de la "
     "feria informan que hay muchas menos paltas a la venta y que su precio subió casi al doble en una "
     "semana.»",
     [("¿Qué explica el aumento del precio según la noticia?",
       "La disminución de la oferta de paltas",
       ["El aumento de la oferta de paltas", "La disminución de la demanda", "Un nuevo impuesto a las frutas"],
       "Con menos paltas a la venta y la misma demanda, el precio sube."),
      ("¿Qué tipo de factor alteró el funcionamiento del mercado en este caso?",
       "Un factor natural que afectó la producción",
       ["Una decisión del Banco Central", "Una huelga de transportistas", "Un cambio en la Constitución"],
       "La helada es un factor climático.")]),

    (ECO, "Lee el siguiente texto sobre la libre competencia (texto elaborado para esta práctica):",
     "«En un caso ficticio, tres empresas que venden casi todo el papel higiénico del país se pusieron de "
     "acuerdo en secreto para subir sus precios al mismo tiempo. La Fiscalía Nacional Económica investigó "
     "y el Tribunal de Defensa de la Libre Competencia las multó.»",
     [("¿Qué falta cometieron las empresas?",
       "Colusión, es decir, un acuerdo para no competir y fijar precios",
       ["Inflación", "Dumping", "Evasión de impuestos"],
       "Acordar precios en secreto es colusión."),
      ("¿Qué muestra el caso sobre la relación entre el Estado y el mercado?",
       "Que el Estado fiscaliza y sanciona prácticas que dañan la competencia",
       ["Que el Estado fija todos los precios", "Que el Estado no participa en la economía",
        "Que las empresas no deben cumplir la ley"],
       "El Estado interviene para proteger la libre competencia y a los consumidores.")]),

    (ECO, "Lee el siguiente texto sobre los modelos de desarrollo (texto elaborado para esta práctica):",
     "«En algunas zonas industriales del país, conocidas como «zonas de sacrificio», la concentración de "
     "fundiciones y centrales termoeléctricas ha generado contaminación del aire, el agua y el suelo. Sus "
     "habitantes reclaman que el crecimiento económico no puede lograrse a costa de su salud.»",
     [("¿Qué problema de ciertos modelos de desarrollo plantea el texto?",
       "Sus impactos ambientales y sociales sobre las comunidades",
       ["La falta de industrias en el país", "El exceso de áreas verdes", "La ausencia de crecimiento económico"],
       "La contaminación afecta la salud de los habitantes."),
      ("¿Qué concepto propone equilibrar crecimiento económico, bienestar social y cuidado ambiental?",
       "Desarrollo sustentable",
       ["Monopolio", "Inflación", "Sufragio censitario"],
       "El desarrollo sustentable busca satisfacer necesidades actuales sin comprometer a las generaciones futuras.")]),

    (ECO, "Lee el siguiente texto sobre los derechos laborales en Chile (texto elaborado para esta práctica):",
     "«Las leyes sociales de 1924 regularon el contrato de trabajo, los accidentes laborales y la "
     "organización sindical. En 1931 se reunieron en el primer Código del Trabajo. Estas normas fueron "
     "en gran parte resultado de décadas de demandas del movimiento obrero.»",
     [("Según el texto, ¿qué influyó en la aprobación de estas leyes?",
       "Las demandas del movimiento obrero",
       ["La crisis de los misiles en Cuba", "La creación de la ONU", "La caída del Muro de Berlín"],
       "El texto dice que fueron resultado de décadas de demandas obreras."),
      ("¿Qué importancia tuvo el Código del Trabajo de 1931?",
       "Reunió en un solo cuerpo legal las normas que protegían a los trabajadores",
       ["Eliminó todos los derechos laborales", "Prohibió los sindicatos", "Estableció el voto femenino"],
       "El Código ordenó las leyes laborales existentes.")]),

    (ECO, "Lee el siguiente texto sobre la organización sindical (texto elaborado para esta práctica):",
     "«En 1953 se fundó la Central Única de Trabajadores (CUT), liderada por Clotario Blest, que reunió a "
     "sindicatos de distintos sectores. Su objetivo era negociar con más fuerza frente a empleadores y "
     "gobiernos, defendiendo salarios y condiciones laborales.»",
     [("¿Por qué los sindicatos se agruparon en una central?",
       "Para tener mayor fuerza al defender sus demandas",
       ["Para disolver los sindicatos existentes", "Para elegir al Presidente de la República",
        "Para administrar las empresas del Estado"],
       "Unidos podían negociar con más fuerza."),
      ("¿Con qué derecho laboral se relaciona directamente esta fuente?",
       "El derecho a la libertad sindical",
       ["El derecho a la propiedad intelectual", "El derecho a voto", "El derecho a la nacionalidad"],
       "La formación de sindicatos y centrales ejerce la libertad sindical.")]),

    (ECO, "Lee el siguiente texto sobre la jornada laboral (texto elaborado para esta práctica):",
     "«En 2023 se aprobó en Chile una ley que reduce gradualmente la jornada laboral de 45 a 40 horas "
     "semanales. Quienes la apoyaron destacaron que mejora la calidad de vida y el tiempo con la familia; "
     "algunos empresarios advirtieron sobre los costos para las pequeñas empresas.»",
     [("¿Qué cambio establece la ley descrita?",
       "La reducción gradual de la jornada laboral semanal",
       ["El aumento de la jornada a 50 horas", "La eliminación del salario mínimo", "La prohibición del teletrabajo"],
       "La ley reduce la jornada de 45 a 40 horas."),
      ("¿Qué hace el texto respecto de la ley?",
       "Presenta argumentos a favor y preocupaciones de distintos actores",
       ["Solo presenta argumentos en contra", "Solo presenta argumentos a favor", "No menciona opiniones"],
       "Incluye la visión de quienes la apoyaron y de algunos empresarios.")]),

    (ECO, "Lee el siguiente testimonio ficticio de un repartidor de aplicación (2024):",
     "«Trabajo con mi bicicleta para una aplicación de reparto. Elijo mis horarios, pero si llueve o me "
     "accidento, nadie me cubre. Hace poco se aprobó una ley que reconoce algunos derechos a los "
     "trabajadores de plataformas, como la cotización para salud y pensiones.»",
     [("¿Qué tendencia del mundo del trabajo muestra el testimonio?",
       "El crecimiento del trabajo en plataformas digitales",
       ["La desaparición de la tecnología", "El regreso al trabajo en el salitre", "La eliminación de los servicios"],
       "El repartidor trabaja a través de una aplicación."),
      ("¿Qué desafío para los derechos laborales plantea esta forma de trabajo?",
       "Asegurar protección social a trabajadores con horarios flexibles",
       ["Prohibir el uso de bicicletas", "Eliminar las leyes laborales", "Aumentar la jornada de trabajo"],
       "El repartidor señala que no tiene cobertura ante accidentes; la ley busca protegerlo.")]),
]
