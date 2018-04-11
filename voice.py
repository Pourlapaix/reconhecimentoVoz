import speech_recognition as speaker
from pygame  import mixer
from gtts import gTTS
import os,json,re,playsound

def falar (frase):
    file = str("hello" + str(frase[0]) + ".mp3")
    gTTS(text=frase, lang='pt').save('/tmp/'+file)
    playsound.playsound('/tmp/'+file,True)
    os.remove('/tmp/'+file)

falar('Bem vindo!')

#Seletor de arquivos
from tkinter import Tk
from tkinter.filedialog import askopenfilename

ftypes = [('Exe files',"*.exe"), ('Photo files',"*.jpg")]
ttl  = "Select the program"
dir1 = 'C:\\'

#Programas já salvos
with open('memoria.json', 'r') as f:
    texto = f.read()

if texto == "":
    listaCaminhos = {'archives': []}
else:
    listaCaminhos = json.loads(texto)

#Reconhecedor do Google
rec = speaker.Recognizer()

#Lista de musicas
musicas = []

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
            selecionar = str(selecionar)[1:-1].split("', ");
            if len(selecionar) == 1:
                selecionar[0] = selecionar[0][0:-1]

            for i in range(len(selecionar)):
                if i == len(selecionar) -1:
                    selecionar[i] = selecionar[i][0:-1]
                musicas.append(selecionar[i][1::])
            reproduzir();
        else:
            falar('Você não selecionou nenhuma música.')
        return musicas

def reproduzir ():
        musicaAtual = 0
        mixer.init()
        while True:
            if mixer.music.get_busy() == False:
                proximaMusica(musicaAtual)
                musicaAtual += 1

def proximaMusica(musicaAtual):
    print("Tocando agora "+musicas[musicaAtual])
    musica_atual = mixer.music.load(musicas[musicaAtual])
    musica_atual = mixer.music.play()

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

    while True:
        try:
            audio = rec.listen(speak)
            fala = rec.recognize_google(audio, language='pt')
            palavras = fala.split()

            if fala == "tocar música":
                escolher();
            elif palavras[0].lower() == "abrir" and len(palavras) > 1:
                fala = fala.lower().replace("abrir ","",1)
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
