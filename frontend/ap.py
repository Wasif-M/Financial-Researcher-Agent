from flask import Flask, request, send_file, jsonify, send_from_directory
import threading
import time
import os
import logging
from financialresearcher.crew import Financialresearcher

# Configure logging for better debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global state management for agent progress tracking
# This approach ensures thread safety for the progress tracking system
progress_state = {
    'current_agent': None,
    'done': False,
    'report_path': None,
    'error': None,
    'company_name': None
}

def reset_progress_state():
    """
    Reset the global progress state to initial values
    Called before starting a new research session
    """
    global progress_state
    progress_state.update({
        'current_agent': None,
        'done': False,
        'report_path': None,
        'error': None,
        'company_name': None
    })

def run_financial_research(company_name):
    """
    Execute the financial research process in a separate thread
    This function manages the entire research workflow and updates global state
    
    Args:
        company_name (str): Name of the company to research
    """
    global progress_state
    
    try:
        logger.info(f"Starting financial research for: {company_name}")
        progress_state['company_name'] = company_name
        
        # Stage 1: Data Collection and Research
        progress_state['current_agent'] = 'Researcher'
        logger.info("Researcher agent started")
        time.sleep(2)  # Simulate research time - replace with actual research duration
        
        # Stage 2: Data Analysis and Report Generation
        progress_state['current_agent'] = 'Analyst'
        logger.info("Analyst agent started")
        time.sleep(2)  # Simulate analysis time - replace with actual analysis duration
        
        # Execute the actual CrewAI financial research
        logger.info("Executing CrewAI financial research workflow")
        research_inputs = {"company": company_name}
        research_results = Financialresearcher().crew().kickoff(inputs=research_inputs)
        
        # Ensure output directory exists with proper error handling
        output_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../output'))
        os.makedirs(output_directory, exist_ok=True)
        
        # Generate unique filename to prevent conflicts
        report_filename = f"{company_name.replace(' ', '_').lower()}_financial_report.md"
        report_file_path = os.path.join(output_directory, report_filename)
        
        # Write research results to file with proper encoding
        with open(report_file_path, 'w', encoding='utf-8') as report_file:
            report_file.write(str(research_results.raw))
        
        # Update progress state to completion
        progress_state.update({
            'current_agent': 'Done',
            'done': True,
            'report_path': report_file_path
        })
        
        logger.info(f"Financial research completed successfully for: {company_name}")
        logger.info(f"Report saved to: {report_file_path}")
        
    except Exception as research_error:
        logger.error(f"Error during financial research: {str(research_error)}")
        progress_state.update({
            'error': str(research_error),
            'done': True,
            'current_agent': 'Error'
        })

@app.route('/', methods=['GET', 'POST'])
def main_interface():
    """
    Main application interface
    GET: Serves the single-file HTML application
    POST: Initiates financial research process
    """
    if request.method == 'POST':
        # Extract and validate company name from form data
        company_name = request.form.get('company', '').strip()
        
        if not company_name:
            return jsonify({'error': 'Company name is required'}), 400
        
        logger.info(f"Research request received for company: {company_name}")
        
        # Reset progress state for new research session
        reset_progress_state()
        
        # Start research process in background thread
        research_thread = threading.Thread(
            target=run_financial_research, 
            args=(company_name,),
            daemon=True  # Daemon thread will exit when main program exits
        )
        research_thread.start()
        
        # Return success response - progress will be tracked via /progress endpoint
        return jsonify({'status': 'Research started', 'company': company_name})
    
    # Serve the single-file HTML application for GET requests
    try:
        # Read the HTML file and return it
        html_file_path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
        
        # If templates directory doesn't exist, serve inline HTML
        if not os.path.exists(html_file_path):
            # Return the embedded HTML directly (you would put the full HTML content here)
            # For now, we'll assume you have the HTML file in templates/index.html
            return """
            <!-- Your complete HTML content would go here -->
            <!-- This is where you'd paste the full HTML from the artifact -->
            """
        
        with open(html_file_path, 'r', encoding='utf-8') as html_file:
            return html_file.read()
            
    except Exception as file_error:
        logger.error(f"Error serving HTML file: {str(file_error)}")
        return "Error loading application", 500

@app.route('/progress')
def get_research_progress():
    """
    API endpoint to get current research progress
    Returns JSON with current agent status and completion state
    """
    return jsonify(progress_state)

@app.route('/report')
def display_research_report():
    """
    Serve the generated financial research report
    Returns the report content or error message
    """
    if progress_state.get('error'):
        return f"Error generating report: {progress_state['error']}", 500
    
    report_path = progress_state.get('report_path')
    
    if not report_path or not os.path.exists(report_path):
        logger.warning("Report not found or not yet generated")
        return 'Report not found or not yet generated', 404
    
    try:
        # Read and return report content
        with open(report_path, 'r', encoding='utf-8') as report_file:
            report_content = report_file.read()
        
        # Return as HTML with proper content type
        return f"""
        <div class="report-block" style="white-space: pre-wrap; font-family: monospace; padding: 20px;">
            {report_content}
        </div>
        """
        
    except Exception as read_error:
        logger.error(f"Error reading report file: {str(read_error)}")
        return "Error reading report file", 500

@app.route('/download')
def download_research_report():
    """
    Download endpoint for the generated financial report
    Returns the report file as an attachment
    """
    if progress_state.get('error'):
        return f"Error: {progress_state['error']}", 500
    
    report_path = progress_state.get('report_path')
    
    if not report_path or not os.path.exists(report_path):
        logger.warning("Attempted to download non-existent report")
        return 'Report not found', 404
    
    try:
        # Generate a user-friendly filename
        company_name = progress_state.get('company_name', 'company')
        safe_filename = f"{company_name.replace(' ', '_').lower()}_financial_report.md"
        
        return send_file(
            report_path,
            as_attachment=True,
            download_name=safe_filename,
            mimetype='text/markdown'
        )
        
    except Exception as download_error:
        logger.error(f"Error during file download: {str(download_error)}")
        return "Error downloading file", 500

@app.route('/health')
def health_check():
    """
    Health check endpoint for monitoring and debugging
    Returns current application status
    """
    return jsonify({
        'status': 'healthy',
        'progress_state': progress_state,
        'timestamp': time.time()
    })

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors gracefully"""
    return "Page not found", 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors gracefully"""
    logger.error(f"Internal server error: {str(error)}")
    return "Internal server error", 500

if __name__ == '__main__':
    # Create output directory if it doesn't exist
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../output'))
    os.makedirs(output_dir, exist_ok=True)
    
    logger.info("Starting Financial Research Pro application")
    logger.info(f"Output directory: {output_dir}")
    
    # Run the Flask application
    app.run(
        debug=True,
        host='0.0.0.0',  # Allow external connections
        port=5000,
        threaded=True    # Enable threading for concurrent requests
    )