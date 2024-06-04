from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators

class CreateVoucherForm(Form):
    voucher = StringField('Voucher', [validators.Length(min=1, max=150), validators.DataRequired()])
    detail = TextAreaField('Detail', [validators.Optional()])
    value = StringField('Value', [validators.Length(min=1, max=150), validators.DataRequired()])
    Price = StringField('Price in Points', [validators.Length(min=1, max=150), validators.DataRequired()])
