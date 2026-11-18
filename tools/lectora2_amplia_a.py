"""Ampliaciones de los textos de Competencia Lectora (parte A).

Para acercar los textos al largo de la prueba real, se agregan oraciones AL FINAL de párrafos
existentes ("amplia": número de párrafo -> texto agregado). No se agregan párrafos nuevos ni se
borra nada, así las preguntas que citan un párrafo o el final del texto siguen siendo válidas.
"nuevas": preguntas nuevas. "reemplaza": índice de pregunta -> pregunta que la reemplaza
(se usa para quitar preguntas fuera del temario, como «¿Qué tipo de texto es?").
Formato de pregunta: (habilidad, enunciado, correcta, [3 incorrectas], explicación)
"""
L, I, E = "Localizar", "Interpretar", "Evaluar"

AMPLIA = [
{
"titulo": "El huerto que unió a una población",
"amplia": {
1: "Durante más de diez años, el terreno había sido un problema para el barrio: se acumulaban neumáticos, colchones y escombros, y por las noches nadie se atrevía a pasar por la vereda del frente. Las vecinas tardaron tres fines de semana en sacar la basura, que llenó dos camiones.",
2: "En las parcelas crecen lechugas, habas, cilantro, zapallos y, por supuesto, frutillas. Las familias acordaron no usar productos químicos y comparten las semillas que guardan de cada temporada. Quien no puede asistir a su turno avisa por un grupo de mensajería y otro vecino lo reemplaza.",
3: "Los sábados por la tarde, adultos mayores que trabajaron en el campo enseñan a los jóvenes a preparar almácigos y a reconocer las plagas. En septiembre se celebró la primera fiesta de la cosecha, con música y una feria donde se intercambiaron verduras por pan amasado y mermeladas.",
4: "Los organizadores también esperan que la experiencia inspire a otras poblaciones de Valle Alto, donde todavía hay varios sitios abandonados. «Si nosotras pudimos, cualquiera puede», resume Rosa Pérez.",
},
"nuevas": [
(L, "Según el texto, ¿qué acordaron las familias sobre el cultivo?", "No usar productos químicos y compartir las semillas", ["Vender toda la cosecha a la municipalidad", "Cultivar solo frutillas", "Contratar a un jardinero"], "Lo dice el párrafo 2."),
(I, "¿Qué función cumple la descripción del terreno en el párrafo 1?", "Mostrar cuán grande fue el cambio al contrastar el pasado del sitio con el huerto actual", ["Criticar a los camiones de basura", "Explicar cómo se cultivan las habas", "Informar el número de familias participantes"], "Describir neumáticos, escombros e inseguridad resalta la transformación."),
],
"reemplaza": {
7: (E, "¿Cuál es el propósito principal del texto?", "Informar sobre una iniciativa vecinal y sus efectos en la comunidad", ["Convencer a la municipalidad de cerrar el huerto", "Enseñar paso a paso a cultivar frutillas", "Narrar una historia inventada para entretener"], "El texto entrega datos, testimonios y planes sobre el huerto."),
},
},
{
"titulo": "¿Prohibir los celulares en la sala de clases?",
"amplia": {
1: "Cualquier profesor ha visto a un estudiante mirar la pantalla por debajo del banco, y los padres saben lo difícil que es separar a un adolescente de su teléfono.",
2: "También permite que un estudiante con dificultades de lectura escuche un texto en voz alta o que otro que faltó a clases revise las tareas en la plataforma del colegio. Ignorar estos usos significa castigar a todos por la conducta de algunos.",
3: "En una de ellas, los estudiantes de cada curso votaron las normas a comienzo de año y eligieron a dos compañeros para revisar su cumplimiento cada mes. Las reglas que uno ayuda a crear son más fáciles de respetar que las impuestas desde arriba.",
4: "Prohibir puede dar tranquilidad por un tiempo, pero educar es una tarea más lenta y, a la larga, más útil.",
},
"nuevas": [
(L, "¿Qué ejemplo da el autor de una escuela que construyó reglas con sus estudiantes?", "Los estudiantes votaron las normas y eligieron compañeros para revisar su cumplimiento", ["La dirección prohibió los celulares sin consultar", "Los padres retiraron los teléfonos en la entrada", "Se instaló una señal que bloquea internet"], "Lo cuenta el párrafo 3."),
(E, "¿Qué efecto busca el autor al mencionar a un estudiante con dificultades de lectura (párrafo 2)?", "Mostrar que una prohibición total también afectaría usos valiosos del celular", ["Demostrar que el celular causa problemas de lectura", "Criticar a los estudiantes que faltan a clases", "Proponer que solo algunos estudiantes usen celular"], "El ejemplo apoya su idea de que prohibir castiga a todos por la conducta de algunos."),
],
"reemplaza": {},
},
{
"titulo": "La última función",
"amplia": {
1: "En la caseta de la boletería todavía colgaba el afiche de la primera película que había proyectado, amarillento y con las esquinas dobladas. Durante la semana había llegado una carta del dueño anunciando que el edificio sería demolido para construir estacionamientos.",
2: "Los ancianos se tomaban de la mano, igual que tantas parejas que don Ernesto había visto envejecer en esas mismas butacas. Los estudiantes reían bajito y compartían una bolsa de maní. La niña, en cambio, no apartaba los ojos de la pantalla ni para comer.",
3: "La luz de la salida iluminaba la mitad de su cara, y don Ernesto pensó que tenía la misma mirada de asombro que él tuvo a su edad, cuando su padre lo llevó a ver su primera película en esa sala.",
4: "Después, don Ernesto apagó la última lámpara, cerró la puerta con llave y caminó hacia la parada del bus sin mirar atrás.",
},
"nuevas": [
(L, "Según el texto, ¿qué pasará con el edificio del cine?", "Será demolido para construir estacionamientos", ["Será convertido en un museo", "Se transformará en un teatro", "Lo comprará don Ernesto"], "Lo dice la carta del dueño, en el párrafo 1."),
(I, "¿Qué relación establece don Ernesto entre la niña y su propia infancia (párrafo 3)?", "Ve en ella el mismo asombro que él sintió al ver su primera película", ["Cree que la niña es su nieta", "Piensa que la niña le recuerda a su padre", "Considera que la niña no entiende el cine"], "Piensa que tiene «la misma mirada de asombro» que él tuvo a su edad."),
],
"reemplaza": {},
},
{
"titulo": "¿Por qué bostezamos?",
"amplia": {
1: "Esa idea, que parecía lógica, se repitió durante décadas en libros y conversaciones cotidianas. El experimento, sin embargo, mostró que una explicación intuitiva no siempre es correcta y que las creencias deben ponerse a prueba.",
2: "Para comprobarlo, un equipo de investigadores observó que las personas bostezaban menos cuando sostenían una compresa fría en la frente y más cuando la compresa estaba tibia. Aunque el resultado apoya la hipótesis, sus autores advierten que se necesitan más estudios con grupos más grandes.",
3: "El contagio no es exclusivo de los seres humanos: también se ha observado en chimpancés y en perros, que pueden bostezar al ver bostezar a sus dueños. Curiosamente, los niños pequeños, que todavía están desarrollando la capacidad de ponerse en el lugar de otros, rara vez se contagian antes de los cuatro o cinco años.",
},
"nuevas": [
(L, "¿Qué resultado apoya la hipótesis de que el bostezo enfría el cerebro?", "Las personas bostezaban menos con una compresa fría en la frente que con una tibia", ["Los niños pequeños bostezaban más que los adultos", "Respirar más oxígeno aumentaba los bostezos", "Los perros bostezaban al ver a desconocidos"], "Lo describe el párrafo 2."),
(E, "¿Por qué es importante que los autores del experimento adviertan que «se necesitan más estudios»?", "Porque muestran que un resultado no basta para dar por comprobada una hipótesis", ["Porque reconocen que su experimento fue un fracaso", "Porque quieren desacreditar a otros investigadores", "Porque el bostezo no puede estudiarse científicamente"], "La advertencia muestra prudencia científica: la hipótesis aún debe confirmarse."),
],
"reemplaza": {},
},
{
"titulo": "Carta al director: el paradero olvidado",
"amplia": {
2: "Cerca del paradero funcionan un consultorio y un liceo, por lo que cada mañana decenas de personas lo usan. La semana pasada, una vecina de ochenta años resbaló en el charco que se forma bajo el techo roto y debió ser atendida en urgencias.",
3: "Uno de esos reclamos fue ingresado con fotografías y con la firma de más de cien vecinos. En la última respuesta se nos indicó que el paradero «no está incluido en el plan de mantención del presente año», sin explicar cuándo lo estará.",
4: "Si las autoridades no pueden hacerlo de inmediato, al menos merecemos saber en qué plazo se hará.",
},
"nuevas": [
(L, "Según la carta, ¿qué le ocurrió a una vecina la semana pasada?", "Resbaló en el charco bajo el techo roto y fue atendida en urgencias", ["La asaltaron en el paradero de noche", "Un bus no se detuvo en el paradero", "Recibió una respuesta de la municipalidad"], "Lo relata el párrafo 2."),
(E, "¿Qué efecto busca la autora al citar la respuesta «no está incluido en el plan de mantención del presente año»?", "Mostrar que la municipalidad evade el problema sin dar una solución ni un plazo", ["Demostrar que el paradero ya fue reparado", "Felicitar a la municipalidad por su planificación", "Explicar cómo funciona el plan de mantención"], "La cita apoya su crítica a respuestas que no resuelven nada."),
],
"reemplaza": {},
},
{
"titulo": "Entrevista a una guardaparques",
"amplia": {
1: "Antes de llegar al parque estudió técnico forestal y trabajó dos temporadas en un vivero de especies nativas.",
2: "En verano, cuando llegan más visitantes, también dicto charlas en el centro de informaciones y reviso que los campamentos estén en los lugares autorizados. En invierno, en cambio, la nieve cierra algunos caminos y el trabajo se vuelve más solitario.",
3: "Hace tres años, una fogata mal apagada quemó cerca de cuarenta hectáreas de bosque. Todavía hoy, cuando paso por ese sector, veo troncos negros donde antes había coihues de más de veinte metros.",
4: "Y que recuerde que no es un visitante en un lugar vacío: aquí viven pumas, huemules y cientos de especies de aves que necesitan silencio y respeto.",
},
"nuevas": [
(L, "Según Camila, ¿qué causó el incendio de hace tres años?", "Una fogata mal apagada", ["Un rayo durante una tormenta", "La basura que dejaron los turistas", "Un accidente de un vehículo"], "Lo cuenta en su respuesta del párrafo 3."),
(E, "¿Qué aporta al texto el relato del incendio en la respuesta de Camila?", "Un ejemplo concreto que respalda su preocupación por los descuidos de los visitantes", ["Una crítica a los bomberos de la zona", "Información sobre cómo hacer una fogata", "Una prueba de que el parque está cerrado"], "El incendio ilustra cómo un descuido destruye en horas el bosque."),
],
"reemplaza": {
6: (E, "¿Para qué incluye el entrevistador las preguntas en el texto?", "Para guiar la conversación hacia los temas que quiere dar a conocer al lector", ["Para examinar los conocimientos de Camila", "Para contradecir las respuestas de la entrevistada", "Para narrar una historia inventada"], "Las preguntas organizan la entrevista en temas: su día, lo difícil y sus consejos."),
},
},
{
"titulo": "Comer insectos: ¿el alimento del futuro?",
"amplia": {
1: "En México, por ejemplo, los chapulines tostados con limón se venden en mercados y estadios, y en Tailandia los grillos fritos son un bocadillo común en la calle.",
2: "Para producir un kilo de proteína de grillo se necesita una fracción del alimento que requiere un kilo de proteína de vacuno, porque los insectos aprovechan mejor lo que comen. Algunos criaderos incluso alimentan a las larvas con restos de frutas y verduras que, de otro modo, terminarían en la basura.",
3: "Una encuesta realizada en una ciudad europea mostró que la mayoría de los consultados estaría dispuesta a probar un producto con insectos, pero solo una minoría lo compraría de manera habitual.",
4: "Los fabricantes apuestan a que, con el tiempo, el rechazo inicial disminuya, como ocurrió con otros alimentos que hace décadas parecían extraños y hoy son comunes.",
},
"nuevas": [
(L, "Según el texto, ¿con qué alimentan algunos criaderos a las larvas?", "Con restos de frutas y verduras que terminarían en la basura", ["Con harina de grillo", "Con carne de vacuno", "Con alimento importado de Asia"], "Lo menciona el párrafo 2."),
(I, "¿Qué muestra la encuesta mencionada en el párrafo 3?", "Que existe una distancia entre la curiosidad por probar y el hábito de consumir insectos", ["Que nadie en Europa probaría insectos", "Que la mayoría ya come insectos todos los días", "Que los insectos son más caros que la carne"], "Muchos probarían, pero pocos los comprarían de forma habitual."),
],
"reemplaza": {},
},
{
"titulo": "Mi primer día de trabajo",
"amplia": {
1: "El cliente, un hombre alto con camisa blanca, me miró en silencio mientras yo pedía perdón con la cara roja. Pensé que esa misma tarde me iban a despedir.",
2: "Después me mostró un pequeño cuaderno donde ella misma había anotado, cuarenta años atrás, los errores de su primer verano detrás del mostrador.",
3: "También aprendí que un helado se sirve más rápido si se prepara la máquina antes de abrir y que una broma a tiempo calma a un cliente impaciente.",
4: "Algunos me miran con la misma cara de susto que tenía yo aquel día; otros se ríen, y entonces sé que entendieron.",
},
"nuevas": [
(L, "¿Qué le mostró la señora Inés al narrador después de pasarle el paño?", "Un cuaderno con los errores de su propio primer verano", ["Una lista de los clientes frecuentes", "El contrato de trabajo del narrador", "Una receta de helado de chocolate"], "Lo cuenta el párrafo 2."),
(I, "¿Qué buscaba la señora Inés al mostrarle su cuaderno?", "Que el narrador viera que ella también se había equivocado al comenzar", ["Que el narrador anotara los vueltos", "Que el narrador renunciara", "Que el narrador memorizara las recetas"], "El cuaderno muestra que equivocarse al inicio es normal."),
],
"reemplaza": {},
},
{
"titulo": "Las abejas en peligro",
"amplia": {
1: "Se estima que una gran parte de las especies de plantas con flor depende, en alguna medida, de animales polinizadores, y las abejas son los más importantes entre ellos. Sin su trabajo, muchos alimentos serían más escasos y más caros.",
2: "Estos factores se refuerzan entre sí: una colonia debilitada por la falta de alimento resiste peor a los parásitos, y los cambios en las temperaturas alteran la época en que florecen las plantas, de modo que las abejas a veces salen a buscar néctar cuando todavía no hay flores.",
3: "En algunas ciudades, además, se han creado «corredores de polinizadores»: franjas de plazas, jardines y techos verdes con flores que se suceden a lo largo del año, para que las abejas encuentren alimento en cada estación.",
},
"nuevas": [
(L, "¿Qué son los «corredores de polinizadores», según el texto?", "Franjas de plazas, jardines y techos verdes con flores durante todo el año", ["Caminos por donde se trasladan las colmenas en camión", "Zonas donde se prohíbe la entrada de abejas", "Cultivos de almendras en el campo"], "Lo explica el párrafo 3."),
(I, "Según el párrafo 2, ¿por qué los cambios de temperatura perjudican a las abejas?", "Porque alteran la época de floración y las abejas salen cuando aún no hay flores", ["Porque el calor derrite la miel de las colmenas", "Porque el frío mata a todas las abejas", "Porque aumentan las flores silvestres"], "El texto explica el desajuste entre la floración y la búsqueda de néctar."),
],
"reemplaza": {
6: (E, "¿Cuál es el propósito principal del texto?", "Explicar la importancia de las abejas, las causas de su disminución y cómo ayudarlas", ["Convencer al lector de no comer miel", "Narrar la historia de un apicultor", "Criticar a quienes plantan flores nativas"], "El texto informa sobre la polinización, las causas del problema y acciones posibles."),
},
},
{
"titulo": "Reseña: «El faro del fin del mundo»",
"amplia": {
1: "Al principio, Julián lleva un diario donde anota la dirección del viento y los barcos que pasan; con el correr de los días, esas anotaciones se transforman en cartas a una hermana que no sabe si volverá a ver.",
2: "La autora evita los adjetivos excesivos y prefiere detalles concretos: el sonido de la lámpara al girar, la sal que se pega en los vidrios, el pan que se endurece. Esa sobriedad hace que los momentos de angustia del protagonista resulten creíbles.",
3: "Tampoco ayuda que la hermana, tan presente en las cartas, nunca llegue a tener voz propia en la historia. Pese a estos reparos, se trata de un debut prometedor, y será interesante ver qué escribe Mena en el futuro.",
},
"nuevas": [
(L, "Según la reseña, ¿en qué se transforman las anotaciones del diario de Julián?", "En cartas a una hermana", ["En un mapa de la isla", "En un informe para la marina", "En una novela de aventuras"], "Lo dice el párrafo 1."),
(E, "¿Qué opina el reseñista sobre el estilo de la autora en el párrafo 2?", "Que su sobriedad y sus detalles concretos hacen creíble la angustia del protagonista", ["Que usa demasiados adjetivos", "Que sus descripciones son confusas", "Que el estilo no tiene importancia en la novela"], "Valora que evite adjetivos excesivos y prefiera detalles concretos."),
],
"reemplaza": {},
},
]
