@echo off

echo Starting execution!

robot --variable BROWSER:firefox -d log1 valid_login.robot
pabot --pabotlib --testlevelsplit -d log2 invalid_login.robot
pabot --pabotlib --testlevelsplit -d log3 polls.robot
robot -d log4 pdfdocs.robot
rebot -d Demo --name Logs log1/output.xml log2/output.xml log3/output.xml log4/output.xml

echo Done!
