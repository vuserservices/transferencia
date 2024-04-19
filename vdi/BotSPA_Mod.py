
import fitz
import datetime
import re
import json
from datetime import datetime
import requests
import os

class SPA_Mod:

    def __init__(self):

        pass

    def ejecutar(self):

        inicio = datetime.now()




        try:
            #test1= pdfx.PDFx(file)
            #urlpdf=(test1.get_references_as_dict()["url"][2])

            descargaarchivolink= "archivodescargalnk.pdf"

            #response = requests.get(urlpdf)
            """
            try:
                response = requests.get(urlpdf, timeout=10)  # Establece un tiempo de espera de 10 segundos
                response.raise_for_status()  # Lanza una excepción en caso de error HTTP
                with open(descargaarchivolink, 'wb') as file:
                    file.write(response.content)
                print(f"Archivo {descargaarchivolink} descargado con éxito.")
                descargacorrecta= "true"
            except requests.exceptions.RequestException as e:
                print(f"Error al descargar el archivo: {e}")
                descargacorrecta= "false"
            

            descargacorrecta= "true"
            if descargacorrecta=="true":
                documentodescargado=fitz.open(descargaarchivolink)
                salidadescarga=open(descargaarchivolink+".txt","wb")

                for pagina in documentodescargado:
                    textdescarga=pagina.get_text().encode("utf8")
                    salidadescarga.write(textdescarga)
                    salidadescarga.write(b'\n------\n')

                salidadescarga.close()

                # Leer el contenido del archivo de texto
                with open('archivodescargalnk.pdf.txt', 'r', encoding='utf-8') as file:
                    contentdescarga = file.read()

                def limpiar_texto(contentdescarga):
                    return re.sub(r'\s+', ' ', contentdescarga).strip()


                # Limpiar el texto completo
                contentdescarga = limpiar_texto(contentdescarga)
                contentdescarga = re.sub(r'Página\s+\d+\s+de.*?------', '', contentdescarga, flags=re.DOTALL)
                contentdescarga = re.sub(r'\s\s', ' ', contentdescarga, flags=re.DOTALL)
                contentdescarga = re.sub(r'\n', '', contentdescarga, flags=re.DOTALL)

            else:
                pass

            firmaelectronica= re.search(r'Firmado electrónicamente el (.*?)', contentdescarga, re.DOTALL).group(1)
            print(firmaelectronica)
            """

            nombrearchivo="pdfactual.pdf"
            doc=fitz.open('./descargas/'+nombrearchivo)
            salida=open('./descargas/'+nombrearchivo+".txt","wb")

            for pagina in doc:
                text=pagina.get_text().encode("utf8")
                salida.write(text)


            doc.close()
            salida.close()

            # Leer el contenido del archivo de texto
            with open('./descargas/'+nombrearchivo+'.txt', 'r', encoding='utf-8') as file:
                content = file.read()




            content = re.sub(r'\s+', ' ', content).strip()
            content = re.sub(r'\s\s', ' ', content, flags=re.DOTALL)
            cve_match = re.search(r'Código de verificación electrónica \(CVE\): (\w+)', content).group(1)
            content = re.sub(r'Página\s+\d+\s+de (.*?) \d\d\:\d\d','', content, flags=re.DOTALL)
            content = re.sub(r'\s+:', ':', content, flags=re.DOTALL)
            content = re.sub(r'\s\s', ' ', content, flags=re.DOTALL)
            total_length = len(content)
            half_length = total_length // 2

            content1 = content[:half_length]
            content2 = content[half_length:]

            errorextraccion="false"
            
        except:
            errorextraccion="true"
        #region ARTICULOS

        try:

            Search_PJ= re.search(r'Rut Sociedad:(.*?)Fecha de ',content, re.DOTALL).group(1)
            match_EIRL=re.search(r'E.I.R.L.',Search_PJ, re.DOTALL)
            match_SPA=re.search(r' SpA',Search_PJ, re.DOTALL)
            match_LTDA= re.search(r'(?<!RESPONSABILIDAD\s)LIMITADA',Search_PJ, re.DOTALL)


            if match_EIRL:
                match_EIRL="true"
                tipoempresa= "EMPRESA INDIVIDUAL DE RESPONSABILIDAD LIMITADA"
            else:
                match_EIRL="false"
                

            if match_SPA:
                match_SPA="true"
                tipoempresa="SpA"
            else:
                match_SPA="false"


            if match_LTDA:
                match_LTDA= "true"
                tipoempresa="LIMITADA"
            else:
                errorarticulos="false"

            if (match_EIRL=="false") and (match_SPA=="false") and (match_LTDA=="false"):
                errorarticulos="true"
            else:
                errorarticulos="false"

        except:
            errorarticulos="true"

        #endregion ARTICULOS


        #region - ESTADO
        # Definir patrones de expresiones regulares para los datos a extraer

        try:

            razon_social_pattern = r'Razón Social: *(.*?) Fecha'

            ultimamodificacion= re.search(r'ACTUACIONES Y ANOTACIONES(.*?) ',content, re.DOTALL)

            rut_sociedad_completo = re.search(r'Rut Sociedad:\s(.*?) Raz', content,re.DOTALL).group(1)

            rut_sociedad_solo = re.search(r'Rut Sociedad:\s(.*?) Raz', content,re.DOTALL).group(1).replace('.','').replace('-','')
            rut_sociedad_guion = re.search(r'Rut Sociedad:\s(.*?) Raz', content,re.DOTALL).group(1).replace('.','')
            razon_social = re.search(r'Razón Social: (.*?) Fecha', content)


            if razon_social:
                razon_social = re.search(r'Razón Social: (.*?) Fecha', content).group(1)
                razonsocialtrue="true"
            else:
                razonsocialtrue="false"


            fecha_junta = inicio.strftime("%Y%m%d%H%M%S%f")

            fecha_match = re.search(r'Fecha de Constitución: (\d{1,2} de [^\d]+\d{4})', content)

            if fecha_match:
                fecha_texto = fecha_match.group(1)
                
                meses = {
                    'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04',
                    'mayo': '05', 'junio': '06', 'julio': '07', 'agosto': '08',
                    'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12'
                }
                
                for nombre_mes, numero_mes in meses.items():
                    fecha_texto = fecha_texto.replace(nombre_mes, numero_mes)
                
                fecha_formateada = re.sub(r'(\d{1,2}) de (\d{2}) del (\d{4})', r'\1-\2-\3', fecha_texto)   
                fechamatchtrue="true"
            else:
                fechamatchtrue="false"

            if (razonsocialtrue=="false") or (fechamatchtrue == "false"):
                errorestado="true"
            else:
                errorestado="false"

        except:
            errorestado="true"




        #endregion ESTADO


        #region - ESTUDIO

        try:

            modificacion=[]

            fecha_separada = inicio.strftime("%Y-%m-%d %H:%M:%S.%f")

            matchestadosempresa=[]
            patron_fecha = r'(CONSTITUCIÓN|MODIFICACIÓN|DISOLUCIÓN|TRANSFORMACIÓN)\s+(\d{2}-\d{2}-\d{4})'
            coincidencias_fecha = re.findall(patron_fecha, content)

            for cuenta in coincidencias_fecha:
                valor=cuenta
                modificacion.append(valor)
                

            ultimoestadoempresa=modificacion[0][0]
            ultimafechamodificacion=modificacion[0][1]
            fechadiames = datetime.strptime(modificacion[0][1], "%d-%m-%Y")
            fechamesdia=fechadiames.strftime("%Y-%m-%d")
            fechadiames=fechadiames.strftime("%d-%m-%Y")



            empresadisuelta = "false"

            for cuenta in modificacion:
                disuelto = cuenta[0]
                if disuelto == "DISOLUCIÓN":
                    # Si se encuentra "DISOLUCIÓN", establece empresadisuelta en "true" y rompe el bucle
                    empresadisuelta = "true"
                    break

            if ultimoestadoempresa=="MODIFICACIÓN":
                empresamodificada="true"
            else:
                empresamodificada="false"


            if ultimoestadoempresa=="TRANSFORMACIÓN":
                empresatransformada="true"

            else:
                empresatransformada="false"

            if ultimoestadoempresa=="CONSTITUCIÓN":
                empresaconstituida="true"
            else:
                empresaconstituida="false"

            


            sociedad_patron = r"se constituyó una(.*?), en adelante la"
            sociedad_coincidencia= coincidencia = re.search(sociedad_patron, content, re.DOTALL)
            if sociedad_coincidencia: texto_extraido = sociedad_coincidencia.group(1).strip().upper()
            else: texto_extraido = None

            patron_sociedad = r"Sociedad por Acciones"
            patron_persona_juridica = r"persona jurídica"

            coincidencia_sociedad = re.search(patron_sociedad, content)
            coincidencia_persona_juridica = re.search(patron_persona_juridica, content)

            if coincidencia_sociedad and coincidencia_persona_juridica:
                tipo_entidad = "Ambos (Sociedad por Acciones y Persona Jurídica) están presentes"
            elif coincidencia_sociedad:
                tipo_entidad = "SOCIEDAD POR ACCIONES"
            elif coincidencia_persona_juridica:
                tipo_entidad = "PERSONA JURIDICA"
            else:
                tipo_entidad = None

            if (empresaconstituida =="false") and (empresamodificada =="false") and empresatransformada =="false" and (empresadisuelta =="false"):
                errorestudio= "true"
            else:
                errorestudio="false"

        except:
            errorestudio="true"





        #endregion - ESTUDIO

        #region Articulos repetidos
        try:

            dict_articulos={}
            list_articulos=["ARTÍCULO PRIMERO: NOMBRE:",
                            "ARTÍCULO SEGUNDO: DOMICILIO:",
                            "ARTÍCULO TERCERO: DURACIÓN:",
                            "ARTÍCULO CUARTO: OBJETO:",
                            "ARTICULO QUINTO:",
                            "ARTÍCULO SEXTO:",
                            "ARTÍCULO SÉPTIMO:",
                            "ARTÍCULO OCTAVO:",
                            "ARTÍCULO NOVENO: JUNTAS DE ACCIONISTAS:",
                            "ARTÍCULO DÉCIMO: COMUNICACIÓN DE LA SOCIEDAD:",
                            "ARTÍCULO DÉCIMO PRIMERO: RESOLUCIÓN DE DIFERENCIAS:",
                            "ARTÍCULO DÉCIMO SEGUNDO: DISTRIBUCIÓN DE UTILIDADES:"
                            ]
            countarti=0
            for checkarticulos in list_articulos:
                articulosrepetidos = re.findall(checkarticulos, content, re.DOTALL)
                repetidos = len(articulosrepetidos)-1



                if repetidos >0:
                    dict_articulos["valor"]=checkarticulos
                    countarti+=1
                else:
                    dict_articulos["valor"]=0
                    pass

            if countarti>0:
                artirepetidostrue="true"
            else:
                artirepetidostrue="false"

        except:
            artirepetidostrue="true"

       

        
        #endregion Articulos repetidos


        #region - prestudio
        try:

            actuacion_match = re.search(r'(CONSTITUCIÓN|MODIFICACIÓN|DISOLUCIÓN|TRANSFORMACIÓN)', content, re.DOTALL)

            if actuacion_match:
                actuacion_find = actuacion_match.group()
                errorpreestudio="false"
            else:
                actuacion_find = ""
                errorpreestudio="true"

            cve_match = re.search(r'El código de verificación electrónico \(CVE\) es: (\w+)', content).group(1)

        except:
            errorpreestudio="true"



        #endregion - prestudio



        #################################################

        #region - ACCIONISTAS

        try:

            texto_accionistasrepresentantesSIIv1= re.findall(r'El o la representante ante el SII es (.*?)\.\s', content, re.DOTALL)
            texto_accionistasrepresentantesSIIv12omas= re.findall(r'Los representantes ante el SII son: (.*?)\.\s', content, re.DOTALL)


            if texto_accionistasrepresentantesSIIv1:

                nombreyrutrepresentantebruto= str(texto_accionistasrepresentantesSIIv1).replace("'",'').replace("[","").replace("]","").replace(" Rut ","")
                nombreyrutrepresentanteseparado= nombreyrutrepresentantebruto.split(",")
                nombreseparadoSII=nombreyrutrepresentanteseparado[0]
                rutseparadoSII=nombreyrutrepresentanteseparado[1]
                textoaccionistastrue="true"

            else: 
                textoaccionistastrue="false"
            
            if texto_accionistasrepresentantesSIIv12omas:
                texto_accionistassplit=texto_accionistasrepresentantesSIIv12omas[0].split(';')
                for representantes in texto_accionistassplit:
                    nombreseparadoSII= representantes.split(',')[0].strip()
                    rutseparadoSII= representantes.split(',')[1].replace(' Rut ', '').strip()

                textoaccionistastrue="true"
            else:
                textoaccionistastrue="false"


            transitorios = re.search(r'TITULO QUINTO.- OTROS PACTOS(.*?) (CONSTITUCIÓN|MODIFICACIÓN|DISOLUCIÓN|TRANSFORMACIÓN) ', content, re.DOTALL)
            texto_accionistas_referencia = [] 
            firmantesdetallelist=[]
            


            if transitorios:
                articulo_referencia = "articulo_13"
                
                # Buscar todas las letras y sus contenidos
                #matches_letras = re.findall(r'([A-Z])\)\s(.*?)(?=\.\s[A-Z]\)|$)', transitorios.group(1), re.DOTALL)
                matches_letras = re.findall(r'([A-Z])\)\s(.*?)[.;]', transitorios.group(1), re.DOTALL)
                countaccionistas= len(matches_letras)

                
                
                

                for letra, contenidoletras in matches_letras:


                    texto_accionistas_referencia.append(contenidoletras)
                    
                firmasconrut= []
                
                for letra, contenidoletras in matches_letras:
                    diccionario_nombres={}  

                    nombres1= re.findall(r'(.*?) suscribe: ', contenidoletras, re.DOTALL)
                    participacion1=re.findall(r'suscribe: (.*?) acciones ', contenidoletras, re.DOTALL)
                    participaciondinero=re.findall(r'\$(.*?)\s', contenidoletras, re.DOTALL)
                    referenciaaccionistas=re.findall(r'\$(.*?)\s', contenidoletras, re.DOTALL)
                    #rutaccionistasunoauno=rutseparadoSII=re.search(re.escape(nombres1.strip())+r'\, Rut (.*?)(\.|\;)',content, re.DOTALL)  #pendiente

                    

                    for contenidoletras in nombres1:
                        try:
                            
                            diccionario_nombres["nombre"]=nombres1
                            rutaccionistasunoauno=rutseparadoSII=re.search(re.escape(contenidoletras)+r'\, Rut (.*?)(\.\s|\;\s)',content, re.DOTALL).group(1) 
                            diccionario_nombres["rut"]=rutaccionistasunoauno

                            
                
                            firmaunitaria={
                                "rut":rutseparadoSII,
                                "nombre":contenidoletras,
                                "firmado":"Firmado electrónicamente el "+fechadiames,
                                "anotacion":""
                            }

                            firmasconrut.append(firmaunitaria)
                            diccionario_nombres["firmas"] = firmasconrut
                            errorcapturafirmantes="true"
                        except:
                            errorcapturafirmantes="false"

                        

                        

                            
                    for contenidoletras in  participacion1:
                        diccionario_nombres["participacion"]=participacion1
                    for contenidoletras in  participaciondinero:
                        diccionario_nombres["participacionDinero"]=participaciondinero
                   
                    diccionario_nombres["participacionExtraccion"]=contenidoletras
                        


                    for contenidoletras in nombres1:
                        nombresseparados=str(contenidoletras).split(" ")
                        countnombres=len(nombresseparados)

                        try:

                            if countnombres == 2:
                                diccionario_nombres["nombres"]=(nombresseparados[0])
                                diccionario_nombres["apellidoPaterno"]=(nombresseparados[1])
                                diccionario_nombres["apellidoMaterno"]="null"
                                errorcapturanombres="true"
                            if countnombres == 4:
                                errorcapturanombres="true"

                                
                                diccionario_nombres["nombres"]=(nombresseparados[0]+' '+nombresseparados[1])
                                diccionario_nombres["apellidoPaterno"]=(nombresseparados[2])
                                diccionario_nombres["apellidoMaterno"]=(nombresseparados[3])
                                
                            if countnombres == 5:
                                diccionario_nombres["nombres"]=(nombresseparados[0]+' '+nombresseparados[1]+' '+nombresseparados[2])
                                diccionario_nombres["apellidoPaterno"]=(nombresseparados[3])
                                diccionario_nombres["apellidoMaterno"]=(nombresseparados[4])
                                errorcapturanombres="true"
                            if countnombres == 6:
                                diccionario_nombres["nombres"]=(nombresseparados[0]+' '+nombresseparados[1]+' '+nombresseparados[2]+' '+nombresseparados[3])
                                diccionario_nombres["apellidoPaterno"]=(nombresseparados[4])
                                diccionario_nombres["apellidoMaterno"]=(nombresseparados[5])
                                errorcapturanombres="true"

                        except:
                            errorcapturanombres="false"


                            
                    
                    firmantesdetallelist.append(diccionario_nombres)
                    validador_accionistas = "true"
            else:   
                    accionistasv2="false"
                    articulo_referencia=""
                    
                    validador_accionistas="false"


            #fecha_formateada = 'Firmado electrónicamente el ' + fecha_formateada
            if (textoaccionistastrue=="false") or (validador_accionistas=="false") or (errorcapturafirmantes=="false") or (errorcapturanombres=="false"):
                erroraccionistas="true"
            else:
                erroraccionistas="false"



        except:
            erroraccionistas="true"
            validador_accionistas="false"
            accionistasv2="false"



        #endregion - ACCIONISTAS



        erroradminad="false"
        erroradmindi="false"
        erroradmingg="false"

        #region - ADMINISTRACIÓN
        try:
                
            articulo_6 = re.search(r'ARTÍCULO SEXTO:(.*?)(?=\s*ARTÍCULO SÉPTIMO:|$)', content, re.DOTALL).group(1)
            provisoriotruegenerico= re.search(r'provisorio', articulo_6, re.DOTALL)

            if provisoriotruegenerico:
                provisoriotrue="true"
            else:
                provisoriotrue="false"


            

            if articulo_6:
                errorconadmin="true"
                articuloadmin="articulo_6"
                referenciafrase = re.search(r'ARTÍCULO SEXTO:(.*?)(?=\.)', content, re.DOTALL).group(1)
                cantidad_administradores = 0
                cantidad_directores = 0
                cantidad_gerentes_generales = 0

                # Buscar número antes de la palabra clave y la palabra clave
                matches = re.finditer(r'(?:un|\d+)\s*(Director(?:es)?|Administrador(?:es)?|Gerente General(?:es)?)', referenciafrase)
                
                cantidad_administradores = 0
                cantidad_directores = 0
                cantidad_gerentes_generales = 0

                for match in matches:

                    cantidad_administradores_actual = 1 if match.group(0).split(' ')[0].startswith('un') else int(match.group(0).split(' ')[0])
                    tipo_administrador = match.group(0).split(' ')[1]

                    # Realizar suma según el tipo de administrador
                    if 'Administrador' in tipo_administrador:
                        cantidad_administradores += cantidad_administradores_actual
                    elif 'Director' in tipo_administrador:
                        cantidad_directores += cantidad_administradores_actual
                    elif 'Gerente General' in tipo_administrador:
                        cantidad_gerentes_generales += cantidad_administradores_actual

                sumaadministradores = cantidad_administradores + cantidad_directores + cantidad_gerentes_generales               



            else:
                errorconadmin="false"

            resultadocompleto= []

            rutfind={}
