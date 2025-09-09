import os
import yaml


def define_env(env):
    @env.macro
    def task(file=None, **parameter):
        params = dict()

        if file:
            file_path = os.path.join(env.project_dir, file)
            with open(file_path, 'r', encoding='utf-8') as file:
                params.update(yaml.safe_load(file))

        params.update(parameter)

        return create_task(**params)

    @env.macro
    def youtube_video(inner_url, title='Video'):
        return youtube_video_admonition(inner_url, title)

    @env.macro
    def python_tutor(code_string, title="Code im Debugger"):
        return generate_pythontutor_iframe(code_string, title=title)

    @env.macro
    def python_tutor_button(code_string, title="Code im Debugger ansehen"):
        return generate_pythontutor_button(code_string, title=title)


def youtube_video_admonition(inner_url, title='Video'):
    return f'''??? video "{title}"

    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;">
        <iframe src="{inner_url}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
    </div>'''


def create_task(title="Aufgabe",
                question="⚠QUESTION_TEXT_MISSING⚠",
                solution="",
                tip="",
                difficulty=0,
                difficulty_icon='🌶',
                collapsed=False,
                solution_video=None,
                question_video=None):
    difficulty_icons = difficulty * difficulty_icon + (" " if difficulty else "")
    collapsed_symbol = "" if collapsed else "+"

    result = f'???{collapsed_symbol} question "{difficulty_icons}{title}"\n'
    if question_video:
        result += add_tabs(youtube_video_admonition(question_video))

    result += add_tabs(question)
    if tip:
        result += add_tabs(f'??? info "Tipp"\n') + add_tabs(tip, 2)
    if solution:
        result += add_tabs(f'??? success "Lösung"\n')
        if solution_video:
            result += add_tabs(youtube_video_admonition(solution_video, "Lösungsvideo"), 2)
        result += add_tabs(solution, 2)
    return result


def add_tabs(text, tabs=1):
    return ('\n' + text).replace('\n', '\n' + '\t' * tabs)


import urllib.parse


def generate_pythontutor_iframe(code_string, title='Python Tutor'):
    base_url = "https://pythontutor.com/iframe-embed.html"

    # Encoding des Codes
    encoded_code = urllib.parse.quote(code_string)

    # Dynamische Berechnung der Höhe basierend auf der Anzahl der Zeilen im Code
    line_count = code_string.count('\n') + 1
    code_div_height = max(line_count * 25, 400)  # Mindestens 400 px, ansonsten 25 px pro Zeile

    # Parameter für den Hash-Teil der URL
    hash_params = {
        "code": encoded_code,
        "cumulative": "false",
        "curInstr": "0",
        "heapPrimitives": "nevernest",
        "origin": "opt-frontend.js",
        "py": "3",
        "rawInputLstJSON": "[]",
        "textReferences": "false",
        "codeDivHeight": str(code_div_height),
        "codeDivWidth": "350"  # Feste Breite für den Code-Editor
    }

    # Hash-String zusammenbauen
    hash_string = "&".join(f"{key}={value}" for key, value in hash_params.items())
    full_url = f"{base_url}#{hash_string}"

    # Generieren des iframe-Tags im Container
    iframe_tag = f'''!!! python_tutor "{title}"

    <div class="python_tutor_container">
        <iframe src="{full_url}" title="{title}" frameborder="0" 
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        referrerpolicy="strict-origin-when-cross-origin" allowfullscreen
        style="width: 100%; height: {code_div_height}px;">
        </iframe>
    </div>
    '''

    return iframe_tag


def generate_pythontutor_button(code_string, title='Python Tutor'):
    base_url = "https://pythontutor.com/render.html"

    # Encoding des Codes
    encoded_code = urllib.parse.quote(code_string)

    # Parameter für den Hash-Teil der URL
    hash_params = {
        "code": encoded_code,
        "cumulative": "false",
        "curInstr": "0",
        "heapPrimitives": "nevernest",
        "origin": "opt-frontend.js",
        "py": "3",
        "rawInputLstJSON": "[]",
        "textReferences": "false"
    }

    # Hash-String zusammenbauen
    hash_string = "&".join(f"{key}={value}" for key, value in hash_params.items())
    full_url = f"{base_url}#{hash_string}"

    # Generieren des Button-Tags im Container
    button_tag = f'<a href="{full_url}" target="_blank" class="md-button" rel="noopener noreferrer">{title}</a>'

    return button_tag
