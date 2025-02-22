from flask import Flask, render_template, request, send_from_directory
import openai
import pyttsx3
import os

app = Flask(__name__)

# Initialize the text-to-speech engine
engine = pyttsx3.init()
pace = "150"
engine.setProperty('rate', pace)
engine.setProperty('volume', 1.0)

def generate_speech(text, filename="audio.wav"):
    try:
        filepath = os.path.join('static', filename)
        engine.save_to_file(text, filepath)
        engine.runAndWait()
        print("Audio generated successfully!")
    except Exception as e:
        print(f"Error generating audio: {e}")

def get_script_and_visuals(api_key, subject):
    try:
        openai.api_key = api_key
        completion = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an amazing writer"},
                {
                    "role": "user",
                    "content": f"Tell me one interesting fan theory about {subject}, and write a small script for my YouTube short. You have to give me a single paragraph which I can read for 40-50 seconds and 8 visuals prompt or suggestions. Make sure to have a catchy hook and light and run content. Small note, mention fan theory word somewhere in a casual way. Make sure to give ###Script### and ###Visuals### so I can segregate later."
                }
            ]
        )

        output = completion.choices[0].message['content']

        script_part = output.split("###Script###")[1].split("###Visuals###")[0].strip()
        suggestions_part = output.split("###Visuals###")[1].strip()

        return script_part, suggestions_part

    except Exception as e:
        print(f"Error generating script and visuals: {e}")
        return None, None

def improve_script(api_key, script, improvement):
    try:
        openai.api_key = api_key
        nextmove = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an amazing writer, help me improve this"},
                {
                    "role": "user",
                    "content": f"I have this script for my YouTube short which is like a single paragraph lasting for 40-50 seconds. The actual script is *{script}*. I want to improve it based on the feedback given *{improvement}*. Make sure to follow the same format in paragraph."
                }
            ]
        )

        newoutput = nextmove.choices[0].message['content']
        return newoutput

    except Exception as e:
        print(f"Error improving script: {e}")
        return None

@app.route('/')
def index():
    error = request.args.get('error')
    return render_template('index.html', error=error)

@app.route('/generate', methods=['POST'])
def generate():
    api_key = request.form['api_key']
    subject = request.form['subject']
    script_part, suggestions_part = get_script_and_visuals(api_key, subject)

    if script_part and suggestions_part:
        return render_template('result.html', script=script_part, suggestions=suggestions_part)
    else:
        error = "Error generating script and visuals"
        return render_template('index.html', error=error)

@app.route('/improve', methods=['POST'])
def improve():
    api_key = request.form['api_key']
    script_part = request.form['script']
    improvement = request.form['improvement']
    new_script_part = improve_script(api_key, script_part, improvement)

    if new_script_part:
        return render_template('result.html', script=new_script_part, improvement=True)
    else:
        error = "Error improving script"
        return render_template('index.html', error=error)

@app.route('/generate_audio', methods=['POST'])
def generate_audio():
    script_part = request.form['script']
    generate_speech(script_part)
    return "Audio generated successfully!"

@app.route('/static/<path:filename>')
def send_file(filename):
    return send_from_directory('static', filename)

if __name__ == "__main__":
    print("Starting Flask app...")
    app.run(debug=True, host='0.0.0.0', port=8000)