################
            if sumaadministradores>1:

                try:
 
                    frasead = re.search(r'Administrador(?:es)?:(.*?)$', articulo_6, re.DOTALL)
                    listfrasead=frasead.group(1).split(';')


                    for nombre_rut in listfrasead:
                        # Dividir cada nombre y rut por ','
                        nombread, rut_part = map(str.strip, nombre_rut.split(','))
                        nombresplit= nombread.split(' ')

                        if len(nombresplit)==2:
                            nombre1y2= nombresplit[0]
                            apellido1= nombresplit[1] 
                            apellido2= ""
                        else:
                            pass

                        if len(nombresplit)==3:
                            nombre1y2= nombresplit[0]+ ' ' + nombresplit[1]
                            apellido1= nombresplit[2] 
                            apellido2= ""
                        else:
                            pass

                        if len(nombresplit)==4:
                            nombre1y2= nombresplit[0]+ ' ' + nombresplit[1]
                            apellido1= nombresplit[2] 
                            apellido2= nombresplit[3] 
                        else:
                            pass

                        if len(nombresplit)==5:
                            nombre1y2= nombresplit[0]+ ' ' + nombresplit[1]+ ' ' + nombresplit[2]
                            apellido1= nombresplit[3] 
                            apellido2= nombresplit[4] 
                        else:
                            pass
                                               
                        
                        # Eliminar la palabra "Rut" y el espacio del inicio del rut
                        rutad = rut_part.replace("Rut", "").strip().split(' ')[0]

                        resultadotestad={

                        "tipo": "Administrador",
                        "provisorio": provisoriotrue,
                        "rut": rutad,
                        "nombre": nombread,
                        "comoAdministra": "representacion",
                        "nombres": nombre1y2,
                        "apellidoPaterno": apellido1,
                        "apellidoMaterno": apellido2,
                    }
                        resultadocompleto.append(resultadotestad)         
                        erroradminad="false"         

                except:
                    erroradminad="true"                   
                    pass


                try:
                    frasegg = re.search(r'Gerente(?:s) General(?:es):(.*?)$', articulo_6, re.DOTALL)
                    listfrasegg=frasegg.group(1).split(';')


                    for nombre_rut in listfrasegg:
                        # Dividir cada nombre y rut por ','
                        nombregg, rut_part = map(str.strip, nombre_rut.split(','))
                        nombresplit= nombregg.split(' ')

                        if len(nombresplit)==2:
                            nombre1y2= nombresplit[0]
                            apellido1= nombresplit[1] 
                            apellido2= ""
                        else:
                            pass

                        if len(nombresplit)==3:
                            nombre1y2= nombresplit[0]+ ' ' + nombresplit[1]
                            apellido1= nombresplit[2] 
                            apellido2= ""
                        else:
                            pass

                        if len(nombresplit)==4:
                            nombre1y2= nombresplit[0]+ ' ' + nombresplit[1]
                            apellido1= nombresplit[2] 
                            apellido2= nombresplit[3] 
                        else:
                            pass

                        if len(nombresplit)==5:
                            nombre1y2= nombresplit[0]+ ' ' + nombresplit[1]+ ' ' + nombresplit[2]
                            apellido1= nombresplit[3] 
                            apellido2= nombresplit[4] 
                        else:
                            pass                        
                        # Eliminar la palabra "Rut" y el espacio del inicio del rut
                        rutgg = rut_part.replace("Rut", "").strip().split(' ')[0]

                        resultadotestgg={

                        "tipo": "Administrador",
                        "provisorio": provisoriotrue,
                        "rut": rutgg,
                        "nombre": nombregg,
                        "nombres": nombre1y2,
                        "apellidoPaterno": apellido1,
                        "apellidoMaterno": apellido2,
                    }
                        resultadocompleto.append(resultadotestgg)         
                        erroradmingg="false"         

                except:
                
                    pass


                try:
                    frasedi = re.search(r'(Director(?:es):(.*?)$', articulo_6, re.DOTALL)
                    listfrasedi=frasedi.group(1).split(';')


                    for nombre_rut in listfrasedi:
                        # Dividir cada nombre y rut por ','
                        nombredi, rut_part = map(str.strip, nombre_rut.split(','))
                        nombresplit= nombregg.split(' ')

                        if len(nombresplit)==2:
                            nombre1y2= nombresplit[0]
                            apellido1= nombresplit[1] 
                            apellido2= ""
                        else:
                            pass

                        if len(nombresplit)==3:
                            nombre1y2= nombresplit[0]+ ' ' + nombresplit[1]
                            apellido1= nombresplit[2] 
                            apellido2= ""
                        else:
                            pass

                        if len(nombresplit)==4:
                            nombre1y2= nombresplit[0]+ ' ' + nombresplit[1]
                            apellido1= nombresplit[2] 
                            apellido2= nombresplit[3] 
                        else:
                            pass

                        if len(nombresplit)==5:
                            nombre1y2= nombresplit[0]+ ' ' + nombresplit[1]+ ' ' + nombresplit[2]
                            apellido1= nombresplit[3] 
                            apellido2= nombresplit[4] 
                        else:
                            pass                         
                        # Eliminar la palabra "Rut" y el espacio del inicio del rut
                        rutdi = rut_part.replace("Rut", "").strip().split(' ')[0]

                        resultadotestdi={

                        "tipo": "Administrador",
                        "provisorio": provisoriotrue,
                        "rut": rutdi,
                        "nombre": nombredi,
                        "comoAdministra": "representacion",
                        "nombres": nombre1y2,
                        "apellidoPaterno": apellido1,
                        "apellidoMaterno": apellido2,
                    }
                        resultadocompleto.append(resultadotestdi)
                        erroradmindi="false"         

                except:
                    
                    pass
              
            
  
