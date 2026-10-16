# Reflexión

**Materia:** Metodología I — Tecnicatura Universitaria en Programación

**Integrantes:** García Juan Martín y Tiziano Valentini

**Fecha:** 16 de octubre de 2026

En el Discovery nos encontramos con datos que no pudimos utilizar tal como estaban. Tres sitios no permitieron verificar el producto: OdontoSaaS no devolvió contenido, y DentalData y Dentap no resolvieron. Además, al comienzo figuraban dominios que no se correspondían con los sistemas reales. xdental.com.br está estacionado y el producto funciona en otro sitio, y odontocloud.com.ar no existe, ya que el sistema consultado es de origen brasileño. Detectamos estas inconsistencias al abrir cada URL y contrastarla con lo que indicaba la nota. En el caso de DentalSoft, el sitio publica detección de solapamiento y precios en pesos. La cantidad de clínicas que declara es una afirmación del propio sitio y no una prueba, por lo que no la tomamos como adopción verificada. Cuando no encontramos evidencia pública, dejamos la celda como "No evidenciado" en lugar de completarla por suposición.

Aplicamos la instancia de Ajustar en dos momentos distintos. En el Discovery, Tiziano solicitó corregir la matriz comparativa, porque los pesos no coincidían con los definidos por la cátedra y el ranking se había construido con criterios ajenos a la consigna. De no haberlo corregido, el informe habría ordenado los sistemas según otra escala y la sección B no habría cumplido lo pedido. Más adelante, en el Propose del único change, Juan Martín pidió fijar tres escenarios: la reserva válida, el rechazo cuando se superpone el profesional o el sillón, y el caso en que el siguiente turno comienza exactamente cuando termina el anterior. También confirmó que la hora se registra con zona horaria y que la comparación se realiza en UTC, y dejó fuera del alcance el login, PostgreSQL y la cancelación. Sin este segundo ajuste, el change podría haberse desviado hacia la autenticación o hacia la base de datos, y no habríamos podido probar ni justificar ese alcance en la entrega.

La diferencia con un prompt suelto es que el comportamiento quedó especificado antes de la implementación. La especificación describe qué ocurre en cada caso con el formato dado, cuando, entonces, y los tests se derivan directamente de ese documento. Ante cualquier discrepancia, se corregía el código tomando la especificación como referencia. En cambio, con un pedido libre el resultado depende de lo que el chat recuerde en ese momento y no existe un contrato que permita evaluar si la solución es correcta.

De la fundación, lo que más aportó al change fue la base de conocimiento, en particular la regla del recurso doble: el turno ocupa un profesional y un sillón a la vez, la duración se determina a partir de la prestación y se admite el encadenado exacto. El roadmap nos sirvió para elegir un único change y para no marcar como realizados los que quedaron pendientes. Lo que menos contribuyó a esta entrega fue la lista extensa de changes futuros, dado que no se implementaron.

Tiziano estuvo a cargo de la fundación: el relevamiento, la base de conocimiento, el roadmap y las reglas del agente. Juan Martín tuvo a su cargo el ajuste a Python, la revisión del Propose, la implementación de este único change, los tests y el informe.

Utilizamos un agente para redactar borradores, organizar documentos y proponer código. Las decisiones de alcance, la lectura de las fuentes y las capturas fueron revisadas por nosotros, por lo que el agente no es el autor del trabajo. Lo que un sitio no publica, no lo dimos por existente.
