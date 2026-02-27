# scripts/bot.py
import sys
import json

def executar_automacao(param1, param2):
    # Aqui entraria seu Selenium ou PyAutoGUI
    print(f"Iniciando automação para: {param1}")
    # Simulando processamento...
    return {"status": "sucesso", "mensagem": f"Processo concluído para {param2}"}

if __name__ == "__main__":
    # Recebe os dados do Electron via argumentos de linha de comando
    dados_json = sys.argv[1]
    params = json.loads(dados_json)
    
    resultado = executar_automacao(params['campo1'], params['campo2'])
    
    # Envia o resultado de volta para o Electron via stdout (print)
    print(json.dumps(resultado))