############CUADNO ES UNO
            if sumaadministradores==1:


                if cantidad_gerentes_generales==1:

                    try:
                            
                        frasegg = re.search(r'El Gerente General será designado en estos estatutos, cuya individualización es: (.*?)$', articulo_6, re.DOTALL)

                        if frasegg:
                            textofrasegg = frasegg.group(1)

                            provisoriogg = re.search(r'provisorio', textofrasegg, re.DOTALL)


                            if provisoriogg:
                                provisorioggtrue = "true"
                            else:
                                provisorioggtrue = "false"





                        #gg1 =  re.findall(r'([^,]+)', textofrasegg, re.DOTALL)
                        gg1=textofrasegg.split(",")[0]

                        nombresplit= gg1.split(' ')

                        if len(nombresplit)==2:
                            nombre1y2= nombresplit[0]
                            apellido1= nombresplit[1] 
                            apellido2= ""
                        else:
                            pass

                        if len(nombresplit)==3:
                            nombre1y2= nombresplit[0]+ ' ' + nombresplit[1]
                            apellido1= nombresplit[2] 
                            apellido2= ""
                        else:
                            pass

                        if len(nombresplit)==4:
                            nombre1y2= nombresplit[0]+ ' ' + nombresplit[1]
                            apellido1= nombresplit[2] 
                            apellido2= nombresplit[3] 
                        else:
                            pass

                        if len(nombresplit)==5:
                            nombre1y2= nombresplit[0]+ ' ' + nombresplit[1]+ ' ' + nombresplit[2]
                            apellido1= nombresplit[3] 
                            apellido2= nombresplit[4] 
                        else:
                            pass

                        rutencontrado= re.findall(re.escape(gg1.strip()) + r',\sRut\s([0-9.-]+)[.,]', content)[0]

                        rutfind["rut"]=rutencontrado
                        resultadotestgg={

                            "tipo": "gerente general",
                            "provisorio": provisorioggtrue,
                            "rut": rutencontrado[1].strip(),
                            "nombre": gg1,
                            "comoAdministra": "individualmente",
                            "nombres": nombre1y2,
                            "apellidoPaterno": apellido1,
                            "apellidoMaterno": apellido2,
                        }
                        resultadocompleto.append(resultadotestgg)
                        erroradmingg="false"

                    except:
                        erroradmingg="true"
                    
                else:
                    
                    pass



                if cantidad_directores>0:
                    try:
                        frasedi = re.search(r'El Director será designado en estos estatutos, cuya individualización es: (.*?)$', articulo_6, re.DOTALL)
                        
                        if frasedi:
                            textofrasedi = frasedi.group(1)

                            provisoriodi = re.search(r'provisorio', textofrasedi, re.DOTALL)


                            if provisoriodi:
                                provisorioditrue = "true"
                            else:
                                provisorioditrue = "false"

                        #di1 =  re.findall(r'([^,]+)', textofrasedi, re.DOTALL)
                        di1=textofrasedi.split(",")[0]
                        nombresplit= di1.split(' ')

                        if len(nombresplit)==2:
                            nombre1y2= nombresplit[0]
                            apellido1= nombresplit[1] 
                            apellido2= ""
                        else:
                            pass

                        if len(nombresplit)==3:
                            nombre1y2= nombresplit[0]+ ' ' + nombresplit[1]
                            apellido1= nombresplit[2] 
                            apellido2= ""
                        else:
                            pass

                        if len(nombresplit)==4:
                            nombre1y2= nombresplit[0]+ ' ' + nombresplit[1]
                            apellido1= nombresplit[2] 
                            apellido2= nombresplit[3] 
                        else:
                            pass

                        if len(nombresplit)==5:
                            nombre1y2= nombresplit[0]+ ' ' + nombresplit[1]+ ' ' + nombresplit[2]
                            apellido1= nombresplit[3] 
                            apellido2= nombresplit[4] 
                        else:
                            pass



                        rutencontrado= re.findall(re.escape(di1.strip()) + r',\sRut\s([0-9.-]+)[.,]', content)[0]

                        rutfind["rut"]=rutencontrado
                        resultadotestdi={

                            "tipo": "gerente general",
                            "provisorio": provisorioditrue,
                            "rut": rutencontrado[1].strip(),
                            "nombre": di1,
                            "comoAdministra": "individualmente",
                            "nombres": nombre1y2,
                            "apellidoPaterno": apellido1,
                            "apellidoMaterno": apellido2,
                        }
                        resultadocompleto.append(resultadotestdi)
                        erroradmindi="false"

                    except:
                        erroradmindi="true"
                    
                else:
                    
                    pass

                
                if cantidad_administradores>0:
                    try:

                        frasead = re.search(r'El Administrador será designado en estos estatutos, cuya individualización es: (.*?)$', articulo_6, re.DOTALL)

                        if frasead:
                            textofrasead = frasead.group(1)

                            provisorioad = re.search(r'provisorio', textofrasead, re.DOTALL)


                            if provisorioad:
                                provisorioadtrue = "true"
                            else:
                                
                                provisorioadtrue = "false"


                        #ad1 =  re.findall(r'([^,]+)', textofrasead, re.DOTALL)
                        ad1=textofrasead.split(",")[0]
                        nombresplit= ad1.split(' ')

                        if len(nombresplit)==2:
                            nombre1y2= nombresplit[0]
                            apellido1= nombresplit[1] 
                            apellido2= ""
                        else:
                            pass

                        if len(nombresplit)==3:
                            nombre1y2= nombresplit[0]+ ' ' + nombresplit[1]
                            apellido1= nombresplit[2] 
                            apellido2= ""
                        else:
                            pass

                        if len(nombresplit)==4:
                            nombre1y2= nombresplit[0]+ ' ' + nombresplit[1]
                            apellido1= nombresplit[2] 
                            apellido2= nombresplit[3] 
                        else:
                            pass

                        if len(nombresplit)==5:
                            nombre1y2= nombresplit[0]+ ' ' + nombresplit[1]+ ' ' + nombresplit[2]
                            apellido1= nombresplit[3] 
                            apellido2= nombresplit[4] 
                        else:
                            pass

                        rutencontrado= re.findall(re.escape(ad1.strip()) + r',\sRut\s([0-9.-]+)[.,]', content)[0]

                        rutfind["rut"]=rutencontrado
                        resultadotestad={

                            "tipo": "gerente general",
                            "provisorio": provisorioadtrue,
                            "rut": rutencontrado[1].strip(),
                            "nombre": ad1,
                            "comoAdministra": "individualmente",
                            "nombres": nombre1y2,
                            "apellidoPaterno": apellido1,
                            "apellidoMaterno": apellido2,
                        }
                        resultadocompleto.append(resultadotestad)
                        erroradminad="false"
                    except:
                        erroradminad="true"
                    
                else:
                  
                   pass

            


            if (erroradminad== "true") or (erroradmindi== "true") or (erroradmingg== "true"):
                errorfataladmin="true"
            else:
                errorfataladmin="false"      

        except:
            errorfataladmin="true"  
            

        #endregion - ADMINISTRACION
        try:
            #region - CAPITAL

            articuloquinto= re.findall(r'ARTICULO QUINTO: (.*?) TITULO TERCERO:', content, re.DOTALL)
            
            if articuloquinto:
                capitaltrue= "true"
                articuloquintotrue="articulo_5"
                artquintofrase= articuloquinto[0]
                artquinto_monto= re.search(r'\$(.*?)\s', artquintofrase, re.DOTALL).group(1)


            else:
                articuloquintotrue=""
                capitaltrue="false"

            #endregion - Capital



            #region domicilio
            art_domicilio_match = re.search(r'ARTÍCULO SEGUNDO: DOMICILIO: (.*?)ARTÍCULO TERCERO', content, re.DOTALL | re.IGNORECASE)

            if art_domicilio_match:
                art_domicilio_true = "true"
                articulo_2="articulo_2"
                texto_domicilio = re.search(r'El domicilio de la Sociedad será(.*?)\s*,\s?sin perjuicio', art_domicilio_match.group(1), re.DOTALL | re.IGNORECASE).group(1)

            else:
                art_domicilio_true = "false"
                texto_domicilio=""
                articulo_2=""


            #endregion domicilio


            #region duracion


            duracion_text = re.search(r'ARTÍCULO TERCERO: DURACIÓN: (.*?) ARTÍCULO CUARTO: OBJETO:', content, re.DOTALL | re.IGNORECASE)

            if duracion_text:
                articuloduraciontrue = "true"

                duracion_match = re.search(r'La Sociedad comenzará a regir con esta fecha y tendrá una duración (.*?)\.', duracion_text.group(1), re.DOTALL)

            if duracion_match:
                duracion = duracion_match.group(1)
                art_tercero = "articulo_3"
                art_tercero_true = "true"

                esindefinida = re.search(r'indefinida', duracion, re.DOTALL | re.IGNORECASE)


                if esindefinida:
                    duracionindefinida = "indefinida"
                else:
                    duracionindefinida = "finita"
                    

                duraciontext2= re.search(r'ARTÍCULO TERCERO:\s*DURACIÓN:\s*(.*?)\.', content, re.DOTALL | re.IGNORECASE).group(1).strip()
            else:
                articuloduraciontrue="false"
                art_tercero_true="false"
                duracion=""

            #si duracion vioene con fecha definida, se debe generar un calculo para saber sie stá vencida o no.
            if (capitaltrue== "false") or (art_domicilio_true== "false")  or (articuloduraciontrue== "false"):
                errordomicilioduracion= "true"
            else:
                errordomicilioduracion="false"


        except:
            errordomicilioduracion= "true"


        #endregion duracion



        #region Facultades

        try:
            primerafrasefacultades = re.search(r'ARTÍCULO OCTAVO:\s*(.*?)\.', content, re.DOTALL ).group(1)

            if primerafrasefacultades:
                articulo_8="articulo_8"
                articulo8true= "true"

            else:
                articulo_8=""
                articulo8true="false"


            facultades= {}


            repreisntituciones= re.search(r'REPRESENTACION ANTE INSTITUCIONES\s*(.*?)\.', content, re.DOTALL )
            if repreisntituciones:
                try:
                    repreisntitucionestrue=1
                    facultades["REPRESENTACION ANTE INSTITUCIONES"]=repreisntituciones.group(1)

                except:
                    repreisntitucionestrue=0


            represociedadesyasoc= re.search(r'REPRESENTACIÓN ANTE SOCIEDADES Y ASOCIACIONES\s*(.*?)\.', content, re.DOTALL )

            if represociedadesyasoc:
                try:
                    represociedadesyasoctrue=1
                    facultades["REPRESENTACIÓN ANTE SOCIEDADES Y ASOCIACIONES"]=represociedadesyasoc.group(1)

                except:
                    represociedadesyasoctrue=0


            reprecelebcontrat= re.search(r'CELEBRACION DE CONTRATOS\s*(.*?)\.', content, re.DOTALL )
            if reprecelebcontrat:
                try:
                    reprecelebcontrattrue=1
                    facultades["CELEBRACION DE CONTRATOS"]=reprecelebcontrat.group(1)
                except:
                    reprecelebcontrattrue=0




            repreconstgarantias= re.search(r'CONSTITUCION DE GARANTIAS\s*(.*?)\.', content, re.DOTALL )
            if repreconstgarantias:
                try:
                    repreconstgarantiastrue=1
                    facultades["CONSTITUCION DE GARANTIAS"]=repreconstgarantias.group(1)
                except:
                    repreconstgarantiastrue=0



            reprecontrtrabajo= re.search(r'CONTRATOS DE TRABAJO\s*(.*?)\.', content, re.DOTALL )

            if reprecontrtrabajo:
                try:
                    reprecontrtrabajotrue=1
                    facultades["CONTRATOS DE TRABAJO"]=reprecontrtrabajo.group(1)
                except:
                    reprecontrtrabajotrue=0



            repreconstsociedades= re.search(r'CONSTITUCION DE SOCIEDADES\s*(.*?)\.', content, re.DOTALL )

            if repreconstsociedades:
                try:
                    repreconstsociedadestrue=1
                    facultades["CONSTITUCION DE SOCIEDADES"]=repreconstsociedades.group(1)
                except:
                    repreconstsociedadestrue=0


            reprecheques= re.search(r'OPERACIONES CON CHEQUES, LETRAS, PAGARES Y OTROS DOCUMENTOS MERCANTILES\s*(.*?)\.', content, re.DOTALL)

            if reprecheques:
                try:
                    reprechequestrue=1
                    facultades["OPERACIONES CON CHEQUES, LETRAS, PAGARES Y OTROS DOCUMENTOS MERCANTILES"]=reprecheques.group(1)
                except:
                    reprechequestrue=0


            reprecobrar= re.search(r'COBRAR Y PERCIBIR\s*(.*?)\.', content, re.DOTALL )

            if reprecobrar:
                try:
                    reprecobrartrue=1
                    facultades["COBRAR Y PERCIBIR"]=reprecobrar.group(1)
                except:
                    reprecobrartrue=0


            reprebancofinan= re.search(r'OPERACIONES CON BANCOS E INSTITUCIONES FINANCIERAS\s*(.*?)\.', content, re.DOTALL )

            if reprebancofinan:
                try:
                    reprebancofinantrue=1
                    facultades["OPERACIONES CON BANCOS E INSTITUCIONES FINANCIERAS"]=reprebancofinan.group(1)
                except:
                    reprebancofinantrue=0


            reprecreditos= re.search(r'CRÉDITOS\s*(.*?)\.', content, re.DOTALL)

            if reprecreditos:
                try:
                    reprecreditostrue=1
                    facultades["CREDITOS"]=reprecreditos.group(1)
                except:
                    reprecreditostrue=0

            reprederivados= re.search(r'DERIVADOS\s*(.*?)\.', content, re.DOTALL)

            if reprederivados:
                try:
                    reprederivadostrue=1
                    facultades["DERIVADOS"]=reprederivados.group(1)
                except:
                    reprederivadostrue =0



            represeguros= re.search(r'SEGUROS\s*(.*?)\.', content, re.DOTALL )

            if represeguros:
                try:
                    represegurostrue=1
                    facultades["SEGUROS"]=represeguros.group(1)
                except:
                    represegurostrue =0


            repreregistro= re.search(r'REGISTRO DE MARCAS\s*(.*?)\.', content, re.DOTALL )

            if repreregistro:
                try:
                    repreregistrotrue=1
                    facultades["REGISTRO DE MARCAS"]=repreregistro.group(1)
                except:
                    repreregistrotrue =0


            repreoperaciones= re.search(r'OPERACIONES DE COMERCIO EXTERIOR\s*(.*?)\.', content, re.DOTALL )

            if repreoperaciones:
                try:
                    repreoperacionestrue=1
                    facultades["OPERACIONES DE COMERCIO EXTERIOR"]=repreoperaciones.group(1)

                except:
                    repreoperacionestrue =0


            reprepagos= re.search(r'PAGOS Y EXTINCION DE OBLIGACIONES\s*(.*?)\.', content, re.DOTALL )

            if reprepagos:
                try:
                    reprepagostrue=1
                    facultades["PAGOS Y EXTINCION DE OBLIGACIONES"]=reprepagos.group(1)
                except:
                    reprepagostrue =0


            reprefirmas= re.search(r'FIRMA DE DOCUMENTOS Y RETIRO DE CORRESPONDENCIA.\s*(.*?)\.', content, re.DOTALL )

            if reprefirmas:
                try:
                    reprefirmastrue=1
                    facultades["FIRMA DE DOCUMENTOS Y RETIRO DE CORRESPONDENCIA"]=reprefirmas.group(1)
                except:
                    reprefirmastrue =0


            repremandatos= re.search(r'MANDATOS\s*(.*?)\.', content, re.DOTALL )


            if repremandatos:
                try:
                    repremandatostrue=1
                    facultades["MANDATOS"]=repremandatos.group(1)
                except:
                    repremandatostrue =0

            reprejudicial= re.search(r'REPRESENTACION JUDICIAL\s*(.*?)\.', content, re.DOTALL )

            if reprejudicial:
                try:
                    reprejudicialtrue=1
                    facultades["REPRESENTACION JUDICIAL"]=reprejudicial.group(1)

                except:
                    reprejudicialtrue =0

            repreauto= re.search(r'AUTOCONTRATACIÓN\s*(.*?)\.', content, re.DOTALL )

            if repreauto:
                try:
                    repreautotrue=1
                    facultades["AUTOCONTRATACION"]=repreauto.group(1)
                except:
                    repreautotrue =0

            facultados="null"  #REVISAR ALGUN DOCUMENTO QUE QUEDE COMO FACULTADOS ALGO
            errorfacultades="false"
        except:
            errorfacultades="true"


        #endregion facultades


        #NOMBRE DE FANTASIA


        try:
                
            articuloprimero = re.search(r'ARTÍCULO PRIMERO: NOMBRE: (.*?)ARTÍCULO SEGUNDO:', content, re.DOTALL)
            nombrefantasia= re.search(r'nombre de fantasía de\s*(.*?)\.', content, re.DOTALL )
            if nombrefantasia and articuloprimero:
                nombrefantasiatrue="true"
                articuloprimerotrue="articulo_1"
                nombrefantasia= re.search(r'nombre de fantasía de\s*(.*?)\.', content, re.DOTALL ).group(1)
                nombrerealempresa= re.search(r'"(.*?)"', articuloprimero.group(1), re.DOTALL ).group(1)

            else:
                nombrefantasiatrue="false"
                articuloprimerotrue=""
                nombrefantasia="null"


            if articuloprimero:
                articuloprimeroexiste="true"
                articuloprimerotrue="articulo_1"
                nombrerealempresa= re.search(r'"(.*?)"', articuloprimero.group(1), re.DOTALL ).group(1)

            else:
                articuloprimeroexiste="false"
                nombrerealempresa="null"
                articuloprimerotrue="articulo_1"
                articuloprimerotrue=""       



            articulocuarto = re.search(r'ARTÍCULO CUARTO: OBJETO: (.*?)TITULO SEGUNDO:', content, re.DOTALL)

            objetosentidad=[] 

            if articulocuarto:
                articulocuartotrue="true"
                articulocuartotexto="articulo_2"
                articulocuartoobjeto = re.search(r'El objeto de la sociedad será(.*?)\.', articulocuarto.group(1), re.DOTALL).group(1)
                objetoslist= articulocuartoobjeto.split(",")
                objetosentidad.extend(objetoslist)  
                countobjetos = len(objetoslist)
            
            else:
                articulocuartotrue= "false"
                articulocuartoobjeto= ""
                articulocuartotexto=""



            if (nombrefantasiatrue == "false") or (articuloprimeroexiste == "false") or (articulocuartotrue == "false"):
                errorfantasiaobjeto="true"
            else:
                errorfantasiaobjeto="false"


        except:
            errorfantasiaobjeto="true"










        try:

            getnetfaltantes=[]
            if reprecelebcontrat and reprecobrar:
                posgetnettrue="true"
            else:
                posgetnettrue="false"
                if reprecelebcontrat:
                    pass
                else:
                    getnetfaltantes.append("CELEBRACION DE CONTRATOS")
                if reprecobrar:
                    pass
                else:
                    getnetfaltantes.append("COBRAR Y PERCIBIR")



            lineacreditofaltantes=[]
            if reprecelebcontrat and reprebancofinan and reprecheques and repreconstgarantias and repremandatos:
                lineacreditotrue="true"
            else:
                lineacreditotrue="false"
                if reprecelebcontrat:
                    pass
                else:
                    lineacreditofaltantes.append("CELEBRACION DE CONTRATOS")
                if reprebancofinan:
                    pass
                else:
                    lineacreditofaltantes.append("OPERACIONES CON BANCOS E INSTITUCIONES FINANCIERAS")
                if reprecheques:
                    pass
                else:
                    lineacreditofaltantes.append("OPERACIONES CON CHEQUES, LETRAS, PAGARES Y OTROS DOCUMENTOS MERCANTILES")
                if repreconstgarantias:
                    pass
                else:
                    lineacreditofaltantes.append("CONSTITUCION DE GARANTIAS")
                if repremandatos:
                    pass
                else:
                    lineacreditofaltantes.append("MANDATOS")

                    




            tarjetacreditofaltantes=[]

            if reprecelebcontrat and reprebancofinan and reprecheques and repreconstgarantias and repremandatos:
                tarjetacreditotrue="true"
            else:
                tarjetacreditotrue="false"
                if reprecelebcontrat:
                    pass
                else:
                    tarjetacreditofaltantes.append("CELEBRACION DE CONTRATOS")
                if reprebancofinan:
                    pass
                else:
                    tarjetacreditofaltantes.append("OPERACIONES CON BANCOS E INSTITUCIONES FINANCIERAS")
                if reprecheques:
                    pass
                else:
                    tarjetacreditofaltantes.append("OPERACIONES CON CHEQUES, LETRAS, PAGARES Y OTROS DOCUMENTOS MERCANTILES")
                if repreconstgarantias:
                    pass
                else:
                    tarjetacreditofaltantes.append("CONSTITUCION DE GARANTIAS")
                if repremandatos:
                    pass
                else:
                    tarjetacreditofaltantes.append("MANDATOS")





            tarjetadebitofaltantes=[]

            if reprecelebcontrat and reprebancofinan and reprecheques and repreconstgarantias and repremandatos:
                tarjetadebitotrue="true"
            else:
                tarjetadebitotrue="false"
                if reprecelebcontrat:
                    pass
                else:
                    tarjetadebitofaltantes.append("CELEBRACION DE CONTRATOS")
                if reprebancofinan:
                    pass
                else:
                    tarjetadebitofaltantes.append("OPERACIONES CON BANCOS E INSTITUCIONES FINANCIERAS")
                if reprecheques:
                    pass
                else:
                    tarjetadebitofaltantes.append("OPERACIONES CON CHEQUES, LETRAS, PAGARES Y OTROS DOCUMENTOS MERCANTILES")
                if repreconstgarantias:
                    pass
                else:
                    tarjetadebitofaltantes.append("CONSTITUCION DE GARANTIAS")
                if repremandatos:
                    pass
                else:
                    tarjetadebitofaltantes.append("MANDATOS")


            ctacorrientefaltantes=[]



            if reprecelebcontrat and reprebancofinan :

                
                ctacorrientetrue="true"
            else:
                ctacorrientetrue="false"
                if reprecelebcontrat:
                    pass
                else:
                    ctacorrientefaltantes.append("CELEBRACION DE CONTRATOS")
                if reprebancofinan:
                    pass
                else:
                    ctacorrientefaltantes.append("OPERACIONES CON BANCOS E INSTITUCIONES FINANCIERAS")


            if (posgetnettrue=="true") and (lineacreditotrue=="true") and (tarjetacreditotrue=="true") and (tarjetadebitotrue=="true") and (ctacorrientetrue=="true"):
                todosproductostrue="true"
            else:
                todosproductostrue="false"

            errorproductos="false"
        except:

            errorproductos="true"


        errorproceso=  errorarticulos + errorestado + errorestudio + errorpreestudio + erroraccionistas + errordomicilioduracion + errorfacultades + errorfantasiaobjeto + errorproductos+ artirepetidostrue + errorfataladmin


        errorestry ={"errorarticulos":errorarticulos,
                    "errorestado":errorestado,
                    "errorestudio":errorestudio,
                    "errorpreestudio":errorpreestudio,
                    "erroraccionistas":erroraccionistas,
                    "errordomicilioduracion":errordomicilioduracion,
                    "errorfacultades": errorfacultades,
                    "errorfantasiaobjeto": errorfantasiaobjeto,
                    "errorproductos":errorproductos,
                    "artirepetidos":artirepetidostrue,
                    "errorfataladmin":errorfataladmin
        }

        errores_fallidos = [error for error, resultado in errorestry.items() if resultado == "true"]


        if errores_fallidos:
            errorfatal = "true"
            mensaje_error = f"Error en: {', '.join(errores_fallidos)}"
        else:
            errorfatal = "false"
            mensaje_error = "-"
        if "true" in errorproceso:
            errorfatal="true"

        else:
            errorfatal="false"


        if errorextraccion and errorfatal == "false":
            preaprobadofinal= "true"
        else:
            preaprobadofinal="false"




        # JSON


        data={
            "content1":
                content1,
            "content2": content2
                ,
            "data": {
                "estado": {
                    "ejecutivo": "testlegalbot",#modificar con la API
                    "estado": "finalizado",
                    "fecha": fecha_junta,
                    "id": 1, #modificar con la API
                    "preEstudio": "null", #modificar con la API
                    "razonSocial": razon_social,
                    "rut": rut_sociedad_solo
                },
                "estudio": {
                    "fechaEstudio": fecha_separada,
                    "rut": rut_sociedad_guion,
                    "tipoSociedad": tipoempresa,
                    "ultimaModificacion":fechamesdia,
                    "modificado": empresamodificada,
                    "transformado": empresatransformada,
                    "errorFatal": errorfatal,
                    "errorExtraccion": errorextraccion,
                    "disuelto": empresadisuelta,
                    "preAprobado": preaprobadofinal,
                    "mensajes": [],
                    "prestudios": [
                        {
                            "rut": rut_sociedad_guion,
                            "fecha": fechamesdia,
                            "cve": cve_match,
                            "preAprobado": preaprobadofinal,
                            "errorFatal": errorfatal,
                            "disuelto": empresadisuelta,
                            "mensajes": [],
                            "tipoActuacion": ultimoestadoempresa,
                            "tipoSociedad": tipo_entidad,
                            "firmas": {
                                "numero": 3, 
                                "tipo": "firmas",
                                "firmas": firmasconrut
                            },
                            "modificacion": {},# cuando es modificaicon se activa algo adiciona?
                            "anexos": [],
                            "articulosRepetidos": {
                                "ok": artirepetidostrue,
                                "mensajes": [],
                                "frasesReferencia": [],
                                "articulosReferencia": dict_articulos,
                                "valor": countarti
                            },
                            "accionistas": {
                                "ok": "false",
                                "mensajes": "null",
                                "frasesReferencia": "null",
                                "articulosReferencia": [
                                    "null"
                                ],
                                "valor": "null"
                            },
                            "administracion": {
                                "ok": errorconadmin,
                                "mensajes": [],
                                "frasesReferencia": [
                                    referenciafrase
                                ],
                                "articulosReferencia": [
                                articuloadmin 
                                ],
                                "valor": {
                                    "todosConRut": "true",
                                    "texto": referenciafrase,
                                    "comoAdministran": "individualmente",#de donde sale este dato?
                                    "quienAdministra": {
                                        "gg": cantidad_gerentes_generales,
                                        "ad": cantidad_administradores,
                                        "di": cantidad_directores,
                                        "todos": sumaadministradores
                                    },
                                    "administradores": resultadocompleto
                                }
                            },
                            "capital": {
                                "ok": capitaltrue,
                                "mensajes": [],
                                "frasesReferencia": [
                                    artquintofrase
                                ],
                                "articulosReferencia": [
                                    articuloquintotrue
                                ],
                                "valor": artquinto_monto
                            },
                            "domicilio": {
                                "ok": art_domicilio_true,
                                "mensajes": [],
                                "frasesReferencia": [
                                    texto_domicilio
                                ],
                                "articulosReferencia": [
                                    articulo_2
                                ],
                                "valor": texto_domicilio
                            },
                            "duracion": {
                                "ok": articuloduraciontrue,
                                "mensajes": [],
                                "frasesReferencia": [
                                    duracionindefinida
                                ],
                                "articulosReferencia": [
                                    art_tercero
                                ],
                                "valor": {
                                    "texto": duraciontext2,
                                    "tags": [
                                        duracion
                                    ],
                                    "finalizada": "false" #CUANDO EXISTA UNA CON FECHA DEFINIDA CALCULAR  UN TRUE O FALSE SEGUN SEA
                                }
                            },
                            "facultades": {
                                "ok": articulo8true,#AGREGAR
                                "mensajes": [],
                                "frasesReferencia": [],
                                "articulosReferencia": [
                                    articulo_8
                                ],
                                
                                "valor": {
                                    "facultades":facultades,
                                    "facultados": facultados,  # REVISAR CUANDO EXISTA ALGUN FACULTADO
                                    "inicio": primerafrasefacultades

                                }
                            },
                            "nombreFantasia": {
                                "ok": nombrefantasiatrue,
                                "mensajes": [],
                                "frasesReferencia": [
                                    nombrefantasia
                                ],
                                "articulosReferencia": [
                                    articuloprimerotrue
                                ],
                                "valor": nombrefantasia
                            },
                            "objeto": {
                                "ok": articulocuartotrue,
                                "mensajes": countobjetos,
                                "frasesReferencia": [
                                    articulocuartoobjeto
                                ],
                                "articulosReferencia": [
                                    articulocuartotexto
                                ],
                                "valor": objetosentidad
                            },
                            "razonSocial": {
                                "ok": articuloprimeroexiste,
                                "mensajes": [],
                                "frasesReferencia": [
                                    nombrerealempresa
                                ],
                                "articulosReferencia": [
                                    "articulo_1"
                                ],
                                "valor": nombrerealempresa
                            }
                        }
                    ],
                    "customer": "santander", #esto viene de la API--------------------------------------------
                    "fechaCambioAdministracion": fechamesdia,
                    "santander": {
                        "disuelto": empresadisuelta,
                        "preAprobado": todosproductostrue,
                        "algunaEncontrada": todosproductostrue,
                        "matrizProductos": [
                            {
                                "producto": "POS getnet",
                                "facultadesNecesarias": [
                                    "CELEBRACION DE CONTRATOS",
                                    "COBRAR Y PERCIBIR"
                                ],
                                "facultadesFaltantes": getnetfaltantes,
                                "ok": posgetnettrue
                            },
                            {
                                "producto": "Línea de crédito",
                                "facultadesNecesarias": [
                                    "CELEBRACION DE CONTRATOS",
                                    "OPERACIONES CON BANCOS E INSTITUCIONES FINANCIERAS",
                                    "OPERACIONES CON CHEQUES, LETRAS, PAGARES Y OTROS DOCUMENTOS MERCANTILES",
                                    "CONSTITUCION DE GARANTIAS",
                                    "MANDATOS"
                                ],
                                "facultadesFaltantes": lineacreditofaltantes,
                                "ok": lineacreditotrue
                            },
                            {
                                "producto": "Tarjeta de crédito",
                                "facultadesNecesarias": [
                                    "CELEBRACION DE CONTRATOS",
                                    "OPERACIONES CON BANCOS E INSTITUCIONES FINANCIERAS",
                                    "OPERACIONES CON CHEQUES, LETRAS, PAGARES Y OTROS DOCUMENTOS MERCANTILES",
                                    "CONSTITUCION DE GARANTIAS",
                                    "MANDATOS"
                                ],
                                "facultadesFaltantes": tarjetacreditofaltantes,
                                "ok": tarjetacreditotrue
                            },
                            {
                                "producto": "Tarjeta de débito",
                                "facultadesNecesarias": [
                                    "CELEBRACION DE CONTRATOS",
                                    "OPERACIONES CON BANCOS E INSTITUCIONES FINANCIERAS",
                                    "OPERACIONES CON CHEQUES, LETRAS, PAGARES Y OTROS DOCUMENTOS MERCANTILES",
                                    "CONSTITUCION DE GARANTIAS",
                                    "MANDATOS"
                                ],
                                "facultadesFaltantes": tarjetadebitofaltantes,
                                "ok": tarjetadebitotrue
                            },
                            {
                                "producto": "Cuenta corriente",
                                "facultadesNecesarias": [
                                    "CELEBRACION DE CONTRATOS",
                                    "OPERACIONES CON BANCOS E INSTITUCIONES FINANCIERAS"
                                ],
                                "facultadesFaltantes": ctacorrientefaltantes,
                                "ok": ctacorrientetrue
                            }
                        ],
                        "razonSocial": nombrerealempresa,
                        "rut": rut_sociedad_guion,
                        "administradores": resultadocompleto,
                        "grupos": [
                            {
                                "nombre": 1,
                                "administradores": resultadocompleto
                            }
                        ],
                        "limitaciones": [],
                        "matrizPoderes": [
                            {
                                "gruposFirmantes": [
                                    [
                                        [
                                            "1",
                                            1
                                        ]
                                    ]
                                ],
                                "facultades": [
                                    1,
                                    2,
                                    3,
                                    4,
                                    5,
                                    6,
                                    7,
                                    8,
                                    9,
                                    10,
                                    11,
                                    12,
                                    13,
                                    14,
                                    15,
                                    16,
                                    17,
                                    18,
                                    19,
                                    20,
                                    26,
                                    27,
                                    28,
                                    29,
                                    30,
                                    31,
                                    32,
                                    33,
                                    34,
                                    35,
                                    36,
                                    37,
                                    38,
                                    39,
                                    40,
                                    41,
                                    42,
                                    43,
                                    44,
                                    45,
                                    46,
                                    47,
                                    48,
                                    49,
                                    50,
                                    51,
                                    53,
                                    54,
                                    55,
                                    56,
                                    57,
                                    58,
                                    59,
                                    60,
                                    61,
                                    62,
                                    64,
                                    65,
                                    68,
                                    69,
                                    70
                                ],
                                "limitaciones": []
                            }
                        ],
                        "facultades": [
                            1,
                            2,
                            3,
                            4,
                            5,
                            6,
                            7,
                            8,
                            9,
                            10,
                            11,
                            12,
                            13,
                            14,
                            15,
                            16,
                            17,
                            18,
                            19,
                            20,
                            26,
                            27,
                            28,
                            29,
                            30,
                            31,
                            32,
                            33,
                            34,
                            35,
                            36,
                            37,
                            38,
                            39,
                            40,
                            41,
                            42,
                            43,
                            44,
                            45,
                            46,
                            47,
                            48,
                            49,
                            50,
                            51,
                            53,
                            54,
                            55,
                            56,
                            57,
                            58,
                            59,
                            60,
                            61,
                            62,
                            64,
                            65,
                            68,
                            69,
                            70
                        ]
                    }
                },
                "ok": preaprobadofinal,
                "id": 1
            },
            "mensaje": mensaje_error,
            "ok": preaprobadofinal
        }


        self.guardar_json(data, rut_sociedad_solo) 

    def guardar_json(self, data, rut_sociedad_solo):


        with open('./jsons/'+rut_sociedad_solo + '.json', 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
        spa_mod_instance = SPA_Mod()
        spa_mod_instance.ejecutar()

