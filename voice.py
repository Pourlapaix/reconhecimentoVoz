import speech_recognition as speaker
import os
import json

#Seletor de arquivos
from tkinter import Tk
from tkinter.filedialog import askopenfilename

ftypes = [('Exe files',"*.exe"), ('Photo files',"*.jpg")]
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
rec = speaker.Recognizer()

def salvarCaminhoPrograma():
    root = Tk()
    caminhoPrograma = askopenfilename(filetypes = ftypes, initialdir = dir1, title = ttl)
    root.destroy();

    if caminhoPrograma != "":
        try:
            os.startfile(caminhoPrograma)
            listaCaminhos['archives'].append({'caminho': caminhoPrograma, 'nome': fala})
            with open('meu_arquivo.json', 'w', encoding='utf-8') as f:
                json.dump(listaCaminhos, f)
            print("Comando salvo com sucesso.")
        except:
            print("Não funcionei com este arquivo.")
    return

print("Olá! Atualmente eu repito o que você diz, e abro programas!")
print("Para abrir programas, fale 'Abrir nomedoprograma', e ele irá abrir uma caixa para você selecionar o exe do arquivo.")

with speaker.Microphone() as speak:
    rec.adjust_for_ambient_noise(speak)

    while True:
        try:
            audio = rec.listen(speak)
            fala = rec.recognize_google(audio, language='pt')
            palavras = fala.split()
            print('Você disse: ', fala)

            if palavras[0].lower() == "abrir" and len(palavras) > 1:
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
        except speaker.UnknownValueError:
            print("Não consegui entender seu áudio")
        except speaker.RequestError as e:
            print("A sua requisição de áudio falhou, verifique se está conectado na internet {0}".format(e))
