from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum, Time, Text
from app import db, app
from sqlalchemy.orm import relationship
from enum import Enum as UserEnum
from flask_login import UserMixin
from datetime import datetime


class UserRole(UserEnum):
    ADMIN = 1
    USER = 2
    STAFF = 3


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class HangMayBay(BaseModel):
    __tablename__ = 'hangmaybay'

    ten = Column(String(50), nullable=False, unique=True)
    gioithieu = Column(Text, nullable=False)
    hinhanh = Column(Text, nullable=False)
    chuyenbays = relationship('ChuyenBay', backref='hangmaybay', lazy=False)

    def __str__(self):
        return self.ten


class SanBay(BaseModel):
    __tablename__ = 'sanbay'

    ten = Column(String(20), nullable=False, unique=True)
    sanbaydungs = relationship('SanBayDung', backref='sanbay', lazy=False)

    # sanbaydis = relationship('TuyenBay', backref='sanbaydi', lazy=False)
    # sanbaydens = relationship('TuyenBay', backref='sanbayden', lazy=False)

    def __str__(self):
        return self.ten


class TuyenBay(BaseModel):
    __tablename__ = 'tuyenbay'

    ten = Column(String(50), nullable=False)
    sanbaydi_ma = Column(Integer, ForeignKey(SanBay.id), nullable=False)
    sanbayden_ma = Column(Integer, ForeignKey(SanBay.id), nullable=False)
    chuyenbays = relationship('ChuyenBay', backref='tuyenbay', lazy=False)
    sanbaydi = relationship("SanBay", foreign_keys=[sanbaydi_ma])
    sanbayden = relationship("SanBay", foreign_keys=[sanbayden_ma])

    def __str__(self):
        return self.ten


class ChuyenBay(BaseModel):
    __tablename__ = 'chuyenbay'

    giodi = Column(DateTime, nullable=False)
    thoigianbay = Column(Integer, nullable=False)
    hangmaybay_ma = Column(Integer, ForeignKey(HangMayBay.id), nullable=False)
    tuyenbay_ma = Column(Integer, ForeignKey(TuyenBay.id), nullable=False)
    sanbaydungs = relationship('SanBayDung', backref='chuyenbay', lazy=False)
    bangdongias = relationship('BangDonGia', backref='chuyenbay', lazy=True)


class SanBayDung(BaseModel):
    __tablename__ = 'sanbaydung'

    sanbay_ma = Column(Integer, ForeignKey(SanBay.id), nullable=False)
    thoigiandung = Column(Integer, nullable=False)
    chuyenbay_ma = Column(Integer, ForeignKey(ChuyenBay.id), nullable=False)


class NguoiDung(BaseModel, UserMixin):
    __tablename__ = 'nguoidung'

    ten = Column(String(50), nullable=False)
    taikhoan = Column(String(50), nullable=False, unique=True)
    matkhau = Column(String(50), nullable=False)
    hoatdong = Column(Boolean, default=True)
    loainguoidung = Column(Enum(UserRole), default=UserRole.USER)
    anhdaidien = Column(String(100), nullable=False)
    vechuyenbays = relationship('VeChuyenBay', backref='nguoidung', lazy=True)

    def __str__(self):
        return self.ten


class HangVe(BaseModel):
    __tablename__ = 'hangve'

    ten = Column(String(50), nullable=False, unique=True)
    bangdongias = relationship('BangDonGia', backref='hangve', lazy=True)

    def __str__(self):
        return self.ten


class BangDonGia(BaseModel):
    __tablename__ = 'bangdongia'

    hangve_ma = Column(Integer, ForeignKey(HangVe.id), nullable=False)
    chuyenbay_ma = Column(Integer, ForeignKey(ChuyenBay.id), nullable=False)
    gia = Column('giatien', Float, default=0)
    vechuyenbays = relationship('VeChuyenBay', backref='bangdongia', lazy=True)
    soghe = Column(Integer, nullable=False)


