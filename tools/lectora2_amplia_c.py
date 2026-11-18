"""Ampliaciones de los textos de Competencia Lectora (parte C). Mismo formato que la parte A."""
L, I, E = "Localizar", "Interpretar", "Evaluar"

AMPLIA = [
{
"titulo": "Los glaciares de Chile",
"amplia": {
1: "El proceso es tan lento que el hielo de algunos glaciares tiene cientos o incluso miles de años. Bajo su propio peso, el glaciar se desplaza muy despacio por las laderas, como un río de hielo, y va desgastando las rocas que encuentra a su paso.",
2: "En la zona central del país, durante los veranos de sequía, una parte importante del caudal de algunos ríos proviene del derretimiento de glaciares de alta montaña. Sin ellos, en esos meses habría mucha menos agua disponible para beber y regar.",
3: "Los científicos estudian estos cambios comparando fotografías tomadas con décadas de diferencia e imágenes de satélite, que muestran glaciares mucho más pequeños que hace cincuenta años. Por eso, distintos especialistas plantean la necesidad de protegerlos y de usar el agua con mayor cuidado.",
},
"nuevas": [
(L, "Según el párrafo 3, ¿cómo estudian los científicos el retroceso de los glaciares?", "Comparando fotografías antiguas y actuales e imágenes de satélite", ["Midiendo la temperatura del mar", "Contando los turistas que los visitan", "Analizando el agua de las ciudades"], "Lo explica el párrafo 3."),
(I, "¿Qué aporta al texto el ejemplo de los ríos de la zona central en verano (párrafo 2)?", "Muestra con un caso concreto por qué los glaciares son reservas de agua importantes", ["Demuestra que los glaciares no sirven en la zona central", "Explica cómo se forma la nieve", "Critica el uso de agua para regar"], "El ejemplo ilustra la idea de los «bancos de agua»."),
],
"reemplaza": {},
},
{
"titulo": "El examen",
"amplia": {
1: "Valentina había hecho resúmenes de cada capítulo, resuelto todos los ejercicios de la guía y preguntado al profesor las dudas que le quedaban. Al oír a sus compañeros, sintió que todo ese esfuerzo de pronto valía menos.",
2: "Pensó en lo que diría su mejor amiga si la viera acusar a alguien frente a todo el curso, y también en lo injusto que era que otros obtuvieran la misma nota sin haber abierto el cuaderno.",
},
"nuevas": [
(L, "Según el párrafo 1, ¿cómo se preparó Valentina para el examen?", "Hizo resúmenes, resolvió la guía y consultó sus dudas al profesor", ["Copió las respuestas de un compañero", "Estudió solo la noche anterior", "Pidió las respuestas por celular"], "Lo detalla el párrafo 1."),
(I, "¿Qué muestran los pensamientos de Valentina en el párrafo 2?", "Su conflicto interno entre la sensación de injusticia y el temor a acusar públicamente", ["Que quería copiar ella también", "Que no le importaba lo que pasaba", "Que estaba segura de que el profesor ya sabía"], "Duda entre lo injusto de la situación y lo que significaría acusar."),
],
"reemplaza": {},
},
{
"titulo": "Normas de uso del laboratorio de computación",
"amplia": {
2: "Los estudiantes que deseen usar el laboratorio en los recreos deberán anotarse previamente en la planilla que se encuentra en la puerta.",
3: "Esta medida protege los teclados y evita que restos de alimentos atraigan insectos.",
4: "Las fallas que no se informen al inicio se considerarán causadas por el último usuario del equipo.",
5: "Si un programa es necesario para una asignatura, el profesor deberá solicitar su instalación a la encargada con al menos una semana de anticipación.",
7: "Antes de aplicar cualquier medida, se escuchará al estudiante involucrado y se informará a su apoderado. Estas normas fueron acordadas por el consejo de profesores y el centro de estudiantes, y rigen durante toda la jornada escolar.",
},
"nuevas": [
(L, "¿Qué debe hacer un profesor si necesita un programa para su asignatura?", "Solicitar su instalación a la encargada con una semana de anticipación", ["Instalarlo él mismo durante la clase", "Pedir que los estudiantes lo instalen", "Comprar un computador nuevo"], "Lo indica la norma 4."),
(I, "Según la norma 3, ¿qué ocurre con las fallas que no se informan al comenzar la clase?", "Se consideran causadas por el último usuario del equipo", ["Se ignoran", "Las repara el centro de estudiantes", "Se cobran a la encargada"], "Lo dice la norma 3."),
],
"reemplaza": {
6: (E, "¿Por qué el párrafo final señala que se escuchará al estudiante antes de aplicar una medida?", "Para asegurar un procedimiento justo antes de sancionar", ["Para que el estudiante elija su castigo", "Para evitar que se cumplan las normas", "Para que los apoderados reparen los equipos"], "Escuchar al involucrado e informar al apoderado garantiza un proceso justo."),
},
},
{
"titulo": "Mujeres en la ciencia: una historia invisible",
"amplia": {
1: "En muchos países, las mujeres solo pudieron estudiar en la universidad a fines del siglo XIX o comienzos del XX, y durante décadas se les impidió dirigir laboratorios o dictar clases.",
2: "También es conocido el caso de la química británica Rosalind Franklin, cuyas imágenes de rayos X fueron decisivas para descubrir la estructura del ADN, aunque durante años su aporte casi no se mencionó.",
3: "Algunos programas escolares ya incluyen biografías de científicas y organizan encuentros entre estudiantes e investigadoras, para que las niñas conozcan modelos cercanos y concretos.",
},
"nuevas": [
(L, "¿Qué aporte de Rosalind Franklin menciona el texto?", "Sus imágenes de rayos X, decisivas para descubrir la estructura del ADN", ["El descubrimiento de la penicilina", "Dos premios Nobel en Física y Química", "La creación de la primera universidad para mujeres"], "Lo dice el párrafo 2."),
(E, "¿Por qué el texto agrega el caso de Rosalind Franklin al de Marie Curie?", "Para reforzar con otro ejemplo la idea de que muchos aportes femeninos no fueron reconocidos", ["Para mostrar que todas las científicas recibieron premios", "Para criticar el trabajo de Marie Curie", "Para explicar cómo funcionan los rayos X"], "Franklin ilustra un aporte decisivo que casi no se mencionó."),
],
"reemplaza": {},
},
{
"titulo": "El regreso de las bicicletas",
"amplia": {
1: "En algunas comunas, los conteos realizados en las principales avenidas muestran que el número de ciclistas se ha duplicado en menos de una década, y el uso aumenta especialmente en primavera y verano.",
2: "En esos tramos, muchos ciclistas optan por usar la vereda, lo que genera conflictos con los peatones. Los urbanistas recomiendan diseñar redes continuas, que conecten barrios, centros de estudio y estaciones de metro.",
3: "Un estacionamiento seguro en una estación de metro, explica, permite que una persona pedalee unos pocos kilómetros y luego continúe su viaje en tren.",
},
"nuevas": [
(L, "Según el párrafo 2, ¿qué hacen muchos ciclistas en los tramos sin ciclovía?", "Usan la vereda, lo que genera conflictos con los peatones", ["Se bajan y toman un taxi", "Circulan por las líneas del metro", "Dejan de usar la bicicleta"], "Lo menciona el párrafo 2."),
(I, "¿Qué ejemplo usa la vocera para explicar que la bicicleta complementa el transporte público?", "Pedalear unos kilómetros, dejar la bicicleta en un estacionamiento seguro y seguir en metro", ["Reemplazar el bus por la bicicleta en todos los viajes", "Subir la bicicleta al techo del bus", "Prohibir los autos en el centro"], "Lo explica en el párrafo 3."),
],
"reemplaza": {
6: (E, "¿Por qué el texto incluye la opinión de la vocera de una agrupación ciclista?", "Para dar a conocer el punto de vista de un actor directamente involucrado", ["Para demostrar que todos los ciclistas opinan igual", "Para promocionar una marca de bicicletas", "Para contradecir los datos del texto"], "Incorporar voces involucradas es propio de un reportaje equilibrado."),
},
},
{
"titulo": "La carta que nunca llegó",
"amplia": {
1: "Había escrito tres borradores antes de decidirse por el definitivo, que terminaba con una pregunta: si ella quería acompañarlo a la fiesta de la primavera. Esperó la respuesta durante semanas, revisando el buzón cada tarde al volver del liceo.",
2: "La bolsa contenía más de doscientas cartas enviadas ese mismo año: saludos de cumpleaños, cuentas, postales de vacaciones. El trabajador las dejó sobre el mesón con cuidado, como si temiera que se deshicieran al tocarlas.",
},
"nuevas": [
(L, "¿Qué le preguntaba Ignacio a Laura al final de su carta?", "Si quería acompañarlo a la fiesta de la primavera", ["Si quería casarse con él", "Por qué se iba al norte", "Si le devolvería un libro"], "Lo dice el párrafo 1."),
(I, "¿Qué revela el detalle de que Ignacio revisaba el buzón «cada tarde» (párrafo 1)?", "Su ilusión y ansiedad por recibir una respuesta", ["Que trabajaba en la oficina de correos", "Que no le interesaba la respuesta", "Que esperaba una cuenta"], "La espera diaria muestra cuánto le importaba la respuesta."),
],
"reemplaza": {},
},
{
"titulo": "¿Por qué el cielo es azul?",
"amplia": {
1: "Esto se puede comprobar con un prisma: al atravesarlo, un rayo de luz blanca se separa en una franja de colores, como ocurre con el arcoíris después de la lluvia.",
2: "Este fenómeno se llama dispersión de Rayleigh, en honor al científico británico que lo explicó en el siglo XIX. Si la luz violeta se dispersa todavía más que la azul, ¿por qué no vemos el cielo violeta? Porque el Sol emite menos luz violeta y porque nuestros ojos son más sensibles al azul.",
3: "Por la misma razón, el Sol se ve más amarillo o anaranjado cuando está cerca del horizonte que cuando está alto en el cielo, al mediodía.",
},
"nuevas": [
(L, "Según el párrafo 2, ¿por qué no vemos el cielo violeta?", "Porque el Sol emite menos luz violeta y nuestros ojos son más sensibles al azul", ["Porque la luz violeta no se dispersa", "Porque el aire absorbe todo el violeta", "Porque el violeta solo existe de noche"], "Lo explica el párrafo 2."),
(I, "¿Qué función cumple la pregunta del párrafo 2 («¿por qué no vemos el cielo violeta?»)?", "Anticipar una duda del lector para luego responderla", ["Mostrar que la explicación anterior es falsa", "Cambiar de tema", "Invitar a hacer un experimento con un prisma"], "El texto plantea la duda y enseguida la responde."),
],
"reemplaza": {},
},
{
"titulo": "Elogio del barrio",
"amplia": {
1: "En la esquina, don Aurelio arregla bicicletas en la puerta de su casa y cobra según lo que cada uno pueda pagar. Los niños aprenden a andar en la calle sin salida, vigilados por todas las ventanas a la vez.",
2: "En el edificio nuevo nadie sabía mi nombre. Saludaba al conserje, pero él cambiaba cada mes. Los primeros meses me sentí libre; después, simplemente solo.",
},
"nuevas": [
(L, "¿Qué hace don Aurelio, según el párrafo 1?", "Arregla bicicletas y cobra según lo que cada uno pueda pagar", ["Atiende el almacén del barrio", "Riega la vereda a las siete de la tarde", "Vigila a los niños desde el columpio"], "Lo cuenta el párrafo 1."),
(I, "¿Qué contraste se establece en la frase «Los primeros meses me sentí libre; después, simplemente solo»?", "El paso del alivio inicial a la soledad por la falta de vínculos", ["El cambio de un trabajo a otro", "La diferencia entre el verano y el invierno", "La alegría de haber dejado para siempre el barrio"], "La libertad del anonimato termina convirtiéndose en soledad."),
],
"reemplaza": {
7: (E, "¿Qué propósito tiene principalmente el texto?", "Compartir una experiencia personal y una reflexión sobre la pertenencia a un lugar", ["Informar sobre los servicios de un barrio", "Convencer de mudarse al centro", "Explicar cómo funciona un almacén"], "El narrador cuenta su experiencia y reflexiona sobre elegir un barrio."),
},
},
{
"titulo": "Tres consejos para preparar una presentación oral",
"amplia": {
1: "No se trata de tener un talento especial: la mayoría de los buenos expositores aprendió con práctica y con algunos trucos sencillos.",
2: "Pregúntate qué saben ya sobre el tema, qué podría interesarles y cuánto tiempo tendrán para escucharte. Un ejemplo cercano a la vida de tu público vale más que una definición complicada.",
3: "Si usas diapositivas, procura que tengan pocas palabras e imágenes claras: deben apoyar lo que dices, no reemplazarte. Leer textos largos en la pantalla aburre a la audiencia y te hace perder contacto con ella.",
4: "El día de la presentación, respira profundo antes de comenzar, mira a distintas personas del público y habla un poco más lento de lo habitual.",
},
"nuevas": [
(L, "Según el texto, ¿cómo deben ser las diapositivas?", "Con pocas palabras e imágenes claras que apoyen lo que se dice", ["Con todo el texto de la presentación", "Con muchos colores y animaciones", "Sin imágenes"], "Lo recomienda el párrafo 3."),
(I, "¿Qué quiere decir que las diapositivas «deben apoyar lo que dices, no reemplazarte»?", "Que el expositor debe seguir siendo el centro de la presentación", ["Que no hay que usar diapositivas", "Que las diapositivas deben leerse completas", "Que otra persona debe exponer"], "Las diapositivas son un apoyo, no un sustituto del expositor."),
],
"reemplaza": {
5: (I, "¿Qué idea expresa la oración «los nervios no desaparecen del todo, pero la preparación ayuda a que no te dominen»?", "La preparación ayuda a controlar los nervios, aunque no los elimine", ["Los nervios desaparecen por completo con práctica", "Es imposible controlar los nervios", "Es mejor no prepararse"], "La oración reconoce que los nervios siguen, pero que prepararse permite manejarlos."),
},
},
{
"titulo": "Las islas de plástico",
"amplia": {
1: "La más conocida se encuentra en el océano Pacífico, entre Hawái y California, y se estima que ocupa una superficie cercana al doble de la de Chile continental, aunque su densidad es muy variable.",
2: "Algunos estudios han detectado microplásticos incluso en la sal de mesa, en el agua potable y en organismos que viven en las zonas más profundas del océano. Los científicos aún investigan qué efectos puede tener esto en la salud humana.",
3: "En Chile, por ejemplo, una ley prohibió la entrega de bolsas plásticas en el comercio, y varias comunas costeras organizan limpiezas de playas con voluntarios. Sin embargo, los especialistas insisten en que la solución de fondo es producir menos plástico de un solo uso.",
},
"nuevas": [
(L, "Según el párrafo 2, ¿dónde se han detectado microplásticos?", "En la sal de mesa, el agua potable y organismos de las profundidades", ["Solo en las playas", "Solo en los ríos", "En los glaciares de Chile"], "Lo menciona el párrafo 2."),
(E, "¿Qué valoración hacen los especialistas de las medidas mencionadas en el párrafo 3?", "Que ayudan, pero que la solución de fondo es producir menos plástico de un solo uso", ["Que son la solución definitiva", "Que son inútiles y deben eliminarse", "Que solo sirven en el océano Pacífico"], "El párrafo 3 termina con esa advertencia."),
],
"reemplaza": {},
},
]
