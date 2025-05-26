
import os
from typing import List

# =============== Helpers =========================

def ler_arquivo(nome_arquivo):
    if not os.path.exists(nome_arquivo):
        return []
    
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            # Lê todas as linhas, remove espaços em branco e filtra linhas vazias
            linhas = []
            for linha in arquivo:
                linha_limpa = linha.strip()
                if linha_limpa:  # Só adiciona se a linha não estiver vazia
                    linhas.append(linha_limpa)
            
            return linhas
            
    except:
        print(f"Erro ao ler arquivo '{nome_arquivo}':")
        return []


def gravar_arquivo(nome_arquivo, linhas):
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            # Grava cada linha seguida de quebra de linha
            for i, linha in enumerate(linhas):
                arquivo.write(linha)
                # Adiciona quebra de linha, exceto na última linha se a lista estiver vazia
                if i < len(linhas) - 1:
                    arquivo.write('\n')
            
            # Adiciona quebra de linha final se houver conteúdo
            if linhas:
                arquivo.write('\n')
                
        return True
        
    except:
        print(f"Erro ao gravar arquivo '{nome_arquivo}'")
        return False