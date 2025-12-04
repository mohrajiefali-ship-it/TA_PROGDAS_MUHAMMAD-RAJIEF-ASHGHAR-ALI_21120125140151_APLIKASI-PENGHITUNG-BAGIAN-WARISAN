import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime

# --- KONSTANTA TAMPILAN (MODUL 8: GUI) ---
BG_MAIN = "#E8F5E9"
SIDEBAR_BG = "#145A32"
SIDEBAR_BTN = "#186A3B"
SIDEBAR_BTN_HOVER = "#1E7D44"
SIDEBAR_BTN_ACTIVE = "#0B4F2A"
CONTENT_BG = "#F1F8E9"
PANEL_BG = "#C8E6C9"
ACCENT_GOLD = "#C9A227"
TEXT_COLOR = "#072A16"
WHITE = "#FFFFFF"
BTN_RESET = "#E57373"

FONT_HEADER = ("Times New Roman", 18, "bold")
FONT_SUB = ("Times New Roman", 12, "italic")
FONT_NORMAL = ("Arial", 11)
FONT_SMALL = ("Arial", 10)
SIDEBAR_WIDTH = 220

# --- HELPER FUNCTIONS (MODUL 4: Function) ---
def format_rp(amount):
    """Format angka ke Rupiah (tanpa desimal)."""
    try:
        # Menggunakan pembulatan ke integer terdekat
        a = int(round(amount))
    except Exception:
        a = 0
    s = f"{a:,}"
    return f"Rp {s}"

def safe_int(s, default=0):
    """Konversi string ke integer dengan aman."""
    try:
        return int(s)
    except:
        return default

# --- KELAS AHLI WARIS (MODUL 5: OOP) ---
class AhliWaris:
    """Kelas dasar untuk ahli waris."""
    def __init__(self, nama):
        self._nama = nama
    def get_nama(self):
        # Getter (Modul 6)
        return self._nama
    def get_bagian(self, harta, ctx):
        # Method ini akan diimplementasikan di subclass (Polimorfisme)
        # Abstraction (Modul 6)
        raise NotImplementedError 

class Ayah(AhliWaris):
    """Implementasi Ayah (bagian 1/6 jika ada anak, ashabah jika tidak ada anak)."""
    def __init__(self): super().__init__("👨 Ayah")
    # Polymorphism: Logika bagian Ayah
    def get_bagian(self, harta, ctx):
        if not ctx.get('ayah', False) or ctx.get('jumlah_anak', 0) == 0: 
            return 0 # Bagian residu (ashabah) ditangani di Calculator jika tidak ada anak
        # Jika ada anak, bagian tetap Ayah adalah 1/6
        return harta * (1/6)

class Ibu(AhliWaris):
    """Implementasi Ibu (1/6 bila ada anak; 1/3 bila tidak ada anak)."""
    def __init__(self): super().__init__("👩 Ibu")
    # Polymorphism: Logika bagian Ibu
    def get_bagian(self, harta, ctx):
        if not ctx.get('ibu', False): return 0
        # Pengkondisian (Modul 2)
        if ctx.get('jumlah_anak', 0) > 0:
            return harta * (1/6)
        return harta * (1/3)

class Suami(AhliWaris):
    """Suami mendapatkan 1/4 (ada anak) atau 1/2 (tidak ada anak)."""
    def __init__(self): super().__init__("👨‍🦱 Suami")
    # Polymorphism: Logika bagian Suami
    def get_bagian(self, harta, ctx):
        if not ctx.get('suami', False): return 0
        # Pengkondisian (Modul 2)
        if ctx.get('jumlah_anak', 0) > 0:
            return harta * (1/4)
        return harta * (1/2)

class Istri(AhliWaris):
    """Istri mendapatkan 1/8 (ada anak) atau 1/4 (tidak ada anak)."""
    def __init__(self): super().__init__("👩‍🦰 Istri")
    # Polymorphism: Logika bagian Istri
    def get_bagian(self, harta, ctx):
        if not ctx.get('istri', False): return 0
        # Pengkondisian (Modul 2)
        if ctx.get('jumlah_anak', 0) > 0:
            return harta * (1/8)
        return harta * (1/4)

