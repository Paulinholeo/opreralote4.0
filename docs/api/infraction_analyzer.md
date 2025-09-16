### InfractionAnalyzer

Analisa e altera códigos de infração em arquivos `.txt` de um lote.

Módulo: `infraction_analyzer.py`

#### Importação

```python
from infraction_analyzer import InfractionAnalyzer
```

#### Inicialização

```python
analyzer = InfractionAnalyzer(directory="/caminho/base")
```

#### Métodos públicos

- `analyze_infractions(lote_name: str) -> dict[str,int]`
  - Conta ocorrências de cada código de infração nos `.txt` do lote (ignorando `md5sum.txt`).

- `change_infraction_codes(lote_name: str, old_code: str, new_code: str) -> tuple[int,int]`
  - Substitui o código de infração (último campo da linha separada por `;`) de `old_code` para `new_code`.
  - Retorna `(arquivos_modificados, linhas_alteradas)`.

- `get_infraction_description(code: str) -> str`
  - Retorna a descrição conhecida para códigos: `5673`, `6050`, `7587`. Para outros, retorna `Código {code}`.

#### Diretórios analisados

- Diretório do lote e seus subdiretórios; inclui `AITs` se existir.

#### Exemplo

```python
analyzer = InfractionAnalyzer("/dados/lotes")
counts = analyzer.analyze_infractions("L05286")
print(counts)
files, lines = analyzer.change_infraction_codes("L05286", "6050", "5673")
print(files, lines)
```

