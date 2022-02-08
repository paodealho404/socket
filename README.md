# SOCKET

Projeto de uma aplicação em redes utilizando sockets apresentado como requisito avaliativo para a disciplina de Redes de computadores, ministrada no Instituto de Computação da Universidade Federal de Alagoas (UFAL)

---
Alunos 
- Lucas Lemos Cerqueira
- Pedro Henrique de Brito Nascimento

## Principais Funcionalidades
A aplicação dispõem de 4 funcionalidades:

    - Upload de arquivos para o servidor
    - Download de arquivos do servidor:
    - Listagem de arquivos do servidor
    - Remoção de arquivos do servidor
    
## O que poderia ser implementado a mais

## Principais dificuldade na implementação do projeto

## Executando o projeto

Com a pasta do projeto na sua máquina, primeiramente separe dois terminais um para o servidor e outro para o cliente, note que o servidor precisa ser o primeiro a ser executado. Para isso, siga o script abaixo para rodar o servidor.

```bash
    $ cd server
    $ python server.py
```

Esse script aceita dois parâmetros adicionais, um para definir o endereço Ip e o outro para definir o número da porta. Caso nenhum parâmetro seja adicionado, por padrão o socket será criado para o endereço IP da sua máquina na porta 20.
```bash
    $ python server.py 192.168.0.21 8080
```
Com o lado do servidor em execução, utilize um outro terminal para executar o cliente. Para isso, siga o script abaixo para rodar o cliente.

```bash
   $ cd client
   $ python client.py
```
O script do cliente também aceita dois parâmetros adicionais da mesma forma que o servidor, um para o endereço IP e outro para definir o número da porta. Caso nenhum parâmetro seja adicionado, por padrão o socket será criado para o endereço IP da sua máquina na porta 20. 
```bash
    $ python client.py 192.168.0.21 8080
```
Com o cliente executando, será disposto um menu como o mostrado abaixo:

    Functionalities:
    - UPLD   Send File to the server      
    - DWLD   Download File from the server
    - SHOW   List all files in the server 
    - DELT   Delete a File from the server
    - HELP   Help
    - DISC   Quit
    Choose one command...

Ao escolher um comando, o mesmo contará com as informações necessárias para o correto funcionamento da funcionalidade.