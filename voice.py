import speech_recognition as speaker
import os
import json

#Seletor de arquivos
from tkinter import Tk
from tkinter.filedialog import askopenfilename

ftypes = [('Exe files',"*.exe")]
ttl  = "Select the program"
dir1 = 'C:\\'

#Programas já salvos
with open('meu_arquivo.json', 'r') as f:
    texto = f.read()

if texto == "":
    listaCaminhos = {'archives': []}
else:
    listaCaminhos = json.loads(texto)

#Reconhecedor do Google
r = speaker.Recognizer()

def salvarCaminhoPrograma():
    root = Tk()
    caminhoPrograma = askopenfilename(filetypes = ftypes, initialdir = dir1, title = ttl)
    root.destroy();

    if(caminhoPrograma != "")
        try:
            os.startfile(caminhoPrograma)
            listaCaminhos['archives'].append({'caminho': caminhoPrograma, 'nome': palavras[1].lower()})
            with open('meu_arquivo.json', 'w', encoding='utf-8') as f:
                json.dump(listaCaminhos, f)
        except:
            print("Dont work this file.")
    return

with speaker.Microphone() as speak:
    r.adjust_for_ambient_noise(speak)

    while True:
        try:
            audio = r.listen(speak)
            fala = r.recognize_google(audio, language='pt')

            palavras = fala.split()

            if palavras[0].lower() == "abrir" and len(palavras) > 1:
                if len(listaCaminhos['archives']) > 0:
                    achouPrograma = False
                    for i in range(len(listaCaminhos['archives'])):
                        programa = listaCaminhos['archives'][i]
                        if programa['nome'] == palavras[1].lower():
                            achouPrograma = True
                            break

                    if achouPrograma:
                        os.startfile(programa['caminho'])
                    else:
                        salvarCaminhoPrograma()
                else:
                    salvarCaminhoPrograma()

            print('Você disse: ', fala)
        except speaker.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except speaker.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
