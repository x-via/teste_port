from flask import Flask, render_template, request, redirect, url_for, flash
import socket
import dns.resolver  # Para resolver nomes DNS

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Necessária para usar mensagens flash

# Lista para armazenar os DNS cadastrados
dns_list = []

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

@app.route('/')
def index():
    return render_template('index.html', dns_list=dns_list)

@app.route('/register_dns', methods=['POST'])
def register_dns():
    dns_name = request.form['dns_name']
    if dns_name and dns_name not in dns_list:
        dns_list.append(dns_name)
        flash(f'DNS "{dns_name}" cadastrado com sucesso!')
    else:
        flash('Erro ao cadastrar DNS ou DNS já cadastrado!')
    return redirect(url_for('index'))

@app.route('/check', methods=['POST'])
def check_ports():
    host = request.form['host']
    ports = request.form['ports'].split(',')
    selected_dns = request.form.get('selected_dns')

    results = []
    for port in ports:
        port = port.strip()
        is_open = is_port_open(host, port)
        results.append({'port': port, 'is_open': is_open})

    dns_resolution = None
    if selected_dns:
        dns_resolution = resolve_dns(selected_dns)

    return render_template(
        'result.html',
        host=host,
        results=results,
        selected_dns=selected_dns,
        dns_resolution=dns_resolution
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1000)

