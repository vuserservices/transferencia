
import fitz
import datetime
import re
import json
from datetime import datetime
import requests
import os
import time

class EIRL:
    def __init__(self):

        pass

    def ejecutar(self):

        inicio = datetime.now()



        try:


            #test1= pdfx.PDFx(file)
            #urlpdf=(test1.get_references_as_dict()["url"][2])


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

            Search_PJ = re.search(r'DE (SOCIEDAD POR ACCIONES|EMPRESA INDIVIDUAL DE RESPONSABILIDAD LIMITADA|SOCIEDAD DE RESPONSABILIDAD LIMITADA) (.*?) (SpA|EMPRESA INDIVIDUAL DE RESPONSABILIDAD LIMITADA|SOCIEDAD DE RESPONSABILIDAD LIMITADA|(?:.*?LIMITADA))', content, re.DOTALL)

            #####
            match_EIRL=re.search(r'EMPRESA INDIVIDUAL DE RESPONSABILIDAD LIMITADA',Search_PJ.group(3), re.DOTALL)
            match_SPA=re.search(r'SpA',Search_PJ.group(3), re.DOTALL)
            if match_EIRL:
                match_LTDA=None
            else:
                match_LTDA = re.search(r'(SOCIEDAD DE RESPONSABILIDAD LIMITADA|(?:.*?LIMITADA))', Search_PJ.group(3), re.DOTALL)

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
                match_LTDA="false"

            if (match_EIRL=="false") and (match_SPA=="false") and (match_LTDA=="false"):
                errorarticulos="true"
            else:
                errorarticulos="false"

        except:
            errorarticulos="true"
        


        #endregion ARTICULOS



        try:
            #region - ESTADO
            rut_sociedad_completo = re.search(r'Rut\s(.*?)\s', content,re.DOTALL).group(1)
            rut_sociedad_solo = rut_sociedad_completo.replace('.','').replace('-','')
            rut_sociedad_guion = rut_sociedad_completo.replace('.','')
            estado_empresav2= re.search(r'(.*?)DE', content, re.DOTALL)
            estado_empresav2=estado_empresav2.group(1).strip()
            razon_social = re.search(r'DE (SOCIEDAD POR ACCIONES|EMPRESA INDIVIDUAL DE RESPONSABILIDAD LIMITADA|SOCIEDAD DE RESPONSABILIDAD LIMITADA) (.+?) (SpA|EMPRESA INDIVIDUAL DE RESPONSABILIDAD LIMITADA|SOCIEDAD DE RESPONSABILIDAD LIMITADA|E.I.R.L.)', content, re.DOTALL)           
            
            if estado_empresav2!="TRANSFORMACIÓN":

                razon_social = razon_social.group(2)+' '+razon_social.group(3)
                razonsocialtrue="true"
            
            else:
                pass


            if estado_empresav2=="TRANSFORMACIÓN":

                razon_social = re.search(r'DE (SOCIEDAD POR ACCIONES|EMPRESA INDIVIDUAL DE RESPONSABILIDAD LIMITADA|SOCIEDAD DE RESPONSABILIDAD LIMITADA) (.+?) (SpA|EMPRESA INDIVIDUAL DE RESPONSABILIDAD LIMITADA|SOCIEDAD DE RESPONSABILIDAD LIMITADA|E.I.R.L.)(.+?)(SpA|EMPRESA INDIVIDUAL DE RESPONSABILIDAD LIMITADA|SOCIEDAD DE RESPONSABILIDAD LIMITADA|E.I.R.L.)', content, re.DOTALL)  
                razon_social=razon_social.group(4)+ razon_social.group(5)
                razonsocialtrue="true"
            
            else:
                pass

            #AGRRGAR QUE FIGURE EL TIPO DE PJ QUE ES...




            fecha_junta = inicio.strftime("%Y%m%d%H%M%S%f")

            fecha_match = re.search(r'Chile, (\d{1,2} de [^\d]+\d{4})', content)

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
            razonsocialtrue="false"





        #endregion ESTADO



        #region - ESTUDIO
        try:

            estado_empresav2= re.search(r'(.*?)DE', content, re.DOTALL)
            fecha_empresav2= re.search(r'Chile\, (.*?)'+re.escape(estado_empresav2.group(1)),content, re.DOTALL)

            ultimafechamodificacion=fecha_empresav2.group(1)

            meses = {
                'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04',
                'mayo': '05', 'junio': '06', 'julio': '07', 'agosto': '08',
                'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12'
            }
            for nombre_mes, numero_mes in meses.items():
                ultimafechamodificacion=ultimafechamodificacion.replace(nombre_mes,numero_mes).replace(' del ','-').replace(' de ','-').strip()
            
            ultimoestadoempresa=estado_empresav2.group(1).strip()

            fechamesdia = datetime.strptime(ultimafechamodificacion, "%d-%m-%Y")
            fecha_separada = inicio.strftime("%Y-%m-%d %H:%M:%S.%f")

            fechadiames=fechamesdia.strftime("%d-%m-%Y")
            fechamesdia=fechamesdia.strftime("%Y-%m-%d")


            searchmodificacion=""
            empresadisuelta = "false"

            if ultimoestadoempresa=="MODIFICACIÓN":
                empresamodificada="true"
                #searchmodificacion=re.search(r"Después de la modificación(.*?)Electrónico de Empresas",content,re.DOTALL).group(1)
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

            if ultimoestadoempresa=="DISOLUCIÓN":
                empresadisuelta="true"
            else:
                empresadisuelta="false"      


            sociedad_coincidencia= re.search(r'DE (.*?) (SpA|EMPRESA INDIVIDUAL DE RESPONSABILIDAD LIMITADA|SOCIEDAD DE RESPONSABILIDAD LIMITADA|E.I.R.L.)', content, re.DOTALL)


            if sociedad_coincidencia:
                tipo_entidad= sociedad_coincidencia.group(2)
                entidadtrue= "true"
            else:
                tipo_entidad=None
                entidadtrue= "false"


            
            if (empresaconstituida =="false") and (empresamodificada =="false") and empresatransformada =="false" and (empresadisuelta =="false") and (entidadtrue =="false"):
                errorestudio= "true"
            else:
                errorestudio="false"

        except:
            errorestudio="true"


        #endregion - ESTUDIO


        #region articulos repetidos

        try:

            dict_articulos={}
            list_articulos=["ARTÍCULO PRIMERO DEL NOMBRE O RAZON SOCIAL:",
                            "ARTÍCULO SEGUNDO OBJETO:",
                            "ARTÍCULO TERCERO DOMICILIO:",
                            "ARTÍCULO CUARTO DURACIÓN:",
                            "ARTÍCULO QUINTO DEL CAPITAL SOCIAL:",
                            "ARTÍCULO SEXTO DE LA RESPONSABILIDAD DEL SOCIO:",
                            "ARTÍCULO SÉPTIMO DE LA ADMINISTRACIÓN:",
                            "ARTÍCULO OCTAVO DE LOS PODERES CONFERIDOS AL ADMINISTRADOR:",
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

        

        #endregion articulos repetidos


        #region - prestudio

        try:

            actuacion_match = re.search(r'(.*?)DE', content, re.DOTALL)
            firmantesEIRL=re.search(r'(compareció:|comparece:)(.*?)\,', content, re.DOTALL)
            firmantesEIRLRUT= re.search(r'\, Rut (.*?)\,', content, re.DOTALL)



            if actuacion_match and firmantesEIRL and firmantesEIRLRUT:
                actuacion_find = actuacion_match.group(1)
                firmantesEIRLRUT=firmantesEIRLRUT.group(1).strip()
                firmantesEIRL= firmantesEIRL.group(2).strip()
                errorpreestudio="false"
                firmanteseirltrue="true"
                firmaelectronica= 'Firmado electrónicamente por '+firmantesEIRL
                
                
            else:
                actuacion_find = ""
                errorpreestudio="true"
                firmanteseirltrue="false"
                firmaelectronica=""

        except:
            errorpreestudio="true"


        #endregion - prestudio
        #region - ACCIONISTAS
        try:
            texto_accionistasrepresentantesSIIv1match= re.search(r'ARTÍCULO QUINTO DEL CAPITAL\s+SOCIAL: (.*?)ARTÍCULO SEXTO DE LA RESPONSABILIDAD DEL\s+SOCIO', content, re.DOTALL)
            textoletraA= re.search(r'A\) (.*?)\;',texto_accionistasrepresentantesSIIv1match.group(1), re.DOTALL)

            firmantesEIRL=re.search(r'(.*?) (tiene|se obliga)',textoletraA.group(1), re.DOTALL)
 
            if texto_accionistasrepresentantesSIIv1match and textoletraA and firmantesEIRL:
                texto_accionistasrepresentantesSIIv1=texto_accionistasrepresentantesSIIv1match.group(1)
                textoletraA= textoletraA.group(1)
                firmantesEIRL=firmantesEIRL.group(1)
                participacionletraA= re.search(r'El capital de la Empresa es la cantidad de (.*?)\s',texto_accionistasrepresentantesSIIv1match.group(1), re.DOTALL).group(1).replace('$','').replace('CL','').replace(' pesos','').strip()
                articulo5true="articulo_5"
                articulo5capital="true"


            else:
                textoletraA==""
                articulo5true=""
                articulo5capital="false"
                participacionletraA=""
                texto_accionistasrepresentantesSIIv1=""



            #endregion -Accionistas


            firmantessplit=len(firmantesEIRL.split(" "))


            try:
                if firmantessplit==2:
                    nombresfirmante=firmantesEIRL.split(" ")[0]
                    apellidopaternofirmante= firmantesEIRL.split(" ")[1]
                    appellidomaternofirmante= "null"
                    errorconnombres="true"
                else:
                    pass

                if firmantessplit==3:
                    nombresfirmante=firmantesEIRL.split(" ")[0]+" "+firmantesEIRL.split(" ")[1]
                    apellidopaternofirmante= firmantesEIRL.split(" ")[2]
                    appellidomaternofirmante= "null"
                    errorconnombres="true"

                else:
                    pass

                if firmantessplit==4:
                    nombresfirmante=firmantesEIRL.split(" ")[0]+" "+firmantesEIRL.split(" ")[1]
                    apellidopaternofirmante= firmantesEIRL.split(" ")[2]
                    appellidomaternofirmante= firmantesEIRL.split(" ")[3]
                    errorconnombres="true"
                else:
                    pass

                if firmantessplit==5:
                    nombresfirmante=firmantesEIRL.split(" ")[0]+" "+firmantesEIRL.split(" ")[1]+" "+firmantesEIRL.split(" ")[2]
                    apellidopaternofirmante= firmantesEIRL.split(" ")[3]
                    appellidomaternofirmante= firmantesEIRL.split(" ")[4]
                    errorconnombres="true"
                else:
                    pass

                if firmantessplit==6:
                    nombresfirmante = firmantesEIRL.split(" ")[0]+" "+firmantesEIRL.split(" ")[1]+" "+firmantesEIRL.split(" ")[2]+" "+firmantesEIRL.split(" ")[3]
                    apellidopaternofirmante = firmantesEIRL.split(" ")[4]
                    appellidomaternofirmante= firmantesEIRL.split(" ")[5]
                    errorconnombres="true"
                else:
                    pass

                if firmantessplit>6:
                    errorconnombres="false"
                else:
                    pass



            except:
                errorconnombres="false"
                
               




            articuloseptoaoctavo=re.search(r'ARTÍCULO SÉPTIMO DE LA ADMINISTRACIÓN:(.*?)ARTÍCULO OCTAVO DE LOS PODERES\s+CONFERIDOS AL ADMINISTRADOR:', content, re.DOTALL)
            
            if articuloseptoaoctavo:
                provisoriomatch=re.search(r'provisorio',articuloseptoaoctavo.group(1), re.DOTALL)
                if provisoriomatch:
                    provisoriotrue="true"
                else:
                    provisoriotrue="false"
            else:
                provisoriotrue="false"




            textoadministracionmatch= re.search(r'ARTÍCULO SÉPTIMO DE LA ADMINISTRACIÓN:(.*?)\.\s', content, re.DOTALL)

            if textoadministracionmatch:
                textoadministraciontrue="true"
                articulo7true="articulo_7"
                textoadministracion=textoadministracionmatch.group(1)
            else:
                textoadministraciontrue="false"
                articulo7true=""
            

            if articulo5capital=="false" or errorconnombres=="false" or  textoadministraciontrue=="false":
                erroraccionistas="true"
            else:
                erroraccionistas="false"


            

        except:
        
            erroraccionistas="true"





        #DURACION 



        try:
                #domicilio
            textodomiciliocompleto= re.search(r'DOMICILIO:(.*?)ARTÍCULO CUARTO DURACIÓN', content, re.DOTALL)

            if textodomiciliocompleto:
                textodomiciliomatch="true"
                articulo3true="articulo_3"
                textodomicilio= re.search(r'El domicilio de la Empresa es (.*?), sin perjuicio', textodomiciliocompleto.group(1), re.DOTALL).group(1)


            else: 
                textodomiciliomatch="false"
                articulo3true=""
                textodomicilio= ""

            articuloduracion= re.search(r'ARTÍCULO CUARTO DURACIÓN:(.*?) ARTÍCULO QUINTO DEL CAPITAL\s+SOCIAL', content, re.DOTALL)


            if articuloduracion:
                articuloduraciontrue="true"
                articuloduracioncompleto= articuloduracion.group(1).replace(',','')
                esindefinida= re.search(r'indefinida.',articuloduracioncompleto,re.DOTALL)
                if esindefinida:
                    duracionindefinida="indefinida"
                else:
                    duracionindefinida="finita"
                    articuloduraciontrue="false"

                articulo4trueduracion="articulo_4"
            else:
                articuloduraciontrue="false"
                duracionentiempo= ""
                articulo4trueduracion=""
                
            errordomicilioduracion="false"




            articuloduracion= re.search(r'ARTÍCULO CUARTO DURACIÓN:(.*?) ARTÍCULO QUINTO DEL CAPITAL SOCIAL', content, re.DOTALL)


            if articuloduracion:
                articuloduraciontrue="true"
                articuloduracioncompleto= articuloduracion.group(1).replace(',','')
                duracionentiempo= re.search(r',([^,]+)\.', articuloduracion.group(1), re.DOTALL).group(1).strip()
                articulo4trueduracion="articulo_4"
            else:
                articuloduraciontrue="false"
                duracionentiempo= ""
                articulo4trueduracion=""

            if articuloduraciontrue=="false" or textodomiciliomatch== "false":
                errordomicilioduracion= "true"
            else:
                errordomicilioduracion="false"


        except:
            errordomicilioduracion="true"









        #region Facultades
        facultados="null"
        try:
            primerafrasefacultades = re.search(r'ARTÍCULO OCTAVO DE LOS PODERES\s+CONFERIDOS AL ADMINISTRADOR', content, re.DOTALL )

            if primerafrasefacultades:
                articulo_8="articulo_8"
                articulo8true= "true"

            else:
                articulo_8=""
                articulo8true="false"



            facultades= {}
            if primerafrasefacultades:
                repreisntituciones= re.search(r'REPRESENTACION ANTE INSTITUCIONES(\.|\s)(.*?)\.', content, re.DOTALL )
                
                if repreisntituciones:
                    repreisntitucionestrue=1
                    facultades["REPRESENTACION ANTE INSTITUCIONES"]=repreisntituciones.group(2)

                else:
                    repreisntitucionestrue=0


                represociedadesyasoc= re.search(r'REPRESENTACIÓN ANTE SOCIEDADES Y ASOCIACIONES(\.|\s)(.*?)\.', content, re.DOTALL )

                if represociedadesyasoc:
                    represociedadesyasoctrue=1
                    facultades["REPRESENTACIÓN ANTE SOCIEDADES Y ASOCIACIONES"]=represociedadesyasoc.group()

                else:
                    represociedadesyasoctrue=0

                reprecelebcontrat= re.search(r'CELEBRACION DE CONTRATOS(\.|\s)(.*?)\.', content, re.DOTALL )
                if reprecelebcontrat:
                    reprecelebcontrattrue=1
                    facultades["CELEBRACION DE CONTRATOS"]=reprecelebcontrat.group(2)
                else:
                    reprecelebcontrattrue=0

                


                repreconstgarantias= re.search(r'CONSTITUCION DE GARANTIAS(\.|\s)(.*?)\.', content, re.DOTALL )
                if repreconstgarantias:
                    repreconstgarantiastrue=1
                    facultades["CONSTITUCION DE GARANTIAS"]=repreconstgarantias.group(2)
                else:
                    repreconstgarantiastrue=0



                reprecontrtrabajo= re.search(r'CONTRATOS DE TRABAJO(\.|\s)(.*?)\.', content, re.DOTALL )

                if reprecontrtrabajo:
                    reprecontrtrabajotrue=1
                    facultades["CONTRATOS DE TRABAJO"]=reprecontrtrabajo.group(2)
                else:
                    reprecontrtrabajotrue=0



                repreconstsociedades= re.search(r'CONSTITUCION DE SOCIEDADES(\.|\s)(.*?)\.', content, re.DOTALL )

                if repreconstsociedades:
                    repreconstsociedadestrue=1
                    facultades["CONSTITUCION DE SOCIEDADES"]=repreconstsociedades.group(2)
                else:
                    repreconstsociedadestrue=0


                reprecheques= re.search(r'OPERACIONES CON CHEQUES, LETRAS, PAGARES Y OTROS DOCUMENTOS MERCANTILES(\.|\s)(.*?)\.', content, re.DOTALL)

                if reprecheques:
                    reprechequestrue=1
                    facultades["OPERACIONES CON CHEQUES, LETRAS, PAGARES Y OTROS DOCUMENTOS MERCANTILES"]=reprecheques.group(2)
                else:
                    reprechequestrue=0


                reprecobrar= re.search(r'COBRAR Y PERCIBIR(\.|\s)(.*?)\.', content, re.DOTALL )

                if reprecobrar:
                    reprecobrartrue=1
                    facultades["COBRAR Y PERCIBIR"]=reprecobrar.group(2)
                else:
                    reprecobrartrue=0


                reprebancofinan= re.search(r'OPERACIONES CON BANCOS E INSTITUCIONES FINANCIERAS(\.|\s)(.*?)\.', content, re.DOTALL )
                if reprebancofinan:
                    reprebancofinantrue=1
                    facultades["OPERACIONES CON BANCOS E INSTITUCIONES FINANCIERAS"]=reprebancofinan.group(2)
                else:
                    reprebancofinantrue=0


                reprecreditos= re.search(r'CRÉDITOS(\.|\s)(.*?)\.', content, re.DOTALL)

                if reprecreditos:
                    reprecreditostrue=1
                    facultades["CREDITOS"]=reprecreditos.group(2)
                else:
                    reprecreditostrue=0

                reprederivados= re.search(r'DERIVADOS(\.|\s)(.*?)\.', content, re.DOTALL)

                if reprederivados:
                    reprederivadostrue=1
                    facultades["DERIVADOS"]=reprederivados.group(2)
                else:
                    reprederivadostrue =0



                represeguros= re.search(r'SEGUROS(\.|\s)(.*?)\.', content, re.DOTALL )

                if represeguros:
                    represegurostrue=1
                    facultades["SEGUROS"]=represeguros.group(2)
                else:
                    represegurostrue =0


                repreregistro= re.search(r'REGISTRO DE MARCAS(\.|\s)(.*?)\.', content, re.DOTALL )

                if repreregistro:
                    repreregistrotrue=1
                    facultades["REGISTRO DE MARCAS"]=repreregistro.group(2)
                else:
                    repreregistrotrue =0


                repreoperaciones= re.search(r'OPERACIONES DE COMERCIO EXTERIOR(\.|\s)(.*?)\.', content, re.DOTALL )

                if repreoperaciones:
                    repreoperacionestrue=1
                    facultades["OPERACIONES DE COMERCIO EXTERIOR"]=repreoperaciones.group(2)

                else:
                    repreoperacionestrue =0


                reprepagos= re.search(r'PAGOS Y EXTINCION DE OBLIGACIONES(\.|\s)(.*?)\.', content, re.DOTALL )

                if reprepagos:
                    reprepagostrue=1
                    facultades["PAGOS Y EXTINCION DE OBLIGACIONES"]=reprepagos.group(2)
                else:
                    reprepagostrue =0


                reprefirmas= re.search(r'FIRMA DE DOCUMENTOS Y RETIRO DE CORRESPONDENCIA(\.|\s)(.*?)\.', content, re.DOTALL )

                if reprefirmas:
                    reprefirmastrue=1
                    facultades["FIRMA DE DOCUMENTOS Y RETIRO DE CORRESPONDENCIA"]=reprefirmas.group(2)
                else:
                    reprefirmastrue =0


                repremandatos= re.search(r'MANDATOS(\.|\s)(.*?)\.', content, re.DOTALL )


                if repremandatos:
                    repremandatostrue=1
                    facultades["MANDATOS"]=repremandatos.group(2)
                else:
                    repremandatostrue =0

                reprejudicial= re.search(r'REPRESENTACION JUDICIAL(\.|\s)(.*?)\.', content, re.DOTALL )

                if reprejudicial:
                    reprejudicialtrue=1
                    facultades["REPRESENTACION JUDICIAL"]=reprejudicial.group(2)

                else:
                    reprejudicialtrue =0

                repreauto= re.search(r'AUTOCONTRATACIÓN(\.|\s)(.*?)\.', content, re.DOTALL )

                if repreauto:
                    repreautotrue=1
                    facultades["AUTOCONTRATACION"]=repreauto.group(2)
                else:
                    repreautotrue =0

                facultados="null"  #REVISAR ALGUN DOCUMENTO QUE QUEDE COMO FACULTADOS ALGO
            else:
                pass

            errorfacultades="false"
        except:
            errorfacultades="true"


        


        #endregion facultades



        #NOMBRE DE FANTASIA
        

        try:


            articuloprimero=re.search(r'ARTÍCULO PRIMERO DEL NOMBRE O RAZON SOCIAL:(.*?) ARTÍCULO SEGUNDO OBJETO', content, re.DOTALL )
            nombrefantasia= re.search(r'nombre de fantasía de\s*(.*?) ARTÍCULO SEGUNDO OBJETO', content, re.DOTALL )

            if nombrefantasia and articuloprimero:
                nombrefantasiatrue="true"
                articuloprimerotrue="articulo_1"
                nombrefantasia= re.search(r'nombre de fantasía de\s*(.*?) ARTÍCULO SEGUNDO OBJETO', content, re.DOTALL ).group(1)
                nombrerealempresa= re.search(r'"(.*?)"', articuloprimero.group(1), re.DOTALL ).group(1)

            else:
                nombrefantasiatrue="false"
                nombrefantasia="null"
                articuloprimerotrue=""

            if articuloprimero:
                articuloprimeroexiste="true"
                articuloprimerotrue="articulo_1"
                nombrerealempresa= re.search(r'"(.*?)"', articuloprimero.group(1), re.DOTALL ).group(1)

            else:
                articuloprimeroexiste="false"
                nombrerealempresa="null"
                articuloprimerotrue="articulo_1"
                articuloprimerotrue=""

            #objetode la entidad
            articulosegundocompleto= re.search(r'ARTÍCULO SEGUNDO OBJETO:(.*?) ARTÍCULO TERCERO', content, re.DOTALL )

            if articulosegundocompleto:
                articulosegundotrue= "true"
                articulo2texto="articulo_2"
                articulosegundoobjeto= re.search(r'desarrollar las siguientes actividades\:(.*?)\.', articulosegundocompleto.group(1), re.DOTALL ).group(1)
                objetoslist= articulosegundoobjeto.split(",")
                countobjetos = len(objetoslist)

            else:
                articulosegundotrue= "false"
                articulosegundoobjeto= ""
                articulo2texto=""

            if  articulosegundotrue=="false" or articuloprimeroexiste =="false":
                errorfantasiaobjeto="true"
            else:
                errorfantasiaobjeto="false"


        except:
            errorfantasiaobjeto="true"



        getnetfaltantes=[]
        lineacreditofaltantes=[]
        tarjetacreditofaltantes=[]
        tarjetadebitofaltantes=[]
        ctacorrientefaltantes=[]
        
        if  primerafrasefacultades:
            try:
            #formulas productos:
                
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


                

                if reprecelebcontrat and reprebancofinan:
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
                
                if posgetnettrue=="true" and lineacreditotrue=="true" and tarjetacreditotrue=="true" and tarjetadebitotrue=="true" and ctacorrientetrue=="true":
                    todosproductostrue="false"
                    preaprobacionproductos="true"
                else:
                    todosproductostrue="true"
                    preaprobacionproductos="false"


                

                errorproductos="false"
            except:
                errorproductos="true"
        else:
            posgetnettrue="false" 
            lineacreditotrue="false"
            tarjetacreditotrue="false"
            tarjetadebitotrue="false"
            ctacorrientetrue="false"
            errorproductos="true"
            todosproductostrue="true"
            preaprobacionproductos="false"

        errorproceso=  errorarticulos + errorestado + errorestudio + errorpreestudio + erroraccionistas + errordomicilioduracion + errorfacultades + errorfantasiaobjeto + errorproductos+ artirepetidostrue+todosproductostrue



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
                    "todosproductostrue":todosproductostrue
        }

        errores_fallidos = [error for error, resultado in errorestry.items() if resultado == "true"]

        if  errores_fallidos:
            errorfatal = "true"
            mensaje_error = f"Error en: {', '.join(errores_fallidos)}"
        else:
            errorfatal = "false"
            mensaje_error = "-"

        if "true" in errorproceso:
            errorfatal="true"

        else:
            errorfatal="false"


        if errorextraccion=="false" and errorfatal == "false":
            preaprobadofinal= "true"
        else:
            preaprobadofinal="false"


        ##############################################################


        data={
            "content1":
                content1
                ,
            "content2":
                content2
                ,                
            "data": {
                "estado": {
                    "ejecutivo": "testlegalbot",
                    "estado": "finalizado",
                    "fecha": fecha_junta,
                    "id": 49579, #ID se debe modificar con el pedido
                    "preEstudio": "null",
                    "razonSocial": razon_social,
                    "rut": rut_sociedad_solo
                },
                "estudio": {
                    "fechaEstudio": fecha_separada,
                    "rut": rut_sociedad_guion,
                    "tipoSociedad": tipoempresa,
                    "ultimaModificacion": fechamesdia, #revisar formula
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
                            "fecha":fechamesdia,
                            "cve": cve_match,
                            "preAprobado": preaprobadofinal, #Revisar si ambos deben ser el mismo 
                            "errorFatal": errorfatal,
                            "disuelto": empresadisuelta,
                            "mensajes": [],
                            "tipoActuacion": ultimoestadoempresa,
                            "tipoSociedad": tipoempresa,
                            "firmas": {
                                "numero": 3,
                                "tipo": "firmas",
                                "firmas": [
                                    {
                                        "rut": firmantesEIRLRUT,
                                        "nombre": firmantesEIRL,
                                        "firmado": firmaelectronica,
                                        "anotacion": ""
                                    }
                                ]
                            },
                            "modificacion": searchmodificacion,
                            "anexos": [],
                            "articulosRepetidos": {
                                "ok": artirepetidostrue,
                                "mensajes": [],
                                "frasesReferencia": [],
                                "articulosReferencia": dict_articulos,
                                "valor": countarti
                            },
                            "accionistas": {
                                "ok": "true",
                                "mensajes": [],
                                "frasesReferencia": [
                                    textoletraA
                                ],
                                "articulosReferencia": [
                                    articulo5true
                                ],
                                "valor": [
                                    {
                                        "nombre": firmantesEIRL,
                                        "participacion": 100,
                                        "participacionDinero": participacionletraA,
                                        "participacionExtraccion": textoletraA,
                                        "rut": firmantesEIRLRUT,
                                        "firmas": [
                                            {
                                                "rut": firmantesEIRLRUT,
                                                "nombre": firmantesEIRL,
                                                "firmado": firmaelectronica,
                                                "anotacion": ""
                                            }
                                        ],
                                        "nombres": nombresfirmante,
                                        "apellidoPaterno": apellidopaternofirmante,
                                        "apellidoMaterno": appellidomaternofirmante
                                    }
                                ]
                            },
                            "administracion": {
                                "ok": textoadministraciontrue,
                                "mensajes": [],
                                "frasesReferencia": [
                                    textoadministracion
                                ],
                                "articulosReferencia": [
                                    articulo7true
                                ],
                                "valor": {
                                    "todosConRut": firmanteseirltrue,
                                    "texto": textoadministracion,
                                    "comoAdministran": "individualmente",
                                    "quienAdministra": {
                                        "gg": 0,
                                        "ad": 1,
                                        "di": 0,
                                        "todos": 1
                                    },
                                    "administradores": [
                                        {
                                            "tipo": "administrador",
                                            "provisorio": provisoriotrue,#revisar si puede haber provisorio
                                            "rut": firmantesEIRLRUT,
                                            "nombre": firmantesEIRL,
                                            "comoAdministra": "individualmente",
                                            "nombres": nombresfirmante,
                                            "apellidoPaterno": apellidopaternofirmante,
                                            "apellidoMaterno": appellidomaternofirmante
                                        }
                                    ]
                                }
                            },
                            "capital": {
                                "ok": articulo5capital,
                                "mensajes": [],
                                "frasesReferencia": [
                                    texto_accionistasrepresentantesSIIv1
                                ],
                                "articulosReferencia": [
                                    articulo5true
                                ],
                                "valor": participacionletraA
                            },
                            "domicilio": {
                                "ok": textodomiciliomatch,
                                "mensajes": [],
                                "frasesReferencia": [
                                    textodomicilio
                                ],
                                "articulosReferencia": [
                                    articulo3true
                                ],
                                "valor": textodomicilio
                            },
                            "duracion": {
                                "ok": articuloduraciontrue,
                                "mensajes": [],
                                "frasesReferencia": [
                                    duracionindefinida,
                                ],
                                "articulosReferencia": [
                                    articulo4trueduracion
                                ],
                                "valor": {
                                    "texto": articuloduracioncompleto,
                                    "tags": [
                                        duracionentiempo,
                                    ],
                                    "finalizada": "false" #cuadno tenga un documento con fecha hayq ue calcularla
                                }
                            },
                            "facultades": {
                                "ok": articulo8true,
                                "mensajes": [],
                                "frasesReferencia": [],
                                "articulosReferencia": [
                                    articulo_8
                                ],
                                "valor": {
                                    "facultades": facultades,
                                    "facultados": facultados,
                                    "inicio": ""
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
                                "ok": articulosegundotrue,
                                "mensajes": [],
                                "frasesReferencia": [
                                    articulosegundoobjeto
                                ],
                                "articulosReferencia": [
                                    articulo2texto
                                ],
                                "valor": objetoslist
                            },
                            "razonSocial": {
                                "ok": articuloprimeroexiste,
                                "mensajes": [],
                                "frasesReferencia": [
                                    nombrerealempresa
                                ],
                                "articulosReferencia": [
                                    articuloprimerotrue
                                ],
                                "valor": nombrerealempresa
                            }
                        }
                    ],
                    "customer": "santander",
                    "fechaCambioAdministracion":fechamesdia,
                    "santander": {
                        "disuelto": empresadisuelta,
                        "preAprobado": preaprobacionproductos, # se preaprueban los productos?
                        "algunaEncontrada": preaprobacionproductos,
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
                        "razonSocial": razon_social,
                        "rut": rut_sociedad_guion,
                        "administradores": [
                            {
                                "tipo": "administrador",
                                "provisorio": provisoriotrue,
                                "rut": rut_sociedad_completo,
                                "nombre": firmantesEIRL,
                                "comoAdministra": "individualmente",
                                "nombres": nombresfirmante,
                                "apellidoPaterno": apellidopaternofirmante,
                                "apellidoMaterno": appellidomaternofirmante
                            }
                        ],
                        "grupos": [
                            {
                                "nombre": "1",
                                "administradores": [
                                    {
                                        "tipo": "administrador",
                                        "provisorio": provisoriotrue,
                                        "rut": rut_sociedad_completo,
                                        "nombre": firmantesEIRL,
                                        "comoAdministra": "individualmente",
                                        "nombres": nombresfirmante,
                                        "apellidoPaterno": apellidopaternofirmante,
                                        "apellidoMaterno": appellidomaternofirmante
                                    }
                                ]
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
                                    24,
                                    25,
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
                            24,
                            25,
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
        eirl_instance = EIRL()
        eirl_instance.ejecutar()


