### Application (GUI)

Classe principal da interface gráfica, definida em `gui.Application`.

#### Importação

```python
from gui import Application
```

#### Inicialização

```python
import customtkinter as tk
root = tk.CTk()
app = Application(master=root)
root.mainloop()
```

#### Principais responsabilidades

- Seleção de diretório de lotes e preenchimento do combobox
- Renomeação orquestrada (diretórios, arquivos e conteúdos)
- Análise automática de infrações e sugestão de padronização
- Diálogos de ajuda e mensagens ao usuário

#### Métodos públicos relevantes

- `create_widgets()`
  - Constrói e posiciona os widgets da janela

- `select_directory()`
  - Abre um seletor de diretórios, instancia utilitários (`FileRenamer`, `TextFileEditor`, `InfractionAnalyzer`) e popula o combobox com lotes

- `rename()`
  - Valida entradas e executa a sequência de renomeação: diretório, arquivos, conteúdo, seguida da análise automática

- `auto_analyze_and_suggest_changes(lote_name)`
  - Executa análise automática de infrações para o lote e prepara sugestões

- `apply_automatic_changes(new_code, lote_name)`
  - Aplica padronização de códigos de infração em todos os arquivos `.txt` pertinentes

#### Exemplo de fluxo (GUI)

1) Usuário seleciona a pasta base
2) Escolhe o lote
3) Define o novo nome
4) Clica em Executar → a aplicação renomeia e sugere padronizações de infração

