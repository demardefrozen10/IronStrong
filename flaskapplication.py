from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route('/data')
def get_data():
    data = warmup.json
    return jsonify(data)
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/warmup')
def warmup():
    return render_template('warmup.html')

@app.route('/exercisepage/<int:index>')
def exercisepage(index):
    force = ""
    muscle =""
    equipment = ""
    difficulty = ""
    instructions = ""
    exercise_name = exerciseList[index]
    exercise_image = imagesList[index]
    for exercise in Dictonary:
        if exercise["name"].lower() == exercise_name.lower():
           force = exercise.get('type').title()
           muscle =exercise.get('muscle').title()
           equipment =exercise.get('equipment').title()
           difficulty =exercise.get('difficulty').title()
           instructions= exercise.get('instructions').title()
    return render_template('exercisepage.html', exercise_name=exercise_name, force=force, muscle=muscle, equipment=equipment, difficulty=difficulty, instructions=instructions, exercise_image = exercise_image)

def webScraper():
    import requests
    from bs4 import BeautifulSoup
    global imagesList
    imagesList = []
    for exercise in exerciseList:
        url = 'https://www.bodybuilding.com/exercises/search?query=' + exercise
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        images = soup.find_all('img')
        for image in images:
           imagesList.append(image['src'])
           break
    return imagesList

@app.route("/", methods = (["POST", "GET"]))
def exercise():
    if request.method == "POST":
        import requests
        import json
        url = "https://exercises-by-api-ninjas.p.rapidapi.com/v1/exercises"
        muscleGroup = request.form.get('exercise')
        exericse1 = request.form.get("exerciselookup")
        if (muscleGroup == 'Muscle'):
            querystring = {"type":"strength","muscle":exericse1}
        else:
            querystring = {"name":exericse1,"type":"strength"}
        headers = {
            "X-RapidAPI-Key": "ece8cbe447msh4845768944b6cb6p169c19jsn8bd3677a3d2f",
            "X-RapidAPI-Host": "exercises-by-api-ninjas.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        global Dictonary
        Dictonary = json.loads(response.text)
        global exerciseList
        exerciseList = []
        muscleList = []
        for x in range (len(Dictonary)):
            capitalizedString = (Dictonary[x].get('name')).title()
            exerciseList.append(capitalizedString)
            muscleList.append((Dictonary[x].get('muscle')))
        imagesList = webScraper()
        if (len(exerciseList) == 0 or len(muscleList) == 0):
            return render_template('exercisenotfound.html')
        else:
            return render_template('exercise.html', exerciseList = exerciseList, len = len(exerciseList), imagesList = imagesList, muscleList = muscleList)
    return render_template('preexercise.html')

if __name__ == "__main__":
    app.run(debug=True)

exerciseList = exercise()
print(exerciseList)
