# Sunrise_sunset_project

In this repository, I have made a custom webapp using flask to fetch the sunrise & sunset time
for each location on the selected date past/present/future.
Below I have discussed step-by-step procedure of this project implementation
- Create a flask webapp using VSCODE
- Deploy the app in Render platform (which is an open source & free web hosting platform)

## Project Implementation and Compatibility
This project has been meticulously developed to seamlessly function on both desktop and mobile platforms. For a live demonstration, please visit our website at https://solarsage.onrender.com/.

## Testing Phase success:
The project has successfully completed its testing phase, which involves the retrieval of current timezone information for various locations. This process is achieved through the following steps:
1. Country Data Mapping: We have created a static file named countries.json as a reference for populating the countries dropdown field. The source of this file can be found on GitHub [Country Code Mapping](https://gist.github.com/keeguon/2310008)
2. Geocoding with API (opencagedata): Our project utilizes the OpenCage Data API to fetch geocoding information. This includes latitude, longitude, sunrise, and sunset times for the selected country and date.
3. City and State Data Retrieval with Google Maps API: For cases where latitude and longitude data are available, our project employs the Google Maps API to retrieve additional data regarding the city and state.
4. Custom API for Sunrise and Sunset Information: To streamline the process, we have created a custom API, accessible at /get_sunrise_sunset. This API allows users to post data related to sunrise and sunset timezones, along with city and state information for their desired country. It not only processes this data but also returns the results efficiently.
5. Also, Users are required to select both a date and a country to access the sunrise and sunset information for their chosen region.

## Process Steps
1. Firstly, Install all the library mentioned on the requirments file.

```python
pip install Flask==2.2.5 opencage==2.3.0 python-dotenv==0.21.1 pytz==2022.1 requests==2.31.0 gunicorn==20.1.0
```

Once you installed the library, Define your folder structure as per below

```bash
├── static
│   ├── bg-building.png
│   ├── cloud1.png
│   ├── cloud2.png
│   ├── cloud3.png
│   ├── styles.css
├── templates   
│   ├── index.html
├── app.py
├── countries.json
├── requirements.txt
```

2. Test your web app in your local machine with the following command
and pushed the codes in new Github respository. Finally, create a new account in render platform and deploy

```python
set FLASK_APP=app.py
set FLASK_ENV=development
flask run
```
## Youtube Materials for Reference
I would highly recommand to watch the youtube videos for the mentioned descriptive steps in order to avoid confusions on the process steps
* More details about [Build a Flask Webapp (Preview)
](https://flask.palletsprojects.com/en/3.0.x/)
* More details about [Render web hosting (Preview)
](https://www.youtube.com/watch?v=4SO3CUWPYf0)
* More details about [cron-job](https://console.cron-job.org/) create cron job & setup an HTTP call after 14 minute
