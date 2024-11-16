import tkinter as tk
from tkinter import ttk, messagebox
import random
import pyperclip
from ttkthemes import ThemedTk

class TaiwanIDApp:
    def __init__(self):
        self.root = ThemedTk(theme="vista")
        self.root.title("臺灣身分證字號生成與驗證")
        self.root.geometry("650x700")
        self.root.resizable(False, False)
        
        self.default_font = ('Microsoft JhengHei UI', 12)
        self.title_font = ('Microsoft JhengHei UI', 14, 'bold')
        self.mono_font = ('Consolas', 16)

        self.letter_map = {
            'A': ('10', '台北市'), 'F': ('15', '新北市'), 'H': ('17', '桃園市'),
            'J': ('18', '新竹縣'), 'O': ('35', '新竹市'), 'K': ('19', '苗栗縣'),
            'B': ('11', '台中市'), 'N': ('22', '彰化縣'), 'M': ('21', '南投縣'),
            'P': ('23', '雲林縣'), 'I': ('34', '嘉義市'), 'Q': ('24', '嘉義縣'),
            'D': ('13', '台南市'), 'E': ('14', '高雄市'), 'T': ('27', '屏東縣'),
            'G': ('16', '宜蘭縣'), 'U': ('28', '花蓮縣'), 'V': ('29', '台東縣'),
            'C': ('12', '基隆市'), 'X': ('30', '澎湖縣'), 'W': ('32', '金門縣'),
            'Z': ('33', '連江縣')
        }

        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.configure('Title.TLabel', font=self.title_font)
        style.configure('Large.TButton', font=self.default_font, padding=5)
        
        main_container = ttk.Frame(self.root, padding="20")
        main_container.pack(fill=tk.BOTH, expand=True)

        title_label = ttk.Label(main_container, text="臺灣身分證字號工具", style='Title.TLabel')
        title_label.pack(pady=(0, 20))

        notebook = ttk.Notebook(main_container)
        notebook.pack(fill=tk.BOTH, expand=True, pady=5)

        generate_frame = ttk.Frame(notebook, padding="15")
        notebook.add(generate_frame, text="生成身分證字號")

        verify_frame = ttk.Frame(notebook, padding="15")
        notebook.add(verify_frame, text="驗證身分證字號")

        area_frame = ttk.LabelFrame(generate_frame, text="戶籍地區", padding="10")
        area_frame.pack(fill=tk.X, pady=10)

        self.area_var = tk.StringVar()
        area_combobox = ttk.Combobox(area_frame, textvariable=self.area_var, state='readonly',
                                    values=[f"{k} - {v[1]}" for k, v in self.letter_map.items()])
        area_combobox.set('A - 台北市')
        area_combobox.pack(fill=tk.X, pady=5)

        gender_frame = ttk.LabelFrame(generate_frame, text="性別", padding="10")
        gender_frame.pack(fill=tk.X, pady=10)

        self.gender_var = tk.StringVar(value="1")
        ttk.Radiobutton(gender_frame, text="男性", variable=self.gender_var, value="1").pack(side=tk.LEFT, padx=30)
        ttk.Radiobutton(gender_frame, text="女性", variable=self.gender_var, value="2").pack(side=tk.LEFT, padx=30)

        ttk.Button(generate_frame, text="產生身分證字號", command=self.generate_id,
                  style='Large.TButton').pack(pady=15)

        result_frame = ttk.LabelFrame(generate_frame, text="生成結果", padding="10")
        result_frame.pack(fill=tk.X, pady=10)

        self.result_var = tk.StringVar()
        result_label = ttk.Label(result_frame, textvariable=self.result_var, 
                               font=('Consolas', 24), foreground='#2196F3')
        result_label.pack(pady=10)

        ttk.Button(result_frame, text="複製到剪貼簿", command=self.copy_to_clipboard,
                  style='Large.TButton').pack(pady=5)

        verify_input_frame = ttk.LabelFrame(verify_frame, text="輸入身分證字號", padding="10")
        verify_input_frame.pack(fill=tk.X, pady=10)

        self.verify_entry = ttk.Entry(verify_input_frame, font=self.mono_font, justify='center')
        self.verify_entry.pack(fill=tk.X, pady=10)

        ttk.Button(verify_frame, text="驗證", command=self.verify_id,
                  style='Large.TButton').pack(pady=15)

        verify_result_frame = ttk.LabelFrame(verify_frame, text="驗證結果", padding="10")
        verify_result_frame.pack(fill=tk.X, pady=10)

        self.verify_result_var = tk.StringVar()
        ttk.Label(verify_result_frame, textvariable=self.verify_result_var,
                 font=self.title_font).pack(pady=10)

        self.verify_details_text = tk.Text(verify_frame, height=8, width=40,
                                         font=self.default_font, wrap=tk.WORD,
                                         background='#F5F5F5', relief='flat')
        self.verify_details_text.pack(fill=tk.X, pady=10)

    def calculate_check_digit(self, id_number):
        weights = [1, 9, 8, 7, 6, 5, 4, 3, 2, 1]

        if isinstance(id_number, str) and len(id_number) == 9:
            area_code = self.letter_map[id_number[0]][0]
            id_number = f"{area_code}{id_number[1:]}"

        nums = [int(x) for x in id_number]

        total = sum(n * w for n, w in zip(nums, weights))

        check = (10 - (total % 10)) % 10

        return str(check)

    def generate_id(self):
        area = self.area_var.get().split(' - ')[0]
        gender = self.gender_var.get()

        random_nums = ''.join([str(random.randint(0, 9)) for _ in range(7)])

        temp_id = f"{area}{gender}{random_nums}"
        check_digit = self.calculate_check_digit(temp_id)

        full_id = f"{temp_id}{check_digit}"
        self.result_var.set(full_id)

        self.verify_entry.delete(0, tk.END)
        self.verify_entry.insert(0, full_id)

    def verify_id(self):
        id_number = self.verify_entry.get().upper()
        details = []
        is_valid = True

        if len(id_number) != 10:
            details.append("❎長度必須為10個字元")
            is_valid = False

        if not id_number[0].isalpha():
            details.append("❎第一個字元必須是英文字母")
            is_valid = False

        if not id_number[1:].isdigit():
            details.append("❎第2-10個字元必須是數字")
            is_valid = False

        if is_valid:
            if id_number[0] not in self.letter_map:
                details.append("❎無效的地區代碼")
                is_valid = False
            else:
                details.append(f"✅地區: {self.letter_map[id_number[0]][1]}")

            if id_number[1] not in ['1', '2']:
                details.append("❎無效的性別代碼")
                is_valid = False
            else:
                details.append(f"✅性別: {'男性' if id_number[1] == '1' else '女性'}")

            if is_valid:
                expected_check = self.calculate_check_digit(id_number[:9])
                if expected_check == id_number[-1]:
                    details.append("✅驗證碼正確")
                else:
                    details.append(f"❎驗證碼錯誤 (正確應為: {expected_check})")
                    is_valid = False

        self.verify_result_var.set("✅ 驗證通過" if is_valid else "❎ 驗證失敗")
        
        self.verify_details_text.delete(1.0, tk.END)
        self.verify_details_text.insert(tk.END, '\n'.join(details))

    def copy_to_clipboard(self):
        id_number = self.result_var.get()
        if id_number:
            pyperclip.copy(id_number)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TaiwanIDApp()
    app.run()