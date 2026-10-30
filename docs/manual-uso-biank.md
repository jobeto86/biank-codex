# Manual de uso de Biank 🌸

> Guía para el equipo. Biank es tu secretaria ejecutiva digital de operaciones — este manual te
> dice cómo arrancar, qué puede hacer y cómo sacarle el máximo jugo.

---

## 1. ¿Qué es Biank?

Biank es una secretaria ejecutiva digital que trabaja contigo en tu computadora, conectada al
sistema de la empresa (el ERP). Le hablas **como le hablarías a una compañera
de oficina** — sin comandos, sin menús, sin capacitación técnica. Tú trabajas
y conversas; ella consulta, registra, recuerda y aprende.

**Lo más importante que debes saber**: Biank **nunca cambia nada sin mostrarte
antes exactamente qué va a hacer y esperar tu "sí"**. Puedes explorar y
preguntar con toda confianza — preguntar no rompe nada.

---

## 2. Cómo arrancar

1. Descomprime el ZIP en una carpeta nueva y abre esa carpeta en Codex o tu arnés compatible.
2. Di **«Hola Biank»**. El agente prepara la carpeta con Python si hace falta y aplica la actualización validada del core disponible en GitHub. Si Python no está instalado, te guía para instalarlo; si no hay red, informa y conserva la copia local utilizable.
3. Autoriza tu propia cuenta de CBSuite desde las conexiones del arnés cuando haga falta. El saludo no inicia sesión por sí mismo ni crea una cuenta o empresa.
4. **Preséntate** con tu nombre para el trato cotidiano; Biank verifica con CBSuite qué usuario y empresa están realmente autorizados antes de operar.
5. Ella misma te trae lo del día con los pendientes que existan y la información que pueda comprobar.

Si es tu **primera vez**, solo di *"hola"* o *"¿qué puedes hacer?"* y ella te da
el tour completo.

---

## 3. Qué puede hacer por ti

### Consultas (pregunta lo que sea, es solo lectura)

| Quieres saber... | Dile algo como... |
|---|---|
| Ventas | *"¿Cuánto vendimos esta semana?"*, *"Busca la venta de Don Toño"* |
| Clientes | *"¿Cuánto debe Ferretería López?"*, *"Estado de cuenta de X"* |
| Inventario | *"¿Cuánto hay de [producto]?"*, *"¿Qué productos andan bajos?"* |
| Caja | *"¿Cuánto hay en caja?"*, *"Movimientos de hoy"* |
| Cobranza | *"¿Quién nos debe?"*, *"Cartera vencida"* |
| Proveedores | *"¿Qué le debemos a Aceros?"*, *"Compras pendientes"* |

### Registrar operaciones (con vista previa siempre)

- *"Registra un pago de $5,000 de Don Toño"* — Biank te repite lo que entendió,
  te muestra el cambio exacto (venta, monto, saldo que queda) y **solo ejecuta
  cuando le digas que sí**.

### Recordatorios y pendientes

- *"Recuérdame marcarle el viernes a López"* — anotado. No necesitas apuntarlo
  en ningún lado: cuando vuelvas a trabajar con Biank te trae lo que toca ese día.
  Una notificación fuera de la conversación necesita programación confirmada.
- *"Ya me pagó López"* — ella registra tu confirmación como antecedente del cierre.
  Eso no equivale a registrar el pago en el ERP; esa operación se verifica por separado.

### Leer documentos

- Súbele la **foto o PDF de un recibo o factura** y pídele: *"sácale los
  datos"*. Ella extrae monto, fecha, concepto y te los presenta.

---

## 4. El superpoder: enseñarle tus procesos

Biank **aprende los flujos de TU trabajo**. Si haces algo repetitivo, enséñaselo
una vez y queda fijo:

- **Enseñar**: *"Quiero que aprendas a hacer el corte de caja como lo hacemos
  aquí"* — le explicas los pasos conversando y ella lo documenta.
- **Usar lo aprendido**: *"Recuerda la habilidad de corte de caja"* o *"hazlo
  como te enseñé"* — y lo ejecuta completo.
