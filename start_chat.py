import os
import sys
import subprocess
import logging
import platform

# Configuração do logging para exibir informações sobre cada etapa
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Nomes de diretórios e arquivos
VENV_DIR = "venv"
REQUIREMENTS_FILE = "requirements.txt"

def get_executable_path(executable_name):
    """Retorna o caminho para o executável dentro do ambiente virtual, compatível com Windows e Unix."""
    if platform.system() == "Windows":
        return os.path.join(VENV_DIR, "Scripts", f"{executable_name}.exe")
    else:
        return os.path.join(VENV_DIR, "bin", executable_name)

def run_command(command, description):
    """Executa um comando no shell e loga sua descrição."""
    logging.info(f"Iniciando: {description}")
    try:
        # Usando shell=True para compatibilidade, especialmente com comandos do Windows
        subprocess.run(command, check=True, shell=True, capture_output=True, text=True)
        logging.info(f"Concluído: {description}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Erro ao executar: {description}")
        logging.error(f"Comando: {e.cmd}")
        logging.error(f"Output: {e.stdout}")
        logging.error(f"Stderr: {e.stderr}")
        sys.exit(1)

def main():
    """Orquestra as etapas de inicialização da aplicação."""
    # 1. Iniciar Docker
    run_command("docker compose up -d", "Iniciando contêineres Docker em segundo plano")

    # 2. Criar ambiente virtual se não existir
    if not os.path.isdir(VENV_DIR):
        logging.info("Criando ambiente virtual...")
        # Usa o executável do Python que está rodando o script para criar o venv
        run_command(f"{sys.executable} -m venv {VENV_DIR}", "Criação do ambiente virtual")
    else:
        logging.info("Ambiente virtual já existe.")

    # Caminhos para os executáveis do venv
    python_executable = get_executable_path("python")
    pip_executable = get_executable_path("pip")

    # 3. Instalar dependências
    run_command(f"{pip_executable} install -r {REQUIREMENTS_FILE}", f"Instalando dependências de {REQUIREMENTS_FILE}")

    # 4. Executar ingestão de dados
    run_command(f"{python_executable} src/ingest.py", "Executando o script de ingestão de dados")

    # 5. Iniciar o chat
    logging.info("Iniciando o chat. Pressione Ctrl+C para sair.")
    # O chat é executado diretamente no terminal atual para permitir interação do usuário
    chat_process = subprocess.run([python_executable, "src/chat.py"])
    
    if chat_process.returncode != 0:
        logging.error("O script de chat terminou com um erro.")

if __name__ == "__main__":
    main()
