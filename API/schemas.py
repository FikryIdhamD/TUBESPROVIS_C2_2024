from pydantic import BaseModel, validator
from datetime import date, datetime
from typing import List, Optional

class UserCreate(BaseModel):
    username: str
    password: str
    no_telp: str
    email: str
    foto: Optional[str] = None

class UserRead(BaseModel):
    id_user: int
    username: str
    no_telp: str
    email: str
    foto: Optional[str] = None

    class Config:
        orm_mode = True

class PasienCreate(BaseModel):
    nik: str
    nama_pasien: str
    gender: str
    alamat: str
    tanggal_lahir: date
    no_telp: str

class PasienRead(BaseModel):
    id_pasien: int
    nik: str
    nama_pasien: str
    gender: str
    alamat: str
    tanggal_lahir: date
    no_telp: str

    class Config:
        orm_mode = True

class HospitalCreate(BaseModel):
    nama_hospital: str
    alamat: str

class HospitalRead(BaseModel):
    id_hospital: int
    nama_hospital: str
    alamat: str

    class Config:
        orm_mode = True

hospital_list = [
    HospitalCreate(
        nama_hospital="RS Pertamina",
        alamat="Jl. Kesehatan No. 1, Jakarta"
    ),
    HospitalCreate(
        nama_hospital="RS Harapan Kita",
        alamat="Jl. Letjen S. Parman No. 87, Jakarta"
    ),
    HospitalCreate(
        nama_hospital="RS Cipto Mangunkusumo",
        alamat="Jl. Diponegoro No. 71, Jakarta"
    ),
    HospitalCreate(
        nama_hospital="RS Siloam",
        alamat="Jl. Sudirman No. 55, Jakarta"
    ),
    HospitalCreate(
        nama_hospital="RS Pondok Indah",
        alamat="Jl. Metro Duta Kav. UE, Jakarta"
    ),
    HospitalCreate(
        nama_hospital="RS MMC",
        alamat="Jl. H.R. Rasuna Said No. 50, Jakarta"
    ),
    HospitalCreate(
        nama_hospital="RS Mayapada",
        alamat="Jl. Lebak Bulus I No. 29, Jakarta"
    ),
    HospitalCreate(
        nama_hospital="RS Puri Indah",
        alamat="Jl. Puri Indah Raya Blok S-2, Jakarta"
    ),
    HospitalCreate(
        nama_hospital="RS Pelni",
        alamat="Jl. Aipda K.S. Tubun No. 92-94, Jakarta"
    ),
    HospitalCreate(
        nama_hospital="RS Hermina",
        alamat="Jl. Raya Jatinegara Barat No. 126, Jakarta"
    )
]


class SpecialityCreate(BaseModel):
    nama_speciality: str

class SpecialityRead(BaseModel):
    id_speciality: int
    nama_speciality: str

    class Config:
        orm_mode = True

speciality_list = [
    SpecialityCreate(nama_speciality="Kardiologi"),
    SpecialityCreate(nama_speciality="Neurologi"),
    SpecialityCreate(nama_speciality="Ortopedi"),
    SpecialityCreate(nama_speciality="Ginekologi"),
    SpecialityCreate(nama_speciality="Pediatri"),
    SpecialityCreate(nama_speciality="Dermatologi"),
    SpecialityCreate(nama_speciality="Oftalmologi"),
    SpecialityCreate(nama_speciality="Psikiatri"),
    SpecialityCreate(nama_speciality="Onkologi"),
    SpecialityCreate(nama_speciality="Gastroenterologi")
]

class JadwalCreate(BaseModel):
    hari: str
    jam: str
    dokter_id: Optional[int] = None 

class JadwalRead(BaseModel):
    id_jadwal: int
    hari: str
    jam: str

    class Config:
        orm_mode = True

class DokterCreate(BaseModel):
    nama_dokter: str
    speciality_id: int
    hospital_id: int
    jadwals: List[JadwalRead] = []

class DokterRead(BaseModel):
    id_dokter: int
    nama_dokter: str
    speciality_id: int
    hospital_id: int
    jadwals: List[JadwalRead] = []

    class Config:
        orm_mode = True

