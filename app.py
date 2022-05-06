from flask import Flask, render_template, request, flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "Secret Key"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql+pymysql://DevLogMaterialInventory_u01:.eL=vW/M::2Oqw5@devux-db.sin.infineon.com:3306/DevLogMaterialInventory'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Main page of glue
class GlueType(db.Model):
    __tablename__ = 'glue_types'

    glue_type_id = db.Column(db.Integer, primary_key=True)
    glue_name = db.Column(db.String(100))
    supplier = db.Column(db.String(100))
    storage_temp = db.Column(db.String(100))
    freezer_no = db.Column(db.String(100))
    syringe_volume = db.Column(db.String(100))
    weight = db.Column(db.String(100))

    glue_description = db.relationship("GlueDescription", cascade="all, delete-orphan")

    def __init__(self, glue_name, supplier, storage_temp, freezer_no, syringe_volume, weight):
        self.glue_name = glue_name
        self.supplier = supplier
        self.storage_temp = storage_temp
        self.freezer_no = freezer_no
        self.syringe_volume = syringe_volume
        self.weight = weight


# factors to classify the glue
class GlueDescription(db.Model):
    __tablename__ = 'glue_descriptions'

    glue_description_id = db.Column(db.Integer, primary_key=True)
    lot_no = db.Column(db.String(100))
    received_date = db.Column(db.String(100))
    expiry_date = db.Column(db.String(100))
    project_leader = db.Column(db.String(100))
    incoming_qty = db.Column(db.String(100))
    withdraw_date = db.Column(db.String(100))
    withdraw_qty = db.Column(db.String(100))
    withdraw_by = db.Column(db.String(100))
    withdraw_purpose = db.Column(db.String(100))
    balance = db.Column(db.String(100))
    trans_type = db.Column(db.String(100))
    release_status = db.Column(db.String(100))
    expiry_status = db.Column(db.String(100))
    created_time = db.Column(db.DateTime, server_default=db.func.now())
    glue_type_id = db.Column(db.Integer, db.ForeignKey('glue_types.glue_type_id'))

    glue_type = db.relationship("GlueType", backref='glue_type')

    def __init__(self, lot_no, received_date, expiry_date, project_leader, incoming_qty, withdraw_date, withdraw_qty,
                 withdraw_by, withdraw_purpose, balance, trans_type, release_status, expiry_status, created_time,
                 glue_type_id):
        self.lot_no = lot_no
        self.received_date = received_date
        self.expiry_date = expiry_date
        self.project_leader = project_leader
        self.incoming_qty = incoming_qty
        self.withdraw_date = withdraw_date
        self.withdraw_qty = withdraw_qty
        self.withdraw_by = withdraw_by
        self.withdraw_purpose = withdraw_purpose
        self.balance = balance
        self.trans_type = trans_type
        self.release_status = release_status
        self.expiry_status = expiry_status
        self.created_time = created_time
        self.glue_type_id = glue_type_id


# Main page of lead frame
class LeadType(db.Model):
    __tablename__ = 'lead_types'

    lead_type_id = db.Column(db.Integer, primary_key=True)
    lead_no = db.Column(db.String(100))
    supplier = db.Column(db.String(100))
    package_no = db.Column(db.String(100))
    title = db.Column(db.String(100))


    lead_description = db.relationship("LeadDescription", cascade="all, delete-orphan")

    def __init__(self, lead_no, supplier, package_no, title):
        self.lead_no = lead_no
        self.supplier = supplier
        self.package_no = package_no
        self.title = title



# factors to classify the lead
class LeadDescription(db.Model):
    __tablename__ = 'lead_descriptions'

    lead_description_id = db.Column(db.Integer, primary_key=True)
    lot_no = db.Column(db.String(100))
    row_location = db.Column(db.String(100))
    received_date = db.Column(db.String(100))
    expiry_date = db.Column(db.String(100))
    manufacturing_date = db.Column(db.String(100))
    project_leader = db.Column(db.String(100))
    record_reff = db.Column(db.String(100))
    invoice_no = db.Column(db.String(100))
    purchasing_order = db.Column(db.String(100))
    incoming_qty = db.Column(db.String(100))
    withdraw_date = db.Column(db.String(100))
    withdraw_qty = db.Column(db.String(100))
    withdraw_by = db.Column(db.String(100))
    withdraw_purpose = db.Column(db.String(100))
    balance = db.Column(db.String(100))
    trans_type = db.Column(db.String(100))
    release_status = db.Column(db.String(100))
    expiry_status = db.Column(db.String(100))
    created_time = db.Column(db.DateTime, server_default=db.func.now())
    lead_type_id = db.Column(db.Integer, db.ForeignKey('lead_types.lead_type_id'))

    lead_type = db.relationship("LeadType", backref='lead_type')

    def __init__(self, lot_no, row_location, received_date, expiry_date, manufacturing_date, project_leader, record_reff, invoice_no, purchasing_order, incoming_qty, withdraw_date, withdraw_qty,
                 withdraw_by, withdraw_purpose, balance, trans_type, release_status, expiry_status, created_time,
                 lead_type_id):
        self.lot_no = lot_no
        self.row_location = row_location
        self.received_date = received_date
        self.expiry_date = expiry_date
        self.manufacturing_date = manufacturing_date
        self.project_leader = project_leader
        self.record_reff = record_reff
        self.invoice_no = invoice_no
        self.purchasing_order = purchasing_order
        self.incoming_qty = incoming_qty
        self.withdraw_date = withdraw_date
        self.withdraw_qty = withdraw_qty
        self.withdraw_by = withdraw_by
        self.withdraw_purpose = withdraw_purpose
        self.balance = balance
        self.trans_type = trans_type
        self.release_status = release_status
        self.expiry_status = expiry_status
        self.created_time = created_time
        self.lead_type_id = lead_type_id


