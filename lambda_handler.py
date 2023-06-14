import html
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import boto3


def lambda_handler(event, context):
    dashboard_name = 'aws-cloudwatch-dashboard-name'
    dashboard_body = get_dashboard_body(dashboard_name)
    email_body = get_html_body(dashboard_body)
    send_email_using_smtp_server(email_body)


def get_dashboard_body(dashboard_name):
    cw = boto3.client('cloudwatch')
    response = cw.get_dashboard(DashboardName=dashboard_name)
    dashboard_body = response['DashboardBody']
    return dashboard_body


def get_html_body(dashboard_source):
    dashboard_source_widgets = dashboard_source['widgets']
    markdowns = ['BATCH DETAILS', 'Database Refresh Status', 'Azure pipeline Run Staus', 'FSX Check',
                 'PROD Daily Billed Amount', 'PROD Cube Upload Task Status', 'DEV Daily Billed Amount']  #Replace with all the markdown values
# update / delete the following lists depending on the requirements, it highlights the following words with different color-bg
    succcess = ['success', 'online', 'pass', 'succeeded']
    failures = ['fail', 'error', 'offline', 'failed']
    warnings = ['partiallysucceeded', 'warning', 'caching']
    html = ""
    for ith_markdown in range(len(dashboard_source_widgets)):
        is_header = 0
        markdown = dashboard_source_widgets[ith_markdown]['properties']['markdown']
        markdown = f"""{markdown}"""
        border = 2
        html = html + f"<table border={border} style='background-color:#FFFFE0'>"
        for line in markdown.splitlines(True):
            line = line.lstrip()
            if line.startswith('#'):
                line = (line[2:])
            line = line.lstrip()
            line = line.rstrip()
            if line in markdowns:
                line = line + " :"
                html += f"<h4 style='width:100%, marginLeft:12%'>{line}</h4>"
                is_header = 1
            else:
                for n in line.split('|'):
                    if n != '|' and not n.startswith('--') and n != "":
                        if is_header == 0:
                            if n.lower() in succcess:
                                html += f"<td style='background-color:#3BEC18'>{n}</td>"
                            elif n.lower() in failures:
                                html += f"<td style='background-color:red'>{n}</td>"
                            elif n.lower() in warnings:
                                html += f"<td style='background-color:yellow'>{n}</td>"
                            else:
                                html += f"<td style=''>{n}</td>"
                        elif is_header == 1:
                            html += f"<th style='width:20%'>{n}</th>"
                is_header = 0
            html += "<tr>"
        html += "</table>"
    return html


def send_email_using_smtp_server(email_body):
    msg = MIMEMultipart()
    # update the following fields with the smtp_server, port, username and password, and also update the from and to email addresses.
    smtp_server = ""
    smtp_port = ""
    smtp_user = os.environ.get("smtp_user")   #username and password should be stored in env, as per the best practice.
    smtp_password = os.environ.get("smtp_password")
    msg["From"] = "abc@xyz.com"
    msg["To"] = "xyz@abc.com"
#     msg["Cc"] = ""
#     msg["Bcc"] = ""
    msg["Subject"] = "Email Subject Headline"
    html_msg = html_un_escape(email_body)
    msg_text = MIMEText(html_msg, "html")
    msg.attach(msg_text)
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo()
        server.starttls()
        server.login(smtp_user, smtp_password)  # can comment this line, if using the in-house smtp server
        server.send_message(msg)


def html_un_escape(text):
    return html.unescape(text)
