from flask import (
        Flask,
        render_template,
        request,
        redirect
)
from requests import get
from pprint import pprint
app = Flask(__name__)

@app.route("/")
def index():
        return render_template("layout.html")

@app.route("/get_weather", methods=["GET", "POST"])
def get_weather():
        if request.method == "POST":
                try:
                        days = request.form.get("days")
                        if days == "1":
                                city = request.form["city"]
                                #print(city)

                                #city -> coordinates
                                API_key = "5c197cedae439a487685ceab5af6fd28"
                                
                                geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=4&appid={API_key}"
                                
                                req = get(geo_url)
                                #print(req.json())
                                if req.status_code != 200:
                                        return render_template("layout.html", text="Tu esi kļūda!")

                                

                                geo_data = req.json()[0]
                                #latitude, longitude 
                                lat = geo_data["lat"]
                                lon = geo_data["lon"]
                                city_name=geo_data["name"]
                                country=geo_data["country"]
                                #print(lat, lon)

                                #lat, lon -> weather report 
                                wench_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&lang=la&appid={API_key}"

                                req = get(wench_url)

                                if req.status_code != 200:
                                        return render_template("layout.html", text="Tu esi kļūda!")
                                
                                wench_data=req.json()

                                temp = wench_data["main"]["temp"]
                                weather = wench_data["weather"][0]["description"]
                                icon = wench_data["weather"][0]["icon"]
                                icon_url = f"https://openweathermap.org/img/wn/{icon}@2x.png"
                                #print(temp, weather, icon)


                                return render_template("layout.html", temp=temp, weather=weather, icon_url=icon_url, city_name=city_name, country=country)
                        elif days == "5":
                                city = request.form["city"]
                                API_key = "5c197cedae439a487685ceab5af6fd28"
                                geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=4&appid={API_key}"
                                req = get(geo_url)

                                if req.status_code != 200:
                                        return render_template("layout.html", text="Tu esi kļūda!")
                                #print(req.json())
                                geo_data = req.json()[0]
                                #latitude, longitude 
                                lat = geo_data["lat"]
                                lon = geo_data["lon"]
                                city_name=geo_data["name"]
                                country=geo_data["country"]
                                wench_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&lang=la&appid={API_key}"
                                req = get(wench_url)
                                if req.status_code != 200:
                                        return render_template("layout.html", text="Tu esi kļūda!")
                                
                                wench_data=req.json()
                                #pprint(wench_data)
                                
                                dates = []
                                for date in wench_data["list"]:
                                        dates.append(date["dt_txt"])

                                wanted = "12:00:00"

                                # using in
                                result = list(filter(lambda x: wanted in x, dates))

                                #print(result)
                                temp_icon = ""
                                weather =  [] #wench_data["weather"][0]["description"]
                                temp2 = []
                                icon = []
                                for date in wench_data["list"]:
                                        if date["dt_txt"] in result:
                                                weather.append(date["weather"][0]["description"])
                                                temp2.append(date["main"]["temp"])
                                                temp_icon = date["weather"][0]["icon"]
                                                icon_url = f"https://openweathermap.org/img/wn/{temp_icon}@2x.png"
                                                icon.append(icon_url)
                                                
                        

                                #print(weather, temp, icon)                
                                return render_template("layout.html", weather=weather, temp2=temp2, icon=icon, dates=dates, city_name=city_name, country=country)
                        else:
                                return redirect("/")
                except:
                        return render_template("layout.html", text="KYS")
        else:
                ...











if __name__=="__main__":
        app.run(debug=True)