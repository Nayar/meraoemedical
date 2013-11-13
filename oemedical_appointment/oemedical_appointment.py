# -*- coding: utf-8 -*-
#/#############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2004-TODAY Tech-Receptives(<http://www.techreceptives.com>)
#    Special Credit and Thanks to Thymbra Latinoamericana S.A.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#/#############################################################################
from osv import osv
from osv import fields

import psycopg2
import random

def presentDocs():
    con = None;
    distinctUsers = []
    try:
        con = psycopg2.connect(database = 'nayahospital', user = 'postgres', host = '192.168.56.101', password = 'lol')
        cur = con.cursor()
        cur.execute("""
					select oemedical_physician.id 
					from oemedical_physician
					INNER JOIN hr_employee
					ON hr_employee.name_related = oemedical_physician.name
					INNER JOIN hr_attendance
					on hr_attendance.employee_id = hr_employee.id
					WHERE hr_attendance.action = 'sign_in'
					EXCEPT ALL
					select oemedical_physician.id
					from oemedical_physician
					INNER JOIN hr_employee
					ON hr_employee.name_related = oemedical_physician.name
					INNER JOIN hr_attendance
					on hr_attendance.employee_id = hr_employee.id
					WHERE hr_attendance.action = 'sign_out'""")
        rows = cur.fetchall()
        for row in rows:
			return rows[0]
    except psycopg2.DatabaseError, e:
        print e
    finally:
        if con:
            con.close()
    if len(distinctUsers) == 0:
        return False
    else:
        ans = random.randint(0,len(distinctUsers)-1)
        return distinctUsers[ans]

class OeMedicalAppointment(osv.Model):
	
    def autoApp(self,cr,uid,ids,appointment_type,context=None):
		if appointment_type:
			
			x=appointment_type
			if x == "newcase":
				
				return {'value':{'doctor': presentDocs()}}
		
		return {'value':{'doctor':''}}
		
    
  
  
    _name = 'oemedical.appointment'

    _columns = {
        'consultations': fields.many2one('product.product',
                                         string='Consultation Services',
                                          help='Consultation Services'),
        'patient_id': fields.many2one('oemedical.patient', string='Patient',
                                   required=True, select=True,
                                   help='Patient Name'),
        'name': fields.char(size=256, string='Appointment ID', readonly=True),
        'appointment_date': fields.datetime(string='Date and Time'),
        'duration': fields.float('Duration'),
        'doctor': fields.many2one('oemedical.physician',
                                  string='Physician',select=True, 
                                  help='Physician\'s Name'),
        'comments': fields.text(string='Comments'),
        'appointment_type': fields.selection([('newcase', 'New Case'),
											 ('ontreatment', 'On Treatment')], 
											 string='Type'),
        'institution': fields.many2one('res.partner',
                                       string='Health Center',
                                       help='Medical Center'),
        'urgency': fields.selection([
            ('a', 'Normal'),
            ('b', 'Emergency'), ],
            string='Urgency Level'),
        'speciality': fields.many2one('oemedical.specialty',
                                      string='Specialty', 
                                      help='Medical Specialty / Sector'),
    }
    
    _defaults = {
         'name': lambda obj, cr, uid, context: 
            obj.pool.get('ir.sequence').get(cr, uid, 'oemedical.appointment'),
		}

OeMedicalAppointment()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

"""'doctor': fields.many2one('oemedical.physician',
                                  string='Physician',select=True, 
                                  help='Physician\'s Name'),"""
