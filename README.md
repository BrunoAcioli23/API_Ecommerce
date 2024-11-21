# API Ecommerce

Uma API desenvolvida em Python com Flask para gerenciar funcionalidades relacionadas a um sistema de ecommerce.

## 🚀 Funcionalidades

- **Gerenciamento de Produtos**:
  - Cadastro, edição, exclusão e listagem de produtos.
- **Gerenciamento de Usuários**:
  - Registro de novos usuários.
  - Autenticação e login.
- **Integração com Swagger**:
  - Documentação interativa disponível via Swagger para testar endpoints.

## 🛠️ Tecnologias Utilizadas

- **Back-end**: Python, Flask
- **Documentação**: Swagger
- **Ambiente Virtual**: Configuração com `venv`
- **Gerenciamento de dependências**: Arquivo `requirements.txt`

## 📦 Instalação e Uso

Siga os passos abaixo para configurar e executar a API localmente:

1. Clone este repositório:
   ```bash
   git clone https://github.com/BrunoAcioli23/API_Ecommerce.git
   ```
2. Navegue até o diretório do projeto:
   ```bash
   cd API_Ecommerce
   ```
3. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```
4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
5. Execute a aplicação:
   ```bash
   python application.py
   ```
6. Acesse a documentação interativa do Swagger em:
   ```
   http://localhost:5000/swagger
   ```

## 📂 Estrutura do Projeto

- `application.py`: Arquivo principal para iniciar a API.
- `requirements.txt`: Lista de dependências necessárias.
- `swagger.yaml`: Configuração para a documentação Swagger.
- `venv/`: Ambiente virtual Python (não incluído no controle de versão).
- `instance/` e `__pycache__/`: Diretórios auxiliares e cache.

## 📝 Licença

Este projeto não possui uma licença especificada. Entre em contato com o autor para mais informações.

---

Desenvolvido por [Bruno Acioli](https://github.com/BrunoAcioli23)