- Ella también es proactiva: si nota que repites lo mismo varias veces en la
  semana, **te va a proponer aprendérselo**. Di que sí — es tiempo que recuperas.

> Nota: los flujos nuevos quedan fijos cuando los aprueba el administrador.
> Si eres operador, Biank guarda tu propuesta y se la presenta.

---

## 5. Cómo sacarle más jugo

1. **Háblale normal.** No busques "el comando correcto" — no existe. *"Oye,
   ¿cómo vamos con lo de López?"* funciona perfecto.
2. **Pídele antecedentes, no solo datos.** En vez de *"saldo de López"*, prueba
   *"¿qué acordamos con López?"* — Biank consulta la tarea y las referencias
   disponibles; si falta evidencia, te lo dice.
3. **Dile lo que decidas.** *"Quedamos con el cliente que paga el lunes"* —
   ella lo anota y le da seguimiento. Lo que no le dices, no lo puede recordar.
4. **Retoma sin ceremonias.** No necesitas decir *"cierra sesión"*: los acuerdos,
   próximos pasos y comprobantes se guardan en el pendiente correspondiente
   mientras trabajan, sin esperar una despedida.
5. **Acepta la revisión semanal.** Una vez por semana te propondrá 5 minutos de
   repaso: archiva lo cerrado, te avisa de seguimientos vencidos y propone
   nuevos flujos cuando hay evidencia suficiente.

---

## 6. Continuidad y memoria

Los pendientes son el registro del trabajo: cada uno conserva responsable, próximo
paso, fecha, acuerdos y referencias al resultado. No se abre otro por cambiar de
conversación. El historial del arnés conserva el detalle de la charla según sus
capacidades; Biank no exige una bitácora ni resúmenes de sesión adicionales.

Una memoria breve opcional de hasta **4096 bytes UTF-8** conserva preferencias
confirmadas y hechos duraderos que sirven para varios asuntos. No copia tareas,
manuales, datos del ERP ni contraseñas. Puedes pedir *"¿qué recuerdas?"*, corregir
una preferencia o solicitar que la olvide. Se consolida y mide antes de guardar;
no se recorta información para cumplir el límite.

Los archivos históricos que ya tengas se conservan. No se borran ni se migran
automáticamente por instalar una actualización. Un contexto antiguo más grande
se consulta sólo cuando haga falta y se propone consolidarlo, sin bloquear tu trabajo.
La memoria propia de cada arnés es una ayuda; no se supone compartida entre ellos.

## 7. Arnés y modelo

La carpeta contiene las instrucciones de Biank; el arnés y el modelo los elige tu organización según su acceso y sus necesidades. Instalar el core no cambia tu suscripción ni tus conexiones.

Para operar CBSuite, autoriza la conexión del arnés con tu propia identidad. No compartas contraseñas ni copies archivos de acceso de otra persona. Biank verifica la cuenta y la empresa antes de trabajar con datos reales.


## 8. Si algo no funciona

- Di **"algo no funciona"** o **"revisa tu instalación"** — Biank corre su
  propio diagnóstico y te dice qué pasa y cómo se arregla.
- Di **"actualízate"** si sientes que le falta algo que debería saber hacer.
- Si de plano no arranca, avisa al administrador — hay problemas que se
  arreglan con una reinstalación rápida.

---

## 9. Las frases que más vas a usar

| Momento | Frase |
|---|---|
| Arrancar el día | *"Hola Biank, soy [tu nombre]"* |
| Ver qué toca | *"¿Qué tenemos hoy?"* |
| Consultar | *"¿Cuánto...?"*, *"Busca..."*, *"¿Quién debe...?"* |
| Registrar | *"Registra un pago de..."* |
| Recordatorio | *"Recuérdame [X] el [día]"* |
| Enseñarle | *"Quiero que aprendas a..."* |
| Usar lo enseñado | *"Recuerda la habilidad de..."* |
| Ayuda | *"¿Qué puedes hacer?"* |
| Problemas | *"Algo no funciona"* |
| Retomar un asunto | *"¿En qué quedó lo de López?"* |

---

*Biank es un producto de CB Inteligencia. ¿Dudas o ideas? Díselas a Biank —
ella las anota y las hace llegar.*