class Anak(AhliWaris):
    """Kelas untuk menampung jumlah anak dan menghitung unit ashabah."""
    def __init__(self, laki=0, perempuan=0):
        super().__init__("Anak-anak")
        self._laki = laki
        self._perempuan = perempuan
    # Setter (Modul 6)
    def set_jumlah(self, laki, perempuan):
        self._laki = laki
        self._perempuan = perempuan
    def total_unit_ashabah(self): 
        # Laki-laki = 2 unit, Perempuan = 1 unit (Modul 1: Variabel/Tipe Data)
        return self._laki * 2 + self._perempuan * 1
    def get_bagian(self, harta, ctx): 
        # Method ini tidak digunakan untuk perhitungan fixed share
        return 0 

class WarisanCalculator:
    """Logika inti perhitungan warisan Faraidh."""
    def __init__(self):
        # Inisialisasi objek ahli waris (Modul 5)
        self.ayah = Ayah()
        self.ibu = Ibu()
        self.suami = Suami()
        self.istri = Istri()
        self.anak = Anak(0,0)
        # List untuk riwayat, bertindak sebagai Stack (Modul 7)
        self.history = [] 

    # Method utama perhitungan (Modul 4)
    def compute(self, total, ayah=False, ibu=False, suami=False, istri=False, anak_laki=0, anak_perempuan=0):
        # Pengkondisian (Modul 2)
        if total <= 0:
            raise ValueError("Total harta harus lebih besar dari 0.")

        # Context untuk perhitungan bagian tetap
        ctx = {
            'ayah': ayah, 'ibu': ibu, 'suami': suami, 'istri': istri,
            'jumlah_anak': anak_laki + anak_perempuan
        }

        self.anak.set_jumlah(anak_laki, anak_perempuan)

        hasil = {}
        fixed_shares = {}
        total_anak = anak_laki + anak_perempuan

        # 1. Hitung bagian tetap (Ashabul Furudh) - Memanggil get_bagian (Polymorphism)
        if ayah and total_anak > 0: 
            fixed_shares[self.ayah.get_nama()] = self.ayah.get_bagian(total, ctx)
        
        # Bagian Ibu, Suami, Istri
        if ibu: fixed_shares[self.ibu.get_nama()] = self.ibu.get_bagian(total, ctx)
        if suami: fixed_shares[self.suami.get_nama()] = self.suami.get_bagian(total, ctx)
        if istri: fixed_shares[self.istri.get_nama()] = self.istri.get_bagian(total, ctx)

        # Bagian Anak Perempuan saja (fixed share) - Pengkondisian (Modul 2)
        if anak_laki == 0 and anak_perempuan > 0:
            if anak_perempuan == 1:
                fixed_shares["👧 Anak Perempuan (1)"] = total * 0.5
            else:
                fixed_shares["👧 Anak Perempuan (total)"] = total * (2/3)

        total_fixed = sum(fixed_shares.values())

        # 2. Aturan Awl - Pengkondisian (Modul 2)
        if total_fixed > total and anak_laki == 0:
            scale = total / total_fixed
            # Perulangan untuk Scale down (Modul 3)
            for k in list(fixed_shares.keys()):
                fixed_shares[k] = fixed_shares[k] * scale
            total_fixed = sum(fixed_shares.values()) # Hitung ulang total fixed setelah Awl

        # Masukkan bagian tetap ke hasil
        hasil.update(fixed_shares)
        sisa = total - total_fixed

        # 3. Pembagian Residu (Ashabah)
        
        # Ashabah anak-anak (sisa dibagi 2:1) - Pengkondisian (Modul 2)
        if anak_laki > 0 and sisa > 0:
            units = self.anak.total_unit_ashabah()
            if units > 0:
                # Anak laki-laki
                if anak_laki > 0:
                    bagian_laki_total = sisa * ((anak_laki * 2) / units)
                    hasil["🧒 Anak Laki-laki (total)"] = bagian_laki_total
                    # Perulangan untuk setiap anak (Modul 3)
                    per = bagian_laki_total / anak_laki
                    for i in range(1, anak_laki + 1):
                        hasil[f"  └─ Anak Laki-laki {i}"] = per
                # Anak perempuan (ikut ashabah)
                if anak_perempuan > 0:
                    # Hapus fixed share anak perempuan jika sudah dihitung di sini
                    if "👧 Anak Perempuan (total)" in hasil:
                         del hasil["👧 Anak Perempuan (total)"]

                    bagian_perempuan_total = sisa * ((anak_perempuan * 1) / units)
                    hasil["👧 Anak Perempuan (total)"] = bagian_perempuan_total
                    # Perulangan untuk setiap anak (Modul 3)
                    per = bagian_perempuan_total / anak_perempuan
                    for i in range(1, anak_perempuan + 1):
                        hasil[f"  └─ Anak Perempuan {i}"] = per
                sisa = 0

        # Ashabah Ayah (jika tidak ada anak sama sekali) - Pengkondisian (Modul 2)
        elif total_anak == 0 and ayah and sisa > 0:
            # Ayah mengambil sisa (menjadi Ashabah Bin-Nafs)
            key = self.ayah.get_nama()
            existing = hasil.get(key, 0)
            hasil[key] = existing + sisa
            sisa = 0

        # 4. Finalisasi dan Pembulatan (Modul 4: Safety / Final Rounding)
        # Perulangan untuk pembulatan (Modul 3)
        for k in list(hasil.keys()):
            # Pastikan pembulatan di akhir perhitungan
            hasil[k] = round(hasil[k])

        # Sisa tidak terdistribusi
        if sisa > 0:
            hasil["📦 Sisa (tidak terdistribusi)"] = round(sisa)
            
        # Simpan riwayat (Modul 7: Stack/Push)
        entry = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'total': round(total),
            'inputs': {'ayah': ayah, 'ibu': ibu, 'suami': suami, 'istri': istri,
                       'anak_laki': anak_laki, 'anak_perempuan': anak_perempuan},
            'hasil': hasil
        }
        self.history.append(entry)
        return hasil

    # --- METHOD UNTUK MANAJEMEN RIWAYAT ---
    def reset_history(self):
        # Non-Return Method (Modul 4)
        self.history.clear()

    def export_txt(self, path):
        """Export riwayat perhitungan ke file teks."""
        # Perulangan (Modul 3) untuk menulis data
        with open(path, "w", encoding="utf-8") as f:
            for i, e in enumerate(self.history, 1):
                f.write(f"=== Riwayat {i} ===\n")
                f.write(f"Waktu: {e['timestamp']}\n")
                f.write(f"Total Harta: {format_rp(e['total'])}\n")
                f.write("Input:\n")
                # Perulangan (Modul 3) untuk input
                for k, v in e['inputs'].items(): 
                    f.write(f"  {k}: {v}\n")
                f.write("Hasil:\n")
                # Perulangan (Modul 3) untuk hasil
                for k, v in e['hasil'].items(): 
                    f.write(f"  {k}: {format_rp(v)}\n")
                f.write("\n")
        return path

