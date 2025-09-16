"""
Configurações e constantes do sistema OperaLote.
"""

# Configurações de padding
DEFAULT_PADDING = 7
MIN_DIRECTORY_LENGTH = 6

# Extensões de arquivo
JPG_EXTENSION = '.jpg'
TXT_EXTENSION = '.txt'
ZIP_EXTENSION = '.zip'
RAR_EXTENSION = '.rar'

# Arquivos especiais
MD5SUM_FILENAME = 'md5sum.txt'

# Padrões de arquivo
L_PREFIX_PATTERN = 'L00'
L00125_PATTERN = 'L00125'

# Configurações de diretório
AITS_DIRECTORY = 'AITs'

# Configurações de texto
TEXT_SEPARATOR = ';'
YEAR_SUFFIX = '/2023'

# Configurações de logging
LOG_SUCCESS = "✅"
LOG_ERROR = "❌"
LOG_WARNING = "⚠️"
LOG_INFO = "ℹ️"

# Mensagens de log
LOG_MESSAGES = {
    'file_renamed': "Arquivo renomeado com sucesso: {} -> {}",
    'file_rename_error': "Erro ao renomear {}: {}",
    'file_exists': "Arquivo de destino já existe: {}",
    'file_exists_info': "Arquivo de destino já existe, não fazendo nada",
    'not_renaming': "Não renomeando: old_filename={}, full_new_filename={}",
    'jpg_updated': "JPG atualizado: {} -> {}",
    'text_file_updated': "Arquivo de texto atualizado: {}",
    'skip_md5sum': "Pulando md5sum.txt (conteúdo preservado): {}",
    'line_processed': "Linha processada: {}",
    'subdirectory_correction': "Verificação OBRIGATÓRIA: corrigindo subdiretórios em {}...",
    'subdirectory_detected': "DETECTADO: Subdiretório {} precisa ser renomeado para {}",
    'subdirectory_correcting': "CORRIGINDO AGORA: {} -> {}",
    'subdirectory_success': "SUCESSO: {}",
    'subdirectory_error': "ERRO ao corrigir subdiretório {}: {}",
    'correction_completed': "✅ CORREÇÃO CONCLUÍDA: {} subdiretório(s) corrigido(s)",
    'verification_ok': "✅ VERIFICAÇÃO OK: Nenhum subdiretório precisa de correção"
}
