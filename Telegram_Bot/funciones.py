
"""
Aqui se encuentran cada una de las funciones que hacen que el Bot funcione. 
Desde llamar a una accion, guardar los datos recolectados, mandar mensajes.
"""

def Valores_Respuestas_Usuario(chatid):
    # A esta funcion le pasamos los datos de las respuestas del usuario en forma de incisos, y generamos
    # una lista pero con los valores numericos de las respuestas para poder obtener la calificacion del usuario.
    respuestas = resp_usuario.get(chatid)
    respuestas_usuario = respuestas[7:]
    valor_respuestas_numerico = []

    f = open('./JSON/CuestionarioBeck.json','r')
    content = f.read()
    cuestionario = json.loads(content)
    
    for i in range(len(respuestas_usuario)):
        resp_user = respuestas_usuario[i]
        tema = cuestionario['Temas'][i]['Tema']
        data = cuestionario['Temas'][i]['Data']
        for x in range(len(data)):
            resp = data[x]['Inciso']
            valor = data[x]['Valor']
            if resp_user == resp:
                valor_respuestas_numerico.append(valor)
    
    return valor_respuestas_numerico

def abrir_json(nombre):
    # Esta funcion nos sirve para poder abrir los archivos JSON en los que tenemos los 
    # diversos temas que se irán tomando en el cuestionario
    f = open(f'./JSON/{nombre}.json','r')
    content = f.read()
    cuestionario = json.loads(content)
    
    inciso = [cuestionario[i]['Inciso'] for i in range(len(cuestionario))]
    respuestas = [cuestionario[i]['Respuesta'] for i in range(len(cuestionario))]
    reply_keyboard = [inciso]

    return inciso, respuestas, reply_keyboard

# Pendiente que no se puedan agregar mas de una vez elregistro. Si el usuario ya contestó la encuesta antes se debe de reiniciar el registro, o agregarlo como duplicado.
def guardar_respuestas_usuarios(chatid, respuesta):
    # Con esta funcion vamos guardando las respuestas de los usuarios en un diccionario, 
    # que despues se almacena como archivo JSON para que podamos leerlo y analizarlo en otro momento
    
    if chatid in resp_usuario.keys():
        # Si el ChatID se encuentra en el diccionario, y tiene menos de 28 registros, se agrega la respuesta
        if len(resp_usuario[chatid]) < 28:
            resp_usuario[chatid].append(respuesta)
        # Si el ChatID se encuentra en el diccionario, y tiene mas de 28 registros, se elimina el registro y se reinicia a agregar los datos,
        # ya que es la segunda vez que el usuario realiza la encuesta.
        elif len(resp_usuario[chatid]) >= 28:
            resp_usuario.pop(chatid)
            resp_usuario.update({chatid:[respuesta]})
    
    # Si no se encuentra el ChatID en el diccionario, se agrega el ID y la primer respuesta.
    elif chatid not in resp_usuario.keys():
        resp_usuario.update({chatid:[respuesta]})

    # abrimos el JSON y estamos escribiendo la data constantemente. 
    with open('./JSON/DataRecolectada.json','w') as f:
        json.dump(resp_usuario,f,indent=4)



#### Aqui inician las funciones para el envio de las preguntas al usuaio y la recoleccion de la data.

