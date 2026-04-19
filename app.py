import tkinter as tk
from pathlib import Path
import random
import sys
import webbrowser
import os
import subprocess
import time

try:
    from PIL import Image, ImageTk
except ImportError:
    print("Instale o Pillow com: pip install pillow")
    sys.exit(1)

BASE_DIR = Path(__file__).resolve().parent
IMG_DIR = BASE_DIR / "imagens"

TEXTO_INICIAL = "ESTOU VENDO VOCÊ"
TEXTO_FINAL = "VOCÊ ESTÁ COM MEDO?"
TEMPO_TEXTO_INICIAL_MS = 2200
TEMPO_CADA_IMAGEM_MS = 900
TEMPO_TEXTO_FINAL_MS = 3500

COR_FUNDO = "black"
COR_TEXTO = "white"
FONTE_TITULO = ("Arial", 34, "bold")
FONTE_FINAL = ("Arial", 30, "bold")
FONTE_GLITCH = ("Consolas", 22, "bold")

MENSAGENS_GLITCH = [
    "EU ESTOU AQUI",
    "OLHE PARA TRÁS",
    "VOCÊ NÃO ESTÁ SOZINHO",
    "EU SEI ONDE VOCÊ ESTÁ",
    "NÃO DESLIGUE",
    "TARDE DEMAIS",
    "VOCÊ ME VIU?",
    "NÃO TENTE FUGIR",
]

