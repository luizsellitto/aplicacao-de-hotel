# Projeto: Sistema de Gerenciamento de Hotel
Este é um **projeto simples** desenvolvido apenas para fins didáticos, utilizando exclusivamente a **linguagem Python** e executado através do **console** (linha de comando). 

O sistema **não utiliza banco de dados**, realizando a **persistência de dados** apenas por meio de **arquivos texto**. Toda a manipulação de informações será feita através de **leitura e escrita de arquivos**, utilizando **dicionários** e outras estruturas básicas de dados, como listas, para o armazenamento temporário das informações em memória.

## Descrição

Este projeto consiste no desenvolvimento de uma aplicação em **Python** para gerenciamento de informações de um hotel, incluindo o controle de **clientes**, **reservas**, **apartamentos** e **relações entre reservas e apartamentos**. A aplicação também possui funcionalidades para geração de **relatórios** com base nos dados cadastrados.

O sistema deverá ser implementado utilizando **funções** para cada operação e deverá realizar a **persistência de dados** através de **arquivos texto**, garantindo que todas as informações sejam salvas mesmo após o encerramento do programa.

---

## Estrutura de Dados

A aplicação deverá manipular as seguintes entidades e atributos:

### Clientes
- **CPF** (chave primária)
- Nome
- Endereço
- Telefone fixo
- Telefone celular
- Data de nascimento

### Reservas
- **Código** (chave primária)
- CPF do cliente

### Apartamentos
- **Código** (chave primária)
- Descrição
- Número de adultos
- Número de crianças
- Valor

### Reserva Apartamento
- **Código da reserva** (chave primária composta)
- **Código do apartamento** (chave primária composta)
- Data de entrada
- Data de saída

> ⚠️ **Atenção:** Os atributos destacados como **chaves** não podem ser duplicados. O sistema deve impedir a inclusão de registros com valores de chave já existentes.

---

## Funcionalidades

A aplicação deve apresentar um **Menu Principal** com as seguintes opções:

1. **Submenu de Clientes**
2. **Submenu de Reservas**
3. **Submenu de Apartamentos**
4. **Submenu de Reserva Apartamentos**
5. **Submenu de Relatórios**
6. **Sair**

### Estrutura dos Submenus

Cada submenu (Clientes, Reservas, Apartamentos, Reserva Apartamentos) deve conter as operações:

- Listar todos os registros
- Listar um registro específico
- Incluir um novo registro (sem permitir repetição de chaves)
- Alterar um registro existente
- Excluir um registro (após confirmação)

---

## Submenu de Relatórios

O submenu de relatórios deve permitir a geração das seguintes consultas:

- a) Mostrar todas as **reservas** de um determinado **apartamento**, informando o **código**.
- b) Mostrar todas as **reservas** de um determinado **cliente**, informando o **CPF**.
- c) Mostrar o **CPF** e **nome** de todos os clientes que fizeram **reservas dentro de um período** (entre datas X e Y, fornecidas pelo usuário).

---

## Requisitos de Implementação

✅ Não utilizar **variáveis globais**.  
✅ Transferir valores entre funções através de **parâmetros**.  
✅ Utilizar **nomes significativos** para variáveis e funções.  
✅ Utilizar **arquivos texto** para a **persistência** de dados.  
✅ Cada entidade terá o seu **arquivo específico**:  
- `clientes.txt`  
- `reservas.txt`  
- `apartamentos.txt`  
- `reserva_apartamentos.txt`

✅ Os **relatórios gerados** também devem ser armazenados em arquivos texto, permitindo a sua consulta posterior.

---

## Boas Práticas

- Estruturar o código com clareza e modularidade.
- Garantir a integridade e consistência dos dados.
- Validar as entradas do usuário, principalmente nas operações de inclusão e alteração.
- Garantir que as operações de exclusão sejam feitas **após confirmação** do usuário.
- Ao listar registros, apresentar os dados de forma clara e organizada.

---

## Considerações Finais

Este projeto visa exercitar e consolidar os seguintes conhecimentos:

- Manipulação de **arquivos texto** em Python.
- Uso adequado de **funções** e **parâmetros**.
- Organização e controle de **estruturas de dados compostas**.
- Desenvolvimento de sistemas com **múltiplas entidades relacionadas**.
- Implementação de **relatórios** automatizados.