texto_start = 'Hola! Esta es una herramienta que aplica la prueba de Inventario de Beck que sirve como auxiliar para la detección de Depresión. Favor de responder a todas las preguntas de manera honesta y no saltarse ninguna. Todos sus datos serán tratados de manera confidencial y no se compartirán con nadie. Esta herramienta no es 100 porciento certera, por lo que en todo momento recomendamos el acudir con un profesional de la salud de su confianza. Este Bot es unicamente un proyecto Final de Ironhack, Ironhack México y Ironhack Global no tienen responsabilidad sobre los fines y usos de este Bot'
texto_sexo = '¿Me puedes indicar tu sexo?'
texto_estatuslaboral = '¿Me puedes indicar tu estatus laboral?'
texto_edocivil = '¿Me puedes indicar tu estado civil?'
texto_edad = '¿Me puedes indicar tu edad?'
texto_diagprevio = '¿Anteriormente has recibido algún diagnostico de depresión?'
texto_cuestionario = 'Lee con atención cada una de las afirmaciones, luego elige la que mejor describa como te has sentido en las ultimas dos semanas, incluyendo el día de hoy.'
disclaimer = 'Muchas gracias por participar en la prueba. Te recuerdo que tus datos permanecerán confidenciales. También te recuerdo que esta prueba simplemente es un apoyo a los profesionales de la salud, por lo tanto, en todo momento recomendamos ampliamente la búsqueda de apoyo de ellos. ' # colocarlo al final

