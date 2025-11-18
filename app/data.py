from flask import Flask, render_template_string
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def load_dataframe():
    """Load gs.us.txt and display as an HTML dataframe"""
    # Get the parent directory path
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(parent_dir, 'gs.us.txt')
    
    # Load the CSV file into a pandas dataframe
    df = pd.read_csv(file_path)
    
    # Convert dataframe to HTML table
    html_table = df.to_html(classes='table table-striped', index=False)
    
    # Create a simple HTML template
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>GS Stock Data</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/css/bootstrap.min.css">
        <style>
            body {{ padding: 20px; }}
            .container {{ max-width: 1200px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Goldman Sachs (GS) Stock Data</h1>
            <p>Historical stock data from {df['Date'].iloc[0]} to {df['Date'].iloc[-1]}</p>
            <p>Total records: {len(df)}</p>
            {html_table}
        </div>
    </body>
    </html>
    """
    
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(debug=True)
