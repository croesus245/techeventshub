from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import os
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect 


load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
csrf = CSRFProtect(app)


db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME', 'techeventshub')
}


@app.route('/')
def index():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

      
        search = request.args.get('search')
        college = request.args.get('college')  
        event_type = request.args.get('type')
        page = request.args.get('page', 1, type=int)
        per_page = 9

        base_query = "FROM events WHERE 1=1"
        params = []

        
        if search:
            base_query += " AND (name LIKE %s OR description LIKE %s)"
            params.extend([f"%{search}%", f"%{search}%"])
            
        if college:  
            base_query += " AND college_name LIKE %s"
            params.append(f"%{college}%")

        if event_type:
            base_query += " AND event_type = %s"
            params.append(event_type)

       
        count_query = f"SELECT COUNT(*) {base_query}"
        cursor.execute(count_query, params)
        total = cursor.fetchone()['COUNT(*)']

        
        data_query = f"SELECT * {base_query} ORDER BY date ASC LIMIT %s OFFSET %s"
        params.extend([per_page, (page - 1) * per_page])
        cursor.execute(data_query, params)
        events = cursor.fetchall()

        return render_template('index.html',
            events=events,
            pagination={
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total // per_page) + (1 if total % per_page else 0)
            }
        )

    except Exception as e:
        flash(f'Database error: {str(e)}', 'danger')
        return render_template('index.html', events=[])
    finally:
        cursor.close()
        connection.close()

@app.route('/submit', methods=['GET', 'POST'])
def submit_event():
    if request.method == 'POST':
        try:
            event_data = {
                'name': request.form['name'],
                'description': request.form['description'],
                'date': request.form['date'],
                'location': request.form['location'],
                'event_type': request.form['event_type'],
                'college_name': request.form['college_name'],
                'registration_link': request.form['registration_link']
            }

            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO events 
                (name, description, date, location, event_type, college_name, registration_link)
                VALUES (%(name)s, %(description)s, %(date)s, %(location)s, %(event_type)s, %(college_name)s, %(registration_link)s)
            """, event_data)
            connection.commit()
            flash('Event submitted successfully!', 'success')
            return redirect(url_for('index'))

        except Exception as e:
            flash(f'Submission failed: {str(e)}', 'danger')
            return redirect(url_for('submit_event'))
        finally:
            cursor.close()
            connection.close()

    return render_template('submit.html')

@app.route('/event/<int:event_id>')
def event_detail(event_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM events WHERE id = %s", (event_id,))
        event = cursor.fetchone()
        return render_template('detail.html', event=event)
    except Exception as e:
        flash('Event not found', 'danger')
        return redirect(url_for('index'))
    finally:
        cursor.close()
        connection.close()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)