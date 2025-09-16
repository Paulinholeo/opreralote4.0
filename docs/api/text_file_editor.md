### TextFileEditor

Atualiza conteúdos de arquivos `.txt` relacionados a um lote, padronizando números e atualizando nomes de arquivos.

Módulo: `text_file_editor.py`

#### Importação

```python
from text_file_editor import TextFileEditor
```

#### Inicialização

```python
editor = TextFileEditor(directory="/caminho/base")
```

#### Métodos públicos

- `edit_text_content(old_name: str, new_name: str) -> None`
  - Para cada arquivo `.txt` (exceto `md5sum.txt`):
    - Atualiza primeiro campo com número do lote (7 dígitos)
    - Acrescenta `/2023` ao segundo campo se ausente
    - Atualiza nomes de `.jpg` e demais campos que contenham o número antigo

#### Regras de atualização de JPG

- Remove prefixo `00` no início do nome, se houver, antes de processar
- Substitui sequências numéricas longas pelo novo número (7 dígitos) preservando o sufixo restante

#### Exemplo

```python
editor = TextFileEditor("/dados/lotes")
editor.edit_text_content("L05282", "L05286")
```

