
import os
# =============== Helpers =========================

def ler_arquivo(nome_arquivo):
    if not os.path.exists(nome_arquivo):
        return []
    
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            linhas = []
            for linha in arquivo:
                linha_limpa = linha.strip()
                if linha_limpa:
                    linhas.append(linha_limpa)
            return linhas
    except IOError:
        return []


def gravar_arquivo(nome_arquivo, linhas):
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            if linhas:
                arquivo.write('\n'.join(linhas) + '\n')
        return True
    except IOError:
        return False