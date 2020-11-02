from cgi import parse_multipart, parse_header
from io import BytesIO
from base64 import b64decode
from ibm_watson import SpeechToTextV1, ApiException
from ibm_cloud_sdk_core.authenticators import BasicAuthenticator
import json, os
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions,SentimentOptions

def transcrevendo_audio_Stt(multipart_data) :
        fo = open("audio_sample.flac", 'wb')
        fo.write(multipart_data.get('audio')[0])
        fo.close()

        # Basic Authentication with Watson STT API
        stt_authenticator = BasicAuthenticator(
            'apikey',
            '_R9ocBEIDmhvdd0yJMn2HoekPwOCB_x79E7lDw2rvmP-'

        )

        # Construct a Watson STT client with the authentication object
        stt = SpeechToTextV1(
            authenticator=stt_authenticator
        )

        # Set the URL endpoint for your Watson STT client
        stt.set_service_url(
            'https://api.us-south.speech-to-text.watson.cloud.ibm.com'
        )

        # Read audio file and call Watson STT API:
        with open(
            os.path.join(
                os.path.dirname(__file__), './.',
                'audio_sample.flac'
            ), 'rb'
        ) as audio_file:
            # Transcribe the audio.flac with Watson STT
            # Recognize method API reference: 
            # https://cloud.ibm.com/apidocs/speech-to-text?code=python#recognize
            stt_result = stt.recognize(
                audio=audio_file,
                content_type='audio/flac',
                model='pt-BR_BroadbandModel'
            ).get_result()
        return stt_result
def analise_de_entidades_sentimentos(doc) :
    entidade = list()
    authenticator = IAMAuthenticator('scbOWMmui5WYlxCKfxqbYKUkSfc1bFVFEiX9nAKJMQIW')
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2020-08-01',authenticator=authenticator)
    natural_language_understanding.set_service_url('https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/9f45857b-9b6a-4f9d-b262-b6e3aa0642b4')  
    for documento in doc.split(',') :
            if len(documento.split()) > 3:
                response = natural_language_understanding.analyze(text = documento,features=Features(entities=EntitiesOptions(sentiment=True,model = '8f0923f4-3718-4533-bd00-2bd90a437b07'))).get_result()   
                entidade = entidade + response["entities"] 
            else :
                None
    if entidade == [] :
        return 0
    else :
        return entidade
def separacao_de_entidade_emocao(entidade) :
    entity = list()
    for dic in entidade :
        dicionario = dict()
        dicionario["entity"] = dic["type"]
        dicionario["mention"] = dic["text"]
        dicionario["sentiment"] = dic["sentiment"]["score"]
        entity = entity + [dicionario]

    return entity
def recomendacao(car,categoria) :
    carros_e_cat = {'SEGURANCA': ['RENEGADE', 'TORO'],'MANUTENCAO': ['FIORINO', 'TORO'],'DESEMPENHO': ['MAREA', 'DUCATO'], 'ACESSORIOS':['TORO', 'CRONOS'], 'CONFORTO': ['CRONOS', 'FIAT 500'],'DESIGN': ['FIAT 500', 'CRONOS'],'CONSUMO': ['ARGO', 'DUCATO'] }
    if car != carros_e_cat[categoria][0] :
        return carros_e_cat[categoria][0]
    else :
         return carros_e_cat[categoria][1]
def recomenda_ou_n(enti_emo):
    soma_sentimento = 0
    for dicionario in enti_emo:
        if dicionario["entity"] != 'MODELO':
            soma_sentimento = soma_sentimento + dicionario['sentiment']
    if soma_sentimento < 0 :
        return 1
    else :
        return 0
def escolha_qual_recomenda(enti):
    Prioridades_reco = {"SEGURANCA" : 7, "CONSUMO":6,"DESEMPENHO" :5,"MANUTENCAO":4, "CONFORTO" :3,"DESIGN" :2,"ACESSORIOS":1 }
    i =0
    for dicionario in enti :
            if dicionario['sentiment'] <0 and dicionario['entity'] != 'MODELO' :
                if i == 0 :
                    menor_valor = dicionario["sentiment"]
                    menor_cat =  dicionario["entity"]

                else :
                        # SE a diferença entre as duas está entre 0.1
                        if ((float(menor_valor) * -1 ) - float(dicionario['sentiment'])* -1) < 0.1 and ((float(menor_valor) * -1 ) - float(dicionario['sentiment'])* -1) > - 0.1 :
                            # Regra de prioridade
                            if Prioridades_reco[dicionario["entity"]] > Prioridades_reco[menor_cat] :
                                            menor_cat = dicionario["entity"] 
                                            menor_valor = dicionario["sentiment"]
                            else :
                                None
                        elif (dicionario["sentiment"] * -1) > (menor_valor* -1):
                            menor_cat = dicionario["entity"] 
                            menor_valor = dicionario["sentiment"]
                        else :
                            None
                i = 1
            else :
                None
    return menor_cat


def main(args):
    # Parse incoming request headers
    _c_type, p_dict = parse_header(
        args['__ow_headers']['content-type']
    )
    # Decode body (base64)
    decoded_string = b64decode(args['__ow_body'])

    # Set Headers for multipart_data parsing
    p_dict['boundary'] = bytes(p_dict['boundary'], "utf-8")
    p_dict['CONTENT-LENGTH'] = len(decoded_string)
    
    # Parse incoming request data
    multipart_data = parse_multipart(
        BytesIO(decoded_string), p_dict
    )
    if multipart_data.get('text') == None:
    # Build flac file from stream of bytes
        stt_result = transcrevendo_audio_Stt(multipart_data)
        doc = str(stt_result['results'][0]['alternatives'][0]['transcript'])
        entidade = analise_de_entidades_sentimentos(doc)
    else :
        doc = multipart_data.get('text')[0]
        entidade = analise_de_entidades_sentimentos(doc)  
    
    if entidade != 0 :
        carro = multipart_data.get('car')[0]
        enti_emo = separacao_de_entidade_emocao(entidade)
        resultado = recomenda_ou_n(enti_emo)
        if resultado == 0 :
            return {
                    "recommendation": "", 
                    "entities" : enti_emo

                }
        else :
            categoria = escolha_qual_recomenda(enti_emo)
            carro_recomendado = recomendacao(carro, categoria)
            return {"recommendation": carro_recomendado, "entities": enti_emo }

   
    else :
    # Return a dictionary with the transcribed text
        
        return {
            "recommendation": "",
                "entities": []
        }