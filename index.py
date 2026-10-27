import csv
import os
import time
import webbrowser
import pyautogui

# Configuração de segurança do PyAutoGUI
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

# Nome padrão do arquivo CSV de notas
NOME_ARQUIVO_CSV = "notas_alunos.csv"


def criar_csv_exemplo_se_nao_existir():
  """Cria um arquivo CSV de exemplo caso ele ainda não exista na pasta do projeto."""
  if not os.path.exists(NOME_ARQUIVO_CSV):
    with open(
        NOME_ARQUIVO_CSV, mode="w", newline="", encoding="utf-8"
    ) as arquivo:
      escritor = csv.writer(arquivo, delimiter=";")
      escritor.writerow(["Nome", "RA", "Nota01", "TF01"])
      # Substituído pelos dados padrão reais do projeto
      escritor.writerow(["Ana Silva", "2026001", "8.5", "9.0"])
      escritor.writerow(["Bruno Souza", "2026002", "7.0", "6.5"])
      escritor.writerow(["Carla Dias", "2026003", "9.2", "8.0"])


def carregar_dados_csv():
  """Carrega os dados dos alunos a partir do arquivo CSV."""
  criar_csv_exemplo_se_nao_existir()
  alunos = []
  with open(
      NOME_ARQUIVO_CSV, mode="r", encoding="utf-8-sig"
  ) as arquivo_csv:
    leitor = csv.DictReader(arquivo_csv, delimiter=";")
    for linha in leitor:
      alunos.append(linha)
  return alunos


def consultar_dados(alunos):
  """Permite consultar os alunos e notas carregadas do arquivo CSV."""
  print("\n--- CONSULTA DE DADOS (CSV) ---")
  if not alunos:
    print("Nenhum aluno encontrado ou arquivo vazio.")
    return
  print(f"Total de alunos carregados: {len(alunos)}")
  for i, aluno in enumerate(alunos, 1):
    print(
        f"{i}. Nome: {aluno.get('Nome')} | RA: {aluno.get('RA')} | Nota:"
        f" {aluno.get('Nota01')}"
    )
  print("-" * 31)


def alterar_configuracoes():
  """Permite alterar parâmetros globais do script em tempo de execução."""
  global NOME_ARQUIVO_CSV
  print("\n--- ALTERAR CONFIGURAÇÕES ---")
  print(f"Arquivo CSV atual: {NOME_ARQUIVO_CSV}")
  novo_nome = input(
      "Digite o novo nome do arquivo CSV (ou aperte Enter para manter): "
  ).strip()
  if novo_nome:
    NOME_ARQUIVO_CSV = novo_nome
    print(f"Arquivo CSV alterado para: {NOME_ARQUIVO_CSV}")
  print("Configurações atualizadas com sucesso!")


def executar_automacao(alunos):
  """Executa o robô de lançamento de notas usando PyAutoGUI."""
  if not alunos:
    print("Erro: Não há alunos carregados para iniciar a automação.")
    return

  print(
      "\nIniciando o robô de lançamento de notas... Posicione o sistema"
      " acadêmico na tela."
  )
  print(
      "Aviso: Para parar o robô de emergência, arraste o mouse para qualquer"
      " canto da tela (Fail-Safe)."
  )

  time.sleep(3)  # Tempo para focar na tela do sistema

  try:
    for aluno in alunos:
      print(
          f"Lançando nota para: {aluno.get('Nome')} (RA:"
          f" {aluno.get('RA')})"
      )

      # 1. Clica na barra de busca do sistema (ajuste as coordenadas x e y conforme sua tela)
      pyautogui.click(x=350, y=200)

      # Limpa o campo
      pyautogui.hotkey("ctrl", "a")
      pyautogui.press("backspace")

      # 2. Digita a matrícula/RA e vai para o próximo campo
      pyautogui.write(aluno.get("RA"))
      pyautogui.press("tab")

      # 3. Digita a nota e confirma/salva
      pyautogui.write(aluno.get("Nota01"))
      pyautogui.press("enter")

      time.sleep(1)  # Pausa para salvamento

    print("Lançamento de notas concluído com sucesso!")

  except pyautogui.FailSafeException:
    print(
        "\n[INTERRUPÇÃO] O Fail-Safe foi acionado! O robô foi parado pelo"
        " usuário."
    )

  finally:
    # Redirecionamento automático para o Google Drive ao finalizar ou interromper
    print("Redirecionando você para o Google Drive...")
    webbrowser.open("https://drive.google.com/")


def main():
  while True:
    alunos = carregar_dados_csv()

    print("\n========================================")
    print("   ROBÔ DE LANÇAMENTO DE NOTAS - MENU")
    print("========================================")
    print("1. Iniciar Automação (Lançar Notas)")
    print("2. Consultar Dados Carregados (CSV)")
    print("3. Alterar Configurações (Nome do Arquivo)")
    print("4. Sair")

    opcao = input("\nEscolha uma opção (1-4): ").strip()

    if opcao == "1":
      executar_automacao(alunos)
    elif opcao == "2":
      consultar_dados(alunos)
    elif opcao == "3":
      alterar_configuracoes()
    elif opcao == "4":
      print("Encerrando o programa. Até logo!")
      break
    else:
      print("Opção inválida! Escolha um número de 1 a 4.")


if __name__ == "__main__":
  main()