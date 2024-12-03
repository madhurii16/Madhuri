from flask import Flask, render_template
from admin_dashboarddb import get_total_spots, get_total_e_waste, get_total_users, get_collection_spots, get_e_waste_items
app = Flask(__name__)
@app.route('/dashboard')
def admin_dashboard():
    total_spots = get_total_spots()
    total_e_waste = get_total_e_waste()
    total_users = get_total_users()
    collection_spots = get_collection_spots()
    e_waste_items = get_e_waste_items()
    
    return render_template('admin_dashboard.html', 
                           total_spots=total_spots, 
                           total_e_waste=total_e_waste, 
                           total_users=total_users,
                           collection_spots=collection_spots,
                           e_waste_items=e_waste_items)
