from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import mysql.connector
import datetime
# Lista com os Id's dos podcasts pré selecionados
lst_id_podcast = ['15cUvjhlItNiuMrgIFMC7X']

# Realizando autenticação no Spotify for developers
sp = spotipy.Spotify(client_credentials_manager = SpotifyClientCredentials(client_id='Sua credencial no spotify for developers', client_secret='Sua credencial no spotify for developers'))

#Conexão com o Banco de dados
cnx = mysql.connector.connect(user='usuario', password='__sua senha__',host='127.0.0.1',database='aplicativo')
def arruma_aspas(name) :
    """Transforma todas as aspas duplas em aspas simples."""
    new_name = ''
    for char in name :
        if char == '"' :
            char = ''
        new_name = new_name + char
    return new_name

for podcast in lst_id_podcast : 
    # método do show() que retorna uma descrição do podcast e um dicionário com todos os episódios
    results = sp.show(podcast, market = 'BR')
    episodes = results['episodes']['items']
    for episode in episodes :
        # Separando os valores que serão adicionados ao banco
        id_ = episode['id']
        url_audio = episode['audio_preview_url'] 
        description = episode['description']
        duration_ms = episode['duration_ms']
        url = episode['external_urls']['spotify']
        name = episode['name']
        release_date = episode['release_date']
        tipo = "PODCAST"
        # limpando o texto para não ocorrer problema quando adicionarmos o nome ao banco de dados
        name = arruma_aspas(name)
        #Adicionando ao banco de dados
        cursor = cnx.cursor()
        cursor.execute(f'INSERT INTO `aplicativo`.`podcast` (`id`, `url`, `name`, `tipo`,`duracao`,`url_audio`,`ativo`,`descricao`, `data_lancamento`) VALUES("{id_}","{url}","{name}","{tipo}","{duration_ms}","{url_audio}",1,"Sem Descrição","{release_date}");')       
cnx.commit()