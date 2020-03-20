# PowerAttack-ML
The project is to build a mechince learning model on sever log data to discern the power attack and develop a detection moudule.

1.Sever usage data collecting module
  The bash script "collect.sh" collect time, current task numbers, cpu usage idle%, mem usage, io and net data, and put them in the "data1.csv".
  The "cpu_avg.log" contains cpu uptime usage% in 1, 5 and 15 minites.
 
 Example:
         ./collect.sh 3 60 wlp3s0