class MoldType(db.Model):
    __tablename__ = 'mold_types'

    mold_type_id = db.Column(db.Integer, primary_key=True)
    mold_name = db.Column(db.String(100))
    supplier = db.Column(db.String(100))
    pellet_size = db.Column(db.String(100))
    part_no = db.Column(db.String(100))

    mold_description = db.relationship("MoldDescription", cascade="all, delete-orphan")

    def __init__(self, mold_name, supplier, pellet_size, part_no):
        self.mold_name = mold_name
        self.supplier = supplier
        self.pellet_size = pellet_size
        self.part_no = part_no


class MoldDescription(db.Model):
    __tablename__ = 'mold_descriptions'

    mold_description_id = db.Column(db.Integer, primary_key=True)
    lot_no = db.Column(db.String(100))
    received_date = db.Column(db.String(100))
    expiry_date = db.Column(db.String(100))
    manufacturing_date= db.Column(db.String(100))
    project_leader = db.Column(db.String(100))
    incoming_qty = db.Column(db.String(100))
    withdraw_date = db.Column(db.String(100))
    withdraw_qty = db.Column(db.String(100))
    withdraw_by = db.Column(db.String(100))
    withdraw_purpose = db.Column(db.String(100))
    balance = db.Column(db.String(100))
    trans_type = db.Column(db.String(100))
    release_status = db.Column(db.String(100))
    expiry_status = db.Column(db.String(100))
    created_time = db.Column(db.DateTime, server_default=db.func.now())
    mold_type_id = db.Column(db.Integer, db.ForeignKey('mold_types.mold_type_id'))

    mold_type = db.relationship("MoldType", backref='mold_type')

    def __init__(self, lot_no, received_date, expiry_date, manufacturing_date, project_leader, incoming_qty, withdraw_date, withdraw_qty,
                 withdraw_by, withdraw_purpose, balance, trans_type, release_status, expiry_status, created_time,
                 mold_type_id):
        self.lot_no = lot_no
        self.received_date = received_date
        self.expiry_date = expiry_date
        self.manufacturing_date = manufacturing_date
        self.project_leader = project_leader
        self.incoming_qty = incoming_qty
        self.withdraw_date = withdraw_date
        self.withdraw_qty = withdraw_qty
        self.withdraw_by = withdraw_by
        self.withdraw_purpose = withdraw_purpose
        self.balance = balance
        self.trans_type = trans_type
        self.release_status = release_status
        self.expiry_status = expiry_status
        self.created_time = created_time
        self.mold_type_id = mold_type_id


class EditHistory(db.Model):
    history_id = db.Column(db.Integer, primary_key=True)
    edit_type = db.Column(db.String(100))
    edit_material = db.Column(db.String(100))
    edit_page = db.Column(db.String(100))
    old_content = db.Column(db.String(200))
    new_content = db.Column(db.String(200))
    changed_by = db.Column(db.String(100))
    changed_time = db.Column(db.String(100))


db.create_all()
db.session.commit()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/history")
def show_history():
    all_history = EditHistory.query.order_by(EditHistory.changed_time.desc()).all()
    return render_template("history.html", histories=all_history)


@app.route("/glue")
def show_glue():
    all_glue = db.session.query(GlueType, GlueDescription).join(GlueDescription).all()
    return render_template("glue.html", glues=all_glue)



@app.route("/lead")
def show_lead():
    all_lead = db.session.query(LeadType, LeadDescription).join(LeadDescription).all()
    return render_template("lead.html", leads=all_lead)



@app.route("/mold")
def show_mold():
    all_mold = db.session.query(MoldType, MoldDescription).join(MoldDescription).all()
    return render_template("mold.html", molds=all_mold)



# Server configurations - REM CHANGE
# app.run(debug=True, host="api.ap-sg-1.icp.infineon.com", port=6443)
if __name__ == "__main__":
        app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)

