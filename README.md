# HYBRID DEEP LEARNING SENTIMENTAL ANALYSIS

### Steps to Run the Program

Step 1 : Download The Required models from the provided link :-```https://drive.google.com/drive/folders/1tOKnP3LyOX68TWVhTL8pqlzxahHrnyOx?usp=sharing```

Step 2 : Add the model in the same folder as of main.py

Step 3 : Install python and pip after that requirements from requirements.txt

Step 4 : Download libretranslate from pip

Step 5 : Execute this command -> ```libretranslate --load-only "es,en,hi,en,fr,en" --host 0.0.0.0 --port 6001 --debug```

Step 6 : This will download the necessary models and start the libretranslate server on port 6001

Step 7 : Run the main.py using the command ```python main.py``` File to start the backend server of port 5000.

Step 8 : Clone the frontend files with command  : git clone https://github.com/dishant2000/Team48-frontend.git 

Step 9 : For the frontend to work make sure your device is on same network with the device where your backend and libretranslate server is running.

Step 10 : If not in same network you can connect through hotspot and wifi.

Step 11 : you can find the default gateway address in wifi settings to be added in the url section of the file src > pages > Home.js > "translateUrl",   "predictUrl", change the url accordingly.
Step 12 : For example if your default gateway is "10.42.0.1" the urls will be 
const translateUrl = "http://10.42.0.1:6001/translate";
const predictUrl = "http://10.42.0.1:5000/predict";

step 13 : Run the server using command : npm start

Step 14 : This will run a frontend server on port 3000 and should automatically open a window on your default browser or else you can type http://locahost:3000 on your browser to run the frontend window.