# --- KELAS UTAMA GUI (MODUL 8: GUI Programming) ---
class AppWarisanUI:
    def __init__(self, root):
        # Constructor (Modul 5)
        self.root = root
        root.title("🕌 Warisan — Aplikasi Penghitung Faraidh")
        root.geometry("980x700")
        root.configure(bg=BG_MAIN)
        self.calc = WarisanCalculator() # Membuat objek kalkulator (Modul 5)

        main = tk.Frame(root, bg=BG_MAIN)
        main.pack(fill="both", expand=True) # Layout Management (Modul 8)

        # Sidebar (Kiri)
        self.sidebar = tk.Frame(main, bg=SIDEBAR_BG, width=SIDEBAR_WIDTH)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Content (Kanan)
        self.content = tk.Frame(main, bg=CONTENT_BG)
        self.content.pack(side="left", fill="both", expand=True)

        # Header (Top of content)
        self.header = tk.Label(self.content, text="", font=FONT_HEADER, bg=CONTENT_BG, fg=TEXT_COLOR)
        self.header.pack(pady=(14,2))
        self.subheader = tk.Label(self.content, text="", font=FONT_SUB, bg=CONTENT_BG, fg=ACCENT_GOLD)
        self.subheader.pack(pady=(0,8))
        
        # Efek pengetikan (opsional tapi menarik)
        root.after(150, lambda: self._fade_in_label(self.header, "Aplikasi Penghitung Warisan", delay=18))
        root.after(500, lambda: self._fade_in_label(self.subheader, "Selamat Mencoba!", delay=16))

        # Button Sidebar
        self.menu_buttons = {}
        menu_items = [
            ("Hitung Warisan", self.show_hitung_view),
            ("Riwayat Perhitungan", self.show_riwayat_view),
            ("Penjelasan Warisan", self.show_penjelasan_view),
            ("Keluar", self.on_quit)
        ]
        # Perulangan untuk membuat tombol (Modul 3)
        for idx, (label, cmd) in enumerate(menu_items):
            b = tk.Button(self.sidebar, text=label, font=("Arial", 12, "bold"),
                          bg=SIDEBAR_BTN, fg=WHITE, activebackground=SIDEBAR_BTN_ACTIVE,
                          bd=0, relief="raised", padx=8, pady=12, command=cmd)
            b.pack(fill="x", padx=14, pady=(18 if idx==0 else 8))
            
            # Binding hover effect (Modul 8)
            b.bind("<Enter>", lambda e, w=b: w.config(bg=SIDEBAR_BTN_HOVER))
            b.bind("<Leave>", lambda e, w=b: w.config(bg=SIDEBAR_BTN))
            b.bind("<ButtonPress-1>", lambda e, w=b: w.config(relief="sunken"))
            b.bind("<ButtonRelease-1>", lambda e, w=b: w.config(relief="raised"))
            self.menu_buttons[label] = b

        self.current_view = None
        self.show_hitung_view()

    # --- UI HELPERS (MODUL 4: Method) ---
    def _fade_in_label(self, label, text, delay=20):
        """Menampilkan teks huruf demi huruf."""
        # Non-Return Method (Modul 4)
        label.config(text="")
        def step(i=0):
            if i <= len(text):
                label.config(text=text[:i])
                label.after(delay, step, i+1)
        step()

    def _fade_insert_lines(self, text_widget, lines, delay=40):
        """Memasukkan baris demi baris ke dalam Text widget."""
        # Non-Return Method (Modul 4)
        text_widget.delete("1.0", tk.END)
        def step(i=0):
            if i < len(lines):
                text_widget.insert(tk.END, lines[i] + "\n")
                text_widget.after(delay, step, i+1)
        step()

    def clear_content(self):
        """Hapus widget konten kecuali header & subheader."""
        # Non-Return Method (Modul 4)
        for child in list(self.content.pack_slaves()):
            if child not in (self.header, self.subheader):
                child.destroy()

    def mark_active(self, label_text):
        """Highlight tombol aktif di sidebar."""
        # Non-Return Method (Modul 4)
        for k, b in self.menu_buttons.items():
            if k == label_text:
                b.config(bg=SIDEBAR_BTN_ACTIVE)
            else:
                b.config(bg=SIDEBAR_BTN)

    # --- VIEW: Hitung Warisan (MODUL 8: Layout) ---
    def show_hitung_view(self):
        # Method untuk menampilkan view (Modul 8)
        self.clear_content()
        self.mark_active("Hitung Warisan")

        # Frame utama input dan output (Modul 8)
        panel = tk.Frame(self.content, bg=PANEL_BG, bd=2, relief="groove")
        panel.pack(padx=16, pady=8, fill="x")

        # Kolom Input (Left)
        left = tk.Frame(panel, bg=PANEL_BG)
        left.pack(side="left", padx=12, pady=12, anchor="n")

        # Input Total Harta (Modul 8)
        tk.Label(left, text="💎 Total Harta (Rp):", bg=PANEL_BG, font=FONT_NORMAL, fg=TEXT_COLOR).grid(row=0, column=0, sticky="w")
        self.ent_harta = tk.Entry(left, width=25, font=FONT_NORMAL)
        self.ent_harta.grid(row=0, column=1, padx=(8,0), pady=6)

        # Input Ahli Waris Fixed (Modul 8)
        tk.Label(left, text="👨‍👩‍👧‍👦 Pilih Ahli Waris:", bg=PANEL_BG, font=FONT_NORMAL, fg=TEXT_COLOR).grid(row=1, column=0, sticky="w", pady=(6,0))
        aw_frame = tk.Frame(left, bg=PANEL_BG)
        aw_frame.grid(row=1, column=1, pady=(6,0), sticky="w")
        self.c_ayah = tk.BooleanVar(); self.c_ibu = tk.BooleanVar(); self.c_suami = tk.BooleanVar(); self.c_istri = tk.BooleanVar()
        tk.Checkbutton(aw_frame, text="👨 Ayah", bg=PANEL_BG, variable=self.c_ayah).pack(anchor="w")
        tk.Checkbutton(aw_frame, text="👩 Ibu", bg=PANEL_BG, variable=self.c_ibu).pack(anchor="w")
        tk.Checkbutton(aw_frame, text="👨‍🦱 Suami", bg=PANEL_BG, variable=self.c_suami).pack(anchor="w")
        tk.Checkbutton(aw_frame, text="👩‍🦰 Istri", bg=PANEL_BG, variable=self.c_istri).pack(anchor="w")

        # Input Anak-anak (Modul 8)
        tk.Label(left, text="🧒 Anak Laki-laki:", bg=PANEL_BG, font=FONT_NORMAL, fg=TEXT_COLOR).grid(row=2, column=0, sticky="w", pady=(8,0))
        self.ent_laki = tk.Entry(left, width=6); self.ent_laki.insert(0,"0"); self.ent_laki.grid(row=2, column=1, sticky="w", pady=(8,0))
        tk.Label(left, text="👧 Anak Perempuan:", bg=PANEL_BG, font=FONT_NORMAL, fg=TEXT_COLOR).grid(row=3, column=0, sticky="w", pady=(6,0))
        self.ent_perempuan = tk.Entry(left, width=6); self.ent_perempuan.insert(0,"0"); self.ent_perempuan.grid(row=3, column=1, sticky="w", pady=(6,0))

        # Tombol Aksi (Modul 8)
        btns = tk.Frame(left, bg=PANEL_BG)
        btns.grid(row=4, column=0, columnspan=2, pady=(12,0))
        tk.Button(btns, text="🔍 Hitung", bg=SIDEBAR_BTN, fg=WHITE, command=self.action_hitung, bd=0, padx=12, pady=6).grid(row=0, column=0, padx=6)
        tk.Button(btns, text="♻ Reset Input", bg=BTN_RESET, fg=WHITE, command=self.action_reset_inputs, bd=0, padx=10, pady=6).grid(row=0, column=1, padx=6)
        tk.Button(btns, text="💾 Export Riwayat", bg=ACCENT_GOLD, fg=WHITE, command=self.action_export, bd=0, padx=10, pady=6).grid(row=0, column=2, padx=6)

        # Kolom Output (Right) (Modul 8)
        right = tk.Frame(panel, bg=PANEL_BG)
        right.pack(side="left", padx=16, pady=12, fill="both", expand=True)

        tk.Label(right, text="📜 Hasil Perhitungan:", bg=PANEL_BG, font=("Arial",12,"bold"), fg=TEXT_COLOR).pack(anchor="w")
        self.txt_hasil = tk.Text(right, height=16, bg=CONTENT_BG, font=FONT_SMALL, bd=0)
        self.txt_hasil.pack(fill="both", expand=True, pady=(4,0))

        self.current_view = "hitung"

    # --- VIEW: Riwayat (MODUL 8: Layout) ---
    def show_riwayat_view(self):
        # Method untuk menampilkan view (Modul 8)
        self.clear_content()
        self.mark_active("Riwayat Perhitungan")

        frame = tk.Frame(self.content, bg=PANEL_BG, bd=2, relief="groove")
        frame.pack(padx=16, pady=8, fill="both", expand=True)

        # List Riwayat (Modul 8)
        left = tk.Frame(frame, bg=PANEL_BG)
        left.pack(side="left", padx=12, pady=12, fill="y")
        tk.Label(left, text="📚 Riwayat:", bg=PANEL_BG, font=("Arial",12,"bold"), fg=TEXT_COLOR).pack(anchor="w")
        self.lb = tk.Listbox(left, width=36, height=20)
        self.lb.pack(pady=(6,0))
        self.lb.bind("<<ListboxSelect>>", self.on_select_history)

        # Populate listbox (Modul 3)
        self.lb.delete(0, tk.END)
        for i, e in enumerate(self.calc.history, 1):
            self.lb.insert(tk.END, f"{i}. {e['timestamp']} — {format_rp(e['total'])}")
        
        # Auto-select last entry
        if self.calc.history:
            self.lb.select_set(tk.END) # Stack/Peek (Modul 7)
            self.lb.see(tk.END)

        # Detail Riwayat (Modul 8)
        right = tk.Frame(frame, bg=PANEL_BG)
        right.pack(side="left", padx=12, pady=12, fill="both", expand=True)
        tk.Label(right, text="Detail Riwayat:", bg=PANEL_BG, font=("Arial",12,"bold"), fg=TEXT_COLOR).pack(anchor="w")
        self.txt_riwayat_detail = tk.Text(right, bg=CONTENT_BG, font=FONT_SMALL, bd=0)
        self.txt_riwayat_detail.pack(fill="both", expand=True, pady=(6,0))

        if self.calc.history:
            last_entry = self.calc.history[-1]
            self.show_riwayat_detail_from_entry(last_entry)

        # Action buttons for Riwayat (Modul 8)
        actions = tk.Frame(frame, bg=PANEL_BG)
        actions.pack(side="bottom", fill="x", padx=12, pady=(0,8))
        
        # TOMBOL BARU: Hapus Riwayat Terpilih
        tk.Button(actions, text="🗑️ Hapus Terpilih", bg="#F44336", fg=WHITE, 
                  command=self.action_delete_selected_history, bd=0).pack(side="left", padx=6) # <-- NEW
                  
        tk.Button(actions, text="Reset Semua Riwayat", bg=BTN_RESET, fg=WHITE, command=self.action_clear_history, bd=0).pack(side="left", padx=6)
        tk.Button(actions, text="💾 Export (.txt)", bg=ACCENT_GOLD, fg=WHITE, command=self.action_export, bd=0).pack(side="left", padx=6)

        self.current_view = "riwayat"

    # --- VIEW: Penjelasan Warisan (MODUL 8: Layout) ---
    def show_penjelasan_view(self):
        # Method untuk menampilkan view (Modul 8)
        self.clear_content()
        self.mark_active("Penjelasan Warisan")

        panel = tk.Frame(self.content, bg=PANEL_BG, bd=2, relief="groove")
        panel.pack(padx=16, pady=8, fill="both", expand=True)

        tk.Label(panel, text="📘 Penjelasan Singkat Faraidh", bg=PANEL_BG, font=("Arial", 14, "bold"), fg=TEXT_COLOR).pack(anchor="w", pady=(6,4))
        teks = tk.Text(panel, wrap="word", bg=CONTENT_BG, font=FONT_SMALL, bd=0)
        teks.pack(fill="both", expand=True, padx=8, pady=(4,8))
        isi = (
            "Faraidh adalah pembagian harta warisan menurut syariat Islam.\n\n"
            "Prinsip (versi aplikasi ini):\n"
            "- Ada bagian tetap (ashabul furudh) dan bagian residu (ashabah).\n"
            "- Anak laki-laki & perempuan: jika ada laki-laki -> mereka sebagai ashabah (2:1).\n"
            "- Jika hanya anak perempuan: 1 anak = 1/2; 2+ anak = 2/3 (fixed).\n"
            "- Ayah mendapatkan 1/6 bila ada anak; jika tidak ada anak, ayah mendapat 1/6 + seluruh sisa.\n"
            "- Suami/istri dan ibu mengikuti aturan bagian tetap (lihat menu Hitung).\n"
            "- Sisa (residu) hanya diberikan kepada anak laki-laki atau ayah (jika tidak ada anak).\n"
            "\nCatatan: Aplikasi ini merupakan simulasi sederhana dan tidak menggantikan fatwa resmi fiqih waris."
        )
        teks.insert("1.0", isi)
        teks.config(state="disabled")
        self.current_view = "penjelasan"
    
    # --- ACTION HANDLERS (MODUL 4: Method) ---
    def action_hitung(self):
        # Action Handler (Modul 8)
        self.hitung_warisan()

    def action_reset_inputs(self):
        """Reset semua input di view Hitung Warisan."""
        # Non-Return Method (Modul 4)
        try:
            self.ent_harta.delete(0, tk.END)
            self.ent_laki.delete(0, tk.END); self.ent_perempuan.delete(0, tk.END)
            self.ent_laki.insert(0,"0"); self.ent_perempuan.insert(0,"0")
            self.c_ayah.set(False); self.c_ibu.set(False); self.c_suami.set(False); self.c_istri.set(False)
            if hasattr(self, "txt_hasil"):
                self.txt_hasil.delete("1.0", tk.END)
            messagebox.showinfo("Reset", "Input berhasil direset.")
        except Exception:
            messagebox.showerror("Error", "Gagal mereset input.")

    def action_export(self):
        """Menyimpan riwayat ke file .txt."""
        # Action Handler (Modul 8)
        if not self.calc.history:
            messagebox.showwarning("Riwayat Kosong", "Tidak ada riwayat untuk disimpan.")
            return
            
        default_filename = f"Warisan_Riwayat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                             initialfile=default_filename,
                                             filetypes=[("Text files","*.txt")])
        if not path: return
        
        try:
            self.calc.export_txt(path)
            messagebox.showinfo("Sukses", f"Riwayat tersimpan di:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan riwayat:\n{e}")

    def update_riwayat_ui_after_delete(self):
        """Fungsi helper untuk memperbarui Listbox dan detail setelah penghapusan."""
        # Perulangan (Modul 3) untuk memperbarui Listbox
        self.lb.delete(0, tk.END)
        for i, e in enumerate(self.calc.history, 1):
            self.lb.insert(tk.END, f"{i}. {e['timestamp']} — {format_rp(e['total'])}")

        # Atur seleksi dan detail
        if self.calc.history:
            # Pilih elemen terakhir sebagai default (Stack/Peek - Modul 7)
            self.lb.select_set(tk.END) 
            self.lb.see(tk.END)
            self.show_riwayat_detail_from_entry(self.calc.history[-1])
        else:
            # Kosongkan detail jika riwayat kosong
            if hasattr(self, "txt_riwayat_detail"):
                self.txt_riwayat_detail.delete("1.0", tk.END)
        
    def action_delete_selected_history(self):
        """Menghapus entri riwayat yang dipilih dari listbox dan data."""
        # Action Handler (Modul 8)
        if not hasattr(self, "lb"): return 

        # Ambil indeks yang dipilih
        selected_indices = self.lb.curselection()
        
        # Pengkondisian (Modul 2)
        if not selected_indices:
            messagebox.showwarning("Peringatan", "Pilih riwayat yang ingin dihapus terlebih dahulu.")
            return

        # Ambil indeks pertama yang dipilih
        idx_to_delete = selected_indices[0]
        
        # Pengkondisian Konfirmasi (Modul 2)
        if messagebox.askyesno("Konfirmasi Hapus", f"Yakin ingin menghapus riwayat ke-{idx_to_delete + 1}?"):
            try:
                # Hapus dari list data inti (Modul 7: Stack/List Operation)
                self.calc.history.pop(idx_to_delete) 

                # Perbarui Listbox UI dan Detail
                self.update_riwayat_ui_after_delete()

                messagebox.showinfo("Sukses", "Riwayat berhasil dihapus.")

            except IndexError:
                messagebox.showerror("Error", "Indeks riwayat tidak valid.")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menghapus riwayat: {e}")

    def action_clear_history(self):
        """Menghapus semua riwayat."""
        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus semua riwayat perhitungan?"):
            self.calc.reset_history()
            
            # Memperbarui tampilan
            if hasattr(self, "lb"): 
                self.update_riwayat_ui_after_delete() 
                 
            messagebox.showinfo("Sukses", "Semua riwayat telah dihapus.")

    # --- LOGIC HANDLER (MODUL 2: Pengkondisian & MODUL 4/5: Logika) ---
    def hitung_warisan(self):
        # Non-Return Method (Modul 4)
        try:
            harta_text = self.ent_harta.get().replace(",", "").strip()
            harta = float(harta_text)
            if harta <= 0: raise ValueError("Total harta harus lebih besar dari 0.") # Pengkondisian (Modul 2)
        except ValueError as e:
            messagebox.showerror("Input Error", "Masukkan jumlah harta (angka positif) dengan benar! " + str(e))
            return
        except Exception:
            messagebox.showerror("Error", "Form hitung tidak ditemukan.")
            return

        # Validasi Suami/Istri (MODUL 2: Pengkondisian)
        if self.c_suami.get() and self.c_istri.get():
            messagebox.showerror("Validasi Faraidh", "Pilih Suami ATAU Istri, tidak keduanya.")
            return

        laki = safe_int(self.ent_laki.get(), 0)
        perempuan = safe_int(self.ent_perempuan.get(), 0)

        # Pengkondisian (Modul 2)
        if laki < 0 or perempuan < 0:
             messagebox.showerror("Input Error", "Jumlah anak tidak boleh negatif.")
             return
        
        # Hitung dengan logika inti
        try:
            # Memanggil Method compute (Modul 4/6)
            hasil = self.calc.compute(
                total=harta,
                ayah=self.c_ayah.get(), ibu=self.c_ibu.get(), 
                suami=self.c_suami.get(), istri=self.c_istri.get(),
                anak_laki=laki, anak_perempuan=perempuan
            )
        except ValueError as e:
            messagebox.showerror("Error Perhitungan", str(e))
            return

        # Tampilkan Hasil (Modul 3: Perulangan)
        lines = [f"Total Harta: {format_rp(harta)}", ""]
        for k, v in hasil.items():
            lines.append(f"{k}: 💰 {format_rp(v)}")
            
        if hasattr(self, "txt_hasil"):
            self._fade_insert_lines(self.txt_hasil, lines)

        # Update riwayat di view Riwayat (jika sudah dibuat)
        if hasattr(self, "lb"): # Pengkondisian (Modul 2)
            last_entry = self.calc.history[-1]
            self.lb.insert(tk.END, f"{len(self.calc.history)}. {last_entry['timestamp']} — {format_rp(last_entry['total'])}")
            self.lb.select_clear(0, tk.END)
            self.lb.select_set(tk.END) # Stack/Peek (Modul 7)
            self.lb.see(tk.END)
        
        # Jika sedang di view riwayat, otomatis tampilkan detailnya (Modul 2)
        if self.current_view == "riwayat" and hasattr(self, "txt_riwayat_detail"):
            self.show_riwayat_detail_from_entry(self.calc.history[-1])

    # --- RIWAYAT HANDLERS ---
    def on_select_history(self, event):
        """Menampilkan detail riwayat yang dipilih di listbox."""
        # Method Event Handler (Modul 4/8)
        sel = event.widget.curselection()
        if not sel: return
        idx = sel[0]
        try:
            entry = self.calc.history[idx]
        except IndexError:
            return
        self.show_riwayat_detail_from_entry(entry)

    def show_riwayat_detail_from_entry(self, entry):
        """Memformat dan menampilkan detail riwayat."""
        # Non-Return Method (Modul 4)
        txt = getattr(self, "txt_riwayat_detail", None)
        if txt is None: return
        txt.delete("1.0", tk.END)
        txt.insert(tk.END, f"Waktu: {entry['timestamp']}\n")
        txt.insert(tk.END, f"Total Harta: {format_rp(entry['total'])}\n\n")
        txt.insert(tk.END, "Input:\n")
        
        # Perulangan (Modul 3)
        input_labels = {
            'ayah': 'Ayah', 'ibu': 'Ibu', 'suami': 'Suami', 'istri': 'Istri',
            'anak_laki': 'Anak Laki-laki (Jumlah)', 'anak_perempuan': 'Anak Perempuan (Jumlah)'
        }
        for k, v in entry['inputs'].items():
            txt.insert(tk.END, f"  {input_labels.get(k, k)}: {v}\n")
            
        txt.insert(tk.END, "\nHasil:\n")
        # Perulangan (Modul 3)
        for k, v in entry['hasil'].items():
            txt.insert(tk.END, f"  {k}: {format_rp(v)}\n")

    def on_quit(self):
        """Konfirmasi keluar aplikasi."""
        # Method Aksi (Modul 4)
        if messagebox.askyesno("Keluar", "Yakin mau keluar aplikasi?"):
            self.root.destroy()

if __name__ == "__main__":
    # Program Utama (Modul 8)
    root = tk.Tk()
    app = AppWarisanUI(root)
    root.mainloop()