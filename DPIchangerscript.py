from flask import Flask, request, render_template_string, redirect, url_for
import os
import re
import subprocess

app = Flask(__name__)

CONFIG_FILE = "config.txt"

# Разрешение доступа в брандмауэре Windows
os.system('netsh advfirewall firewall add rule name="Python Flask Server" dir=in action=allow protocol=TCP localport=5000')

# Функция для сохранения пути в файл
def save_folder_path(path):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        f.write(path)

# Функция для загрузки пути из файла
def load_folder_path():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None

# HTML-интерфейс
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>RawAccel DPI Changer</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: Arial, sans-serif;
            background-color: #121212;
            color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            text-align: center;
        }
        .container {
            width: 100%;
            max-width: 400px;
            padding: 20px;
            background-color: #1e1e1e;
            border-radius: 10px;
            box-shadow: 0px 0px 15px rgba(187, 134, 252, 0.5);
        }
        h1 {
            color: #bb86fc;
            margin-bottom: 20px;
        }
        form { display: flex; flex-direction: column; }
        input {
            padding: 12px;
            margin: 10px 0;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            text-align: center;
        }
        button {
            padding: 12px;
            background-color: #bb86fc;
            color: #121212;
            font-size: 16px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.3s;
        }
        button:hover { background-color: #9b6bd4; }
        .change-folder {
            margin-top: 15px;
            font-size: 14px;
            text-decoration: underline;
            cursor: pointer;
            color: #bb86fc;
        }
    </style>
</head>
<body>
    <div class="container">
        {% if not folder %}
            <h1>Enter RawAccel Folder Path</h1>
            <form method="post" action="{{ url_for('set_folder') }}">
                <input type="text" name="folder" placeholder="C:\\rawaccel" required>
                <button type="submit">Save</button>
            </form>
        {% else %}
            <h1>Enter New DPI Value</h1>
            <form method="post" action="{{ url_for('set_dpi') }}">
                <input type="number" name="dpi" placeholder="44000" required>
                <button type="submit">Apply</button>
            </form>
            <div class="change-folder" onclick="window.location.href='{{ url_for('reset_folder') }}'">
                Change RawAccel Folder
            </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    folder = load_folder_path()  # Загружаем путь из config.txt
    return render_template_string(HTML_TEMPLATE, folder=folder)

@app.route('/set_folder', methods=['POST'])
def set_folder():
    folder = request.form.get('folder')
    if not os.path.isdir(folder):
        return "Folder not found. Please check the path and try again.", 400
    save_folder_path(folder)  # Сохраняем путь в config.txt
    return redirect(url_for('index'))

@app.route('/reset_folder')
def reset_folder():
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)  # Удаляем сохраненный путь
    return redirect(url_for('index'))

@app.route('/set_dpi', methods=['POST'])
def set_dpi():
    folder = load_folder_path()  # Загружаем путь из config.txt
    if not folder:
        return redirect(url_for('index'))
    
    settings_path = os.path.join(folder, 'settings.json')
    
    dpi_value = request.form.get('dpi')
    try:
        dpi_value_int = int(dpi_value)
    except ValueError:
        return "Invalid DPI value. It must be a number.", 400

    if not os.path.isfile(settings_path):
        return "settings.json file not found in the specified folder.", 400
    
    try:
        with open(settings_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return f"Error reading file: {e}", 500

    # Регулярное выражение для замены значения DPI
    pattern = r'("DPI \(normalizes sens to 1000dpi and converts input speed unit: counts/ms -> in/s\)"\s*:\s*)(\d+)'
    replacement = r'\g<1>' + str(dpi_value_int)
    new_content, count = re.subn(pattern, replacement, content)

    if count == 0:
        return "DPI key not found in settings.json file.", 400

    try:
        with open(settings_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    except Exception as e:
        return f"Error writing file: {e}", 500

    writer_path = os.path.join(folder, 'writer.exe')
    if not os.path.isfile(writer_path):
        return "writer.exe file not found in the specified folder.", 400

    try:
        subprocess.run([writer_path, settings_path], check=True)
    except subprocess.CalledProcessError as e:
        return f"Error executing writer.exe: {e}", 500

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)