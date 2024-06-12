from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal, engine, Base
from models import Artikel, Jadwal, Notifikasi, Pembayaran, Speciality, Status, User, Pasien, Hospital, Dokter, BookAppointment, Konsultasi, MedicalRecord, Transaksi
from schemas import (
    ArtikelCreate, ArtikelRead, JadwalCreate, JadwalRead, NotifikasiCreate, NotifikasiRead, PembayaranCreate, PembayaranRead, SpecialityCreate, SpecialityRead, StatusCreate, StatusRead, UserCreate, UserRead, PasienCreate, PasienRead, HospitalCreate, HospitalRead,
    DokterCreate, DokterRead, BookAppointmentCreate, BookAppointmentRead,
    KonsultasiCreate, KonsultasiRead, MedicalRecordCreate, MedicalRecordRead,
    TransaksiCreate, TransaksiRead
)
from schemas import hospital_list, speciality_list, statuses_list
import passlib.hash as _hash
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app = APIRouter()


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Utility function to get user by username
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    return {"user_id": user.id_user, "username": user.username, "email": user.email}

# User routes
@app.post("/users/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = _hash.bcrypt.hash(user.password)
    db_user = User(username=user.username, password=hashed_password, no_telp=user.no_telp, email=user.email, foto=user.foto)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id_user == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/users/", response_model=List[UserRead])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@app.put("/users/{user_id}", response_model=UserRead)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id_user == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    hashed_password = _hash.bcrypt.hash(user.password)
    db_user.username = user.username
    db_user.password = hashed_password
    db_user.no_telp = user.no_telp
    db_user.email = user.email
    db_user.foto = user.foto
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}", response_model=UserRead)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id_user == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user

# Pasien routes
@app.post("/pasiens/", response_model=PasienRead)
def create_pasien(pasien: PasienCreate, db: Session = Depends(get_db)):
    db_pasien = Pasien(**pasien.dict())
    db.add(db_pasien)
    db.commit()
    db.refresh(db_pasien)
    return db_pasien

@app.post("/{user_id}/pasiens/", response_model=PasienRead)
def create_pasien_for_user(user_id: int, pasien: PasienCreate, db: Session = Depends(get_db)):
    # Add user_id to the pasien data before creating the record
    pasien_data = pasien.model_dump()
    pasien_data["user_id"] = user_id
    
    db_pasien = Pasien(**pasien_data)
    db.add(db_pasien)
    db.commit()
    db.refresh(db_pasien)
    return db_pasien

@app.get("/{user_id}/pasiens", response_model=List[PasienRead])
def read_pasiens_for_user(user_id: int, db: Session = Depends(get_db)):
    db_pasiens = db.query(Pasien).filter(Pasien.user_id == user_id).all()
    if not db_pasiens:
        raise HTTPException(status_code=404, detail="No pasiens found for this user")
    return db_pasiens

