# MyPlantPal  


# Alexa
Create a node.js Custom Skill. Follow next [tutorial](https://www.youtube.com/watch?v=CzTKDu7Qgjs&t=2s) step by step.  

In order to do a request from a Custom Skill, use library node-fetch. This package has been added to the github [Lambda_Function](https://github.com/ViridianaVM/MyPlantPal/tree/main/Lambda_Function/Custome_Skill_myPlantPal) repository. Send all files to a Zip folder, and then import them inside your Custome Skill by selecting "Import Code" inside the "Code" section.

Whit this, the functionality to make requests to the MyPlantPal API (Azure) from the skill will work. 

Now, in order to link your device (raspberry pi) with your Amazon Login Account, you need to create a Smart Home Skill. Follow next [tutorial](https://developer.amazon.com/en-US/docs/alexa/smarthome/steps-to-build-a-smart-home-skill.html) step by step.

To call my AWS Lambda Function inside this Smart Home skill, go to "Smart Home Service Endpoint" and add my [Lambda function](amzn1.ask.skill.ae9f061d-a7c0-4532-a239-55785cadb7b8). You can add the same values in "Pick a geographical region that is closest to your target customers and setup geographic specific endpoints".

With this, the authentication with Login With Amazon and device discovery should work.

Now, you can go to your Alexa application and enable the skill.


# Raspberry Pi
In order to set your raspberry pi as a web server, you need to install Apache and mod-wsgi. Follow next tutorials ([1](https://www.atlantic.net/vps-hosting/how-to-install-apache-with-python-mod_wsgi-on-debian-10/) and [2](https://docs.appseed.us/content/how-to/flask-apache-centos-virtualenv-minimal-configuration#:~:text=Go%20to%20%2Fvar%2Fwww%20-%20the%20www_root%20of%20Apache,defined%20in%20the%20app%20directory.%20return%20%22Hello%20world%21%22)) step by step. They will help to install Python as well.

After that, you can install Flask by using: `sudo apt-get install flask`  

Go to `/var/www/` and create a folder to store your BackEnd.
Inside that folder, you can copy everything that I have in my [RaspberryPi](https://github.com/ViridianaVM/MyPlantPal/tree/main/RaspberryPi-BackEnd) repository.  

In your router, assign a fixed IP to your raspberry pi and redirect all traffic from internet to port 5000(flask). 

To run Flask you need to use: `flask run --host=192.XXX.X.XXX` (raspberry pi's IP).

In ordert to keep running flask all time, create chrone service. 


### You are all set!
