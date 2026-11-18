"""Preguntas de habilidades científicas (temario oficial: observar y plantear preguntas,
planificar y conducir una investigación, procesar y analizar la evidencia, evaluar).

Cada experimento ficticio genera 5 preguntas: variable independiente, variable dependiente,
variable controlada, pregunta de investigación y conclusión.
"""
from ciencias_comun import AMB, ATO, ELE, EST, HER, MEC, OND, PROC, make, rnd

# Cada experimento: área, descripción, variable independiente, variable dependiente,
# variables controladas, resultado, conclusión correcta, conclusiones incorrectas.
EXPERIMENTOS = [
    (AMB, "Un grupo de estudiantes ilumina tres ramas iguales de Elodea (planta acuática) con luz roja, azul y verde, a la misma distancia y en agua a la misma temperatura. Cuentan las burbujas de oxígeno que libera cada rama en 5 minutos.",
     "El color de la luz", "El número de burbujas de oxígeno liberadas", ["La temperatura del agua", "La distancia de la lámpara", "El tamaño de las ramas"],
     "Con luz verde se liberaron muchas menos burbujas que con luz roja o azul.",
     "La luz verde es menos eficaz para la fotosíntesis de la Elodea que la roja y la azul",
     ["La luz verde es la más eficaz para la fotosíntesis", "El color de la luz no afecta la fotosíntesis",
      "La temperatura del agua fue la causa de la diferencia"]),
    (AMB, "Se colocan hojas iguales de espinaca en cuatro vasos con agua que contienen distintas cantidades de bicarbonato (fuente de CO₂): 0 g, 1 g, 2 g y 3 g. Todos los vasos reciben la misma luz y están a 25 °C. Se mide el tiempo que tardan las hojas en flotar, lo que indica producción de oxígeno.",
     "La cantidad de bicarbonato (CO₂ disponible)", "El tiempo que tardan las hojas en flotar", ["La intensidad de la luz", "La temperatura del agua", "El tipo de hoja"],
     "Mientras más bicarbonato había en el vaso, menos tiempo tardaron las hojas en flotar.",
     "Al aumentar el CO₂ disponible aumenta la rapidez de la fotosíntesis",
     ["El CO₂ disminuye la rapidez de la fotosíntesis", "La luz fue la única causa de la diferencia",
      "Las hojas flotan porque pierden masa al respirar"]),
    (AMB, "Se preparan tubos con la misma cantidad de levadura, agua y azúcar, y se ponen a 10 °C, 25 °C y 40 °C. Después de 20 minutos se mide la altura de la espuma de CO₂ que se forma en cada tubo.",
     "La temperatura", "La cantidad de CO₂ producido (altura de la espuma)", ["La cantidad de azúcar", "La cantidad de levadura", "El tiempo de medición"],
     "A 40 °C se formó más espuma que a 25 °C, y a 10 °C casi no se formó espuma.",
     "En ese rango, al aumentar la temperatura aumenta la producción de CO₂ de la levadura",
     ["La levadura produce más CO₂ con el frío", "La temperatura no influye en la levadura",
      "El azúcar fue la variable que se modificó"]),
    (PROC, "Para estudiar el efecto de la cafeína, 30 estudiantes que durmieron 8 horas realizan una prueba de reacción (atrapar una regla que cae) a la misma hora. La mitad toma una bebida con cafeína y la otra mitad una bebida igual sin cafeína. Se mide el tiempo de reacción de cada uno.",
     "El consumo de cafeína", "El tiempo de reacción", ["Las horas de sueño", "La hora de la prueba", "El tipo de prueba"],
     "El grupo que tomó cafeína tuvo, en promedio, un tiempo de reacción menor.",
     "En estas condiciones, la cafeína disminuyó el tiempo de reacción",
     ["La cafeína aumentó el tiempo de reacción", "Las horas de sueño causaron la diferencia",
      "La cafeína no tiene ningún efecto sobre el sistema nervioso"]),
    (PROC, "Un investigador forma tres grupos de jóvenes que, durante una semana, duermen 5, 7 y 9 horas por noche. Al final, todos rinden la misma prueba de memoria a la misma hora y en la misma sala. Se registra el puntaje de cada grupo.",
     "Las horas de sueño", "El puntaje en la prueba de memoria", ["El tipo de prueba", "La hora de la prueba", "El lugar de la prueba"],
     "El grupo que durmió 9 horas obtuvo el mayor puntaje y el de 5 horas, el menor.",
     "Dormir más horas se asoció a un mejor rendimiento en la prueba de memoria",
     ["Dormir menos mejora la memoria", "El lugar de la prueba explica las diferencias",
      "El sueño no tiene relación con la memoria"]),
    (HER, "Se cultivan bacterias de una misma cepa en placas con 0, 2, 4 y 8 unidades de un antibiótico, a la misma temperatura y con el mismo medio de cultivo. Después de 24 horas se cuenta el número de colonias en cada placa.",
     "La concentración del antibiótico", "El número de colonias de bacterias", ["La temperatura", "El tipo de medio de cultivo", "El tiempo de incubación"],
     "Al aumentar la concentración del antibiótico disminuyó el número de colonias, pero en la placa con 8 unidades aún crecieron algunas.",
     "Algunas bacterias de la población eran resistentes al antibiótico",
     ["El antibiótico no tuvo efecto sobre las bacterias", "Las bacterias se volvieron resistentes porque quisieron",
      "La temperatura fue la causa de la disminución de colonias"]),
    (MEC, "Un estudiante tira de un carrito con un dinamómetro aplicando siempre la misma fuerza neta de 10 N sobre una superficie lisa. En cada ensayo le agrega más masa al carrito (1, 2, 4 y 5 kg) y mide su aceleración.",
     "La masa del carrito", "La aceleración del carrito", ["La fuerza aplicada", "El tipo de superficie", "El modelo de carrito"],
     "La aceleración fue 10, 5, 2,5 y 2 m/s², respectivamente.",
     "Con fuerza neta constante, la aceleración es inversamente proporcional a la masa",
     ["La aceleración aumenta al aumentar la masa", "La aceleración no depende de la masa",
      "La fuerza aplicada fue cambiando en cada ensayo"]),
    (MEC, "Se arrastra el mismo bloque de madera, a velocidad constante, sobre vidrio, madera y lija. Se mide con un dinamómetro la fuerza necesaria en cada superficie.",
     "El tipo de superficie", "La fuerza necesaria para arrastrar el bloque", ["La masa del bloque", "La velocidad del arrastre", "El dinamómetro usado"],
     "Sobre lija se necesitó la mayor fuerza y sobre vidrio, la menor.",
     "La fuerza de roce cinético depende de las superficies en contacto",
     ["El roce es igual en todas las superficies", "La masa del bloque cambió en cada ensayo",
      "Sobre vidrio el roce es mayor que sobre lija"]),
    (ELE, "Se conectan alambres de nicrom del mismo grosor y de 10, 20, 40 y 80 cm de largo a una misma pila de 3 V. En cada caso se mide la corriente con un amperímetro.",
     "El largo del alambre", "La intensidad de corriente", ["El voltaje de la pila", "El material del alambre", "El grosor del alambre"],
     "Al duplicar el largo del alambre, la corriente se redujo aproximadamente a la mitad.",
     "La resistencia del alambre aumenta con su largo",
     ["La resistencia disminuye al aumentar el largo", "El largo no influye en la corriente",
      "La corriente cambió porque se usaron pilas distintas"]),
    (OND, "Se hace incidir un rayo láser desde el aire sobre un bloque de acrílico con ángulos de incidencia de 20°, 40° y 60°. Para cada caso se mide el ángulo de refracción dentro del bloque, usando siempre el mismo láser y el mismo bloque.",
     "El ángulo de incidencia", "El ángulo de refracción", ["El color del láser", "El material del bloque", "La forma del bloque"],
     "En los tres casos el ángulo de refracción fue menor que el de incidencia, y aumentó al aumentar el de incidencia.",
     "Al entrar al acrílico la luz se acerca a la normal",
     ["La luz no cambia de dirección al entrar al acrílico", "La luz se aleja de la normal al entrar al acrílico",
      "El color del láser causó los cambios"]),
    (EST, "Se agrega azúcar poco a poco a 100 g de agua, agitando, hasta que ya no se disuelve más. El procedimiento se repite con agua a 20 °C, 40 °C, 60 °C y 80 °C, usando el mismo tipo de azúcar.",
     "La temperatura del agua", "La masa máxima de azúcar disuelta", ["La masa de agua", "El tipo de azúcar", "La forma de agitar"],
     "A mayor temperatura se disolvió una mayor masa de azúcar.",
     "La solubilidad del azúcar en agua aumenta con la temperatura",
     ["La solubilidad del azúcar disminuye con la temperatura", "La masa de agua cambió en cada ensayo",
      "La temperatura no influye en la solubilidad"]),
    (EST, "Se intenta disolver 5 g de sal de mesa en 50 mL de tres líquidos distintos: agua, alcohol y aceite, todos a 20 °C y con la misma agitación. Se mide la masa de sal que queda sin disolver.",
     "El tipo de solvente", "La masa de sal que queda sin disolver", ["La temperatura", "El volumen de solvente", "La masa de sal agregada"],
     "En agua se disolvió casi toda la sal, en alcohol muy poca y en aceite nada.",
     "La sal es más soluble en solventes polares como el agua",
     ["La sal se disuelve igual en cualquier solvente", "El aceite es el mejor solvente para la sal",
      "La temperatura explica las diferencias"]),
    (EST, "Se toman 10 mL de una solución azul de sulfato de cobre y se diluyen en matraces hasta completar 20, 50 y 100 mL. Se compara la intensidad del color de cada solución con una escala de colores.",
     "El volumen final de la solución (la cantidad de agua agregada)", "La intensidad del color", ["El volumen inicial de solución tomada", "El tipo de soluto", "La escala de colores usada"],
     "Mientras mayor era el volumen final, más clara era la solución.",
     "Al diluir, la concentración de la solución disminuye aunque la cantidad de soluto sea la misma",
     ["Al diluir aumenta la cantidad de soluto", "La concentración aumenta al agregar agua",
      "El color no tiene relación con la concentración"]),
    (ATO, "Se calientan 100 mL de agua y 100 mL de alcohol en recipientes iguales con la misma fuente de calor. Se registra la temperatura a la que cada líquido comienza a hervir, a la misma presión.",
     "El tipo de líquido", "La temperatura de ebullición", ["El volumen de líquido", "La fuente de calor", "La presión"],
     "El alcohol hirvió a unos 78 °C y el agua a 100 °C.",
     "Los líquidos tienen distintas temperaturas de ebullición, lo que permite separarlos por destilación",
     ["Todos los líquidos hierven a la misma temperatura", "El agua hierve antes que el alcohol",
      "La fuente de calor causó la diferencia"]),
]


