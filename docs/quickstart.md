### Quickstart

Este guia mostra como iniciar a aplicação e executar tarefas comuns.

#### Executar a aplicação GUI

```bash
python main.py
```

Na janela:
- Clique em "Selecione a Pasta" e escolha o diretório onde estão os lotes
- Selecione o lote desejado no combobox
- Digite o novo nome (ex.: L05286)
- Clique em "Executar"

Após renomear, a aplicação analisará automaticamente infrações e poderá sugerir uma padronização.

#### Uso programático (sem GUI)

```python
from file_renamer import FileRenamer
from text_file_editor import TextFileEditor
from infraction_analyzer import InfractionAnalyzer

base_dir = "/caminho/para/lotes"

# Renomeação de diretório, arquivos e conteúdo de texto
renamer = FileRenamer(base_dir)
renamer.rename_directory("L05282", "L05286")
renamer.rename_files("L05282", "L05286")
renamer.rename_text_content("L05282", "L05286")

# Atualização de conteúdo de texto (isolada)
editor = TextFileEditor(base_dir)
editor.edit_text_content("L05286", "L05286")

# Análise e padronização de infrações
analyzer = InfractionAnalyzer(base_dir)
counts = analyzer.analyze_infractions("L05286")
print(counts)

# Converter todas as ocorrências 6050 -> 5673
files_mod, lines_mod = analyzer.change_infraction_codes("L05286", "6050", "5673")
print(files_mod, lines_mod)
```

