# Lea Record Shop
Sistema para a loja de discos Lea Record Shop, que essencialmente 
implementa um CRUD modificado para o catalogo e vendas da loja.

## Tecnologias empregadas
- PostgreSQL - Banco de dados usado para o armazenamento.
- Django - Modela o problema em uma arquitetura MTV, ou 
nesse caso, MC, já que não implementamos front-end 
- Django Rest Framework - permite expor os modelos django como uma aplicação REST.
- Pytest - sistema de testes para Python
- DRF-Yasg - ferramenta de geração de documentação Swagger automatizada

## Requisitos
- Python 3.10
- PostgreSQL 14.1
- - Um banco de dados dentro do PostgreSQL que possa ser usado pela aplicação
- - Um usuário com permissão total nesse banco

## Instruções para rodar o projeto
- Copie o arquivo .env.example, renomeando-o para .env
- Abra o arquivo em algum editor de texto (como o Notepad, ou Nano), 
e preencha as variáveis de conexão ao banco de dados
- Em uma ferramenta de linha de comando (como o Bash, ou o PowerShell), 
vá na pasta raiz do projeto e execute os seguintes comandos:
> pip install -r requirements.txt
> 
> python manage.py migrate
>
> 
> python manage.py runserver

## Versão funcional
O sistema pode ser visto em funcionamento em https://arcane-mesa-31455.herokuapp.com/
