### Visão geral

Este projeto fornece uma aplicação de desktop (GUI) baseada em CustomTkinter para:

- Renomear diretórios de lotes e seus arquivos relacionados
- Padronizar nomes e números com zeros à esquerda
- Atualizar conteúdos de arquivos `.txt` relacionados ao lote
- Analisar automaticamente infrações e sugerir padronizações de códigos
- Utilizar componentes UI auxiliares como `CTkListbox` e menus suspensos roláveis

Aplicação principal: `gui.Application` (iniciada por `main.py`).

### Requisitos e instalação

1) Crie e ative um ambiente virtual (opcional)
2) Instale dependências:

```bash
pip install -r requirements.txt
```

3) Execute a aplicação:

```bash
python main.py
```

### Documentação

- Guia Rápido: `docs/quickstart.md`
- Referência de API:
  - `docs/api/application.md`
  - `docs/api/file_renamer.md`
  - `docs/api/text_file_editor.md`
  - `docs/api/infraction_analyzer.md`
  - `docs/api/ctk_listbox.md`
  - `docs/api/ctk_scrollable_dropdown.md`

### Estrutura principal do código

- `main.py`: ponto de entrada da aplicação
- `gui.py`: classe `Application` (janela e widgets)
- `file_renamer.py`: utilitário para renomeação de diretórios, arquivos e conteúdos
- `text_file_editor.py`: utilitário para atualizar linhas em arquivos `.txt`
- `infraction_analyzer.py`: análise e alteração de códigos de infração
- `CTkListbox/`, `CTkScrollableDropdown/`: componentes UI reutilizáveis

