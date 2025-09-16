import customtkinter as tk

from tkinter import filedialog, messagebox
from file_renamer import FileRenamer
from PIL import Image, ImageTk
import os
from text_file_editor import TextFileEditor
from CTkScrollableDropdown import *
from infraction_analyzer import InfractionAnalyzer


class Application(tk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("850x800")  # Aumentado para acomodar novos campos
        self.master.title("LOTE BRASCONTROL")
        self.master.iconbitmap('logo/b.ico')  
        self.pack(padx=12,pady=12)
        self.file_list = []
        self.infraction_analyzer = None
        self.create_widgets()

    def show_message(self, message):
        messagebox.showinfo("Renomear Lote BRC", message)
    
    def event(self):
        if self.switch_var.get() == 'Ativado':
            tk.set_appearance_mode('Light')
        elif self.switch_var.get() == 'Desativado':
            tk.set_appearance_mode('Dark')
        else:
            tk.set_appearance_mode('System')
            
        print("Tema Claro: ", self.switch_var.get())

    def create_widgets(self):
        self.file_renamer = None
        self.text_file_editor = None
        self.switch_var = tk.StringVar(value="on")      

        self.directory_label = tk.CTkLabel(self, text="Operação do Lote", font=("Roboto ", 24))
        self.directory_label.pack(padx=12, pady=10)
        self.directory_entry = tk.CTkEntry(self, width=350, height=35, placeholder_text="Clique no botão abaixo e Selecione diretorio dos lotes  ")
        self.directory_entry.pack(padx=12,pady=5)


        self.directory_button = tk.CTkButton(self, width=150, text="Selecione a Pasta", command= self.select_directory)
        self.directory_button.pack(padx=12,pady=10)

        self.space_label = tk.CTkLabel(self, text="", height=2)
        self.space_label.pack()

        self.old_name_label = tk.CTkLabel(self, text="Escolha o lote a ser renomeado", font=("Arial", 15))
        self.old_name_label.pack()
        self.lote_combo = tk.CTkComboBox(self, width=250)
        self.lote_combo.pack(fill="x", padx=12, pady=10)

        self.space_label = tk.CTkLabel(self, text="", height=2)
        self.space_label.pack()

        self.new_name_label = tk.CTkLabel(self, text="Digite o novo nome do lote", font=("Arial", 15))
        self.new_name_label.pack()
        self.new_name_entry = tk.CTkEntry(self, width=350, height=35, placeholder_text="ex.: L05286")
        self.new_name_entry.pack(padx=12, pady=10)
    
        self.directory_button = tk.CTkButton(self, width=150, text="Executar", command= self.rename)
        self.directory_button.pack(padx=12,pady=10)
              
        self.space_label = tk.CTkLabel(self, text="", height=1)
        self.space_label.pack()

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "logo")
        self.logo_image = tk.CTkImage(Image.open(os.path.join(image_path, "brc_b3.png")), size=(200, 100))
        self.logo_label = tk.CTkLabel(self, text=None, image=self.logo_image)
        self.logo_label.pack()


        self.space_label = tk.CTkLabel(self, text="", height=1)
        self.space_label.pack()


        self.help_icon = tk.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(25, 25))

        self.help_button = tk.CTkButton(self, image=self.help_icon, command=self.show_help_message,corner_radius=0, height=40, border_spacing=10, text="Ajuda",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"))
        self.help_button.pack(padx=10)
        self.switch= tk.CTkSwitch(self,
                                text="Tema",
                                command=self.event,
                                variable=self.switch_var,
                                onvalue="Ativado",
                                offvalue="Desativado")
        self.switch.pack(padx=10, pady=10)
        
        self.copyright_label = tk.CTkLabel(self, text="Versão 4.0 - © Brascontrol", font=("Arial", 12))
        self.copyright_label.pack()

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory_entry.delete(0, tk.END)
            self.directory_entry.insert(0, directory)
            self.file_renamer = FileRenamer(directory)
            self.text_file_editor = TextFileEditor(directory)
            self.infraction_analyzer = InfractionAnalyzer(directory)
            self.file_list = os.listdir(directory)
            CTkScrollableDropdown(self.lote_combo, values=self.file_list, justify="left", button_color="transparent")   
        else:
            messagebox.showinfo("Renomear Lote BRC", "Diretório não encontrado")

   
    def rename(self):
        old_name = self.lote_combo.get()
        new_name = self.new_name_entry.get()
        
        if not old_name or not new_name:
            messagebox.showwarning("Aviso", "Selecione um lote e digite o novo nome")
            return
            
        if self.file_renamer.rename_directory(old_name, new_name):
            self.file_renamer.rename_files(old_name, new_name)
            self.file_renamer.rename_text_content(old_name, new_name)
            self.text_file_editor.edit_text_content(old_name, new_name)
            
            # === ANÁLISE AUTOMÁTICA DE INFRAÇÕES APÓS RENOMEAÇÃO ===
            self.auto_analyze_and_suggest_changes(new_name)
            
            self.show_message("Renomeado com Sucesso")  
        else:
            self.show_message("Falha ao Renomear o Lote. Verifique se o lote existe")  


    def show_help_message(self):
        message = "1 - Selecione o diretorio onde se encontra os Lotes:\n2 - Escolha o lote a ser renomeado poder pasta ou arquivo zip\n3 - digite o novo nome do Lote\n4 - Clique em Executar\n\nNome de lotes aceitos:\nL05282, 0005282, L0230712\nL05282.zip, 000582.zip, L0230712.zip\n\nFuncionalidades de Infrações:\n- Analise automática de códigos de infração\n- Alteração em massa de códigos\n- 5673: Parado sobre faixa de pedestre\n- 6050: Avanço de sinal vermelho\n- 7587: Transitar em faixa exclusiva"                  
        messagebox.showinfo("Ajuda", message)

    def auto_analyze_and_suggest_changes(self, lote_name):
        """Analisa automaticamente as infrações após renomeação e sugere mudanças"""
        if not self.infraction_analyzer:
            return
            
        try:
            print(f"\n=== ANÁLISE AUTOMÁTICA DE INFRAÇÕES PARA {lote_name} ====")
            
            # Analisa as infrações do lote renomeado
            self.infraction_counts = self.infraction_analyzer.analyze_infractions(lote_name)
            
            if not self.infraction_counts:
                print("Nenhuma infração encontrada para análise")
                return
                
            # Analisa e sugere mudanças baseado em regras inteligentes
            suggestion = self.analyze_and_suggest_infraction_changes()
            
            if suggestion:
                self.prompt_automatic_change(suggestion, lote_name)
                
        except Exception as e:
            print(f"Erro na análise automática: {e}")
    
    def analyze_and_suggest_infraction_changes(self):
        """Analisa padrões e sugere mudanças inteligentes de códigos"""
        if not self.infraction_counts:
            return None
            
        total_infractions = sum(self.infraction_counts.values())
        
        # Regra 1: Se mais de 70% são de um tipo específico, sugere padronizar
        for code, count in self.infraction_counts.items():
            percentage = (count / total_infractions) * 100
            if percentage >= 70 and code in ["5673", "6050", "7587"]:
                description = self.infraction_analyzer.get_infraction_description(code)
                return {
                    "type": "padronizar_majoritario",
                    "suggested_code": code,
                    "description": description,
                    "count": count,
                    "total": total_infractions,
                    "percentage": percentage,
                    "reason": f"Maioria das infrações ({percentage:.1f}%) já são do tipo {code}"
                }
        
        # Regra 2: Se há mistura de códigos, sugere o mais comum dos conhecidos
        known_codes = {"5673": 0, "6050": 0, "7587": 0}
        for code in known_codes:
            known_codes[code] = self.infraction_counts.get(code, 0)
            
        if sum(known_codes.values()) > 0:
            most_common_code = max(known_codes.keys(), key=lambda k: known_codes[k])
            most_common_count = known_codes[most_common_code]
            
            if most_common_count > 0 and len([c for c in known_codes.values() if c > 0]) > 1:
                description = self.infraction_analyzer.get_infraction_description(most_common_code)
                return {
                    "type": "unificar_comum",
                    "suggested_code": most_common_code,
                    "description": description,
                    "count": most_common_count,
                    "total": total_infractions,
                    "reason": f"Unificar para o código mais comum: {most_common_code} ({most_common_count} ocorrências)"
                }
        
        # Regra 3: Se há códigos desconhecidos, sugere padronizar para 5673 (mais comum)
        unknown_codes = {code: count for code, count in self.infraction_counts.items() 
                        if code not in ["5673", "6050", "7587"]}
        
        if unknown_codes and not any(known_codes.values()):
            return {
                "type": "padronizar_desconhecidos",
                "suggested_code": "5673",
                "description": "PARADO SOBRE A FAIXA DE PEDESTRE",
                "count": 0,
                "total": total_infractions,
                "unknown_codes": unknown_codes,
                "reason": "Códigos desconhecidos encontrados. Sugerindo padronizar para 5673 (mais comum)"
            }
            
        return None
    
    def prompt_automatic_change(self, suggestion, lote_name):
        """Pergunta ao usuário se quer aplicar a sugestão automaticamente com interface melhorada"""
        try:
            suggestion_type = suggestion["type"]
            suggested_code = suggestion["suggested_code"]
            description = suggestion["description"]
            reason = suggestion["reason"]
            total = suggestion["total"]
            
            # Cria janela popup personalizada com seleção de infrações
            popup = tk.CTkToplevel(self.master)
            popup.title("🤖 Seleção de Infração")
            popup.geometry("500x400")
            popup.resizable(False, False)
            popup.transient(self.master)  # Mantém sobre a janela principal
            popup.grab_set()  # Bloqueia interação com a janela principal
            
            # Centraliza o popup
            popup.update_idletasks()
            x = (popup.winfo_screenwidth() // 2) - (500 // 2)
            y = (popup.winfo_screenheight() // 2) - (400 // 2)
            popup.geometry(f"500x400+{x}+{y}")
            
            # Frame principal
            main_frame = tk.CTkFrame(popup)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Título
            title_label = tk.CTkLabel(main_frame, text="📊 Análise Automática Concluída", 
                                     font=("Arial", 16, "bold"))
            title_label.pack(pady=(10, 5))
            
            # Informações da análise
            info_text = f"Encontradas {total} infrações no lote."
            info_label = tk.CTkLabel(main_frame, text=info_text)
            info_label.pack(pady=5)
            
            # Motivo da sugestão
            reason_label = tk.CTkLabel(main_frame, text=f"\ud83d\udd0d {reason}", 
                                      font=("Arial", 12), wraplength=450)
            reason_label.pack(pady=5)
            
            # Separação
            separator = tk.CTkFrame(main_frame, height=2)
            separator.pack(fill="x", pady=10)
            
            # Instrução
            instruction_label = tk.CTkLabel(main_frame, text="🎯 Escolha a infração para padronização:", 
                                           font=("Arial", 14, "bold"))
            instruction_label.pack(pady=(5, 10))
            
            # Lista de infrações disponíveis
            infractions_list = [
                ("5673", "PARADO SOBRE A FAIXA DE PEDESTRE"),
                ("6050", "AVANÇO DE SINAL VERMELHO"),
                ("7587", "TRANSITAR EM FAIXA EXCLUSIVA")
            ]
            
            # Variável para armazenar a escolha
            selected_code = tk.StringVar(value=suggested_code)
            
            # Frame para os radio buttons
            options_frame = tk.CTkFrame(main_frame)
            options_frame.pack(fill="both", expand=True, pady=10)
            
            # Cria radio buttons para cada infração
            for code, desc in infractions_list:
                radio_frame = tk.CTkFrame(options_frame, fg_color="transparent")
                radio_frame.pack(fill="x", pady=2)
                
                radio = tk.CTkRadioButton(radio_frame, text=f"{code} - {desc}", 
                                         variable=selected_code, value=code)
                radio.pack(side="left", padx=10)
                
                # Marca o sugerido por padrão
                if code == suggested_code:
                    radio.select()
            
            # Frame para botões
            buttons_frame = tk.CTkFrame(main_frame, fg_color="transparent")
            buttons_frame.pack(fill="x", pady=10)
            
            # Botão para aplicar
            def apply_selection():
                chosen_code = selected_code.get()
                chosen_desc = dict(infractions_list)[chosen_code]
                popup.destroy()
                self.apply_automatic_changes(chosen_code, lote_name)
                
                # Mensagem de sucesso
                success_msg = (f"\u2705 Padronização aplicada com sucesso!\n\n"
                             f"Todas as {total} infrações foram convertidas para:\n"
                             f"Código: {chosen_code}\n"
                             f"Tipo: {chosen_desc}")
                messagebox.showinfo("\u2705 Sucesso", success_msg)
            
            apply_button = tk.CTkButton(buttons_frame, text="✅ Aplicar Seleção", 
                                       command=apply_selection, 
                                       fg_color="green", hover_color="darkgreen")
            apply_button.pack(side="left", padx=10, pady=10)
            
            # Botão para fechar
            close_button = tk.CTkButton(buttons_frame, text="❌ Fechar", 
                                       command=popup.destroy,
                                       fg_color="red", hover_color="darkred")
            close_button.pack(side="right", padx=10, pady=10)
            
            # Foco no popup
            popup.focus_set()
            
        except Exception as e:
            print(f"Erro ao criar popup de seleção: {e}")
            # Fallback para messagebox simples
            self.fallback_prompt(suggestion, lote_name)
    
    def fallback_prompt(self, suggestion, lote_name):
        """Fallback para messagebox simples caso o popup personalizado falhe"""
        try:
            suggested_code = suggestion["suggested_code"]
            description = suggestion["description"]
            reason = suggestion["reason"]
            total = suggestion["total"]
            
            message = (f"\ud83d\udcca ANÁLISE AUTOMÁTICA CONCLUÍDA \ud83d\udcca\n\n"
                      f"Encontradas {total} infrações no lote.\n\n"
                      f"\ud83d\udd0d SUGESTÃO INTELIGENTE:\n"
                      f"{reason}\n\n"
                      f"\u2699\ufe0f Ação Recomendada:\n"
                      f"Padronizar TODAS as infrações para:\n"
                      f"Código: {suggested_code}\n"
                      f"Tipo: {description}\n\n"
                      f"Deseja aplicar esta padronização automaticamente?")
            
            response = messagebox.askyesno("\ud83e\udd16 Sugestão Automática de Infrações", message)
            
            if response:
                self.apply_automatic_changes(suggested_code, lote_name)
            else:
                print("Usuário optou por não aplicar as mudanças automáticas")
                
        except Exception as e:
            print(f"Erro no fallback: {e}")
            # Fallback para messagebox simples
            self.fallback_prompt(suggestion, lote_name)
    
    def apply_automatic_changes(self, new_code, lote_name):
        """Aplica as mudanças automáticas de código"""
        try:
            total_files_modified = 0
            total_lines_modified = 0
            
            print(f"\n=== APLICANDO MUDANÇAS AUTOMÁTICAS ====")
            print(f"Alterando todos os códigos para: {new_code}")
            
            # Aplica mudanças para todos os códigos existentes
            for old_code in self.infraction_counts.keys():
                if old_code != new_code:  # Não alterar se já é o código desejado
                    files_mod, lines_mod = self.infraction_analyzer.change_infraction_codes(lote_name, old_code, new_code)
                    total_files_modified += files_mod
                    total_lines_modified += lines_mod
            
            # Re-analisa para atualizar contadores
            self.infraction_counts = self.infraction_analyzer.analyze_infractions(lote_name)
            
            description = self.infraction_analyzer.get_infraction_description(new_code)
            
            success_message = (f"\u2705 PADRONIZAÇÃO AUTOMÁTICA CONCLUÍDA!\n\n"
                             f"📋 Resultados:\n"
                             f"Arquivos modificados: {total_files_modified}\n"
                             f"Linhas alteradas: {total_lines_modified}\n\n"
                             f"🎯 Todas as infrações agora são:\n"
                             f"Código: {new_code}\n"
                             f"Tipo: {description}")
            
            messagebox.showinfo("✅ Sucesso Automático", success_message)
            
            print(f"Mudanças automáticas aplicadas: {total_files_modified} arquivos, {total_lines_modified} linhas")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao aplicar mudanças automáticas: {e}")
            print(f"Erro nas mudanças automáticas: {e}")








