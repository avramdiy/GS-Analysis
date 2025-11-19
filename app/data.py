from flask import Flask, render_template_string
import pandas as pd
import os
import matplotlib.pyplot as plt
import io
import base64

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

@app.route('/volume-analysis')
def volume_analysis():
    """Visualize average yearly volume for all three periods as a bar chart"""
    df, df_pre_crisis, df_crisis_recovery, df_post_recovery = load_and_process_data()
    
    # Calculate average yearly volume for each period
    def get_yearly_avg_volume(dataframe, period_name):
        """Calculate average volume by year"""
        dataframe['Year'] = dataframe['Date'].dt.year
        yearly_volume = dataframe.groupby('Year')['Volume'].mean()
        return yearly_volume
    
    yearly_pre_crisis = get_yearly_avg_volume(df_pre_crisis.copy(), 'Pre-2008')
    yearly_crisis_recovery = get_yearly_avg_volume(df_crisis_recovery.copy(), '2008-2012')
    yearly_post_recovery = get_yearly_avg_volume(df_post_recovery.copy(), '2013-2017')
    
    # Create bar chart
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle('Average Yearly Trading Volume by Period', fontsize=16, fontweight='bold')
    
    # Pre-2008 Crisis
    axes[0].bar(yearly_pre_crisis.index, yearly_pre_crisis.values, color='#2E86AB', alpha=0.8)
    axes[0].set_title('Pre-2008 Financial Crisis\n(1999-2007)', fontweight='bold')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Average Volume')
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].grid(axis='y', alpha=0.3)
    
    # Crisis & Recovery
    axes[1].bar(yearly_crisis_recovery.index, yearly_crisis_recovery.values, color='#A23B72', alpha=0.8)
    axes[1].set_title('Financial Crisis & Recovery\n(2008-2012)', fontweight='bold')
    axes[1].set_xlabel('Year')
    axes[1].set_ylabel('Average Volume')
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].grid(axis='y', alpha=0.3)
    
    # Post-Recovery Growth
    axes[2].bar(yearly_post_recovery.index, yearly_post_recovery.values, color='#F18F01', alpha=0.8)
    axes[2].set_title('Post-Recovery Growth\n(2013-2017)', fontweight='bold')
    axes[2].set_xlabel('Year')
    axes[2].set_ylabel('Average Volume')
    axes[2].tick_params(axis='x', rotation=45)
    axes[2].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    
    # Convert plot to base64 image
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=100, bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    # Create HTML template with chart
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>GS Volume Analysis</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/css/bootstrap.min.css">
        <style>
            body {{ padding: 20px; }}
            .container {{ max-width: 1400px; }}
            .chart-container {{ margin-top: 30px; text-align: center; }}
            img {{ max-width: 100%; height: auto; }}
            .nav-links {{ margin-bottom: 20px; }}
            a {{ margin-right: 15px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="nav-links">
                <a href="/" class="btn btn-primary btn-sm">View All Data</a>
                <a href="/volume-analysis" class="btn btn-info btn-sm">Volume Analysis</a>
            </div>
            
            <h1>Goldman Sachs (GS) - Average Yearly Trading Volume Analysis</h1>
            <p><strong>Analysis Period:</strong> 1999-2017</p>
            
            <div class="chart-container">
                <img src="data:image/png;base64,{plot_url}" alt="Average Yearly Volume Chart">
            </div>
            
            <div style="margin-top: 40px;">
                <h3>Period Summary</h3>
                <div class="row">
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Pre-2008 Crisis</h5>
                                <p class="card-text">Years: 1999-2007</p>
                                <p class="card-text"><strong>Avg Volume:</strong> {yearly_pre_crisis.mean():,.0f}</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Crisis & Recovery</h5>
                                <p class="card-text">Years: 2008-2012</p>
                                <p class="card-text"><strong>Avg Volume:</strong> {yearly_crisis_recovery.mean():,.0f}</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Post-Recovery Growth</h5>
                                <p class="card-text">Years: 2013-2017</p>
                                <p class="card-text"><strong>Avg Volume:</strong> {yearly_post_recovery.mean():,.0f}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    return render_template_string(html_template)

@app.route('/price-analysis')
def price_analysis():
    """Visualize yearly average open price for all three periods as a line chart"""
    df, df_pre_crisis, df_crisis_recovery, df_post_recovery = load_and_process_data()
    
    # Calculate average yearly open price for each period
    def get_yearly_avg_open_price(dataframe, period_name):
        """Calculate average open price by year"""
        dataframe['Year'] = dataframe['Date'].dt.year
        yearly_open_price = dataframe.groupby('Year')['Open'].mean()
        return yearly_open_price
    
    yearly_open_pre_crisis = get_yearly_avg_open_price(df_pre_crisis.copy(), 'Pre-2008')
    yearly_open_crisis_recovery = get_yearly_avg_open_price(df_crisis_recovery.copy(), '2008-2012')
    yearly_open_post_recovery = get_yearly_avg_open_price(df_post_recovery.copy(), '2013-2017')
    
    # Create line chart with all three periods on one plot for comparison
    fig, ax = plt.subplots(figsize=(14, 7))
    fig.suptitle('Yearly Average Opening Price Trends by Period', fontsize=16, fontweight='bold')
    
    # Plot lines for each period
    ax.plot(yearly_open_pre_crisis.index, yearly_open_pre_crisis.values, marker='o', 
            linewidth=2.5, markersize=8, label='Pre-2008 Crisis (1999-2007)', color='#2E86AB')
    ax.plot(yearly_open_crisis_recovery.index, yearly_open_crisis_recovery.values, marker='s', 
            linewidth=2.5, markersize=8, label='Crisis & Recovery (2008-2012)', color='#A23B72')
    ax.plot(yearly_open_post_recovery.index, yearly_open_post_recovery.values, marker='^', 
            linewidth=2.5, markersize=8, label='Post-Recovery Growth (2013-2017)', color='#F18F01')
    
    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_ylabel('Average Opening Price ($)', fontsize=12, fontweight='bold')
    ax.legend(loc='best', fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    
    # Convert plot to base64 image
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=100, bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    # Create HTML template with chart
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>GS Price Analysis</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/css/bootstrap.min.css">
        <style>
            body {{ padding: 20px; }}
            .container {{ max-width: 1400px; }}
            .chart-container {{ margin-top: 30px; text-align: center; }}
            img {{ max-width: 100%; height: auto; }}
            .nav-links {{ margin-bottom: 20px; }}
            a {{ margin-right: 15px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="nav-links">
                <a href="/" class="btn btn-primary btn-sm">View All Data</a>
                <a href="/volume-analysis" class="btn btn-info btn-sm">Volume Analysis</a>
                <a href="/price-analysis" class="btn btn-success btn-sm">Price Analysis</a>
            </div>
            
            <h1>Goldman Sachs (GS) - Yearly Average Opening Price Analysis</h1>
            <p><strong>Analysis Period:</strong> 1999-2017</p>
            
            <div class="chart-container">
                <img src="data:image/png;base64,{plot_url}" alt="Yearly Average Opening Price Chart">
            </div>
            
            <div style="margin-top: 40px;">
                <h3>Period Summary</h3>
                <div class="row">
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Pre-2008 Crisis</h5>
                                <p class="card-text">Years: 1999-2007</p>
                                <p class="card-text"><strong>Avg Open Price:</strong> ${yearly_open_pre_crisis.mean():.2f}</p>
                                <p class="card-text"><small>Range: ${yearly_open_pre_crisis.min():.2f} - ${yearly_open_pre_crisis.max():.2f}</small></p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Crisis & Recovery</h5>
                                <p class="card-text">Years: 2008-2012</p>
                                <p class="card-text"><strong>Avg Open Price:</strong> ${yearly_open_crisis_recovery.mean():.2f}</p>
                                <p class="card-text"><small>Range: ${yearly_open_crisis_recovery.min():.2f} - ${yearly_open_crisis_recovery.max():.2f}</small></p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Post-Recovery Growth</h5>
                                <p class="card-text">Years: 2013-2017</p>
                                <p class="card-text"><strong>Avg Open Price:</strong> ${yearly_open_post_recovery.mean():.2f}</p>
                                <p class="card-text"><small>Range: ${yearly_open_post_recovery.min():.2f} - ${yearly_open_post_recovery.max():.2f}</small></p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    return render_template_string(html_template)

@app.route('/close-analysis')
def close_analysis():
    """Visualize yearly average close price for all three periods as a line chart"""
    df, df_pre_crisis, df_crisis_recovery, df_post_recovery = load_and_process_data()
    
    # Calculate average yearly close price for each period
    def get_yearly_avg_close_price(dataframe, period_name):
        """Calculate average close price by year"""
        dataframe['Year'] = dataframe['Date'].dt.year
        yearly_close_price = dataframe.groupby('Year')['Close'].mean()
        return yearly_close_price
    
    yearly_close_pre_crisis = get_yearly_avg_close_price(df_pre_crisis.copy(), 'Pre-2008')
    yearly_close_crisis_recovery = get_yearly_avg_close_price(df_crisis_recovery.copy(), '2008-2012')
    yearly_close_post_recovery = get_yearly_avg_close_price(df_post_recovery.copy(), '2013-2017')
    
    # Create line chart with all three periods on one plot for comparison
    fig, ax = plt.subplots(figsize=(14, 7))
    fig.suptitle('Yearly Average Closing Price Trends by Period', fontsize=16, fontweight='bold')
    
    # Plot lines for each period
    ax.plot(yearly_close_pre_crisis.index, yearly_close_pre_crisis.values, marker='o', 
            linewidth=2.5, markersize=8, label='Pre-2008 Crisis (1999-2007)', color='#2E86AB')
    ax.plot(yearly_close_crisis_recovery.index, yearly_close_crisis_recovery.values, marker='s', 
            linewidth=2.5, markersize=8, label='Crisis & Recovery (2008-2012)', color='#A23B72')
    ax.plot(yearly_close_post_recovery.index, yearly_close_post_recovery.values, marker='^', 
            linewidth=2.5, markersize=8, label='Post-Recovery Growth (2013-2017)', color='#F18F01')
    
    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_ylabel('Average Closing Price ($)', fontsize=12, fontweight='bold')
    ax.legend(loc='best', fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    
    # Convert plot to base64 image
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=100, bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    # Create HTML template with chart
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>GS Close Price Analysis</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/css/bootstrap.min.css">
        <style>
            body {{ padding: 20px; }}
            .container {{ max-width: 1400px; }}
            .chart-container {{ margin-top: 30px; text-align: center; }}
            img {{ max-width: 100%; height: auto; }}
            .nav-links {{ margin-bottom: 20px; }}
            a {{ margin-right: 15px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="nav-links">
                <a href="/" class="btn btn-primary btn-sm">View All Data</a>
                <a href="/volume-analysis" class="btn btn-info btn-sm">Volume Analysis</a>
                <a href="/price-analysis" class="btn btn-success btn-sm">Price Analysis</a>
                <a href="/close-analysis" class="btn btn-warning btn-sm">Close Price Analysis</a>
            </div>
            
            <h1>Goldman Sachs (GS) - Yearly Average Closing Price Analysis</h1>
            <p><strong>Analysis Period:</strong> 1999-2017</p>
            
            <div class="chart-container">
                <img src="data:image/png;base64,{plot_url}" alt="Yearly Average Closing Price Chart">
            </div>
            
            <div style="margin-top: 40px;">
                <h3>Period Summary</h3>
                <div class="row">
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Pre-2008 Crisis</h5>
                                <p class="card-text">Years: 1999-2007</p>
                                <p class="card-text"><strong>Avg Close Price:</strong> ${yearly_close_pre_crisis.mean():.2f}</p>
                                <p class="card-text"><small>Range: ${yearly_close_pre_crisis.min():.2f} - ${yearly_close_pre_crisis.max():.2f}</small></p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Crisis & Recovery</h5>
                                <p class="card-text">Years: 2008-2012</p>
                                <p class="card-text"><strong>Avg Close Price:</strong> ${yearly_close_crisis_recovery.mean():.2f}</p>
                                <p class="card-text"><small>Range: ${yearly_close_crisis_recovery.min():.2f} - ${yearly_close_crisis_recovery.max():.2f}</small></p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Post-Recovery Growth</h5>
                                <p class="card-text">Years: 2013-2017</p>
                                <p class="card-text"><strong>Avg Close Price:</strong> ${yearly_close_post_recovery.mean():.2f}</p>
                                <p class="card-text"><small>Range: ${yearly_close_post_recovery.min():.2f} - ${yearly_close_post_recovery.max():.2f}</small></p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    return render_template_string(html_template)
    app.run(debug=True)
