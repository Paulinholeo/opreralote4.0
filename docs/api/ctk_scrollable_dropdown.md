### CTkScrollableDropdown e CTkScrollableDropdownFrame

Menus suspensos roláveis para CustomTkinter.

Pacote: `CTkScrollableDropdown`

#### Importação

```python
from CTkScrollableDropdown import CTkScrollableDropdown, CTkScrollableDropdownFrame
```

#### CTkScrollableDropdown (janela flutuante)

Construtor principal:

```python
CTkScrollableDropdown(
    attach, x=None, y=None, button_color=None, height: int = 200, width: int = None,
    fg_color=None, button_height: int = 20, justify="center", scrollbar_button_color=None,
    scrollbar=True, scrollbar_button_hover_color=None, frame_border_width=2, values=[],
    command=None, image_values=[], alpha: float = 0.97, frame_corner_radius=20,
    double_click=False, resize=True, frame_border_color=None, text_color=None,
    autocomplete=False, **button_kwargs
)
```

Métodos úteis:
- `popup(x=None, y=None)`
- `insert(value, **kwargs)`
- `configure(**kwargs)` (troca `values`, `height`, `width`, `button_color`, etc.)

Exemplo:

```python
dropdown = CTkScrollableDropdown(combo, values=["A", "B", "C"], justify="left")
dropdown.popup()
```

#### CTkScrollableDropdownFrame (embutido em frame)

Construtor principal:

```python
CTkScrollableDropdownFrame(
    attach, x=None, y=None, button_color=None, height: int = 200, width: int = None,
    fg_color=None, button_height: int = 20, justify="center", scrollbar_button_color=None,
    scrollbar=True, scrollbar_button_hover_color=None, frame_border_width=2, values=[],
    command=None, image_values=[], double_click=False, frame_corner_radius=True,
    resize=True, frame_border_color=None, text_color=None, autocomplete=False, **button_kwargs
)
```

Métodos úteis são equivalentes: `place_dropdown()`, `insert`, `configure`.

