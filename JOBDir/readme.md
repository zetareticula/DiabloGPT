# Mumford Grammar
# 2022-01-01

## Introduction

This is a Mumford grammar for the Leanred Join Order problem. The grammar is based on the Mumford grammar for the RTOS problem. The grammar is used to generate the input files for the RTOS problem. The input files are then used to generate the input files for the Leanred Join Order problem.

Reinforcement Learning with Tree-LSTM for Join Order Selection(RTOS) is an optimizer which focous on Join order Selection(JOS) problem.  RTOS learn from previous queries to build plan for further queries with the help of DQN and TreeLSTM.

## How to use

### 1. Generate input files for RTOS

The input files for RTOS are generated by the Mumford grammar. The Mumford grammar is based on the Mumford grammar for the RTOS problem. The Mumford grammar is used to generate the input files for the RTOS problem. The input files are then used to generate the input files for the Leanred Join Order problem.

The Mumford grammar is based on the Mumford grammar for the RTOS problem. The Mumford grammar is used to generate the input files for the RTOS problem. The input files are then used to generate the input files for the Leanred Join Order problem.


### 2. Generate input files for Leanred Join Order

The input files for Leanred Join Order are generated by the Mumford grammar. The Mumford grammar is based on the Mumford grammar for the RTOS problem. The Mumford grammar is used to generate the input files for the RTOS problem. The input files are then used to generate the input files for the Leanred Join Order problem.


### 3. Run Leanred Join Order

The input files for Leanred Join Order are generated by the Mumford grammar. The Mumford grammar is based on the Mumford grammar for the RTOS problem. The Mumford grammar is used to generate the input files for the RTOS problem. The input files are then used to generate the input files for the Leanred Join Order problem.


# Development

This repository contains a very early version of RTOS.It is written in python and built on PostgreSQL. It now contains the training and testing part of our system. 



It has been fully tested on <a href="http://www.vldb.org/pvldb/vol9/p204-leis.pdf">join order benchmark(JOB)</a>. You can train RTOS and see its' performance on JOB.

This code is still under development and not stable, add issues if you have any questions. We will polish our code and provide further tools. 

# Important parameters
Here we have listed the most important parameters you need to configure to run RTOS on a new database. 

## 1. Database

The database we used is JOB. You can download it from <a href="http://www.vldb.org/pvldb/vol9/p204-leis.pdf">here</a>.

## 2. Configuration file

The configuration file is in the folder "config". You need to configure the following parameters in the configuration file.



## 3. Input files
- schema-file
    - <a href ="https://github.com/gregrahn/join-order-benchmark/blob/master/schema.sql"> a sample</a>
- syntheticDir
    - Directory contains the sytheic workload(queries), more sythetic queries will help RTOS make better plans. 
    - It is nesscery when you want apply RTOS for a new database.  
- JOBDir
    - Directory contains all JOB queries. 
- Configure of PostgreSQL
    - dbName : the name of database 
    - userName : the user name of database
    - password : your password of userName
    - ip : ip address of PostgreSQL
    - port : port of PostgreSQL

# Requirements
- Pytorch 1.0
- Python 3.7
- torchfold
- psqlparse

# Run the JOB 
1. Follow the https://github.com/gregrahn/join-order-benchmark to configure the database
2. Add JOB queries in JOBDir.
3. Add sythetic queries in sytheticDir, more sythetic queries will help RTOS generate better results. E.g. You can generate queries by using templates.
4. Cost Training, It will store the model which optimize on cost in PostgreSQL

		python3 CostTraining.py

5. Latency Tuning, It will load the cost training model and generate the latency training model
	
		python3 LatencyTuning.py 


# Questions
Contact Xiang Yu (x-yu17@mails.tsinghua.edu.cn) if you have any questions.