def lc(s):
    """Pasa a minúscula solo la primera letra (no cambia símbolos como CO₂)."""
    return s[0].lower() + s[1:]


def preguntas_de(exp):
    area, desc, vi, vd, controls, res, concl, concl_w = exp
    ctrl = rnd.choice(controls)
    yield make(area, f"{desc}\n\n¿Cuál es la variable independiente de este experimento?", vi, [vd] + controls,
               f"La variable independiente es la que el investigador modifica a propósito: {lc(vi)}.")
    yield make(area, f"{desc}\n\n¿Cuál es la variable dependiente de este experimento?", vd, [vi] + controls,
               f"La variable dependiente es la que se mide como resultado: {lc(vd)}.")
    yield make(area, f"{desc}\n\n¿Cuál de las siguientes es una variable controlada (que se mantiene constante)?", ctrl,
               [vi, vd, f"{vi} y {lc(vd)}"],
               f"Las variables controladas se mantienen iguales en todos los ensayos para que solo influya {lc(vi)}.")
    otra = rnd.choice(controls)
    yield make(area, f"{desc}\n\n¿Qué pregunta de investigación intenta responder este experimento?",
               f"¿Cómo influye {lc(vi)} en {lc(vd)}?",
               [f"¿Cómo influye {lc(vd)} en {lc(vi)}?", f"¿Cómo influye {lc(otra)} en {lc(vd)}?",
                f"¿Qué es {lc(vd)}?"],
               "La pregunta de investigación relaciona la variable que se modifica con la que se mide.")
    yield make(area, f"{desc} Resultado: {res}\n\n¿Qué conclusión es coherente con estos resultados?", concl, concl_w,
               f"La conclusión debe basarse en los datos y en la variable que se modificó. {res}")


def build():
    out = []
    for exp in EXPERIMENTOS:
        out.extend(preguntas_de(exp))
    return out
