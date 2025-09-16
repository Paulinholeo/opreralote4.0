### CTkListbox

Listbox rolável para CustomTkinter.

Pacote: `CTkListbox`

#### Importação

```python
from CTkListbox import CTkListbox
```

#### Inicialização

```python
import customtkinter as tk
root = tk.CTk()
lb = CTkListbox(root, width=250, height=120, multiple_selection=True)
lb.pack(fill="x")
```

#### Métodos principais

- `insert(index, option, **kwargs)`
- `delete(index | "all" | "end")`
- `select(index)` / `activate(index | "all")`
- `deselect(index)` / `deactivate(index | "all")`
- `get(index=None)` retorna seleção atual (ou item por índice)
- `curselection()` retorna tupla de índices selecionados (em múltipla seleção)
- `size()` número de itens
- `configure(**kwargs)` altera opções (ex.: `hover_color`, `highlight_color`, `text_color`, `font`, `command`)

#### Exemplo

```python
lb.insert("end", "Item 1")
lb.insert("end", "Item 2")
lb.select(0)
print(lb.get())
```

