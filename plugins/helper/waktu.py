import json

class Waktu:
    def __init__(self, data):
        self.data = data
        self.hari = data.get('hari')
        self.tanggal = data.get('tanggal')
        self.bulan = data.get('bulan')
        self.tahun = data.get('tahun')
        self.jam = data.get('jam')
        self.full_time = data.get('full')

    def __str__(self) -> str:
        return (f"Hari: {self.hari}, Tanggal: {self.tanggal}, Bulan: {self.bulan}, "
                f"Tahun: {self.tahun}, Jam: {self.jam}, Full Time: {self.full_time}")

# Definisikan data
data = {
    'hari': 'Senin',
    'tanggal': '04',
    'bulan': 'Agustus',
    'tahun': '2024',
    'jam': '10:00',
    'full': 'Senin, 04 Agustus 2024, 10:00 WIB'
}

# Membuat instance Waktu
waktu = Waktu(data)
print(waktu)
