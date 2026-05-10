# Administrasi-SPBU-sederhana-berbasis-python
import os
import json
from datetime import datetime
from typing import Dict, List, Any

# Fungsi clear screen
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class SPBUSystem:
    def __init__(self):
        self.harga_bbm = {
            "premium": 8000,
            "Pertalite": 10000,
            "Pertamax": 14000,
            "Solar": 6800,
            "Dexlite": 12500
        }
        
        self.stok_bbm = {
            "premium": 1000,
            "Pertalite": 1000,
            "Pertamax": 800,
            "Solar": 1200,
            "Dexlite": 600
        }
        
        self.posisi = {
            "pos1": {"nama": "Pompa Premium", "status": "Aktif"},
            "pos2": {"nama": "Pompa Pertalite", "status": "Aktif"},
            "pos3": {"nama": "Pompa Pertamax", "status": "Aktif"},
            "pos4": {"nama": "Pompa Solar", "status": "Aktif"},
            "pos5": {"nama": "Pompa Dexlite", "status": "Aktif"}
        }
        
        self.transaksi = []
        self.petugas_aktif = "Admin SPBU"  # Default petugas
        self.load_data()
    
    def load_data(self):
        """Load data dari file JSON"""
        try:
            if os.path.exists('spbu_data.json'):
                with open('spbu_data.json', 'r') as f:
                    data = json.load(f)
                    self.stok_bbm = data.get('stok_bbm', self.stok_bbm)
                    self.harga_bbm = data.get('harga_bbm', self.harga_bbm)
                    self.transaksi = data.get('transaksi', [])
        except:
            pass
    
    def save_data(self):
        """Save data ke file JSON"""
        data = {
            'stok_bbm': self.stok_bbm,
            'harga_bbm': self.harga_bbm,
            'transaksi': self.transaksi
        }
        with open('spbu_data.json', 'w') as f:
            json.dump(data, f, indent=2)
    
    def tampilkan_menu_utama(self):
        clear()
        print("=== SISTEM ADMINISTRASI SPBU ===")
        print(f"👤 Petugas: {self.petugas_aktif}")
        print("1. Input Transaksi")
        print("2. Kelola Harga BBM (Upgrade Harga)")
        print("3. Kelola Stok")
        print("4. Kelola Posisi Pompa")
        print("5. Lihat Laporan Lengkap")
        print("6. Lihat Stok & Status")
        print("0. Keluar")
    
    def input_transaksi(self):
        clear()
        print("--- INPUT TRANSAKSI ---")
        print("🔧 Posisi Pompa:")
        
        for i, (pos, info) in enumerate(self.posisi.items(), 1):
            print(f"{i}. {info['nama']} - {info['status']}")
        
        try:
            pos_pilihan = int(input("Pilih posisi pompa (1-5): ")) - 1
            posisi = list(self.posisi.keys())[pos_pilihan]
            if self.posisi[posisi]['status'] != 'Aktif':
                print("❌ Pompa tidak aktif!")
                input("Tekan Enter...")
                return
        except:
            print("❌ Pilihan tidak valid!")
            input("Tekan Enter...")
            return
        
        print("\n⛽ Jenis BBM:")
        for i, bbm in enumerate(self.harga_bbm.keys(), 1):
            print(f"{i}. {bbm.capitalize()} - Rp{self.harga_bbm[bbm]:,} /liter (Stok: {self.stok_bbm[bbm]} L)")
        
        try:
            pilihan = int(input("Pilih jenis BBM (1-5): ")) - 1
            jenis = list(self.harga_bbm.keys())[pilihan]
        except:
            print("❌ Input tidak valid!")
            input("Tekan Enter...")
            return
        
        liter = float(input("Jumlah liter: "))
        
        if liter > self.stok_bbm[jenis]:
            print(f"❌ Stok tidak mencukupi! Stok tersedia: {self.stok_bbm[jenis]} L")
            input("Tekan Enter...")
            return
        
        total = liter * self.harga_bbm[jenis]
        
        # Kurangi stok
        self.stok_bbm[jenis] -= liter
        
        # Simpan transaksi
        transaksi_baru = {
            "id": len(self.transaksi) + 1,
            "jenis": jenis,
            "liter": liter,
            "total": total,
            "posisi": posisi,
            "petugas": self.petugas_aktif,
            "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.transaksi.append(transaksi_baru)
        
        print(f"\n=== 📄 STRUK TRANSAKSI ===")
        print(f"⛽ Jenis BBM: {jenis.capitalize()}")
        print(f"📏 Liter: {liter} L")
        print(f"💰 Harga: Rp{self.harga_bbm[jenis]:,}/L")
        print(f"💵 Total: Rp{total:,}")
        print(f"👤 Petugas: {self.petugas_aktif}")
        print(f"🔧 Posisi: {self.posisi[posisi]['nama']}")
        print("✅ Transaksi berhasil!")
        
        if self.stok_bbm[jenis] < 100:
            print("⚠️  PERINGATAN: Stok hampir habis!")
        
        self.save_data()
        input("\nTekan Enter untuk kembali...")
    
    def upgrade_harga(self):
        clear()
        print("--- 💰 UPGRADE HARGA BBM ---")
        print("Harga saat ini:")
        for bbm, harga in self.harga_bbm.items():
            print(f"  {bbm.capitalize()}: Rp{harga:,}")
        
        print("\nPilih BBM untuk diubah (0 untuk selesai):")
        for i, bbm in enumerate(self.harga_bbm.keys(), 1):
            print(f"{i}. {bbm.capitalize()}")
        
        while True:
            try:
                pilihan = int(input("Pilih (0-5): "))
                if pilihan == 0:
                    break
                bbm = list(self.harga_bbm.keys())[pilihan - 1]
                harga_baru = int(input(f"Harga baru untuk {bbm.capitalize()} (Rp): "))
                self.harga_bbm[bbm] = harga_baru
                print(f"✅ Harga {bbm.capitalize()} diupdate menjadi Rp{harga_baru:,}")
                self.save_data()
            except:
                print("❌ Input tidak valid!")
                continue
    
    def kelola_stok(self):
        clear()
        print("--- 📦 KELOLA STOK ---")
        print("1. Tambah Stok")
        print("2. Lihat Stok")
        pilihan = input("Pilih: ")
        
        if pilihan == "1":
            print("\nStok saat ini:")
            for bbm, stok in self.stok_bbm.items():
                print(f"  {bbm.capitalize()}: {stok} L")
            
            bbm = input("\nJenis BBM: ").lower()
            if bbm in self.stok_bbm:
                tambah = float(input("Jumlah tambah (L): "))
                sebelum = self.stok_bbm[bbm]
                self.stok_bbm[bbm] += tambah
                print(f"✅ Stok {bbm.capitalize()} bertambah {tambah} L")
                print(f"   Sebelum: {sebelum} L → Sekarang: {self.stok_bbm[bbm]} L")
                self.save_data()
            else:
                print("❌ Jenis BBM tidak valid!")
        
        elif pilihan == "2":
            self.lihat_stok_status()
        
        input("\nTekan Enter...")
    
    def kelola_posisi(self):
        clear()
        print("--- 🔧 KELOLA POSISI POMPA ---")
        for i, (pos, info) in enumerate(self.posisi.items(), 1):
            print(f"{i}. {info['nama']} - Status: {info['status']}")
        
        try:
            pilihan = int(input("\nPilih pompa untuk ubah status (1-5): ")) - 1
            posisi = list(self.posisi.keys())[pilihan]
            status_sekarang = self.posisi[posisi]['status']
            status_baru = "Nonaktif" if status_sekarang == "Aktif" else "Aktif"
            self.posisi[posisi]['status'] = status_baru
            print(f"✅ Status {self.posisi[posisi]['nama']} diubah menjadi {status_baru}")
        except:
            print("❌ Pilihan tidak valid!")
        
        input("\nTekan Enter...")
    
    def lihat_laporan_lengkap(self):
        clear()
        print("=== 📊 LAPORAN LENGKAP SPBU ===")
        print(f"👤 Petugas: {self.petugas_aktif}")
        print(f"📅 Tanggal: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 80)
        
        if not self.transaksi:
            print("📭 Belum ada transaksi.")
        else:
            total_pendapatan = sum(t['total'] for t in self.transaksi)
            print(f"{'No':<4} {'Jenis':<12} {'Liter':<7} {'Total':<13} {'Posisi':<20} {'Waktu'}")
            print("-" * 80)
            
            for t in self.transaksi[-20:]:  # 20 transaksi terakhir
                nama_posisi = self.posisi[t['posisi']]['nama'][:17]  # PERBAIKAN DI SINI
                print(f"{t['id']:<4} {t['jenis'].capitalize():<12} {t['liter']:<7.1f} "
                      f"Rp{t['total']:>10,} {nama_posisi:<20} {t['waktu']}")
            
            print("-" * 80)
            print(f"💰 TOTAL PENDAAPTAN:   Rp{total_pendapatan:,}")
            print(f"📊 TOTAL TRANSAKSI:    {len(self.transaksi)}")
            if self.transaksi:
                rata_rata = total_pendapatan / len(self.transaksi)
                print(f"📈 RATA-RATA TRANSAKSI: Rp{rata_rata:,.0f}")
        
        input("\nTekan Enter...")
    
    def lihat_stok_status(self):
        clear()
        print("=== 📦 STOK & 🔧 STATUS POMPA ===")
        print(f"{'BBM':<12} {'Stok':<8} {'Harga':<12} {'Status'}")
        print("-" * 40)
        
        for bbm in self.harga_bbm.keys():
            status = "⚠️ LOW" if self.stok_bbm[bbm] < 100 else "✅ OK"
            print(f"{bbm.capitalize():<12} {self.stok_bbm[bbm]:<8.0f} Rp{self.harga_bbm[bbm]:>9,} {status}")
        
        print("\n🔧 Status Pompa:")
        for pos, info in self.posisi.items():
            icon = "🟢" if info['status'] == "Aktif" else "🔴"
            print(f"{icon} {info['nama']}: {info['status']}")
        
        input("\nTekan Enter...")
    
    def run(self):
        input("👋 Tekan Enter untuk memulai sistem...")
        while True:
            self.tampilkan_menu_utama()
            pilih = input("Pilih menu: ")
            
            if pilih == "1":
                self.input_transaksi()
            elif pilih == "2":
                self.upgrade_harga()
            elif pilih == "3":
                self.kelola_stok()
            elif pilih == "4":
                self.kelola_posisi()
            elif pilih == "5":
                self.lihat_laporan_lengkap()
            elif pilih == "6":
                self.lihat_stok_status()
            elif pilih == "0":
                print("👋 Terima kasih! Sampai jumpa.")
                self.save_data()
                break
            else:
                print("❌ Pilihan tidak valid!")
                input("Tekan Enter...")

# Jalankan sistem
if __name__ == "__main__":
    spbu = SPBUSystem()
    spbu.run()
