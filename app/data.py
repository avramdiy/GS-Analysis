from flask import Flask, render_template_string
import pandas as pd
import os

app = Flask(__name__)

def load_and_process_data():
    """Load gs.us.txt, drop OpenInt column, and create time-based dataframes"""
    # Get the parent directory path
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(parent_dir, 'gs.us.txt')
    
    # Load the CSV file into a pandas dataframe
    df = pd.read_csv(file_path)
    
    # Drop the OpenInt column
    df = df.drop('OpenInt', axis=1)
    
    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Create three dataframes based on time ranges:
    # 1. Pre-2008 Financial Crisis (1999-05-04 to 2007-12-31): Early growth period
    df_pre_crisis = df[df['Date'] < '2008-01-01'].copy()
    
    # 2. Financial Crisis & Recovery (2008-01-01 to 2012-12-31): Crisis and recovery period
    df_crisis_recovery = df[(df['Date'] >= '2008-01-01') & (df['Date'] < '2013-01-01')].copy()
    
    # 3. Post-Recovery Growth (2013-01-01 to 2017-11-10): Sustained growth period
    df_post_recovery = df[df['Date'] >= '2013-01-01'].copy()
    
    return df, df_pre_crisis, df_crisis_recovery, df_post_recovery

@app.route('/')
def load_dataframe():
    """Load gs.us.txt and display as an HTML dataframe"""
    df, df_pre_crisis, df_crisis_recovery, df_post_recovery = load_and_process_data()
    
    # Convert dataframes to HTML tables
    html_table = df.to_html(classes='table table-striped table-sm', index=False)
    html_pre_crisis = df_pre_crisis.to_html(classes='table table-striped table-sm', index=False)
    html_crisis_recovery = df_crisis_recovery.to_html(classes='table table-striped table-sm', index=False)
    html_post_recovery = df_post_recovery.to_html(classes='table table-striped table-sm', index=False)
    
    # Create a simple HTML template
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>GS Stock Data</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/css/bootstrap.min.css">
        <style>
            body {{ padding: 20px; }}
            .container {{ max-width: 1400px; }}
            .section {{ margin-top: 40px; }}
            h2 {{ margin-top: 30px; margin-bottom: 15px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Goldman Sachs (GS) Stock Data Analysis</h1>
            <p><strong>Date Range:</strong> {df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}</p>
            <p><strong>Total Records:</strong> {len(df)}</p>
            <p><em>OpenInt column removed for analysis focus</em></p>
            
            <div class="section">
                <h2>Complete Dataset</h2>
                <p>Records: {len(df)}</p>
                {html_table}
            </div>
            
            <div class="section">
                <h2>Period 1: Pre-2008 Financial Crisis (1999-05-04 to 2007-12-31)</h2>
                <p>Records: {len(df_pre_crisis)} | Early growth and market expansion period</p>
                {html_pre_crisis}
            </div>
            
            <div class="section">
                <h2>Period 2: Financial Crisis & Recovery (2008-01-01 to 2012-12-31)</h2>
                <p>Records: {len(df_crisis_recovery)} | Crisis impact and recovery period</p>
                {html_crisis_recovery}
            </div>
            
            <div class="section">
                <h2>Period 3: Post-Recovery Growth (2013-01-01 to 2017-11-10)</h2>
                <p>Records: {len(df_post_recovery)} | Sustained growth and market recovery</p>
                {html_post_recovery}
            </div>
        </div>
    </body>
    </html>
    """
    
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(debug=True)