# Obtencion de datos personales del usuario
def start(update: Update, context: CallbackContext) -> int:
    
    reply_keyboard = [['OK']]
    update.message.reply_text(texto_start,
         reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    return Sexo


def Sexo(update: Update, context: CallbackContext) -> int:
    
    reply_keyboard = [['Hombre', 'Mujer', 'Prefiero no Decir']]
    update.message.reply_text(texto_sexo,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )
    
    texto = update.message.text
    chat = update.message.chat
    guardar_respuestas_usuarios(chat.id, chat.first_name) #Nombre y ID

    return Inicio


def Inicio(update: Update, context: CallbackContext) -> int:
    
    reply_keyboard = [['Empleado', 'Desempleado Buscando', 'Desempleado no Buscando', \
                       'Estudiante', 'Autoempleado']]
    update.message.reply_text(texto_estatuslaboral,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    texto = update.message.text
    chat = update.message.chat
    guardar_respuestas_usuarios(chat.id, texto)
    
    return Edo_Civil


def Edo_Civil(update: Update, context: CallbackContext) -> int:
    
    reply_keyboard = [['Soltero', 'Casado', 'Union Libre']]
    update.message.reply_text(texto_edocivil,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )
    
    texto = update.message.text
    chat = update.message.chat
    guardar_respuestas_usuarios(chat.id, texto)
    
    return Edad


def Edad(update: Update, context: CallbackContext) -> int:
    
    update.message.reply_text(texto_edad)    
    
    texto = update.message.text
    chat = update.message.chat
    guardar_respuestas_usuarios(chat.id, texto)

    return Diag_Previo


def Diag_Previo(update: Update, context: CallbackContext) -> int:
    
    reply_keyboard = [['SI','NO']]
    update.message.reply_text(texto_diagprevio,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
           
    texto = update.message.text
    chat = update.message.chat
    guardar_respuestas_usuarios(chat.id, texto)

    return Tristeza
   
# Inicia la aplicacion del inventario de Beck
def Tristeza(update: Update, context: CallbackContext) -> int:   
    
    inciso, respuestas, reply_keyboard = abrir_json('Tristeza')
    # Impresion del mensaje
    update.message.reply_text(texto_cuestionario)
    for i in range(len(inciso)):
        update.message.reply_text(f'{inciso[i]}: {respuestas[i]}',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    texto = update.message.text
    chat = update.message.chat
    guardar_respuestas_usuarios(chat.id, texto)
    
    return Pesimismo


def Pesimismo(update: Update, context: CallbackContext) -> int:  
    
    inciso, respuestas, reply_keyboard = abrir_json('Pesimismo')
    # Impresion del mensaje
    update.message.reply_text(texto_cuestionario)
    for i in range(len(inciso)):
        update.message.reply_text(f'{inciso[i]}: {respuestas[i]}',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
   
    texto = update.message.text
    chat = update.message.chat
    guardar_respuestas_usuarios(chat.id, texto)    

    return Fracaso


def Fracaso(update: Update, context: CallbackContext) -> int:

    inciso, respuestas, reply_keyboard = abrir_json('Fracaso')
    # Impresion del mensaje
    update.message.reply_text(texto_cuestionario)
    for i in range(len(inciso)):
        update.message.reply_text(f'{inciso[i]}: {respuestas[i]}',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    texto = update.message.text
    chat = update.message.chat
    guardar_respuestas_usuarios(chat.id, texto)

    return Perdida_de_Placer


def Perdida_de_Placer(update: Update, context: CallbackContext) -> int:

    inciso, respuestas, reply_keyboard = abrir_json('Perdida de Placer')
    # Impresion del mensaje
    update.message.reply_text(texto_cuestionario)
    for i in range(len(inciso)):
        update.message.reply_text(f'{inciso[i]}: {respuestas[i]}',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        
    texto = update.message.text
    chat = update.message.chat
    guardar_respuestas_usuarios(chat.id, texto)

    return Sentimientos_de_Culpa


def Sentimientos_de_Culpa(update: Update, context: CallbackContext) -> int:

    inciso, respuestas, reply_keyboard = abrir_json('Sentimientos de Culpa')
    # Impresion del mensaje
    update.message.reply_text(texto_cuestionario)
    for i in range(len(inciso)):
        update.message.reply_text(f'{inciso[i]}: {respuestas[i]}',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    texto = update.message.text
    chat = update.message.chat
    guardar_respuestas_usuarios(chat.id, texto)

    return Sentimientos_de_Castigo


def Sentimientos_de_Castigo(update: Update, context: CallbackContext) -> int:

    inciso, respuestas, reply_keyboard = abrir_json('Sentimientos de Castigo')
    # Impresion del mensaje
    update.message.reply_text(texto_cuestionario)
    for i in range(len(inciso)):
        update.message.reply_text(f'{inciso[i]}: {respuestas[i]}',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    texto = update.message.text
    chat = update.message.chat
    guardar_respuestas_usuarios(chat.id, texto)

    return Disconformidad_con_uno_mismo


def Disconformidad_con_uno_mismo(update: Update, context: CallbackContext) -> int:

    inciso, respuestas, reply_keyboard = abrir_json('Disconformidad con uno mismo')
    # Impresion del mensaje
    update.message.reply_text(texto_cuestionario)
    for i in range(len(inciso)):
        update.message.reply_text(f'{inciso[i]}: {respuestas[i]}',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    texto = update.message.text
    chat = update.message.chat
    guardar_respuestas_usuarios(chat.id, texto)

    return Autocritica


def Autocritica(update: Update, context: CallbackContext) -> int:

    inciso, respuestas, reply_keyboard = abrir_json('Autocritica')
    # Impresion del mensaje
    update.message.reply_text(texto_cuestionario)
    for i in range(len(inciso)):
        update.message.reply_text(f'{inciso[i]}: {respuestas[i]}',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    texto = update.message.text
    chat = update.message.chat
    guardar_respuestas_usuarios(chat.id, texto)

    return Pensamientos_o_Deseos_Suicidas


def Pensamientos_o_Deseos_Suicidas(update: Update, context: CallbackContext) -> int:

    inciso, respuestas, reply_keyboard = abrir_json('Pensamientos o Deseos Suicidas')

    # Impresion del mensaje
    update.message.reply_text(texto_cuestionario)
    for i in range(len(inciso)):
        update.message.reply_text(f'{inciso[i]}: {respuestas[i]}',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    texto = update.message.text
    chat = update.message.chat
    guardar_respuestas_usuarios(chat.id, texto)

    return Llanto


def Llanto(update: Update, context: CallbackContext) -> int:

    inciso, respuestas, reply_keyboard = abrir_json('Llanto')
    # Impresion del mensaje
    update.message.reply_text(texto_cuestionario)
    for i in range(len(inciso)):
        update.message.reply_text(f'{inciso[i]}: {respuestas[i]}',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    texto = update.message.text
    chat = update.message.chat
    guardar_respuestas_usuarios(chat.id, texto)

    return Agitación


def Agitación(update: Update, context: CallbackContext) -> int:

    inciso, respuestas, reply_keyboard = abrir_json('Agitación')
    # Impresion del mensaje
    update.message.reply_text(texto_cuestionario)
    for i in range(len(inciso)):
        update.message.reply_text(f'{inciso[i]}: {respuestas[i]}',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    texto = update.message.text
    chat = update.message.chat
    guardar_respuestas_usuarios(chat.id, texto)

    return Perdida_de_Interés


def Perdida_de_Interés(update: Update, context: CallbackContext) -> int:

    inciso, respuestas, reply_keyboard = abrir_json('Perdida de Interés')
    # Impresion del mensaje
    update.message.reply_text(texto_cuestionario)
    for i in range(len(inciso)):
        update.message.reply_text(f'{inciso[i]}: {respuestas[i]}',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    texto = update.message.text
    chat = update.message.chat
    guardar_respuestas_usuarios(chat.id, texto)

    return Indecisión


def Indecisión(update: Update, context: CallbackContext) -> int:

    inciso, respuestas, reply_keyboard = abrir_json('Indecisión')
    # Impresion del mensaje
    update.message.reply_text(texto_cuestionario)
    for i in range(len(inciso)):
        update.message.reply_text(f'{inciso[i]}: {respuestas[i]}',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    texto = update.message.text
    chat = update.message.chat
    guardar_respuestas_usuarios(chat.id, texto)

    return Desvalorización


def Desvalorización(update: Update, context: CallbackContext) -> int:

    inciso, respuestas, reply_keyboard = abrir_json('Desvalorización')
    # Impresion del mensaje
    update.message.reply_text(texto_cuestionario)
    for i in range(len(inciso)):
        update.message.reply_text(f'{inciso[i]}: {respuestas[i]}',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    texto = update.message.text
    chat = update.message.chat
    guardar_respuestas_usuarios(chat.id, texto)

    return Perdida_de_Energía


def Perdida_de_Energía(update: Update, context: CallbackContext) -> int:

    inciso, respuestas, reply_keyboard = abrir_json('Perdida de Energía')
    # Impresion del mensaje
    update.message.reply_text(texto_cuestionario)
    for i in range(len(inciso)):
        update.message.reply_text(f'{inciso[i]}: {respuestas[i]}',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    texto = update.message.text
    chat = update.message.chat
    guardar_respuestas_usuarios(chat.id, texto)

    return Cambios_en_los_Hábitos_de_Sueño


def Cambios_en_los_Hábitos_de_Sueño(update: Update, context: CallbackContext) -> int:

    inciso, respuestas, reply_keyboard = abrir_json('Cambios en los Hábitos de Sueño')
    # Impresion del mensaje
    update.message.reply_text(texto_cuestionario)
    for i in range(len(inciso)):
        update.message.reply_text(f'{inciso[i]}: {respuestas[i]}',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    texto = update.message.text
    chat = update.message.chat
    guardar_respuestas_usuarios(chat.id, texto)

    

    return Irritabilidad


def Irritabilidad(update: Update, context: CallbackContext) -> int:

    inciso, respuestas, reply_keyboard = abrir_json('Irritabilidad')
    # Impresion del mensaje
    update.message.reply_text(texto_cuestionario)
    for i in range(len(inciso)):
        update.message.reply_text(f'{inciso[i]}: {respuestas[i]}',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    texto = update.message.text
    chat = update.message.chat
    guardar_respuestas_usuarios(chat.id, texto)

    return Cambios_en_el_Apetito


def Cambios_en_el_Apetito(update: Update, context: CallbackContext) -> int:
    
    inciso, respuestas, reply_keyboard = abrir_json('Cambios en el Apetito') 
    # Impresion del mensaje
    update.message.reply_text(texto_cuestionario)
    for i in range(len(inciso)):
        update.message.reply_text(f'{inciso[i]}: {respuestas[i]}',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    texto = update.message.text
    chat = update.message.chat
    guardar_respuestas_usuarios(chat.id, texto)

    return Dificultad_de_Concentración


def Dificultad_de_Concentración(update: Update, context: CallbackContext) -> int:

    inciso, respuestas, reply_keyboard = abrir_json('Dificultad de Concentración')
    # Impresion del mensaje
    update.message.reply_text(texto_cuestionario)
    for i in range(len(inciso)):
        update.message.reply_text(f'{inciso[i]}: {respuestas[i]}',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    texto = update.message.text
    chat = update.message.chat
    guardar_respuestas_usuarios(chat.id, texto)

    return Cansancio_o_Fatiga


def Cansancio_o_Fatiga(update: Update, context: CallbackContext) -> int:

    inciso, respuestas, reply_keyboard = abrir_json('Cansancio o Fatiga')
    # Impresion del mensaje
    update.message.reply_text(texto_cuestionario)
    for i in range(len(inciso)):
        update.message.reply_text(f'{inciso[i]}: {respuestas[i]}',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    texto = update.message.text
    chat = update.message.chat
    guardar_respuestas_usuarios(chat.id, texto)

    return Perdida_de_Interés_en_el_Sexo


def Perdida_de_Interés_en_el_Sexo(update: Update, context: CallbackContext) -> int:
    
    inciso, respuestas, reply_keyboard = abrir_json('Perdida de Interés en el Sexo')
    # Impresion del mensaje
    update.message.reply_text(texto_cuestionario)
    for i in range(len(inciso)):
        update.message.reply_text(f'{inciso[i]}: {respuestas[i]}',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    texto = update.message.text
    chat = update.message.chat
    guardar_respuestas_usuarios(chat.id, texto)

    return Respuesta_Recibida


def Respuesta_Recibida(update: Update, context: CallbackContext) -> int:
    texto = update.message.text
    chat = update.message.chat
    guardar_respuestas_usuarios(chat.id, texto)

    update.message.reply_text('Si alguna vez te has sentido triste o deprimido y has buscado apoyo en familiares y amigos, me puedes indicar ¿Qué es lo que te dijeron? o ¿Cuál es la frase o palabras que mas escuchaste?')

    return Final

# Termina la aplicacion del Inventario de Beck
def Final(update: Update, context: CallbackContext) -> int:    
    
    reply_keyboard = [['OK']]
    update.message.reply_text('Estamos Calculamdo tus resultados.',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    texto = update.message.text
    chat = update.message.chat
    guardar_respuestas_usuarios(chat.id, texto)

    return Resultados


def Resultados(update: Update, context: CallbackContext) -> int:
    
    chat = update.message.chat

    int_cal = Valores_Respuestas_Usuario(chat.id)
    
    """
    Clasificacion de la depresion:
    baja = 0-13
    leve = 14-19
    moderada = 20-28
    grave = 29-63
    """
    baja = 'Veo que estás muy bien! Sigue así y nunca dudes en acudir a un profesional de la salud si lo crees conveniente.'
    leve='Veo que tienes algunos temas, te recomiendo acudir a un profesional de la salud si lo deseas'
    moderada = 'Me preocupas un poco. Te recomiendo acudir a un profesional de la salud lo antes posible.'
    grave = 'Te recomiendo acudir a un profesional de la salud lo antes posible para que te puedan brindar ayuda inmediata.'

    total = sum(int_cal)
    if (total >= 0) & (total <= 13):
        update.message.reply_text(baja)

    elif (total >= 14) & (total <= 19):
        update.message.reply_text(leve)
    
    elif (total >= 20) & (total <= 28):
        update.message.reply_text(moderada)
    
    elif (total >= 29) & (total <= 63):
        update.message.reply_text(grave)

    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Espero verte pronto.', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