class VeChuyenBay(BaseModel):
    __tablename__ = 'vechuyenbay'

    tennguoidi = Column(String(50), nullable=False)
    cccd = Column(String(20), nullable=False)
    nguoidung_ma = Column(Integer, ForeignKey(NguoiDung.id), nullable=False)
    bangdongia_ma = Column(Integer, ForeignKey(BangDonGia.id), nullable=False)
    Ngaydat = Column(DateTime, default=datetime.now())


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        c1 = HangMayBay(ten='Vietnam Airlines',
                        gioithieu="L?? m???t H??ng h??ng kh??ng qu???c gia c?? quy m?? ho???t ?????ng to??n c???u v?? c?? t???m c??? t???i khu v???c.Vietnam Airlines cam k???t s??? lu??n ?????ng h??nh c??ng c??c c??? ????ng, minh b???ch c??ng khai th??ng tin, duy tr?? v?? n??ng cao c??c k??nh ?????i tho???i m??? v???i c??? ????ng, t??? ch???c ho???t ?????ng kinh doanh an to??n, ch???t l?????ng v?? c?? hi???u qu??? tr??n c?? s??? c??n ?????i h??i h??a l???i ??ch c???a c??? ????ng v???i vi???c ????p ???ng nhu c???u ph??t tri???n kinh t??? c???a ?????t n?????c.",
                        hinhanh="https://res.cloudinary.com/dfzvtpwsd/image/upload/v1669997776/T%C6%B0_v%E1%BA%A5n_ajewn9.jpg")
        c2 = HangMayBay(ten='Bamboo Airwayss',
                        gioithieu="L?? h??ng h??ng kh??ng t?? nh??n ?????u ti??n t???i Vi???t Nam xa??c ??i??nh theo ??u????i mu??c ti??u cung c????p di??ch vu?? ha??ng kh??ng ??i??nh h??????ng chu????n qu????c t????. Tr??n h??nh tr??nh s???i c??nh v????n xa, chi???n l?????c c???t l??i c???a Bamboo Airways l?? k???t n???i c??c v??ng ?????t ti???m n??ng, g??p ph???n qu???ng b?? s??u r???ng v?? hi???u qu??? gi?? tr??? t???t ?????p c???a v??n ho??, con ng?????i Vi???t Nam t???i b???n b?? th??? gi???i.",
                        hinhanh="https://res.cloudinary.com/dfzvtpwsd/image/upload/v1669997776/Bamboo_Airways_khai_th%C3%A1c_an_to%C3%A0n_1_000_chuy%E1%BA%BFn_bay_trong_5_tu%E1%BA%A7n_t%C3%ADnh_t%C4%83ng_l%C3%AAn_100_chuy%E1%BA%BFn_ng%C3%A0y_a0ifja.jpg")
        c3 = HangMayBay(ten='Vietjet Air',
                        gioithieu="L?? h??ng h??ng kh??ng ?????u ti??n t???i Vi???t Nam v???n h??nh theo m?? h??nh h??ng kh??ng th??? h??? m???i, chi ph?? th???p v?? cung c???p ??a d???ng c??c d???ch v??? cho kh??ch h??ng l???a ch???n. H??ng kh??ng ch??? v???n chuy???n h??ng kh??ng m?? c??n cung c???p c??c nhu c???u ti??u d??ng h??ng ho?? v?? d???ch v??? cho kh??ch h??ng th??ng qua c??c ???ng d???ng c??ng ngh??? th????ng m???i ??i???n t??? ti??n ti???n.",
                        hinhanh="https://res.cloudinary.com/dfzvtpwsd/image/upload/v1669997775/Airbus_A321XLR_pour_VietJet_A350-900_pour_South_African_Airways___Air_Journal_cblehe.jpg")
        c4 = HangMayBay(ten='Pacific Airlines',
                        gioithieu="H??ng h??ng kh??ng Pacific Airlines ???????c bi???t t???i l?? h??ng h??ng kh??ng ??i ti??n phong trong m???ng v?? m??y bay gi?? r??? t???i Vi???t Nam. M???c ti??u ho???t ?????ng l?? ??em ?????n nh???ng t???m v?? m??y bay gi?? r??? t???i t???n tay ng?????i ti??u dung h??ng ng??y. C?? th??? n??i Pacific Airlines L?? m???t b?????c ngo???c l???n trong ng??nh h??ng kh??ng v???n chuy???n v?? trong th???i ?????i kinh t??? th??? tr?????ng ?????y bi???n ?????ng hi???n nay.",
                        hinhanh="https://res.cloudinary.com/dfzvtpwsd/image/upload/v1669998060/Web_maybay_zikhqo.jpg")
        c5 = HangMayBay(ten='Jetstar',
                        gioithieu="C?? th???, b???n bi???t ?????n ch??ng t??i nh?? h??ng h??ng kh??ng n???i ti???ng v??? cung c???p gi?? v?? r???. Nh??ng b???n c?? bi???t r???ng m???i tu???n ch??ng t??i th???c hi???n h??n 5,000 chuy???n bay ?????n h??n 85 ??i???m ?????n hay ch??ng t??i ???? gi??p quy??n g??p ???????c h??n 10 tri???u ???? la ??c. B???n c?? th??? theo c??c li??n k???t t???i ????y ????? t??m hi???u tri???t l?? kinh doanh c???a ch??ng t??i, v??? ?????i bay ?????y ???n t?????ng c???a ch??ng t??i v?? c??c c?? h???i ????? B???N c?? th??? ?????n v???i Jetstar.",
                        hinhanh="https://res.cloudinary.com/dfzvtpwsd/image/upload/v1669998050/a321_neo_ugtnjh.jpg")
        db.session.add_all([c1, c2, c3, c4, c5])
        db.session.commit()

        v1 = HangVe(ten='H???ng 1')
        v2 = HangVe(ten='H???ng 2')
        db.session.add_all([v1, v2])
        db.session.commit()

        import hashlib

        password = str(hashlib.md5('123'.encode('utf-8')).hexdigest())
        u1 = NguoiDung(ten='Hoang', taikhoan='admin', matkhau=password, loainguoidung=UserRole.ADMIN,
                       anhdaidien='https://res.cloudinary.com/dfzvtpwsd/image/upload/v1670221889/2_pzciij.png')
        u2 = NguoiDung(ten='Duc', taikhoan='staff', matkhau=password, loainguoidung=UserRole.STAFF,
                       anhdaidien='https://res.cloudinary.com/dfzvtpwsd/image/upload/v1670221889/3_gpownw.png')
        u3 = NguoiDung(ten='Du', taikhoan='user', matkhau=password, loainguoidung=UserRole.USER,
                       anhdaidien='https://res.cloudinary.com/dfzvtpwsd/image/upload/v1670221889/1_beeily.png')
        db.session.add_all([u1, u2, u3])
        db.session.commit()

        s1 = SanBay(ten='Bu??n M?? Thu???t')
        s2 = SanBay(ten='H??? Ch?? Minh')
        s3 = SanBay(ten='H?? N???i')
        s4 = SanBay(ten='Vinh')
        s5 = SanBay(ten='Nha Trang')
        s6 = SanBay(ten='V??ng T??u')
        s7 = SanBay(ten='Hu???')
        s8 = SanBay(ten='H???i Ph??ng')
        s9 = SanBay(ten='C???n Th??')
        s10 = SanBay(ten='???? N???ng')
        db.session.add_all([s1, s2, s3, s4, s5, s6, s7, s8, s9, s10])
        db.session.commit()

        t1 = TuyenBay(ten="Tuy???n 1", sanbaydi_ma=1, sanbayden_ma=2)
        t2 = TuyenBay(ten="Tuy???n 2", sanbaydi_ma=2, sanbayden_ma=3)
        t3 = TuyenBay(ten="Tuy???n 3", sanbaydi_ma=3, sanbayden_ma=4)
        t4 = TuyenBay(ten="Tuy???n 4", sanbaydi_ma=4, sanbayden_ma=5)
        t5 = TuyenBay(ten="Tuy???n 5", sanbaydi_ma=5, sanbayden_ma=6)
        db.session.add_all([t1, t2, t3, t4, t5])
        db.session.commit()

        c1 = ChuyenBay(giodi=datetime.strptime('12/19/22 13:55:00', '%m/%d/%y %H:%M:%S'), thoigianbay=30,
                       hangmaybay_ma=1, tuyenbay_ma=1)
        c2 = ChuyenBay(giodi=datetime.strptime('12/20/22 7:00:00', '%m/%d/%y %H:%M:%S'), thoigianbay=180,
                       hangmaybay_ma=2, tuyenbay_ma=2)
        c3 = ChuyenBay(giodi=datetime.strptime('12/20/22 9:35:00', '%m/%d/%y %H:%M:%S'), thoigianbay=70,
                       hangmaybay_ma=3, tuyenbay_ma=3)
        c4 = ChuyenBay(giodi=datetime.strptime('12/29/22 6:55:00', '%m/%d/%y %H:%M:%S'), thoigianbay=90,
                       hangmaybay_ma=4, tuyenbay_ma=4)
        c5 = ChuyenBay(giodi=datetime.strptime('12/25/22 19:55:00', '%m/%d/%y %H:%M:%S'), thoigianbay=120,
                       hangmaybay_ma=5, tuyenbay_ma=5)
        c6 = ChuyenBay(giodi=datetime.strptime('1/19/23 13:55:00', '%m/%d/%y %H:%M:%S'), thoigianbay=90,
                       hangmaybay_ma=3, tuyenbay_ma=1)
        c7 = ChuyenBay(giodi=datetime.strptime('12/20/22 7:00:00', '%m/%d/%y %H:%M:%S'), thoigianbay=180,
                       hangmaybay_ma=5, tuyenbay_ma=2)
        c8 = ChuyenBay(giodi=datetime.strptime('12/20/22 9:35:00', '%m/%d/%y %H:%M:%S'), thoigianbay=70,
                       hangmaybay_ma=1, tuyenbay_ma=1)
        c9 = ChuyenBay(giodi=datetime.strptime('12/29/22 6:55:00', '%m/%d/%y %H:%M:%S'), thoigianbay=90,
                       hangmaybay_ma=4, tuyenbay_ma=4)
        c10 = ChuyenBay(giodi=datetime.strptime('12/25/22 19:55:00', '%m/%d/%y %H:%M:%S'), thoigianbay=120,
                        hangmaybay_ma=2, tuyenbay_ma=3)
        db.session.add_all([c1, c2, c3, c4, c5, c6, c7, c8, c9, c10])
        db.session.commit()

        sd1 = SanBayDung(sanbay_ma=3, thoigiandung=22, chuyenbay_ma=1)
        sd2 = SanBayDung(sanbay_ma=1, thoigiandung=22, chuyenbay_ma=2)
        sd3 = SanBayDung(sanbay_ma=7, thoigiandung=26, chuyenbay_ma=2)
        sd4 = SanBayDung(sanbay_ma=9, thoigiandung=20, chuyenbay_ma=3)
        sd5 = SanBayDung(sanbay_ma=8, thoigiandung=30, chuyenbay_ma=4)
        db.session.add_all([sd1, sd2, sd3, sd4, sd5])
        db.session.commit()

        b1 = BangDonGia(hangve_ma=1, chuyenbay_ma=1, gia=1000000, soghe=20)
        b2 = BangDonGia(hangve_ma=2, chuyenbay_ma=1, gia=900000, soghe=15)
        b3 = BangDonGia(hangve_ma=1, chuyenbay_ma=2, gia=800000, soghe=50)
        b4 = BangDonGia(hangve_ma=1, chuyenbay_ma=3, gia=1300000, soghe=30)
        b5 = BangDonGia(hangve_ma=2, chuyenbay_ma=3, gia=1000000, soghe=20)
        b6 = BangDonGia(hangve_ma=1, chuyenbay_ma=4, gia=1000000, soghe=35)
        b7 = BangDonGia(hangve_ma=2, chuyenbay_ma=4, gia=1500000, soghe=10)
        b8 = BangDonGia(hangve_ma=1, chuyenbay_ma=5, gia=1000000, soghe=40)
        b9 = BangDonGia(hangve_ma=1, chuyenbay_ma=6, gia=1300000, soghe=30)
        b10 = BangDonGia(hangve_ma=2, chuyenbay_ma=7, gia=1000000, soghe=20)
        b11 = BangDonGia(hangve_ma=1, chuyenbay_ma=8, gia=1000000, soghe=35)
        b12 = BangDonGia(hangve_ma=2, chuyenbay_ma=9, gia=7500000, soghe=10)
        b13 = BangDonGia(hangve_ma=1, chuyenbay_ma=10, gia=1000000, soghe=40)
        db.session.add_all([b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13])
        db.session.commit()