@app.get("/pasiens/", response_model=List[PasienRead])
def read_pasiens(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    pasiens = db.query(Pasien).offset(skip).limit(limit).all()
    return pasiens

@app.put("/pasiens/{pasien_id}", response_model=PasienRead)
def update_pasien(pasien_id: int, pasien: PasienCreate, db: Session = Depends(get_db)):
    db_pasien = db.query(Pasien).filter(Pasien.id_pasien == pasien_id).first()
    if db_pasien is None:
        raise HTTPException(status_code=404, detail="Pasien not found")
    for var, value in vars(pasien).items():
        setattr(db_pasien, var, value) if value else None
    db.commit()
    db.refresh(db_pasien)
    return db_pasien

@app.delete("/pasiens/{pasien_id}", response_model=PasienRead)
def delete_pasien(pasien_id: int, db: Session = Depends(get_db)):
    db_pasien = db.query(Pasien).filter(Pasien.id_pasien == pasien_id).first()
    if db_pasien is None:
        raise HTTPException(status_code=404, detail="Pasien not found")
    db.delete(db_pasien)
    db.commit()
    return db_pasien


# Hospital routes
@app.post("/hospitals/", response_model=HospitalRead)
def create_hospital(hospital: HospitalCreate, db: Session = Depends(get_db)):
    db_hospital = Hospital(**hospital.dict())
    db.add(db_hospital)
    db.commit()
    db.refresh(db_hospital)
    return db_hospital

@app.get("/hospitals/{hospital_id}", response_model=HospitalRead)
def read_hospital(hospital_id: int, db: Session = Depends(get_db)):
    db_hospital = db.query(Hospital).filter(Hospital.id_hospital == hospital_id).first()
    if db_hospital is None:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return db_hospital

@app.get("/hospitals/", response_model=List[HospitalRead])
def read_hospitals(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    hospitals = db.query(Hospital).offset(skip).limit(limit).all()
    return hospitals

@app.put("/hospitals/{hospital_id}", response_model=HospitalRead)
def update_hospital(hospital_id: int, hospital: HospitalCreate, db: Session = Depends(get_db)):
    db_hospital = db.query(Hospital).filter(Hospital.id_hospital == hospital_id).first()
    if db_hospital is None:
        raise HTTPException(status_code=404, detail="Hospital not found")
    for var, value in vars(hospital).items():
        setattr(db_hospital, var, value) if value else None
    db.commit()
    db.refresh(db_hospital)
    return db_hospital

@app.delete("/hospitals/{hospital_id}", response_model=HospitalRead)
def delete_hospital(hospital_id: int, db: Session = Depends(get_db)):
    db_hospital = db.query(Hospital).filter(Hospital.id_hospital == hospital_id).first()
    if db_hospital is None:
        raise HTTPException(status_code=404, detail="Hospital not found")
    db.delete(db_hospital)
    db.commit()
    return db_hospital

@app.post("/import_hospitals/")
def import_hospitals(db: Session = Depends(get_db)):
    for hospital in hospital_list:
        create_hospital(hospital, db)
    return {"message": "Hospitals imported successfully"}

# Speciality routes
@app.post("/specialitys/", response_model=SpecialityRead)
def create_speciality(speciality: SpecialityCreate, db: Session = Depends(get_db)):
    db_speciality = Speciality(**speciality.dict())
    db.add(db_speciality)
    db.commit()
    db.refresh(db_speciality)
    return db_speciality

@app.get("/specialitys/{speciality_id}", response_model=SpecialityRead)
def read_speciality(speciality_id: int, db: Session = Depends(get_db)):
    db_speciality = db.query(Speciality).filter(Speciality.id_speciality == speciality_id).first()
    if db_speciality is None:
        raise HTTPException(status_code=404, detail="Speciality not found")
    return db_speciality

@app.get("/specialitys/", response_model=List[SpecialityRead])
def read_specialitys(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    specialitys = db.query(Speciality).offset(skip).limit(limit).all()
    return specialitys

@app.put("/specialitys/{speciality_id}", response_model=SpecialityRead)
def update_speciality(speciality_id: int, speciality: SpecialityCreate, db: Session = Depends(get_db)):
    db_speciality = db.query(Speciality).filter(Speciality.id_speciality == speciality_id).first()
    if db_speciality is None:
        raise HTTPException(status_code=404, detail="Speciality not found")
    for var, value in vars(speciality).items():
        setattr(db_speciality, var, value) if value else None
    db.commit()
    db.refresh(db_speciality)
    return db_speciality

@app.delete("/specialitys/{speciality_id}", response_model=SpecialityRead)
def delete_speciality(speciality_id: int, db: Session = Depends(get_db)):
    db_speciality = db.query(Speciality).filter(Speciality.id_speciality == speciality_id).first()
    if db_speciality is None:
        raise HTTPException(status_code=404, detail="Speciality not found")
    db.delete(db_speciality)
    db.commit()
    return db_speciality

@app.post("/import_specialities/")
def import_specialities(db: Session = Depends(get_db)):
    for speciality in speciality_list:
        create_speciality(speciality, db)
    return {"message": "Specialities imported successfully"}

# Jadwal routes
@app.post("/jadwals/", response_model=JadwalRead)
def create_jadwal(jadwal: JadwalCreate, db: Session = Depends(get_db)):
    db_jadwal = Jadwal(**jadwal.dict())
    db.add(db_jadwal)
    db.commit()
    db.refresh(db_jadwal)
    return db_jadwal

@app.get("/jadwals/{jadwal_id}", response_model=JadwalRead)
def read_jadwal(jadwal_id: int, db: Session = Depends(get_db)):
    db_jadwal = db.query(Jadwal).filter(Jadwal.id_jadwal == jadwal_id).first()
    if db_jadwal is None:
        raise HTTPException(status_code=404, detail="Jadwal not found")
    return db_jadwal

@app.get("/jadwals/", response_model=List[JadwalRead])
def read_jadwals(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    jadwals = db.query(Jadwal).offset(skip).limit(limit).all()
    return jadwals

@app.put("/jadwals/{jadwal_id}", response_model=JadwalRead)
def update_jadwal(jadwal_id: int, jadwal: JadwalCreate, db: Session = Depends(get_db)):
    db_jadwal = db.query(Jadwal).filter(Jadwal.id_jadwal == jadwal_id).first()
    if db_jadwal is None:
        raise HTTPException(status_code=404, detail="Jadwal not found")
    for var, value in vars(jadwal).items():
        setattr(db_jadwal, var, value) if value else None
    db.commit()
    db.refresh(db_jadwal)
    return db_jadwal

@app.delete("/jadwals/{jadwal_id}", response_model=JadwalRead)
def delete_jadwal(jadwal_id: int, db: Session = Depends(get_db)):
    db_jadwal = db.query(Jadwal).filter(Jadwal.id_jadwal == jadwal_id).first()
    if db_jadwal is None:
        raise HTTPException(status_code=404, detail="Jadwal not found")
    db.delete(db_jadwal)
    db.commit()
    return db_jadwal

# Dokter routes
@app.post("/dokters/", response_model=DokterRead)
def create_dokter(dokter: DokterCreate, db: Session = Depends(get_db)):
    db_dokter = Dokter(**dokter.dict())
    db.add(db_dokter)
    db.commit()
    db.refresh(db_dokter)
    return db_dokter

@app.get("/dokters/{dokter_id}", response_model=DokterRead)
def read_dokter(dokter_id: int, db: Session = Depends(get_db)):
    db_dokter = db.query(Dokter).filter(Dokter.id_dokter == dokter_id).first()
    if db_dokter is None:
        raise HTTPException(status_code=404, detail="Dokter not found")
    return db_dokter

@app.get("/dokters/", response_model=List[DokterRead])
def read_dokters(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    dokters = db.query(Dokter).offset(skip).limit(limit).all()
    return dokters

@app.put("/dokters/{dokter_id}", response_model=DokterRead)
def update_dokter(dokter_id: int, dokter: DokterCreate, db: Session = Depends(get_db)):
    db_dokter = db.query(Dokter).filter(Dokter.id_dokter == dokter_id).first()
    if db_dokter is None:
        raise HTTPException(status_code=404, detail="Dokter not found")
    for var, value in vars(dokter).items():
        setattr(db_dokter, var, value) if value else None
    db.commit()
    db.refresh(db_dokter)
    return db_dokter

@app.delete("/dokters/{dokter_id}", response_model=DokterRead)
def delete_dokter(dokter_id: int, db: Session = Depends(get_db)):
    db_dokter = db.query(Dokter).filter(Dokter.id_dokter == dokter_id).first()
    if db_dokter is None:
        raise HTTPException(status_code=404, detail="Dokter not found")
    db.delete(db_dokter)
    db.commit()
    return db_dokter

# BookAppointment routes
@app.post("/book_appointments/", response_model=BookAppointmentRead)
def create_book_appointment(book_appointment: BookAppointmentCreate, db: Session = Depends(get_db)):
    db_book_appointment = BookAppointment(**book_appointment.dict())
    db.add(db_book_appointment)
    db.commit()
    db.refresh(db_book_appointment)
    return db_book_appointment

@app.get("/book_appointments/{appointment_id}", response_model=BookAppointmentRead)
def read_book_appointment(appointment_id: int, db: Session = Depends(get_db)):
    db_book_appointment = db.query(BookAppointment).filter(BookAppointment.id == appointment_id).first()
    if db_book_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return db_book_appointment

@app.get("/book_appointments/", response_model=List[BookAppointmentRead])
def read_book_appointments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    book_appointments = db.query(BookAppointment).offset(skip).limit(limit).all()
    return book_appointments

@app.put("/book_appointments/{appointment_id}", response_model=BookAppointmentRead)
def update_book_appointment(appointment_id: int, book_appointment: BookAppointmentCreate, db: Session = Depends(get_db)):
    db_book_appointment = db.query(BookAppointment).filter(BookAppointment.id == appointment_id).first()
    if db_book_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    for var, value in vars(book_appointment).items():
        setattr(db_book_appointment, var, value) if value else None
    db.commit()
    db.refresh(db_book_appointment)
    return db_book_appointment

@app.delete("/book_appointments/{appointment_id}", response_model=BookAppointmentRead)
def delete_book_appointment(appointment_id: int, db: Session = Depends(get_db)):
    db_book_appointment = db.query(BookAppointment).filter(BookAppointment.id == appointment_id).first()
    if db_book_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db.delete(db_book_appointment)
    db.commit()
    return db_book_appointment

# Konsultasi routes
@app.post("/konsultasis/", response_model=KonsultasiRead)
def create_konsultasi(konsultasi: KonsultasiCreate, db: Session = Depends(get_db)):
    db_konsultasi = Konsultasi(**konsultasi.dict())
    db.add(db_konsultasi)
    db.commit()
    db.refresh(db_konsultasi)
    return db_konsultasi

@app.get("/konsultasis/{konsultasi_id}", response_model=KonsultasiRead)
def read_konsultasi(konsultasi_id: int, db: Session = Depends(get_db)):
    db_konsultasi = db.query(Konsultasi).filter(Konsultasi.id_konsultasi == konsultasi_id).first()
    if db_konsultasi is None:
        raise HTTPException(status_code=404, detail="Konsultasi not found")
    return db_konsultasi

@app.get("/konsultasis/", response_model=List[KonsultasiRead])
def read_konsultasis(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    konsultasis = db.query(Konsultasi).offset(skip).limit(limit).all()
    return konsultasis

@app.put("/konsultasis/{konsultasi_id}", response_model=KonsultasiRead)
def update_konsultasi(konsultasi_id: int, konsultasi: KonsultasiCreate, db: Session = Depends(get_db)):
    db_konsultasi = db.query(Konsultasi).filter(Konsultasi.id_konsultasi == konsultasi_id).first()
    if db_konsultasi is None:
        raise HTTPException(status_code=404, detail="Konsultasi not found")
    for var, value in vars(konsultasi).items():
        setattr(db_konsultasi, var, value) if value else None
    db.commit()
    db.refresh(db_konsultasi)
    return db_konsultasi

@app.delete("/konsultasis/{konsultasi_id}", response_model=KonsultasiRead)
def delete_konsultasi(konsultasi_id: int, db: Session = Depends(get_db)):
    db_konsultasi = db.query(Konsultasi).filter(Konsultasi.id_konsultasi == konsultasi_id).first()
    if db_konsultasi is None:
        raise HTTPException(status_code=404, detail="Konsultasi not found")
    db.delete(db_konsultasi)
    db.commit()
    return db_konsultasi

# MedicalRecord routes
@app.post("/medical_records/", response_model=MedicalRecordRead)
def create_medical_record(medical_record: MedicalRecordCreate, db: Session = Depends(get_db)):
    db_medical_record = MedicalRecord(**medical_record.dict())
    db.add(db_medical_record)
    db.commit()
    db.refresh(db_medical_record)
    return db_medical_record

@app.get("/medical_records/{medical_record_id}", response_model=MedicalRecordRead)
def read_medical_record(medical_record_id: int, db: Session = Depends(get_db)):
    db_medical_record = db.query(MedicalRecord).filter(MedicalRecord.id_medical_record == medical_record_id).first()
    if db_medical_record is None:
        raise HTTPException(status_code=404, detail="Medical record not found")
    return db_medical_record

@app.get("/medical_records/", response_model=List[MedicalRecordRead])
def read_medical_records(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    medical_records = db.query(MedicalRecord).offset(skip).limit(limit).all()
    return medical_records

@app.put("/medical_records/{medical_record_id}", response_model=MedicalRecordRead)
def update_medical_record(medical_record_id: int, medical_record: MedicalRecordCreate, db: Session = Depends(get_db)):
    db_medical_record = db.query(MedicalRecord).filter(MedicalRecord.id_medical_record == medical_record_id).first()
    if db_medical_record is None:
        raise HTTPException(status_code=404, detail="Medical record not found")
    for var, value in vars(medical_record).items():
        setattr(db_medical_record, var, value) if value else None
    db.commit()
    db.refresh(db_medical_record)
    return db_medical_record

@app.delete("/medical_records/{medical_record_id}", response_model=MedicalRecordRead)
def delete_medical_record(medical_record_id: int, db: Session = Depends(get_db)):
    db_medical_record = db.query(MedicalRecord).filter(MedicalRecord.id_medical_record == medical_record_id).first()
    if db_medical_record is None:
        raise HTTPException(status_code=404, detail="Medical record not found")
    db.delete(db_medical_record)
    db.commit()
    return db_medical_record

# Transaksi routes
@app.post("/transaksis/", response_model=TransaksiRead)
def create_transaksi(transaksi: TransaksiCreate, db: Session = Depends(get_db)):
    db_transaksi = Transaksi(**transaksi.dict())
    db.add(db_transaksi)
    db.commit()
    db.refresh(db_transaksi)
    return db_transaksi

@app.get("/transaksis/{transaksi_id}", response_model=TransaksiRead)
def read_transaksi(transaksi_id: int, db: Session = Depends(get_db)):
    db_transaksi = db.query(Transaksi).filter(Transaksi.id_transaksi == transaksi_id).first()
    if db_transaksi is None:
        raise HTTPException(status_code=404, detail="Transaksi not found")
    return db_transaksi

@app.get("/transaksis/", response_model=List[TransaksiRead])
def read_transaksis(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    transaksis = db.query(Transaksi).offset(skip).limit(limit).all()
    return transaksis

@app.put("/transaksis/{transaksi_id}", response_model=TransaksiRead)
def update_transaksi(transaksi_id: int, transaksi: TransaksiCreate, db: Session = Depends(get_db)):
    db_transaksi = db.query(Transaksi).filter(Transaksi.id_transaksi == transaksi_id).first()
    if db_transaksi is None:
        raise HTTPException(status_code=404, detail="Transaksi not found")
    for var, value in vars(transaksi).items():
        setattr(db_transaksi, var, value) if value else None
    db.commit()
    db.refresh(db_transaksi)
    return db_transaksi

@app.delete("/transaksis/{transaksi_id}", response_model=TransaksiRead)
def delete_transaksi(transaksi_id: int, db: Session = Depends(get_db)):
    db_transaksi = db.query(Transaksi).filter(Transaksi.id_transaksi == transaksi_id).first()
    if db_transaksi is None:
        raise HTTPException(status_code=404, detail="Transaksi not found")
    db.delete(db_transaksi)
    db.commit()
    return db_transaksi

# Artikel routes
@app.post("/artikels/", response_model=ArtikelRead)
def create_artikel(artikel: ArtikelCreate, db: Session = Depends(get_db)):
    db_artikel = Artikel(**artikel.dict())
    db.add(db_artikel)
    db.commit()
    db.refresh(db_artikel)
    return db_artikel

@app.get("/artikels/{artikel_id}", response_model=ArtikelRead)
def read_artikel(artikel_id: int, db: Session = Depends(get_db)):
    db_artikel = db.query(Artikel).filter(Artikel.id_artikel == artikel_id).first()
    if db_artikel is None:
        raise HTTPException(status_code=404, detail="Artikel not found")
    return db_artikel

@app.get("/artikels/", response_model=List[ArtikelRead])
def read_artikels(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    
    artikels = db.query(Artikel).offset(skip).limit(limit).all()
    return artikels

@app.put("/artikels/{artikel_id}", response_model=ArtikelRead)
def update_artikel(artikel_id: int, artikel: ArtikelCreate, db: Session = Depends(get_db)):
    db_artikel = db.query(Artikel).filter(Artikel.id_artikel == artikel_id).first()
    if db_artikel is None:
        raise HTTPException(status_code=404, detail="Artikel not found")
    for var, value in vars(artikel).items():
        setattr(db_artikel, var, value) if value else None
    db.commit()
    db.refresh(db_artikel)
    return db_artikel

@app.delete("/artikels/{artikel_id}", response_model=ArtikelRead)
def delete_artikel(artikel_id: int, db: Session = Depends(get_db)):
    db_artikel = db.query(Artikel).filter(Artikel.id_artikel == artikel_id).first()
    if db_artikel is None:
        raise HTTPException(status_code=404, detail="Artikel not found")
    db.delete(db_artikel)
    db.commit()
    return db_artikel


# Pembayaran routes
@app.post("/pembayarans/", response_model=PembayaranRead)
def create_pembayaran(pembayaran: PembayaranCreate, db: Session = Depends(get_db)):
    db_pembayaran = Pembayaran(**pembayaran.dict())
    db.add(db_pembayaran)
    db.commit()
    db.refresh(db_pembayaran)
    return db_pembayaran

@app.get("/pembayarans/{pembayaran_id}", response_model=PembayaranRead)
def read_pembayaran(pembayaran_id: int, db: Session = Depends(get_db)):
    db_pembayaran = db.query(Pembayaran).filter(Pembayaran.id_pembayaran == pembayaran_id).first()
    if db_pembayaran is None:
        raise HTTPException(status_code=404, detail="Pembayaran not found")
    return db_pembayaran

@app.get("/pembayarans/", response_model=List[PembayaranRead])
def read_pembayarans(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    pembayarans = db.query(Pembayaran).offset(skip).limit(limit).all()
    return pembayarans

@app.put("/pembayarans/{pembayaran_id}", response_model=PembayaranRead)
def update_pembayaran(pembayaran_id: int, pembayaran: PembayaranCreate, db: Session = Depends(get_db)):
    db_pembayaran = db.query(Pembayaran).filter(Pembayaran.id_pembayaran == pembayaran_id).first()
    if db_pembayaran is None:
        raise HTTPException(status_code=404, detail="Pembayaran not found")
    for var, value in vars(pembayaran).items():
        setattr(db_pembayaran, var, value) if value else None
    db.commit()
    db.refresh(db_pembayaran)
    return db_pembayaran

@app.delete("/pembayarans/{pembayaran_id}", response_model=PembayaranRead)
def delete_pembayaran(pembayaran_id: int, db: Session = Depends(get_db)):
    db_pembayaran = db.query(Pembayaran).filter(Pembayaran.id_pembayaran == pembayaran_id).first()
    if db_pembayaran is None:
        raise HTTPException(status_code=404, detail="Pembayaran not found")
    db.delete(db_pembayaran)
    db.commit()
    return db_pembayaran


# Notifikasi routes
@app.post("/notifikasis/", response_model=NotifikasiRead)
def create_notifikasi(notifikasi: NotifikasiCreate, db: Session = Depends(get_db)):
    db_notifikasi = Notifikasi(**notifikasi.dict())
    db.add(db_notifikasi)
    db.commit()
    db.refresh(db_notifikasi)
    return db_notifikasi

@app.get("/notifikasis/{notifikasi_id}", response_model=NotifikasiRead)
def read_notifikasi(notifikasi_id: int, db: Session = Depends(get_db)):
    db_notifikasi = db.query(Notifikasi).filter(Notifikasi.id_notifikasi == notifikasi_id).first()
    if db_notifikasi is None:
        raise HTTPException(status_code=404, detail="Notifikasi not found")
    return db_notifikasi

@app.get("/notifikasis/", response_model=List[NotifikasiRead])
def read_notifikasis(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    notifikasis = db.query(Notifikasi).offset(skip).limit(limit).all()
    return notifikasis

@app.put("/notifikasis/{notifikasi_id}", response_model=NotifikasiRead)
def update_notifikasi(notifikasi_id: int, notifikasi: NotifikasiCreate, db: Session = Depends(get_db)):
    db_notifikasi = db.query(Notifikasi).filter(Notifikasi.id_notifikasi == notifikasi_id).first()
    if db_notifikasi is None:
        raise HTTPException(status_code=404, detail="Notifikasi not found")
    for var, value in vars(notifikasi).items():
        setattr(db_notifikasi, var, value) if value else None
    db.commit()
    db.refresh(db_notifikasi)
    return db_notifikasi

@app.delete("/notifikasis/{notifikasi_id}", response_model=NotifikasiRead)
def delete_notifikasi(notifikasi_id: int, db: Session = Depends(get_db)):
    db_notifikasi = db.query(Notifikasi).filter(Notifikasi.id_notifikasi == notifikasi_id).first()
    if db_notifikasi is None:
        raise HTTPException(status_code=404, detail="Notifikasi not found")
    db.delete(db_notifikasi)
    db.commit()
    return db_notifikasi

# Statuse routes
@app.post("/statuses/", response_model=StatusRead)
def create_status(status: StatusCreate, db: Session = Depends(get_db)):
    db_status = Status(**status.dict())
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    return db_status

@app.get("/statuses/{status_id}", response_model=StatusRead)
def read_status(status_id: int, db: Session = Depends(get_db)):
    db_status = db.query(Status).filter(Status.id_status == status_id).first()
    if db_status is None:
        raise HTTPException(status_code=404, detail="Status not found")
    return db_status

@app.get("/statuses/", response_model=List[StatusRead])
def read_statuss(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    
    statuss = db.query(Status).offset(skip).limit(limit).all()
    return statuss

@app.put("/statuses/{status_id}", response_model=StatusRead)
def update_status(status_id: int, status: StatusCreate, db: Session = Depends(get_db)):
    db_status = db.query(Status).filter(Status.id_status == status_id).first()
    if db_status is None:
        raise HTTPException(status_code=404, detail="Status not found")
    for var, value in vars(status).items():
        setattr(db_status, var, value) if value else None
    db.commit()
    db.refresh(db_status)
    return db_status

@app.delete("/statuses/{status_id}", response_model=StatusRead)
def delete_status(status_id: int, db: Session = Depends(get_db)):
    db_status = db.query(Status).filter(Status.id_status == status_id).first()
    if db_status is None:
        raise HTTPException(status_code=404, detail="Status not found")
    db.delete(db_status)
    db.commit()
    return db_status

@app.post("/import_statusess/")
def import_statuses(db: Session = Depends(get_db)):
    for status in statuses_list:
        create_status(status, db)
    return {"message": "Statuses imported successfully"}


# Endpoint to retrieve medical record by appointment ID
@app.get("/medical_records/by_appointment/{appointment_id}", response_model=MedicalRecordRead)
def get_medical_record_by_appointment_id(appointment_id: int, db: Session = Depends(get_db)):
    # Query to find the BookAppointment record with the given appointment_id
    appointment = db.query(BookAppointment).filter(BookAppointment.id == appointment_id).first()
    
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    # Query to find the MedicalRecord associated with the appointment
    medical_record = db.query(MedicalRecord).filter(MedicalRecord.appointment_id == appointment_id).first()
    
    if not medical_record:
        raise HTTPException(status_code=404, detail="Medical record not found")
    
    return medical_record