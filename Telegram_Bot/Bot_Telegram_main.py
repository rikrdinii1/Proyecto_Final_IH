import json
import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, ChatAction
from telegram.ext import (Updater,CommandHandler,MessageHandler,Filters,ConversationHandler,CallbackContext)
from funciones import *

TOKEN = 'SECRETO'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)   
        
# Temas a tratar
Edad ,Sexo,Resultados, Final,Diag_Previo,Edo_Civil,Inicio, Tristeza,Pesimismo,Fracaso,Perdida_de_Placer,\
Sentimientos_de_Culpa,Sentimientos_de_Castigo,Disconformidad_con_uno_mismo,Autocritica,\
Pensamientos_o_Deseos_Suicidas,Llanto,Agitación,Perdida_de_Interés,Indecisión,Desvalorización,Perdida_de_Energía,\
Cambios_en_los_Hábitos_de_Sueño,Irritabilidad,Cambios_en_el_Apetito,Dificultad_de_Concentración,\
Cansancio_o_Fatiga,Perdida_de_Interés_en_el_Sexo, Respuesta_Recibida = range(29)

    
#### Funciones para el tratamiento de las respuestas recibidas

resp_usuario = dict() # En este diccionario vamos a ir almacenando las respuestas del usuario.



# Funcion Principal del Bot. 
# Se van a ir llamando las funciones en el archivo "funciones", y se va a ir iterando por cada una de ellas hasta completar el 
# cuestionario de Beck.

def main() -> None:
    
    updater = Updater(TOKEN)
    
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            Sexo: [MessageHandler(Filters.regex('^(OK)$'),Sexo)],
            Inicio: [MessageHandler(Filters.regex('^(Hombre|Mujer|Prefiero no Decir)$'),Inicio)],
            Edo_Civil: [MessageHandler(Filters.regex('^(Empleado|Desempleado Buscando|Desempleado no Buscando|Estudiante|Autoempleado)$'),Edo_Civil)],
            Edad: [MessageHandler(Filters.regex('^(Soltero|Casado|Union Libre)$'),Edad)],
            Diag_Previo: [MessageHandler(Filters.regex('^([0-9]{1,2})$'),Diag_Previo)],
            Tristeza: [MessageHandler(Filters.regex('^(SI|NO)$'),Tristeza)],
            
            #Sustituir el filtro con cada uno de los incisos de las respuestas recibidas
            Pesimismo: [MessageHandler(Filters.regex('^(A|B|C|D)$'),Pesimismo)],
            Fracaso: [MessageHandler(Filters.regex('^(A|B|C|D)$'),Fracaso)],
            Perdida_de_Placer: [MessageHandler(Filters.regex('^(A|B|C|D)$'),Perdida_de_Placer)],
            Sentimientos_de_Culpa: [MessageHandler(Filters.regex('^(A|B|C|D)$'),Sentimientos_de_Culpa)],
            Sentimientos_de_Castigo: [MessageHandler(Filters.regex('^(A|B|C|D)$'),Sentimientos_de_Castigo)],
            Disconformidad_con_uno_mismo: [MessageHandler(Filters.regex('^(A|B|C|D)$'),Disconformidad_con_uno_mismo)],
            Autocritica: [MessageHandler(Filters.regex('^(A|B|C|D)$'),Autocritica)],
            Pensamientos_o_Deseos_Suicidas: [MessageHandler(Filters.regex('^(A|B|C|D)$'),Pensamientos_o_Deseos_Suicidas)],
            Llanto: [MessageHandler(Filters.regex('^(A|B|C|D)$'),Llanto)],
            Agitación: [MessageHandler(Filters.regex('^(A|B|C|D)$'),Agitación)],
            Perdida_de_Interés: [MessageHandler(Filters.regex('^(A|B|C|D)$'),Perdida_de_Interés)],
            Indecisión: [MessageHandler(Filters.regex('^(A|B|C|D)$'),Indecisión)],
            Desvalorización: [MessageHandler(Filters.regex('^(A|B|C|D)$'),Desvalorización)],
            Perdida_de_Energía: [MessageHandler(Filters.regex('^(A|B|C|D)$'),Perdida_de_Energía)],
            Cambios_en_los_Hábitos_de_Sueño: [MessageHandler(Filters.regex('^(A|B|C|D)$'),Cambios_en_los_Hábitos_de_Sueño)],
            Irritabilidad: [MessageHandler(Filters.regex('^(A|B|C|D|E|F|G)$'),Irritabilidad)],
            Cambios_en_el_Apetito: [MessageHandler(Filters.regex('^(A|B|C|D)$'),Cambios_en_el_Apetito)],
            Dificultad_de_Concentración: [MessageHandler(Filters.regex('^(A|B|C|D|E|F|G)$'),Dificultad_de_Concentración)],
            Cansancio_o_Fatiga: [MessageHandler(Filters.regex('^(A|B|C|D)$'),Cansancio_o_Fatiga)],
            Perdida_de_Interés_en_el_Sexo: [MessageHandler(Filters.regex('^(A|B|C|D)$'),Perdida_de_Interés_en_el_Sexo)],
            Respuesta_Recibida: [MessageHandler(Filters.regex('^(A|B|C|D)$'),Respuesta_Recibida)],
            Final: [MessageHandler(Filters.all,Final)],
            
            # Mostramos los resultados que obtuvo el usuario y el mensaje final para terminar la conversacion.
            Resultados: [MessageHandler(Filters.regex('^(OK)$'),Resultados)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Inicio del Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
    