class BookAppointmentCreate(BaseModel):
    user_id: int
    pasien_id: int
    hospital_id: int
    dokter_id: int
    jadwal_id: int
    status_id: int
    tanggal: Optional[datetime] = None

    @validator('tanggal', pre=True)
    def parse_tanggal(cls, value):
        if value:
            # Parse the incoming string date into a datetime object
            return datetime.strptime(value, '%Y-%m-%d')
        else:
            # If no value provided, set default date format
            return date(1111, 11, 11)  # or date(0000, 00, 00)

class BookAppointmentRead(BaseModel):
    id: int
    user_id: int
    pasien_id: int
    hospital_id: int
    dokter_id: int
    jadwal_id: int
    status_id: int
    tanggal: Optional[datetime] = None

    class Config:
        orm_mode = True

class KonsultasiCreate(BaseModel):
    user_id:int
    pasien_id: int
    dokter_id: int
    metode_pembayaran: str

class KonsultasiRead(BaseModel):
    id_konsultasi: int
    user_id:int
    pasien_id: int
    dokter_id: int
    metode_pembayaran: str

    class Config:
        orm_mode = True

class MedicalRecordCreate(BaseModel):
    user_id:int
    pasien_id: int
    appointment_id: int
    bloodpressure: str
    tinggi_badan: str
    berat_badan: str
    complain: str
    hasil_pemeriksaan: str
    riwayat_medis: str
    dokumen_pdf: Optional[str] = None

class MedicalRecordRead(BaseModel):
    id_medical_record: int
    user_id:int
    pasien_id: int
    appointment_id: int
    bloodpressure: str
    tinggi_badan: str
    berat_badan: str
    complain: str
    hasil_pemeriksaan: str
    riwayat_medis: str
    dokumen_pdf: Optional[str] = None

    class Config:
        orm_mode = True

class TransaksiCreate(BaseModel):
    user_id: int
    pasien_id: int
    appointment_id: int
    konsultasi_id: int
    status_id: int

class TransaksiRead(BaseModel):
    id_transaksi: int
    user_id: int
    pasien_id: int
    appointment_id: int
    konsultasi_id: int
    status_id: int

    class Config:
        orm_mode = True

class StatusCreate(BaseModel):
    nama_status: str
    deskripsi: str

class StatusRead(BaseModel):
    id_status: int
    nama_status: str
    deskripsi: str

    class Config:
        orm_mode = True

statuses_list = [
    StatusRead(id_status=1, nama_status="Scheduled", deskripsi="Appointment sudah di Buat"),
    StatusRead(id_status=2, nama_status="Registration", deskripsi="Silakan Scan Kode QR di pintu masuk ya"),
    StatusRead(id_status=3, nama_status="Nurse Station", deskripsi="Waktunya pemeriksaan awal, ditunggu di Nurse Station ya"),
    StatusRead(id_status=4, nama_status="See Doctor", deskripsi="Silakan masuk ke ruangan Dokter, Waktunya pemeriksaan"),
    StatusRead(id_status=5, nama_status="Payment", deskripsi="Silakan lakukan Pembayaran, Terima Kasih"),
    StatusRead(id_status=6, nama_status="Finished", deskripsi="Sudah selesai, Semoga sehat selalu"),
]

class ArtikelBase(BaseModel):
    deskripsi_artikel: str
    title_artikel: str
    foto_artikel: Optional[str] = None

class ArtikelCreate(ArtikelBase):
    pass

class ArtikelRead(ArtikelBase):
    id_artikel: int

    class Config:
        orm_mode = True


class PembayaranBase(BaseModel):
    nama_metode_pembayaran: str
    jumlah: int

class PembayaranCreate(PembayaranBase):
    user_id: int
    transaksi_id: int

class PembayaranRead(PembayaranBase):
    id_pembayaran: int
    user_id: int
    transaksi_id: int

    class Config:
        orm_mode = True
    

class NotifikasiCreate(BaseModel):
    user_id:int
    deskripsi: str
    jenis: str

class NotifikasiRead(BaseModel):
    id_notifikasi: int
    user_id:int
    deskripsi: str
    jenis: str

    class Config:
        orm_mode = True
