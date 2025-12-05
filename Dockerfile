# Base Python
FROM python:3

# Define o diretório da aplicação
WORKDIR /app


# Copia o arquivo de dependências
COPY requirements.txt .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Expõe a porta do Django
EXPOSE 8000

# Comando padrão ao iniciar o container
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
