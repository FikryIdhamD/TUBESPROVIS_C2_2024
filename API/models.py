from sqlalchemy import Column, DateTime, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
import passlib.hash as _hash
from database import Base


class User(Base):
    __tablename__ = "users"

    id_user = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    no_telp = Column(String)
    email = Column(String)
    foto = Column(String)

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.password)

class Pasien(Base):
    __tablename__ = "pasiens"

    id_pasien = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id_user'))
    nik = Column(String)
    nama_pasien = Column(String)
    gender = Column(String)
    alamat = Column(String)
    tanggal_lahir = Column(Date)
    no_telp = Column(String)

class Hospital(Base):
    __tablename__ = "hospitals"

    id_hospital = Column(Integer, primary_key=True, index=True)
    nama_hospital = Column(String)
    alamat = Column(String)
    
class Speciality(Base):
    __tablename__ = "specialities"

    id_speciality = Column(Integer, primary_key=True, index=True)
    nama_speciality = Column(String)


class Dokter(Base):
    __tablename__ = "dokters"

    id_dokter = Column(Integer, primary_key=True, index=True)
    nama_dokter = Column(String)
    speciality_id = Column(Integer, ForeignKey('specialities.id_speciality'))
    hospital_id = Column(Integer, ForeignKey('hospitals.id_hospital'))

    speciality = relationship("Speciality")
    hospital = relationship("Hospital")
    jadwals = relationship("Jadwal", back_populates="dokter")  # Relationship to Jadwal


class Jadwal(Base):
    __tablename__ = "jadwals"

    id_jadwal = Column(Integer, primary_key=True, index=True)
    hari = Column(String)
    jam = Column(String)
    dokter_id = Column(Integer, ForeignKey('dokters.id_dokter'))  # Foreign key to Dokter

    dokter = relationship("Dokter", back_populates="jadwals")  # Relationship to Dokter
    
class Status(Base):
    __tablename__ = "statuses"

    id_status = Column(Integer, primary_key=True, index=True)
    nama_status = Column(String)
    deskripsi = Column(String)

class BookAppointment(Base):
    __tablename__ = "book_appointments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id_user'))
    pasien_id = Column(Integer, ForeignKey('pasiens.id_pasien'))
    hospital_id = Column(Integer, ForeignKey('hospitals.id_hospital'))
    dokter_id = Column(Integer, ForeignKey('dokters.id_dokter'))
    jadwal_id = Column(Integer, ForeignKey('jadwals.id_jadwal'))
    status_id = Column(Integer, ForeignKey('statuses.id_status'))
    tanggal = Column(DateTime, default=None, nullable=True)

    pasien = relationship("Pasien")
    hospital = relationship("Hospital")
    dokter = relationship("Dokter")
    jadwal = relationship("Jadwal") 
    status = relationship("Status")


class Artikel(Base):
    __tablename__ = "artikels"

    id_artikel = Column(Integer, primary_key=True, index=True)
    deskripsi_artikel = Column(String)
    title_artikel = Column(String)
    foto_artikel = Column(String)


class Pembayaran(Base):
    __tablename__ = "pembayarans"

    id_pembayaran = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id_user'))
    nama_metode_pembayaran = Column(String)
    transaksi_id = Column(Integer, ForeignKey('transaksis.id_transaksi'))
    jumlah = Column(Integer)

    user = relationship("User")
    transaksi = relationship("Transaksi")


class Konsultasi(Base):
    __tablename__ = "konsultasis"

    id_konsultasi = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id_user'))
    pasien_id = Column(Integer, ForeignKey('pasiens.id_pasien'))
    dokter_id = Column(Integer, ForeignKey('dokters.id_dokter'))
    metode_pembayaran = Column(String)

    pasien = relationship("Pasien")
    dokter = relationship("Dokter")


class MedicalRecord(Base):
    __tablename__ = "medical_records"

    id_medical_record = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id_user'))
    pasien_id = Column(Integer, ForeignKey('pasiens.id_pasien'))
    appointment_id = Column(Integer, ForeignKey('book_appointments.id'))
    bloodpressure = Column(String)
    tinggi_badan = Column(String)
    berat_badan = Column(String)
    complain = Column(String)
    hasil_pemeriksaan = Column(String)
    riwayat_medis = Column(String)
    dokumen_pdf = Column(String)

    pasien = relationship("Pasien")
    appointment = relationship("BookAppointment")


class Transaksi(Base):
    __tablename__ = "transaksis"

    id_transaksi = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id_user'))
    pasien_id = Column(Integer, ForeignKey('pasiens.id_pasien'))
    appointment_id = Column(Integer, ForeignKey('book_appointments.id'))
    konsultasi_id = Column(Integer, ForeignKey('konsultasis.id_konsultasi'))
    status_id = Column(Integer, ForeignKey('statuses.id_status'))

    user = relationship("User")
    pasien = relationship("Pasien")
    appointment = relationship("BookAppointment")
    konsultasi = relationship("Konsultasi")
    status = relationship("Status")


class Notifikasi(Base):
    __tablename__ = "notifikasis"

    id_notifikasi = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id_user'))
    deskripsi = Column(String)
    jenis = Column(String)
