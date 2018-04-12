import speech_recognition as speaker
import os,json,re,playsound,random
from pygame  import mixer
from gtts import gTTS
from tkinter import Tk
from tkinter.filedialog import askopenfilename

#Reconhecedor do Google
rec = speaker.Recognizer()
#Configuracoes do seletor
ftypes = [('Exe files',"*.exe"), ('Photo files',"*.jpg")]
ttl  = "Select the program"
dir1 = 'C:\\'
#Setar variáveis padroes
musicaAtual = 0
estadoMusica = False

def falar (frase):
    file = str("voice" + str(random.randint(0,9)) + str(random.randint(0,9)) + ".mp3")
    gTTS(text=frase, lang='pt').save('/tmp/'+file)
    playsound.playsound('/tmp/'+file,True)
    os.remove('/tmp/'+file)

falar('Bem vindo!')

#Ler programas já salvos
with open('memoria.json', 'r') as f:
    texto = f.read()

if texto == "":
    listaCaminhos = {'archives': []}
    musicas = []
else:
    #Caminho dos programas
    listaCaminhos = json.loads(texto)
    #Lista de musicas
    musicas = listaCaminhos["playlist"]

def escolher ():
        falar('Ok! Selecione as músicas que deseja ouvir.')
        root = Tk();
        selecionar = askopenfilename(initialdir=dir1,
                           filetypes =(("Arquivo de audio", "*.mp3"),("All Files","*.*")),
                           title = "Selecione as musicas",
                           multiple = True
                           )
        root.destroy();

        if selecionar != '':
            global musicas
            musicas = []
            selecionar = str(selecionar)[1:-1].split("', ");
            if len(selecionar) == 1:
                selecionar[0] = selecionar[0][0:-1]

            for i in range(len(selecionar)):
                if i == len(selecionar) -1:
                    selecionar[i] = selecionar[i][0:-1]
                musicas.append(selecionar[i][1::])
            iniciarMusica()
        else:
            falar('Você não selecionou nenhuma música.')
        return musicas

def carregarPlaylist():
    falar('Carregando playlist salva')
    musicas = listaCaminhos["playlist"]
    iniciarMusica()

def iniciarMusica():
    falar('Iniciando sua playlist')
    global musicaAtual
    musicaAtual = 0
    global estadoMusica
    estadoMusica = True

def pularMusica():
    print("Tocando agora "+musicas[musicaAtual])
    mixer.music.load(musicas[musicaAtual])
    mixer.music.play()

def voltarMusica():
    global musicaAtual
    if musicaAtual > 0:
        musicaAtual -= 1
    print("Tocando agora "+musicas[musicaAtual])
    mixer.music.load(musicas[musicaAtual])
    mixer.music.play()

def pararMusica():
    global estadoMusica
    estadoMusica = False
    mixer.music.stop()
    falar('Você desligou a música.')

def salvarPlaylist():
    listaCaminhos["playlist"] = musicas
    with open('memoria.json', 'w', encoding='utf-8') as f:
        json.dump(listaCaminhos, f)
        falar('Playlist salva com sucesso!')

def excluirPlaylist():
    listaCaminhos["playlist"] = []
    with open('memoria.json', 'w', encoding='utf-8') as f:
        json.dump(listaCaminhos, f)
        falar('Playlist deletada com sucesso!')

def salvarCaminhoPrograma():
    root = Tk()
    caminhoPrograma = askopenfilename(filetypes = ftypes, initialdir = dir1, title = ttl)
    root.destroy();

    if caminhoPrograma != "":
        try:
            os.startfile(caminhoPrograma)
            listaCaminhos['archives'].append({'caminho': caminhoPrograma, 'nome': fala})
            with open('memoria.json', 'w', encoding='utf-8') as f:
                json.dump(listaCaminhos, f)
            falar('Comando salvo com sucesso!')
        except:
            falar('Infelizmente aconteceu algum erro com este arquivo')
    return

with speaker.Microphone() as speak:
    rec.adjust_for_ambient_noise(speak)
    mixer.init()

    while True:
        if mixer.music.get_busy() == False and estadoMusica and musicaAtual <= len(musicas):
            print("Tocando agora "+musicas[musicaAtual])
            mixer.music.load(musicas[musicaAtual])
            mixer.music.play()
            musicaAtual += 1

        try:
            audio = rec.listen(speak)
            fala = rec.recognize_google(audio, language='pt').lower()
            palavras = fala.split()

            if fala == "tocar música":
                if estadoMusica:
                    pararMusica()
                escolher()
            elif fala == "tocar playlist" and musicas != '':
                iniciarMusica()
            elif fala == "pular música" or fala == "próxima música" and estadoMusica:
                pularMusica()
            elif fala == "voltar música" or fala == "música anterior" and estadoMusica:
                voltarMusica()
            elif fala == "parar música" and estadoMusica:
                pararMusica()
            elif fala == "carregar playlist salva":
                carregarPlaylist()
            elif fala == "salvar playlist":
                salvarPlaylist()
            elif fala == "excluir playlist":
                excluirPlaylist()
            elif palavras[0] == "abrir" and len(palavras) > 1:
                fala = fala.replace("abrir ","",1)
                if len(listaCaminhos['archives']) > 0:
                    achouPrograma = False
                    for i in range(len(listaCaminhos['archives'])):
                        programa = listaCaminhos['archives'][i]
                        if programa['nome'] == fala:
                            achouPrograma = True
                            break

                    if achouPrograma:
                        os.startfile(programa['caminho'])
                    else:
                        salvarCaminhoPrograma()
                else:
                    salvarCaminhoPrograma()
            else:
                print("Você falou: "+fala)
        except speaker.RequestError as e:
            print("A sua requisição de áudio falhou, verifique se está conectado na internet {0}".format(e))
        except speaker.UnknownValueError:
            print
