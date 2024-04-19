
import fitz
import datetime
import re
import json
from datetime import datetime
import requests
import os

class LTDA:
    def __init__(self):

        pass

    def ejecutar(self):

        inicio = datetime.now()



        try:#try para saber si existe algun problema con la lectura de documento con fitz


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



        try:
            estado_empresav2= re.search(r'(.*?)DE', content, re.DOTALL)
            Search_PJ = re.search(r'DE (SOCIEDAD POR ACCIONES|EMPRESA INDIVIDUAL DE RESPONSABILIDAD LIMITADA|SOCIEDAD DE RESPONSABILIDAD LIMITADA) (.*?) (SpA|EMPRESA INDIVIDUAL DE RESPONSABILIDAD LIMITADA|SOCIEDAD DE RESPONSABILIDAD LIMITADA|(?:.*?LIMITADA))', content, re.DOTALL)
            #ESTO VA A CAMBIAR SOCIEDAD LIMITADA ES SOLO LIMITADA Y EEMPRESINDIVIDUAL ES EIRL EN LA SEGUNDA PARTE DEL GRUPO...

            #####
            match_EIRL=re.search(r'EMPRESA INDIVIDUAL DE RESPONSABILIDAD LIMITADA',Search_PJ.group(3), re.DOTALL)
            match_SPA=re.search(r'SpA',Search_PJ.group(3), re.DOTALL)
            match_LTDA= re.search(r'(SOCIEDAD DE RESPONSABILIDAD LIMITADA|(?:.*?LIMITADA))',Search_PJ.group(3), re.DOTALL)


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






        try:

            rut_sociedad_completo = re.search(r'Rut\s(.*?)\s', content,re.DOTALL).group(1)
            rut_sociedad_solo = rut_sociedad_completo.replace('.','').replace('-','')
            rut_sociedad_guion = rut_sociedad_completo.replace('.','')

            razon_social = re.search(r'DE (SOCIEDAD POR ACCIONES|EMPRESA INDIVIDUAL DE RESPONSABILIDAD LIMITADA|SOCIEDAD DE RESPONSABILIDAD LIMITADA) (.+?) (SpA|EMPRESA INDIVIDUAL DE RESPONSABILIDAD LIMITADA|SOCIEDAD DE RESPONSABILIDAD LIMITADA|LIMITADA)', content, re.DOTALL)                      
            #AGRRGAR QUE FIGURE EL TIPO DE PJ QUE ES...

            if razon_social:
                razon_social = razon_social.group(2)+' '+razon_social.group(3)
                razonsocialtrue="true"
            else:
                razonsocialtrue="false"


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
            fechamatchtrue="false"


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

            empresadisuelta = "false"

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

            if ultimoestadoempresa=="DISOLUCIÓN":
                empresadisuelta="true"
            else:
                empresadisuelta="false"                


            sociedad_coincidencia= re.search(r'DE (.*?) (SpA|EMPRESA INDIVIDUAL DE RESPONSABILIDAD LIMITADA| SOCIEDAD DE RESPONSABILIDAD LIMITADA)', content, re.DOTALL)

            if sociedad_coincidencia:
                tipo_entidad= sociedad_coincidencia.group(2)
                entidadtrue= "true"
            else:
                tipo_entidad=None
                entidadtrue= "false"
            if empresamodificada=="true":
                modifico= re.search(r'Menciones Antes de la modificación Después de la modificación (.*?) (Se ha modificado|comuna)(.*?)\,', content, re.DOTALL).group(0)
            else:
                modifico=""


            if (empresaconstituida =="false") and (empresamodificada =="false") and empresatransformada =="false" and (empresadisuelta =="false") and (entidadtrue =="false"):
                errorestudio= "true"
            else:
                errorestudio="false"

        except:
            errorestudio="true"



        #region articulos repetidos
        try:
            countarti=0
            dict_articulos={}
            list_articulos=["ARTÍCULO PRIMERO DEL NOMBRE O RAZON SOCIAL:",
                            "ARTÍCULO SEGUNDO OBJETO:",
                            "ARTÍCULO TERCERO DOMICILIO:",
                            "ARTÍCULO CUARTO DURACIÓN:",
                            "ARTÍCULO QUINTO DEL CAPITAL SOCIAL:",
                            "ARTÍCULO SEXTO DE LA RESPONSABILIDAD DE LOS SOCIOS:",
                            "ARTÍCULO SÉPTIMO DE LA ADMINISTRACIÓN:",
                            "ARTÍCULO OCTAVO DE LAS UTILIDADES Y PÉRDIDAS, Y LOS RETIROS PARA GASTOS:",
                            "ARTÍCULO NOVENO DEL ARBITRAJE:",
                            "ARTÍCULO DÉCIMO DE LA LIQUIDACIÓN:",
                            "ARTÍCULO DÉCIMO PRIMERO DE LOS PODERES CONFERIDOS A O LOS ADMINISTRADORES:",
                            "ARTÍCULO DÉCIMO SEGUNDO OTROS:"
                            ]
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


        try:

            actuacion_match = re.search(r'(.*?)DE', content, re.DOTALL)

            if actuacion_match:
                actuacion_find = actuacion_match.group(1)
                errorpreestudio="false"
                
            else:
                actuacion_find = ""
                errorpreestudio="true"



        except:
            errorpreestudio="true"
        

        fraseaccionistasreferenciatrue="false"

        firmaselectronicas=[]
        administradoreslist=[]

        try:


            texto_accionistasrepresentantesSIIv1match= re.search(r'ARTÍCULO QUINTO DEL CAPITAL SOCIAL:(.*?)ARTÍCULO SEXTO DE LA RESPONSABILIDAD DE LOS SOCIOS:', content, re.DOTALL)
            cuentaacciionistas= re.findall(r'([A-Z])\)\s(.*?)\;', texto_accionistasrepresentantesSIIv1match.group(1),re.DOTALL)
            
            if texto_accionistasrepresentantesSIIv1match:

                firmantesdetalle = re.findall(r'([A-Z])\) (.*?)se obliga a enterar el equivalente al (.*?)por ciento del capital social, mediante el aporte de \$(.*?)pesos', texto_accionistasrepresentantesSIIv1match.group(1), re.DOTALL)


                for  letra, cuenta in cuentaacciionistas:
                    

                    searchrut = re.search(r'(.*?) (se|tiene)', cuenta, re.DOTALL)
              

                    accionrut=re.search(r'(equivalente al|de un) (.*?) por', cuenta, re.DOTALL)

                    montorut=re.search(r'(aporte de|cantidad de) \$(.*?)pesos', cuenta, re.DOTALL)
                    



                    administradoresdicc={}
                    administradoresdicc["tipo"]="administrador"
                    administradoresdicc["provisorio"]="false"  
                    nombrerutencontrado = re.search(re.escape(searchrut.group(1).strip()) + r', Rut ([0-9Kk.-]+),', content)
                    administradoresdicc["rut"]=nombrerutencontrado.group(1)
                    


                    administradoresdicc["nombre"]=searchrut.group(1)
                    administradoresdicc["comoAdministra"]="separadamente"

                    nombrecompleto=searchrut.group(1).strip().split(" ")



                    try:

                        if len(nombrecompleto)==4:
                            
                            administradoresdicc["nombres"]=nombrecompleto[0]+" "+nombrecompleto[1]
                            administradoresdicc["apellidopaterno"]=nombrecompleto[2]
                            administradoresdicc["apellidomaterno"]=nombrecompleto[3]
                            errorconnombres="true"
                        else: pass



                        if len(nombrecompleto)==2:
                            administradoresdicc["nombres"]=nombrecompleto[0]
                            administradoresdicc["apellidopaterno"]= nombrecompleto[1]
                            administradoresdicc["apellidomaterno"]= "null"
                            errorconnombres="true"
                        else:
                            pass

                        if len(nombrecompleto)==3:
                            administradoresdicc["nombres"]=nombrecompleto[0]+" "+nombrecompleto[1]
                            administradoresdicc["apellidopaterno"]= nombrecompleto[2]
                            administradoresdicc["apellidomaterno"]= "null"
                            errorconnombres="true"

                        else:
                            pass


                        if len(nombrecompleto)==5:
                            administradoresdicc["nombres"]=nombrecompleto[0]+" "+nombrecompleto[1]+" "+nombrecompleto[2]
                            administradoresdicc["apellidopaterno"]= nombrecompleto[3]
                            administradoresdicc["apellidomaterno"]= nombrecompleto[4]
                            errorconnombres="true"
                        else:
                            pass
                        


                    except Exception as exc:

                        errorconnombres = "false"

                   
                    administradoreslist.append(administradoresdicc)      
        



        except:
            errorconnombres = "false"
        
        frasereferenciaaccionistas=[]
        firmantesdetallelist=[]
        try:
            
                  
            articuloseptoaoctavo=re.search(r'ARTÍCULO SÉPTIMO DE LA ADMINISTRACIÓN:(.*?)ARTÍCULO OCTAVO DE LAS UTILIDADES', content, re.DOTALL)
            
            if articuloseptoaoctavo:
                articuloseptimotrue="true"
                articulo7="articulo_7"

                administracionfirmantes= re.search(r'La administración de la (Sociedad|Empresa) y el uso de su razón social corresponderá a (.*?)\.', content, re.DOTALL).group(2).split(",")
                
                


                ultimafraseadministradores=administracionfirmantes[-1]
                if ultimafraseadministradores == " como un solo socio" or ultimafraseadministradores == " cualquiera indistintamente" or ultimafraseadministradores  == " todos conjuntamente":
                    cuentaadministradores= len(administracionfirmantes)-1
                else:
                    cuentaadministradores= len(administracionfirmantes)

            else:
                articuloseptimotrue="false"
                articulo7=""
                administracionfirmantes=""
                ultimafraseadministradores=""

            ultimafraseadministradores=administracionfirmantes[-1]


            #articulo5
            articulo5match=re.search(r'ARTÍCULO QUINTO DEL CAPITAL SOCIAL:(.*?) ARTÍCULO SEXTO DE LA RESPONSABILIDAD (DE LOS SOCIOS|DEL SOCIO):',content, re.DOTALL)

            if articulo5match:

                articulo5true="true"
                articulo5posicion="articulo_5"
                articulo5matchfrase=articulo5match.group(1)

                articulo5monto=re.search(r'(\$|CL)(.*?)\s',articulo5match.group(1),re.DOTALL).group(2)



            else:
                articulo5true="false"
                articulo5matchfrase=""            


            

            try:
                
                
                for cuenta in cuentaacciionistas:



                    textolargo= cuenta[1]
                    frasereferenciaaccionistas.append(textolargo)
            except: 
                fraseaccionistasreferenciatrue="false"
                frasereferenciaaccionistas=[]

            if len(frasereferenciaaccionistas)>=2:

                count_accionistas= len(frasereferenciaaccionistas)
                fraseaccionistasreferenciatrue="true"
            else:

                fraseaccionistasreferenciatrue="false"
                frasereferenciaaccionistas=[]
                count_accionistas= 1

            
            

            


            

        

            if texto_accionistasrepresentantesSIIv1match:
                
                

                

                firmantesdetalle= re.findall(r'([A-Z])\)\s(.*?)se obliga a enterar el equivalente al (.*?) por ciento del capital social, mediante el aporte de (\$|CL)(.*?)\s', texto_accionistasrepresentantesSIIv1match.group(1),re.DOTALL)
                

                for  letra, cuenta in cuentaacciionistas:
                    firmantesdetalledicc={}
                    

                    searchrut = re.search(r'(.*?) (se|tiene)', cuenta, re.DOTALL)


                    accionrut=re.search(r'(equivalente al|de un) (.*?) por', cuenta, re.DOTALL)



                    montorut=re.search(r'(aporte de|cantidad de) (\$|CL)(.*?) pesos', cuenta, re.DOTALL)

                    firmantesdetalledicc["nombre"]=searchrut.group(1)
                    firmantesdetalledicc["participacion"]=accionrut.group(2).replace(".","")
                    firmantesdetalledicc["participacionDinero"]=int(montorut.group(3).replace(".","").replace(" de",""))
                    firmantesdetalledicc["frasereferencia"]=searchrut.group(1)+" se obliga a enterar el equivalente al "+accionrut.group(2)+" por ciento del capital social, mediante el aporte de $"+montorut.group(3)+" pesos"
                    nombrerutencontrado = re.search(re.escape(searchrut.group(1).strip()) + r', Rut ([0-9Kk.-]+),', content)
                    firmantesdetalledicc["rut"]=nombrerutencontrado.group(1)
                    firmanteselectronicos={}                   
                    firmanteselectronicos["rut"]=nombrerutencontrado.group(1)
        


                    

                    for firma_electronica in firmaselectronicas:
                        if firma_electronica["rut"] ==firmantesdetalledicc["rut"]:
                            firmantesdetalledicc["firmas"]=firma_electronica 

                    firmanteselectronicos["nombre"]=searchrut.group(1)
                    firmanteselectronicos["firmado"]="Firmado electrónicamente el "+fechadiames
                    firmanteselectronicos["anotacion"]=""
                    firmaselectronicas.append(firmanteselectronicos)


                    nombrecompleto=searchrut.group(1).split(" ")
                    

                    try:

                        if len(nombrecompleto)==4:
                            
                            firmantesdetalledicc["nombres"]=nombrecompleto[0]+" "+nombrecompleto[1]
                            firmantesdetalledicc["apellidopaterno"]=nombrecompleto[2]
                            firmantesdetalledicc["apellidomaterno"]=nombrecompleto[3]
                            errorconnombres="true"
                        else: pass



                        if len(nombrecompleto)==2:
                            firmantesdetalledicc["nombres"]=nombrecompleto[0]
                            firmantesdetalledicc["apellidopaterno"]= nombrecompleto[1]
                            firmantesdetalledicc["apellidomaterno"]= "null"
                            errorconnombres="true"
                        else:
                            pass

                        if len(nombrecompleto)==3:
                            firmantesdetalledicc["nombres"]=nombrecompleto[0]+" "+nombrecompleto[1]
                            firmantesdetalledicc["apellidopaterno"]= nombrecompleto[2]
                            firmantesdetalledicc["apellidomaterno"]= "null"
                            errorconnombres="true"

                        else:
                            pass


                        if len(nombrecompleto)==5:
                            firmantesdetalledicc["nombres"]=nombrecompleto[0]+" "+nombrecompleto[1]+" "+nombrecompleto[2]
                            firmantesdetalledicc["apellidopaterno"]= nombrecompleto[3]
                            firmantesdetalledicc["apellidomaterno"]= nombrecompleto[4]
                            errorconnombres="true"
                        else:
                            pass

                    except: 
                        errorconnombres="false"

                    

                        
                    firmantesdetallelist.append(firmantesdetalledicc)
                    diccionarioadmins=administradoreslist

                    try:

                        if ultimafraseadministradores  == " cualquiera indistintamente" or ultimafraseadministradores  == " todos conjuntamente":
                            diccionarioadmins=administradoreslist
                            erroradmins="true"


                        elif ultimafraseadministradores == " como un solo socio":
                            filtrados = [d for d in administradoreslist if d["nombre"] == administracionfirmantes[0]]

                            for diccionario in filtrados:
                                diccionarioadmins=diccionario
                            erroradmins="true"
                        else:
                            pass

                    except:
                        erroradmins="false"
                    


                    

            if fraseaccionistasreferenciatrue=="false" or errorconnombres=="false" or  articulo5true=="false" or articuloseptimotrue=="false" or erroradmins=="false":
                erroraccionistas="true"
            else:
                erroraccionistas="false"

        except Exception as e:
            count_accionistas=1
            articulo5true="false"
            articulo5matchfrase=""
            articulo5monto=""
            erroraccionistas="true"
            print(e)



        

        









        duracionentiempo=""

        try:
            #region  - domicilio duracion

            textoinicioaarticulo1= re.search(r'ARTÍCULO TERCERO DOMICILIO:(.*?) ARTÍCULO CUARTO',content,re.DOTALL)
            if textoinicioaarticulo1:    
                try:       
            
                    domiciliofinal=re.search(r'El domicilio de la (Sociedad|Empresa) es(.*?),\ssin perjuicio',textoinicioaarticulo1.group(1),re.DOTALL).group(2)
                    articulo3domiciliotrue="true"
                    mensajedomicilio=""
                except:
                    
                    domiciliofinal=re.search(r'El domicilio de la (Sociedad|Empresa) es(.*?)$',textoinicioaarticulo1.group(1),re.DOTALL).group(2)
                    articulo3domiciliotrue="true"
                    mensajedomicilio="Existe una excepcion para el domicilio"
            else:
                
                articulo3domiciliotrue="false"
                domiciliofinal=""
                mensajedomicilio=""
                


            #DURACION 

            articuloduracion= re.search(r'ARTÍCULO CUARTO DURACIÓN:(.*?) ARTÍCULO QUINTO DEL CAPITAL SOCIAL', content, re.DOTALL)


            if articuloduracion:
                articuloduraciontrue="true"
                articuloduracioncompleto= articuloduracion.group(1).replace(',','')

                esindefinida= re.search(r'indefinida.',articuloduracioncompleto,re.DOTALL)
                renovable1= re.search(r'renovables de (\d+)\s',articuloduracioncompleto,re.DOTALL)

                if esindefinida:

                    duracionindefinida="indefinida"
                    duracionentiempo= ""
                    articuloduraciontrue="true"
                else:
                    try:

                        duracionindefinida="finita"
                        articuloduraciontrue="true"
                        duracionentiempo="finita"


                    except:

                        duracionindefinida="finita"
                        articuloduraciontrue="true"   
                        duracionentiempo= renovable1.group(1)


            else:
                articuloduraciontrue="false"
                duracionentiempo= ""
                duracionindefinida="otro"
                errordomicilioduracion="false"


            
            


            if articuloduraciontrue== "false" or articulo3domiciliotrue== "false":
                errordomicilioduracion= "true"
            else:
                errordomicilioduracion="false"

        except:
            errordomicilioduracion="true"


            #fecha_formateada = 'Firmado electrónicamente el ' + fecha_formateada

            #endregion  - domicilio duracion


        facultados="null"
        try:
            #region Facultades
            primerafrasefacultades = re.search(r'ARTÍCULO DÉCIMO PRIMERO DE LOS PODERES CONFERIDOS A O LOS ADMINISTRADORES:', content, re.DOTALL )
            
            if primerafrasefacultades:
                articulo_11="articulo_11"
                articulo11true= "true"

            else:
                articulo_11="articulo_11"
                articulo11true= "false"


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
                    facultades["REPRESENTACIÓN ANTE SOCIEDADES Y ASOCIACIONES"]=represociedadesyasoc.group(2)

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


                reprefirmas= re.search(r'FIRMA DE DOCUMENTOS Y RETIRO DE CORRESPONDENCIA.(\.|\s)(.*?)\.', content, re.DOTALL )

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
            articulo11true= "false"
            



        #endregion facultades


        try:
        #region NOMBRE DE FANTASIA y objeto

            articuloprimero=re.search(r'ARTÍCULO PRIMERO DEL NOMBRE O RAZON SOCIAL:(.*?) ARTÍCULO SEGUNDO OBJETO:', content, re.DOTALL )
            nombrefantasia= re.search(r'nombre de fantasía de\s*(.*?) ARTÍCULO SEGUNDO OBJETO', content, re.DOTALL )
            
            if nombrefantasia and articuloprimero:
                nombrefantasiatrue="true"
                articuloprimerotrue="articulo_1"
                nombrefantasia= re.search(r'nombre de fantasía de\s*(.*?) ARTÍCULO SEGUNDO OBJETO', content, re.DOTALL ).group(1)
                nombrerealempresa= re.search(r'"(.*?)"', articuloprimero.group(1), re.DOTALL ).group(1)

            else:
                nombrefantasiatrue="true"
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

            articulosegundocompleto= re.search(r'ARTÍCULO SEGUNDO OBJETO:(.*?) ARTÍCULO TERCERO DOMICILIO:', content, re.DOTALL )

            objetosentidad= []
            if articulosegundocompleto:
                articulosegundotrue= "true"
                articulo2texto="articulo_2"

                articulosegundoobjeto= re.search(r'La (Sociedad|Empresa) (.*?): (.*?)$', articulosegundocompleto.group(1), re.DOTALL ).group(3) 

                objetoslist= articulosegundoobjeto.split(",")
                objetoslist.extend(objetosentidad)
                countobjetos = len(objetosentidad)


            
            else:
                articulosegundotrue= "false"
                articulosegundoobjeto= ""
                articulo2texto=""

            if  nombrefantasiatrue== "false" or articulosegundotrue== "false" or articuloprimeroexiste =="false":
                errorfantasiaobjeto="true"
            else:
                errorfantasiaobjeto="false"
            
        except:
            errorfantasiaobjeto="true"
            articulosegundoobjeto= ""
            nombrefantasiatrue="false"


        #endregion nombre de fantasia y objeto
        tarjetadebitofaltantes=[]
        tarjetacreditofaltantes=[]
        getnetfaltantes=[]
        lineacreditofaltantes=[]
        ctacorrientefaltantes=[]

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



            if (posgetnettrue=="true") and (lineacreditotrue=="true") and (tarjetacreditotrue=="true") and (tarjetadebitotrue=="true") and (ctacorrientetrue=="true"):
                todosproductostrue="false"
                preaprobacionproductos="true"
            else:
                todosproductostrue="true"
                preaprobacionproductos="false"

            errorproductos="false"



        except:
            
            posgetnettrue="false" 
            lineacreditotrue="false"
            tarjetacreditotrue="false"
            tarjetadebitotrue="false"
            ctacorrientetrue="false"
            errorproductos="true"
            todosproductostrue="true"
            preaprobacionproductos="false"


        errorproceso=  errorarticulos + errorestado + errorestudio + errorpreestudio + erroraccionistas + errordomicilioduracion + errorfacultades + errorfantasiaobjeto + errorproductos+ artirepetidostrue


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
                    "todosproductostrue":todosproductostrue,
        }

        errores_fallidos = [error for error, resultado in errorestry.items() if resultado == "true"]


        if errores_fallidos:
            errorfatal = "true"
            mensaje_error = f"Error en: {', '.join(errores_fallidos)}"
        else:
            errorfatal = "false"
            mensaje_error = "-"



        if errorextraccion=="false" and errorfatal=="false":
            preaprobadofinal= "true"
        else:
            preaprobadofinal="false"



        ####### LIMITADA$$$$$#####
        data={
            "content1":content1,
            "content2":content2,

            "data": {
                "estado": {
                    "ejecutivo": "testlegalbot",
                    "estado": "finalizado",
                    "fecha": fecha_junta,
                    "id": 1,
                    "preEstudio": "null", # est
                    "razonSocial": razon_social,
                    "rut": rut_sociedad_solo
                },
                "estudio": {
                    "fechaEstudio": fecha_separada,
                    "rut": rut_sociedad_guion,
                    "tipoSociedad": tipoempresa,
                    "ultimaModificacion": fechamesdia,
                    "modificado": empresamodificada,
                    "transformado": empresatransformada,
                    "errorFatal": errorfatal,
                    "errorExtraccion": errorextraccion,
                    "disuelto": empresadisuelta,
                    "preAprobado": preaprobadofinal,# este se podríoa definir si está transformado o modificado, figure como false, a menos que existe un error enel codigo y tambien diga flase
                    "mensajes": [],
                    "prestudios": [
                        {
                            "rut": rut_sociedad_guion,
                            "fecha": fechamesdia,
                            "cve": cve_match,
                            "preAprobado": preaprobadofinal, #hacer calzar con el preaprobado de transformado o modificaado
                            "errorFatal": errorfatal,
                            "disuelto": empresadisuelta,
                            "mensajes": [],
                            "tipoActuacion": ultimoestadoempresa,
                            "tipoSociedad": tipoempresa,
                            "firmas": {
                                "numero": 3,
                                "tipo": "firmas",
                                "firmas": firmaselectronicas
                            },
                            "modificacion": modifico,
                            "anexos": [],
                            "articulosRepetidos": {
                                "ok": artirepetidostrue,#REVISAR SI EXISTEN TODOS LOS ARTICULOS
                                "mensajes": [],
                                "frasesReferencia": [],
                                "articulosReferencia": dict_articulos,
                                "valor": countarti
                            },
                            "accionistas": {
                                "ok": fraseaccionistasreferenciatrue,
                                "mensajes": [count_accionistas],
                                "frasesReferencia": frasereferenciaaccionistas,
                                "articulosReferencia": [
                                    "articulo_5"
                                ],
                                "valor":firmantesdetallelist
                                
                            },
                            "administracion": {
                                "ok": articuloseptimotrue,
                                "mensajes": [],
                                "frasesReferencia": administracionfirmantes,
                                "articulosReferencia": [
                                    articulo7
                                ],
                                "valor": {
                                    "todosConRut": "true",
                                    "texto": ultimafraseadministradores,
                                    "comoAdministran": "separadamente",
                                    "quienAdministra": {
                                        "gg": 0,
                                        "ad": cuentaadministradores,
                                        "di": 0,
                                        "todos": cuentaadministradores
                                    },
                                    "administradores": diccionarioadmins
                                }
                            },
                            "capital": {
                                "ok": articulo5true,
                                "mensajes": [],
                                "frasesReferencia": [
                                    articulo5matchfrase
                                ],
                                "articulosReferencia": [
                                    "articulo_5"
                                ],
                                "valor": articulo5monto
                            },
                            "domicilio": {
                                "ok": articulo3domiciliotrue,
                                "mensajes": mensajedomicilio,
                                "frasesReferencia": [
                                    domiciliofinal
                                ],
                                "articulosReferencia": [
                                    "articulo_3"
                                ],
                                "valor": domiciliofinal
                            },
                            "duracion": {
                                "ok": articuloduraciontrue,
                                "mensajes": [duracionindefinida],
                                "frasesReferencia": [
                                    duracionindefinida
                                ],
                                "articulosReferencia": [
                                    "articulo_4"
                                ],
                                "valor": {
                                    "texto": articuloduracioncompleto,
                                    "tags": [
                                        duracionentiempo
                                    ],
                                    "finalizada": "false"   #revisar cuando alguna tenga fecha para generar este formula
                                }
                            },
                            "facultades": {
                                "ok": articulo11true,
                                "mensajes": [],
                                "frasesReferencia": [],
                                "articulosReferencia": [
                                    articulo_11
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
                                    "articulo_1"
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
                                    "articulo_2"
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
                    "customer": "santander",
                    "fechaCambioAdministracion": fechamesdia,
                    "santander": {
                        "disuelto": empresadisuelta, 
                        "preAprobado": preaprobacionproductos,
                        "algunaEncontrada": preaprobacionproductos, #esto aún nose de donde viene
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
                        "administradores": diccionarioadmins
                        ,
                        "grupos": [
                            {
                                "nombre": count_accionistas,
                                "administradores": diccionarioadmins
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
                                    21,
                                    22,
                                    23,
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
                                    63,
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
                            21,
                            22,
                            23,
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
                            63,
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
        ltda_instance = LTDA()
        ltda_instance.ejecutar()