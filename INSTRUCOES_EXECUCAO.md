# 🚀 Instruções de Execução - OperaLote 4.3

## 📋 Como Executar a Aplicação

### Método 1: Script de Execução (RECOMENDADO)
```cmd
start.bat
```

### Método 2: Execução Direta
```cmd
cd src
python main.py
```

### Método 3: Execução da Raiz
```cmd
python main.py
```

## 🏗️ Estrutura de Execução

### Arquivos de Execução:
- `start.bat` - Script de execução automática
- `main.py` - Ponto de entrada da raiz
- `run.py` - Alternativa de execução
- `src/main.py` - Ponto de entrada principal

### Configuração de Path:
- O `main.py` da raiz configura automaticamente o path
- Adiciona `src/` ao `sys.path` do Python
- Permite imports relativos funcionarem

## 🔧 Solução de Problemas

### Erro: "ModuleNotFoundError: No module named 'src'"
**Solução:**
- Use `start.bat` ou execute de dentro de `src/`
- Verifique se está no diretório correto

### Erro: "No module named 'file_renamer'"
**Solução:**
- Execute de dentro da pasta `src/`
- Use o script `start.bat`

### Erro: "Cannot find icon file"
**Solução:**
- Verifique se a pasta `assets/logo/` existe
- Execute da raiz do projeto

## 📁 Estrutura de Arquivos

```
OperaLote_3.0/
├── start.bat              # Script de execução
├── main.py                # Ponto de entrada da raiz
├── run.py                 # Alternativa de execução
├── src/                   # Código fonte
│   ├── main.py           # Ponto de entrada principal
│   ├── gui.py            # Interface gráfica
│   └── ...               # Outros módulos
├── assets/                # Recursos
│   └── logo/             # Logos e ícones
└── ...                   # Outros diretórios
```

## 🎯 Recomendação

**Use `start.bat`** para execução mais simples e confiável:
- ✅ Configura automaticamente o ambiente
- ✅ Navega para o diretório correto
- ✅ Executa a aplicação
- ✅ Pausa para ver erros

## 🔍 Verificação

### Teste de Execução:
1. Execute `start.bat`
2. Verifique se a interface gráfica abre
3. Teste as funcionalidades básicas
4. Verifique se não há erros no console

### Logs:
- Verifique a pasta `logs/` para arquivos de log
- Execute em modo console para debug detalhado

---
**Estrutura organizada e pronta para execução!**
