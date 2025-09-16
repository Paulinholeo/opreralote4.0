### FileRenamer

Utilitário para renomear diretórios de lotes, corrigir estruturas internas e renomear arquivos e conteúdos.

Módulo: `file_renamer.py`

#### Importação

```python
from file_renamer import FileRenamer
```

#### Inicialização

```python
renamer = FileRenamer(directory="/caminho/base")
```

#### Métodos públicos

- `rename_directory(old_name: str, new_name: str) -> bool`
  - Renomeia o diretório do lote. Trata `.zip`/`.rar`. Atualiza estrutura interna (subdiretórios numéricos, `AITs`).

- `rename_files(old_name: str, new_name: str) -> None`
  - Renomeia arquivos em múltiplos diretórios relevantes. Regras especiais para `.jpg` e nomes como `L00125`.

- `rename_text_content(old_name: str, new_name: str) -> None`
  - Atualiza linhas em `.txt`: primeiro campo (número do lote padronizado com 7 dígitos), acrescenta `/2023` no segundo campo (se ausente), e atualiza nomes de arquivos.

- `rename_subdirectory_and_files(parent_directory: str, old_subdir_name: str, new_subdir_name: str) -> bool`
  - Renomeia subdiretório específico e seus arquivos, útil para `L08685/0000125 -> L08685/0008685`.

- `update_internal_structure(directory_name: str, old_internal_name: str, new_internal_name: str) -> bool`
  - Atualiza apenas a estrutura interna sem renomear o diretório principal.

#### Observações de comportamento

- Padding: números de lote são padronizados para 7 dígitos.
- Ignora `md5sum.txt` ao alterar conteúdos.
- Extrai e move conteúdo se houver conflito de diretório alvo já existente.

#### Exemplos

```python
renamer = FileRenamer("/dados/lotes")
renamer.rename_directory("L05282", "L05286")
renamer.rename_files("L05282", "L05286")
renamer.rename_text_content("L05282", "L05286")
```

