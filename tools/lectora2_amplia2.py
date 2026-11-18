"""Segunda ampliación de los textos de Competencia Lectora: más oraciones al final de párrafos
existentes (título -> {número de párrafo: texto}). No se toca el último párrafo de los cuentos ni
de los textos cuyas preguntas aluden a su final, para que todas las preguntas sigan siendo válidas.
"""

AMPLIA2 = {
"¿Prohibir los celulares en la sala de clases?": {
1: "En Chile, varios colegios ya han probado distintas fórmulas, y el debate suele reaparecer cada vez que se conoce un caso de ciberacoso.",
},
"La última función": {
2: "Afuera llovía, y el ruido del agua sobre el techo de calamina se mezclaba con la música de los créditos iniciales.",
},
"¿Por qué bostezamos?": {
3: "Por eso, algunos estudios han comparado a personas con distinta capacidad empática para ver si se contagian con la misma facilidad.",
},
"Carta al director: el paradero olvidado": {
2: "Además, el letrero con los recorridos fue arrancado, de modo que quienes no conocen el sector ni siquiera saben qué buses se detienen allí.",
3: "Incluso acudimos a una sesión del concejo municipal, donde un concejal prometió visitar el lugar; esa visita nunca se concretó.",
},
"Entrevista a una guardaparques": {
2: "Llevo siempre una radio, un botiquín y una libreta donde anoto todo lo que observo.",
3: "Por eso, parte de mi trabajo es conversar con los visitantes, explicarles las reglas y, cuando es necesario, multar a quienes no las respetan.",
},
"Comer insectos: ¿el alimento del futuro?": {
3: "Otros recuerdan que no todos los insectos son comestibles y que algunos deben cocinarse para eliminar microorganismos.",
},
"Mi primer día de trabajo": {
3: "Me aprendí de memoria los precios, inventé un orden para guardar las monedas en la caja y descubrí que los niños siempre piden probar tres sabores antes de elegir el de siempre.",
},
"Las abejas en peligro": {
2: "En algunos países, los apicultores han perdido en un solo invierno hasta un tercio de sus colmenas.",
3: "También es útil dejar en el jardín un pequeño recipiente con agua y piedras, donde las abejas puedan beber sin ahogarse.",
},
"Reseña: «El faro del fin del mundo»": {
2: "Mena también alterna las escenas del presente con recuerdos de la infancia de Julián en una ciudad ruidosa, un contraste que vuelve aún más intenso el silencio de la isla.",
},
"Discurso de fin de año": {
3: "Hubo días en que conectarse a una clase desde un teléfono compartido con tres hermanos parecía imposible.",
4: "Don Raúl, que nos saludaba por nuestro nombre aunque fuéramos cientos, y la profesora que se quedaba después de clases para resolver dudas son parte de lo que hoy celebramos.",
},
"El valor de equivocarse": {
2: "Hasta los grandes inventores llenaban cuadernos con intentos fallidos antes de lograr un resultado.",
},
"El origen del ajedrez": {
3: "En Chile, numerosos clubes y colegios organizan torneos escolares cada año.",
},
"El perro que esperaba el tren": {
2: "Un vecino recuerda que, cuando el ferroviario regresaba cada tarde, Canelo corría a recibirlo moviendo la cola desde que oía el pitazo.",
3: "Cuando el tren se atrasa, algunos pasajeros se acercan a acariciarlo y le conversan, como si él también estuviera aguardando a alguien.",
},
"La comida chatarra y la publicidad infantil": {
2: "Diversos estudios han mostrado que la publicidad influye en lo que los niños piden a sus padres en el supermercado.",
3: "Además, la información en los envases también sirve a los adultos, que muchas veces desconocen cuánta azúcar tiene un producto.",
},
"La señora del tercer piso": {
1: "Una vez, desde el pasillo, creyó ver por una rendija una mesa llena de herramientas y pequeñas cabezas de madera, y salió corriendo sin mirar atrás.",
2: "Tomás, sentado en la escalera, no se atrevió a acercarse hasta que el dragón le guiñó un ojo.",
},
"El agua que no vemos": {
1: "Esta agua no sale de nuestra llave, pero sí de ríos, lagos y napas subterráneas de los lugares donde se fabrican los productos.",
2: "En una hamburguesa, por ejemplo, se suma el agua del pan, de las verduras y, sobre todo, la de la carne.",
3: "Algunas empresas ya calculan la huella hídrica de sus productos y la informan a los consumidores.",
},
"Los videojuegos y el aprendizaje": {
1: "Estas investigaciones no afirman que todos los juegos sean buenos, sino que conviene distinguir entre ellos.",
2: "En otros juegos, el jugador debe leer instrucciones, interpretar mapas o tomar decisiones con información incompleta, tareas que también se exigen en la vida escolar.",
3: "Los especialistas también recuerdan que jugar en familia puede ser una buena oportunidad para conversar.",
},
"Una feria libre en peligro": {
2: "La municipalidad también señaló que en los últimos meses ha recibido reclamos de vecinos por los ruidos y la basura que quedan al terminar la jornada.",
3: "Otra comerciante, que vende pescado, explicó que el nuevo terreno queda junto a una avenida de alto tráfico y sin sombra para los puestos.",
},
"El arte de no hacer nada": {
1: "Incluso en las conversaciones con amigos, cada vez más gente revisa el teléfono cada pocos minutos, como si estar desconectado un rato fuera una pérdida.",
2: "Algunos estudios sobre creatividad muestran que, después de una actividad aburrida y sin exigencias, las personas proponen ideas más originales. La mente divaga, y en ese aparente desorden realiza una de sus tareas más valiosas. No es casual que muchas culturas hayan valorado la siesta, el paseo sin rumbo o la conversación lenta en la plaza.",
},
"Los glaciares de Chile": {
1: "En Chile hay glaciares desde la zona norte hasta Magallanes, y los de los Campos de Hielo Patagónicos se cuentan entre los más extensos fuera de las regiones polares.",
2: "Además, los glaciares influyen en la temperatura y la humedad de los valles cercanos.",
},
"El examen": {
1: "Era la última prueba del semestre y de ella dependía que pudiera postular al taller de ciencias que tanto quería. Su hermano mayor le había dicho una vez que estudiar de verdad era como ahorrar: nadie podía quitarle lo aprendido.",
2: "El reloj de la sala avanzaba más lento que nunca.",
},
"Normas de uso del laboratorio de computación": {
3: "Las botellas de agua deben dejarse en el estante ubicado junto a la entrada.",
6: "Los archivos guardados en el escritorio del computador se borran automáticamente cada viernes; por eso, cada estudiante debe guardar sus trabajos en su cuenta o en un dispositivo propio.",
},
"Mujeres en la ciencia: una historia invisible": {
2: "Durante mucho tiempo, los libros de texto mencionaron casi exclusivamente a científicos hombres, lo que reforzó la idea de que la ciencia era una actividad masculina.",
3: "En Chile, la proporción de mujeres en carreras como ingeniería ha aumentado en las últimas décadas, aunque todavía está lejos de la mitad.",
},
"El regreso de las bicicletas": {
1: "Muchos ciclistas destacan, además, que pedalear les permite llegar más despiertos y de mejor ánimo.",
3: "Las autoridades de transporte, por su parte, estudian permitir el ingreso de bicicletas plegables a los vagones fuera de las horas punta.",
},
"La carta que nunca llegó": {
1: "Laura era la mejor alumna de Castellano y siempre leía en voz alta los textos del curso; Ignacio pensó que una carta escrita con cuidado sería la única forma de acercarse a ella.",
2: "El jefe de correos, recién llegado al pueblo, pasó la tarde leyendo los nombres de los destinatarios y descubrió que reconocía algunos apellidos de los vecinos más antiguos.",
},
"¿Por qué el cielo es azul?": {
1: "Nuestros ojos perciben esa mezcla como luz blanca porque reciben todos los colores al mismo tiempo.",
2: "Un fenómeno parecido explica por qué las montañas lejanas se ven azuladas.",
3: "En días con mucho polvo o humo en el aire, los atardeceres pueden ser todavía más intensos.",
},
"Elogio del barrio": {
1: "Los viernes, el olor a pan amasado sale de la casa de la esquina, y en invierno las vecinas se turnan para llevarle sopa a don Aurelio, que vive solo.",
2: "Cuando llegaba tarde, el vecino del frente dejaba encendida la luz de su patio hasta verme entrar.",
},
"Tres consejos para preparar una presentación oral": {
2: "Si es posible, averigua cuánto tiempo tendrás y si habrá preguntas al final.",
},
"Las islas de plástico": {
1: "Los científicos que han navegado por esas zonas describen el agua como una «sopa» de pequeños trozos de colores.",
2: "Las tortugas marinas, por ejemplo, pueden confundir una bolsa plástica con una medusa, uno de sus alimentos.",
},
"Mi abuelo y la radio": {
1: "Mi abuela decía que era su manera de viajar sin moverse de la silla.",
2: "Esas conversaciones duraban a veces más que el programa. Con los años entendí que su casa de adobe era la de su propia infancia, en un campo del sur.",
},
"Reducir la jornada laboral: ¿un beneficio para todos?": {
1: "Antes de esta ley, Chile tenía una de las jornadas legales más largas entre los países de la OCDE.",
2: "En algunos rubros, como el comercio o la salud, los turnos ya son complejos de organizar.",
3: "También será importante evaluar los resultados en cada etapa y corregir lo que no funcione.",
},
"Una vacuna, muchas protecciones": {
2: "Por eso, una persona vacunada puede contagiarse en algunos casos, pero suele presentar síntomas más leves.",
3: "Vacunarse, entonces, es una decisión que también protege a los demás.",
},
"El festival que salvó un pueblo": {
1: "La plaza, que habitualmente está casi vacía, se llenó de familias, y los dos únicos restaurantes del pueblo tuvieron que contratar ayuda extra.",
2: "La cooperativa que agrupa a los productores pasó de doce a cuarenta socios en tres años.",
},
"Cómo leer una etiqueta nutricional": {
2: "Muchas veces un paquete contiene varias porciones, aunque parezca para una sola persona.",
3: "Los sellos se ubican en la parte frontal del envase para que puedan verse con facilidad.",
},
"El arte callejero: ¿vandalismo o expresión?": {
1: "Los municipios gastan cada año una parte de su presupuesto en limpiar fachadas y monumentos.",
2: "Algunos murales chilenos incluso han sido reconocidos internacionalmente y aparecen en guías turísticas.",
3: "Los artistas también tienen una responsabilidad: respetar el patrimonio y los espacios que la comunidad quiere conservar.",
},
"La primera nevada": {
1: "Su padre había conseguido trabajo en una central hidroeléctrica y la casa nueva tenía una chimenea que Martina nunca había visto encendida.",
2: "Una compañera, Ignacia, le prestó unos guantes de lana «para cuando llegue tu famosa nieve», y Martina los llevó en el bolsillo de su chaqueta todos los días.",
},
"El sueño adolescente": {
1: "En los niños, en cambio, la melatonina suele aumentar más temprano en la noche.",
2: "Algunos estudiantes reconocen quedarse dormidos en las primeras clases de la mañana.",
3: "Las familias también pueden ayudar evitando discusiones o tareas pesadas justo antes de acostarse.",
},
"El valor del patrimonio cotidiano": {
1: "También lo son las fiestas de un pueblo, los cantos de trabajo o el modo de preparar el pan en un horno de barro.",
3: "Un teléfono basta para grabar una entrevista y guardarla para las próximas generaciones.",
},
"La biblioteca de los objetos perdidos": {
1: "El estante está al fondo, detrás de los diccionarios, y tiene una cortina verde que la bibliotecaria corre cada mañana.",
2: "Cuando alguien reconoce algo suyo, ella le pide que cuente cómo lo perdió antes de devolvérselo, y anota la historia en un cuaderno.",
},
}
