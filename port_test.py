from flask import Flask, render_template, request
import socket
import subprocess
import dns.resolver  # Para resolver nomes DNS

app = Flask(__name__)

def is_port_open(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        result = sock.connect_ex((host, int(port)))
        return result == 0

def resolve_dns(name):
    try:
        result = dns.resolver.resolve(name, 'A')
        return [str(ip) for ip in result]
    except Exception as e:
        return None

def check_route(host, method):
    if method == "dig":
        try:
            result = subprocess.run(['dig', host], capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            return str(e)
    elif method == "tracert":
        try:
            result = subprocess.run(['traceroute', host], capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            return str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_ports():
    host = request.form['host']
    ports = request.form['ports'].split(',')
    dns_name = request.form.get('dns_name')
    route_method = request.form.get('route_check')

    results = []
    for port in ports:
        port = port.strip()
        is_open = is_port_open(host, port)
        results.append({'port': port, 'is_open': is_open})

    dns_resolution = None
    if dns_name:
        dns_resolution = resolve_dns(dns_name)

    route_result = check_route(host, route_method)

    return render_template(
        'result.html',
        host=host,
        results=results,
        dns_name=dns_name,
        dns_resolution=dns_resolution,
        route_method=route_method,
        route_result=route_result
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1000)