COMANDOS_CMD = [
    "echo ACESSO NEGADO...",
    "echo INVADINDO SISTEMA...",
    "echo COLETANDO DADOS...",
    "echo ERRO CRITICO...",
    "echo VOCE NAO DEVIA TER ABERTO ISSO...",
    "tree C:\\ /f",
    "echo SEU IP FOI CAPTURADO",
    "ping localhost -n 10",
    "color 0a",
    "color 4c",
    "dir C:\\ /s",
    "echo VOCE ESTA SENDO RASTREADO"
]

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Apresentação")
        self.root.configure(bg=COR_FUNDO)
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda e: self.cleanup_and_exit(desligar=False))

        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()

        self.main_label = tk.Label(
            root,
            text="",
            fg=COR_TEXTO,
            bg=COR_FUNDO,
            font=FONTE_TITULO,
            wraplength=self.screen_w - 100,
            justify="center"
        )
        self.main_label.place(relx=0.5, rely=0.5, anchor="center")

        self.image_label = tk.Label(root, bg=COR_FUNDO, bd=0, highlightthickness=0)
        self.image_label.place(relx=0.5, rely=0.5, anchor="center")

        self.glitch_labels = []
        self.images = sorted([
            p for p in IMG_DIR.iterdir()
            if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
        ]) if IMG_DIR.exists() else []

        self.current_index = 0
        self.photo_ref = None
        
        self.running = True
        self.janelas_abertas = []
        
        self.start_background_tasks()

        self.show_start_text()
    
    def start_background_tasks(self):
        self.schedule_video_open()
        self.schedule_cmd_open()
    
    def schedule_video_open(self):
        if not self.running:
            return
        
        num_videos = random.randint(1, 3)
        for _ in range(num_videos):
            self.abrir_video_janela_posicionado()
        
        intervalo = random.randint(5000, 12000)
        self.root.after(intervalo, self.schedule_video_open)
    
    def schedule_cmd_open(self):
        if not self.running:
            return
        
        num_cmds = random.randint(1, 3)
        for _ in range(num_cmds):
            self.abrir_cmd_janela_posicionado()
        
        intervalo = random.randint(3000, 8000)
        self.root.after(intervalo, self.schedule_cmd_open)
    
    def abrir_video_janela_posicionado(self):
        links_videos = [
            "https://youtu.be/DCsRmdYrRGw?si=38PEFt1DWSHpeWTA",
            "https://youtu.be/dQw4w9WgXcQ",
            "https://youtu.be/9bZkp7q19f0",
            "https://youtu.be/kJQP7kiw5Fk",
            "https://youtu.be/lAIGb1lfpBw",
            "https://youtu.be/UGLxIHVfTuk",
        ]
        
        link = random.choice(links_videos)
        
        larguras = [400, 500, 600, 700, 800]
        alturas = [300, 400, 500, 600]
        
        largura = random.choice(larguras)
        altura = random.choice(alturas)
        
        pos_x = random.randint(0, self.screen_w - largura - 50)
        pos_y = random.randint(0, self.screen_h - altura - 50)

        navegadores = [
            f'start chrome --new-window --window-size={largura},{altura} --window-position={pos_x},{pos_y} "{link}"',
            f'start firefox -new-window -width {largura} -height {altura} "{link}"',
            f'start msedge --new-window --window-size={largura},{altura} --window-position={pos_x},{pos_y} "{link}"',
        ]
        
        for navegador in navegadores:
            try:
                subprocess.Popen(navegador, shell=True)
                break
            except:
                continue
        else:
            webbrowser.open_new(link)
    
    def abrir_cmd_janela_posicionado(self):
        num_comandos = random.randint(3, 6)
        comandos_escolhidos = random.sample(COMANDOS_CMD, min(num_comandos, len(COMANDOS_CMD)))
        
        comando_encadeado = " & ".join(comandos_escolhidos)
        
        cores = ["0a", "0c", "0e", "1f", "2a", "4c", "5e"]
        cor_aleatoria = random.choice(cores)
        
        tamanhos = ["80x25", "100x30", "120x35", "90x28", "110x32"]
        tamanho = random.choice(tamanhos)

        pos_x = random.randint(50, self.screen_w - 400)
        pos_y = random.randint(50, self.screen_h - 300)
        
        ps_script = f'''
        Add-Type @"
          using System;
          using System.Runtime.InteropServices;
          public class Window {{
            [DllImport("user32.dll")]
            public static extern bool MoveWindow(IntPtr hWnd, int X, int Y, int nWidth, int nHeight, bool bRepaint);
            [DllImport("user32.dll")]
            public static extern IntPtr FindWindow(string className, string windowName);
          }}
        "@
        Start-Sleep -Milliseconds 500
        $hwnd = [Window]::FindWindow("ConsoleWindowClass", "SISTEMA COMPROMETIDO")
        if ($hwnd -ne 0) {{
          [Window]::MoveWindow($hwnd, {pos_x}, {pos_y}, 800, 500, $true)
        }}
        '''
        
        ps_file = f"temp_pos_{random.randint(1000, 9999)}.ps1"
        with open(ps_file, "w", encoding="utf-8") as f:
            f.write(ps_script)

        cmd_completo = f'start cmd /k "color {cor_aleatoria} & title SISTEMA COMPROMETIDO & echo ======================================== & echo    ACESSO NAO AUTORIZADO DETECTADO & echo ======================================== & echo. & {comando_encadeado} & echo. & echo Pressione qualquer tecla para fechar..."'
        
        try:
            subprocess.Popen(cmd_completo, shell=True)
            
            subprocess.Popen(f'powershell -ExecutionPolicy Bypass -File "{ps_file}"', shell=True)
            
            self.root.after(3000, lambda: self.remover_script_temp(ps_file))
            
        except Exception as e:
            print(f"Erro ao abrir CMD: {e}")
    
    def remover_script_temp(self, arquivo):
        try:
            if os.path.exists(arquivo):
                os.remove(arquivo)
        except:
            pass
    
    def fechar_todas_janelas(self):
        try:
            os.system('taskkill /f /im cmd.exe 2>nul')
            os.system('taskkill /f /im chrome.exe 2>nul')
            os.system('taskkill /f /im firefox.exe 2>nul')
            os.system('taskkill /f /im msedge.exe 2>nul')
            os.system('taskkill /f /im iexplore.exe 2>nul')
            os.system('taskkill /f /im opera.exe 2>nul')
            os.system('taskkill /f /im powershell.exe 2>nul')
            print("Todas as janelas foram fechadas!")
        except Exception as e:
            print(f"Erro ao fechar janelas: {e}")
    
    def abrir_imagem_final(self):
        self.clear_screen()
        
        imagem_final_path = IMG_DIR / "foto_7.jpg"
        
        if not imagem_final_path.exists():
            for ext in [".png", ".jpeg", ".webp"]:
                teste_path = IMG_DIR / f"foto_7{ext}"
                if teste_path.exists():
                    imagem_final_path = teste_path
                    break
        
        if imagem_final_path.exists():
            img = Image.open(imagem_final_path)
            img = img.resize((self.screen_w, self.screen_h))
            self.photo_ref = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.photo_ref)
            
            self.main_label.config(
                text="VOCÊ VIU DEMAIS...",
                fg="red",
                bg="black",
                font=("Arial", 48, "bold")
            )
            self.main_label.place(relx=0.5, rely=0.9, anchor="center")
        else:
            self.main_label.config(
                text="FOTO_7.JPG NÃO ENCONTRADA\nVOCÊ VIU DEMAIS...",
                fg="red",
                bg="black",
                font=("Arial", 42, "bold")
            )
            self.main_label.place(relx=0.5, rely=0.5, anchor="center")
    
    def desligar_computador(self):
        try:
            print("Desligando o computador em 3 segundos...")
            self.main_label.config(
                text="DESLIGANDO SISTEMA...",
                fg="red",
                bg="black",
                font=("Arial", 36, "bold")
            )
            self.root.update()
            
            time.sleep(3)
            
            os.system('shutdown /s /f /t 5')
            
        except Exception as e:
            print(f"Erro ao desligar: {e}")
            try:
                os.system('shutdown -s -f -t 5')
            except:
                pass
    
    def cleanup_and_exit(self, desligar=True):
        self.running = False
        
        self.fechar_todas_janelas()
        
        if desligar:
            self.abrir_imagem_final()
            self.root.after(5000, self.desligar_computador)
            self.root.after(15000, lambda: self.root.destroy())
        else:
            self.root.destroy()

    def abrir_cmds_aleatorios(self, quantidade=1):
        for _ in range(quantidade):
            self.abrir_cmd_janela_posicionado()
    
    def abrir_videos_aleatorios(self, quantidade=1):
        for _ in range(quantidade):
            self.abrir_video_janela_posicionado()

    def clear_screen(self):
        self.main_label.config(text="", fg=COR_TEXTO, bg=COR_FUNDO, font=FONTE_TITULO)
        self.image_label.config(image="")
        self.photo_ref = None
        for lbl in self.glitch_labels:
            lbl.destroy()
        self.glitch_labels.clear()
        self.root.configure(bg=COR_FUNDO)

    def show_start_text(self):
        self.clear_screen()
        self.main_label.config(text=TEXTO_INICIAL, font=("Arial", 42, "bold"))
        self.root.after(500, self.spawn_glitch_text)
        self.root.after(1200, self.spawn_glitch_text)
        
        self.root.after(100, lambda: self.abrir_cmds_aleatorios(2))
        self.root.after(200, lambda: self.abrir_videos_aleatorios(2))
        
        self.root.after(TEMPO_TEXTO_INICIAL_MS, self.flash_sequence)

    def spawn_glitch_text(self):
        for _ in range(random.randint(4, 8)):
            texto = random.choice(MENSAGENS_GLITCH)
            cor = random.choice(["white", "red"])
            x = random.randint(100, self.screen_w - 250)
            y = random.randint(80, self.screen_h - 80)

            lbl = tk.Label(
                self.root,
                text=texto,
                fg=cor,
                bg="black",
                font=FONTE_GLITCH
            )
            lbl.place(x=x, y=y)
            self.glitch_labels.append(lbl)
            
            self.root.after(random.randint(1000, 2000), lbl.destroy)

    def flash_sequence(self):
        self.clear_screen()
        self.flash_count = 0
        
        self.abrir_cmds_aleatorios(2)
        self.abrir_videos_aleatorios(2)
        
        self.do_flash()

    def do_flash(self):
        if self.flash_count >= 10:
            self.show_bug_effect()
            return

        cor = "white" if self.flash_count % 2 == 0 else "black"
        self.root.configure(bg=cor)
        self.main_label.config(
            text=random.choice(MENSAGENS_GLITCH) if self.flash_count % 2 == 0 else "",
            fg="red" if cor == "white" else "white",
            bg=cor,
            font=("Arial", 36, "bold")
        )
        self.flash_count += 1
        self.root.after(120, self.do_flash)

    def show_bug_effect(self):
        self.clear_screen()
        self.bug_steps = 0
        
        self.abrir_cmds_aleatorios(3)
        self.abrir_videos_aleatorios(2)
        
        self.bug_effect_loop()

    def bug_effect_loop(self):
        if self.bug_steps >= 18:
            self.show_next_image()
            return

        fundo = random.choice(["black", "white", "#111111", "#220000"])
        fg = random.choice(["red", "white", "black"])
        texto = random.choice(MENSAGENS_GLITCH)

        self.root.configure(bg=fundo)

        offset_x = random.randint(-20, 20)
        offset_y = random.randint(-20, 20)

        self.main_label.config(
            text=texto,
            fg=fg,
            bg=fundo,
            font=("Arial", random.randint(28, 48), "bold")
        )
        self.main_label.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            x=offset_x,
            y=offset_y
        )

        if random.random() > 0.4:
            self.spawn_glitch_text()

        self.bug_steps += 1
        self.root.after(90, self.bug_effect_loop)

    def show_next_image(self):
        self.clear_screen()

        if self.current_index >= len(self.images):
            self.show_final_image_stack()
            return

        img_path = self.images[self.current_index]
        self.current_index += 1

        img = Image.open(img_path)
        img_ratio = img.width / img.height
        screen_ratio = self.screen_w / self.screen_h

        if img_ratio > screen_ratio:
            new_height = self.screen_h
            new_width = int(new_height * img_ratio)
        else:
            new_width = self.screen_w
            new_height = int(new_width / img_ratio)

        img = img.resize((new_width, new_height))

        left = (new_width - self.screen_w) // 2
        top = (new_height - self.screen_h) // 2
        img = img.crop((left, top, left + self.screen_w, top + self.screen_h))
        
        self.photo_ref = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.photo_ref)

        if random.random() > 0.3:
            self.spawn_glitch_text()

        if random.random() > 0.6:
            self.abrir_cmds_aleatorios(random.randint(1, 2))
        if random.random() > 0.75:
            self.abrir_videos_aleatorios(random.randint(1, 2))

        self.root.after(TEMPO_CADA_IMAGEM_MS, self.show_next_image)

    def show_final_image_stack(self):
        self.clear_screen()

        if not self.images:
            self.cleanup_and_exit(desligar=True)
            return

        self.stack_labels = []
        self.stack_count = 0
        self.max_stack = 60
        self.stack_images_refs = []

        self.stack_next_image()

    def stack_next_image(self):
        if self.stack_count >= self.max_stack:
            self.cleanup_and_exit(desligar=True)
            return

        img_path = random.choice(self.images)
        img = Image.open(img_path)

        modo = random.choice(["fullscreen", "medium", "small"])

        if modo == "fullscreen":
            img = img.resize((self.screen_w, self.screen_h))
            x = 0
            y = 0
        else:
            if modo == "medium":
                largura = random.randint(
                    max(300, self.screen_w // 3),
                    max(500, self.screen_w // 2)
                )
            else:
                largura = random.randint(180, 350)

            proporcao = img.height / img.width
            altura = int(largura * proporcao)
            img = img.resize((largura, altura))

            max_x = max(0, self.screen_w - largura)
            max_y = max(0, self.screen_h - altura)

            x = random.randint(0, max_x)
            y = random.randint(0, max_y)

        photo = ImageTk.PhotoImage(img)
        self.stack_images_refs.append(photo)

        lbl = tk.Label(self.root, image=photo, bd=0, highlightthickness=0)
        lbl.place(x=x, y=y)
        self.stack_labels.append(lbl)

        if random.random() > 0.4:
            self.spawn_glitch_text()
        
        if random.random() > 0.8:
            self.abrir_cmds_aleatorios(1)

        self.stack_count += 1
        self.root.after(120, self.stack_next_image)

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()