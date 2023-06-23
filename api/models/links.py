from ..extensions import db
from datetime import datetime
from io import BytesIO
import random
import string as str
import qrcode


# --------------------------
def generate_current_date():
    current_date = f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year}"
    return current_date


# ----------------------------------
class Link(db.Model):
    __tablename__ = "urls"

    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(512), nullable=False)
    short_url = db.Column(db.String(7), nullable=False, unique=True)
    custom_url = db.Column(db.String(50), unique=True)
    visit = db.Column(db.Integer, default=0)
    qr_code = db.Column(db.LargeBinary, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.String(20), default=generate_current_date())

    # ----------------------------------------
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.short_url = self.shorten_url()
        # self.qr_code = self.generate_qr_code()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # ------------------------------------------
    def shorten_url(self):
        characters = str.digits + str.ascii_letters
        short_url = "".join(random.choices(characters, k=7))
        url_link = self.query.filter_by(short_url=short_url).first()
        if url_link:
            return self.shorten_url()
        return short_url

    # -----------------------------------------------------
    # def generate_qr_code(self):
    #     qr = qrcode.QRCode(version=1, box_size=10, border=5)
    #     qr.add_data(self.short_url)
    #     qr.make(fit=True)
    #     img = qr.make_image(fill="black", back_color="white")
    #     buffer = BytesIO()
    #     img.save(buffer, format="JPEG")
    #     buffer.seek(0)
    #     # getting the value of the buffer as bytes
    #     qr_code = buffer.getvalue()
    #     return qr_code


# --------------------------------------------------