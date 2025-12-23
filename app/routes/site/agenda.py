# Agenda Routes
from flask import render_template
from app.models.models import Agenda
# from app.routes.public import public_bp
from app.routes.site import site_bp as public_bp


@public_bp.route('/agenda')
def agenda():
    """School agenda/events page."""
    agenda_list = Agenda.query.order_by(Agenda.tanggal.desc()).all()
    return render_template('agenda.html', 
                           title='Agenda Sekolah',
                           agenda_list=agenda_list)
