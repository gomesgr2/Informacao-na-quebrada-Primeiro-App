from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import mysql.connector
import datetime

def arruma_aspas(name) :
    "Transforma todas as aspas duplas em aspas simples"
    new_name = ''
    for char in name :
        if char == '"' :
            char = ''
        new_name = new_name + char
    return new_name

def query_id(cnx) :
    "Seleciona Id's de uma tabela MySQL"
    Result = list()
    cursor = cnx.cursor()
    cursor.execute('SELECT `id` FROM `aplicativo`.`id_podcast`')
    query = cursor.fetchall()
    for id_ in query :
        Result = Result + [id_[0]]
    return Result
def check(id_,cnx, table) :
    "Checa se o id já esta na tabela"
    cursor = cnx.cursor()
    cursor.execute(f'SELECT * FROM `aplicativo`.{table} WHERE `id` = "{id_}"')
    query = cursor.fetchall()
    return query
def save_podcast(resultado) :
    cnx = mysql.connector.connect(user='root', password='gabriel2011',host='127.0.0.1',database='aplicativo')
    id_pod = resultado['id']
    imagem_pod = resultado['images'][1]['url']
    nome_pod = resultado['name']
    autor_pod = resultado['publisher']
    total_epi = resultado['total_episodes']
    descricao_pod = resultado['description']
    url_pod = resultado['href']
    print(id_pod,imagem_pod,nome_pod,autor_pod,total_epi,descricao_pod,url_pod)
    cursor = cnx.cursor()
    cursor.execute(f'INSERT INTO `aplicativo`.`info_podcats` (`id`, `nome`, `url`, `autor`,`descricao`,`total_ep`,`imagem`) VALUES("{id_pod}","{nome_pod}","{url_pod}","{autor_pod}","{descricao_pod}",{total_epi},"{imagem_pod}");')
    cnx.commit()
    
    

def main() :
    # Realizando autenticação no Spotify for developers
    sp = spotipy.Spotify(client_credentials_manager = SpotifyClientCredentials(client_id='e459b2ff04c543d5bc21b03762794877', client_secret='4409b2dd45b14511ae64c26f095d59f1'))

    #Conexão com o Banco de dados
    cnx = mysql.connector.connect(user='root', password='gabriel2011',host='127.0.0.1',database='aplicativo')

    # adicionando os valores em uma lista
    lst_id_podcast = query_id(cnx)
    

    for podcast in lst_id_podcast : 
        # método do show() que retorna uma descrição do podcast e um dicionário com todos os episódios
        results = sp.show(podcast, market = 'BR')
        image = results['images'][2]['url']
        autor = results['name']
        episodes = results['episodes']['items']
        
        
        # Se o podcast não estiver registrado na tabela info_podcasts, então iremos registra-lo
        if check(results['id'],cnx, 'info_podcats') == [] :
            save_podcast(results)
        
        

        for episode in episodes :
            # Separando os valores que serão adicionados ao banco
            id_ = episode['id']
            #Conferindo se o episódio ja está na tabela
            if check(id_, cnx, 'podcasts') == [] : 
                autor = results['name']
                url_audio = episode['audio_preview_url'] 
                description = arruma_aspas(episode['description'])
                duration_ms = episode['duration_ms']
                url = 'https://open.spotify.com/embed/episode/' + episode['id']
                name = episode['name']
                release_date = episode['release_date']
                tipo = "PODCAST"
                # limpando o texto para não ocorrer problema quando adicionarmos o nome ao banco de dados
                name = arruma_aspas(name)
                #Adicionando ao banco de dados
                cursor = cnx.cursor()
                cursor.execute(f'INSERT INTO `aplicativo`.`podcasts` (`id`, `url`, `name`, `tipo`,`duracao`,`url_audio`,`ativo`,`descricao`, `data_lancamento`,`autores`,`imagens`) VALUES("{id_}","{url}","{name}","{tipo}","{duration_ms}","{url_audio}",1,"{description}","{release_date}","{autor}", "{image}");')   
        
    cnx.commit()

if __name__ == '__main__':
    main()
