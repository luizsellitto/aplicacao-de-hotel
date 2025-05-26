# =============== Helpers =========================

def ler_arquivo(nome_arquivo):
    if not os.path.exists(nome_arquivo):
        return []
    with open(nome_arquivo, 'r', encoding='utf-8') as f:
        return [linha.strip() for linha in f.readlines() if linha.strip()]

def gravar_arquivo(nome_arquivo, linhas):
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        f.write('\n'.join(linhas) + ('\n' if linhas else ''))