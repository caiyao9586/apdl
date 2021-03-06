#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import os
import subprocess
# 生成apdl命令流文件


time = datetime.datetime.now().strftime('%Y%m%d%H%M')


def command_genertate(work_dir, content, soft_name):
    """
    :param soft_name: ansys or fluent
    :param work_dir: 工作目录
    :param content: 命令流str
    :return: 生成命令流文件，返回文件名
    """
    suffix = {
        'ansys': '.inp',
        'fluent': '.jou',
    }
    file_path = os.path.join(work_dir,
                             '{}'.format(soft_name) +
                             '{}'.format(suffix[f'{soft_name}']))
    with open(file_path, 'w') as f:
        f.write(content)
#    file_name = os.path.split(file_path)[-1]
    return file_path


def command_stream(ansys_dir, fluent_dir, film_thick='0.005', **kwargs):
    """
    :param ansys_dir:
    :param fluent_dir:
    :param film_thick: 膜厚
    :return: 命令流str
    """
    cdb_name = str(float(film_thick)*1000)+'um'
    inp = f'''\
/clear
/filname,seal_groove

/units,si
pi=4*ATAN(1) 
*afun,deg
C={film_thick}                                                  
R_I=28
W_1=1.2
R_O=R_I+W_1
H=5.1
H_1=0.5
H_2=1.4
H_3=1                                                    
H_4=0.6
W=5.3
W_2=0.5
R_S=31.75
R_Ange=0.7
R_Low=1.6                                               
R_L=R_I+W_2
Ang_0=25
Ang_1=55+44/60
Ang_2=54
Ang_3=58.5
Ang_4=64
Ang_5=59.5
Ang_6=53+17/60
Ang_7=13
Ang_8=34
Ang_9=53
Ang_10=48.5
E=0.1
L=4

/prep7

et,1,mesh200
et,2,fluid142                                           
keyopt,1,1,6
keyopt,1,2,1                                             
keyopt,2,1,6
keyopt,2,3,0
keyopt,2,4,0

seltol,1e-7

k,,                                                        
k,,,,H
cyl4,,,R_I-C,0,R_I,120,H
k,,R_I-H_1,,H-H_1
k,,R_O,,H-H_1
k,,R_O,,H-H_1-H_2
k,,R_I-H_1,,H-H_1-H_2
lstr,11,12
lstr,12,13
lstr,13,14
lstr,14,11
lfillt,13,14,R_Ange
lfillt,15,14,R_Ange
lstr,15,17
al,16,13,17,18,15
al,16,13,14,15
vrotat,7,8,,,,,1,2,Ang_1+Ang_0

wprota,Ang_7+Ang_0                                        
cyl4,R_L-R_Low,0,R_Low,360
k,,,,H_3

adele,17
ldele,31,32,1,1
lsbl,30,4,,,keep
lsbl,33,4,,,keep
ldele,32,34,2,1

csys,4

kbetw,24,1,,,1/28
kbetw,27,1,,,1/28
lstr,24,23
lstr,27,25
lstr,23,25
al,32,31,30,33,34
vext,17,,,,,H
numcmp,all

wprota,-Ang_7                                              
wprota,Ang_3-1.5,90
rectng,R_I-W,R_I+W,0,H
vrotat,24,,,,,,1,2,15

wprota,,,1.5
wpoffs,R_I,H
wprota,,180-2
vsbw,5
vdele,6,,,1
wprota,,2-180

wpoffs,-R_I                                                 
wprota,,,2+Ang_5-Ang_6
wpoffs,R_I

wpoffs,W,-H                                                 
wprota,,-11
vsbw,7
vdele,5,,,1
wprota,,11
wpoffs,-W,H

wpoffs,-R_I                                                 
wprota,,,-(2+Ang_5-Ang_6)+(Ang_4-Ang_3)
wpoffs,R_I

wpoffs,,H_4-H                                             
wprota,,-90,-50
vsbw,6
wprota,,,50
wprota,,90
wpoffs,,H-H_4

wpoffs,W                                                    
wprota,90,-6
vsbw,5
wprota,,6
wprota,-90
wpoffs,-W-R_I

wprota,,,-(Ang_4-Ang_3-2)                                   
wpoffs,R_I,-H
wprota,,-2
vsbw,7

wprota,,2
wpoffs,,H
wpoffs,-R_I
wprota,,,-(2+Ang_3+Ang_0)                                   

vdele,8,9,1,1

circle,2,R_S,,,120
adrag,53,,,,,,9
ldele,51,,,1
vsba,6,27,,,dele
vdele,8,,,1

wprota,,-90
wpstyl,,,,,,1
vgen,2,4,,,,Ang_8-Ang_7                                   
vgen,2,4,,,,Ang_9-Ang_7                                    
vgen,2,4,,,,-(2*Ang_7)                                      
vgen,2,4,,,,Ang_3-Ang_7+2+(Ang_5-Ang_10)                    
vgen,2,4,,,,Ang_3-Ang_7+2+(Ang_5-Ang_10)+(Ang_10-Ang_8)     

agen,2,7,8,,,Ang_0+Ang_3+2+Ang_5-Ang_2                      
vrotat,70,71,,,,,1,2,120-(Ang_0+Ang_3+2+Ang_5-Ang_2)

vovlap,all
numcmp,all

vsel,s,,,2,12,2
vsel,a,,,13
vsel,a,,,25,28,1
vsel,a,,,74,84,1
vsel,a,,,87,92,1
cm,v_1,volu
vdele,v_1,,,1                                              
allsel
numcmp,all

kwplan,,2,56,1                                              
vsbw,65
kwplan,,2,16,1 
vsbw,68
kwplan,,102,27,101
vsbw,70
kwplan,,104,31,103
vsbw,71

wpcsys,,1
circle,2,R_I+0.5,,,120                                      
ldele,409,,,1
adrag,410,,,,,,120
vsba,7,298,,,dele
numcmp,all

vsel,u,,,13,42,29
vsel,u,,,62,63,1
vsel,u,,,70,72,2
cm,v_2,volu                                                 
allsel

lstr,1,21
lstr,1,19
lextnd,422,21,H,1
lextnd,423,19,H,1
ldele,422,423,1,1
lstr,1,2
adrag,424,425,,,,,422

agen,2,307,308,1,,Ang_8-Ang_7                              
agen,2,307,308,1,,Ang_9-Ang_7                               
agen,2,307,308,1,,-(2*Ang_7)                                
agen,2,307,308,1,,Ang_3-Ang_7+2+(Ang_5-Ang_10)              
agen,2,307,308,1,,Ang_3-Ang_7+2+(Ang_5-Ang_10)+(Ang_10-Ang_8)

asel,s,,,307,318,1                                         
cm,a_1,area                                                 

vsba,v_2,a_1,,,delete
allsel,all
ldele,422,,,1

allsel
numcmp,all                                                                                                                             

mopt,qmesh,main
mopt,split,2 
lesize,337,,,L
lesize,334,,,L
lesize,368,,,L
esize,E

vsel,s,,,62,64,2                                           
vsel,a,,,13
accat,1,66
accat,278,281
lesize,402,,,8
lesize,404,,,8
cm,v_3,volu
allsel
vsweep,v_3
adele,355,356,1,1
ldele,482,485,1,1
                                                  
vsel,s,,,18,39,1                                        
vsel,a,,,42,53,1
vsel,a,,,56,61,1
vsel,a,,,63
cm,v_4,volu                                               
allsel,below,volu
asel,r,loc,x,R_I
allsel,below,area
amesh,all
allsel
vsweep,v_4 
                                                
vsel,s,,,7,12,1
vsel,a,,,65,76,1
vsel,a,,,78,79,1
vsel,a,,,81,84,1
cm,v_5,volu                                              
allsel,below,volu
asel,r,loc,z,H-H_1                                        
allsel,below,area
amesh,all
allsel
vsweep,v_5
                                                                                                  
vsel,s,,,1,6,1                                             
cm,v_6,volu
allsel
vsweep,v_6

aclear,all

vgen,3,all,,,,120,,,0

nummrg,node,1e-7,,,low
nummrg,elem,,,,low
nummrg,kp,1e-7,,,low

vsel,s,,,14,17,1
vsel,a,,,40,41,1
vsel,a,,,98,101,1
vsel,a,,,124,125,1
vsel,a,,,182,185,1
vsel,a,,,208,209,1
cm,v_7,volu 
allsel,below,volu
asel,r,loc,x,R_I
allsel,below,area
amesh,all
allsel                                                                                                      
vsweep,v_7

vsel,s,,,77,80,3
vsel,a,,,161,164,3
vsel,a,,,245,248,3
cm,v_8,volu
allsel
vsweep,v_8

vsel,s,,,54,55,1
vsel,a,,,138,139,1
vsel,a,,,222,223,1
cm,v_9,volu
allsel
vsweep,v_9

nummrg,node,1e-7,,,low
nummrg,elem,,,,low
nummrg,kp,1e-7,,,low

aclear,all

allsel
cm,fluid,elem

nsel,all
nsel,s,loc,x,R_I-C
allsel,below,node                                           
cm,mwall,node                                               

allsel
asel,s,loc,z,0
asel,a,,,1
asel,a,,,413
asel,a,,,767
cm,a_2,area
nsla,s,1                                                    
cm,inlet,node

allsel
asel,s,loc,z,H
asel,u,,,277
asel,u,,,643
asel,u,,,997
cm,a_3,area                                                 
nsla,s,1
cm,outlet,node 

allsel
asel,s,,,996,998,1
asel,a,,,1004,1006,2
asel,a,,,764,768,4
asel,a,,,948,965,17
asel,a,,,1047,1049,2
asel,a,,,64,65,1
asel,a,,,279,280,1
asel,a,,,270,277,7
asel,a,,,99,189,90
asel,a,,,241,271,30
asel,a,,,236
asel,a,,,642,644,1
asel,a,,,650,652,2
asel,a,,,693,695,2
asel,a,,,410,414,4
asel,a,,,594,611,17
cm,a_4,area
nsla,s,1                                                    
cm,outwall1,node

allsel,all
asel,s,ext
asel,u,loc,x,R_I-C
asel,u,,,a_2
asel,u,,,a_3
asel,u,,,a_4
nsla,s,1                                                    
cm,outwall2,node

allsel
CDWRITE,DB,'{cdb_name}','cdb'        
'''
    jou = f'''\
/file/import/mechanical-apdl/input "{os.path.join(ansys_dir, cdb_name+'.cdb')}"
/mesh/scale 0.001 0.001 0.001
/define/units angular-velocity rpm 
/define/boundary-conditions/wall mwall y motion-bc-moving no no y no {kwargs['rpm']} 0 0 0 0 0 1 
/define/boundary-conditions/zone-type inlet pressure-inlet 
/define/boundary-conditions/zone-type outlet pressure-outlet 
/define/boundary-conditions/pressure-inlet inlet yes no {kwargs['inlet']} no 0 no yes 
/define/boundary-conditions/pressure-outlet outlet no {kwargs['outlet']} no yes no no no
/define/operating-conditions/operating-pressure 0
/solve/monitors/residual/convergence-criteria 1e-5 1e-5 1e-5 1e-5
/solve/monitors/surface/set-monitor surf-mon-1 "Mass Flow Rate" outlet () n n y "{os.path.join(
        fluent_dir, 'massflow.out'
    )}" 1
/solve/monitors/surface/set-monitor surf-mon-2 "Area-Weighted Average" pressure outwall2 () n n y "{os.path.join(
        fluent_dir, 'pressure.out'
    )}" 1
/solve/initialize/hyb-initialization
/solve/set/number-of-iterations {kwargs['iterate']}
/solve/iterate {kwargs['iterate']} 
/file/write-case-data "{os.path.join(
        fluent_dir, cdb_name+'.cas'
    )}"
/exit
'''
    return inp, jou


def make_work_dir(name):
    """
    :param name: ansys or fluent
    :return: 判断文件夹是否存在，不存在则创建
    """
    path = r'.\log\{0}\{1}'.format(name, name+time)
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def error_find(output_file):
    """
    :param output_file: ansys output 文件
    :return: 建模过程中是否不正常退出，error数量
    """
    with open(output_file, 'r') as f:
        for line in f:
            if 'NUMBER OF ERROR' in line:
                error_num = int(line.split()[-1])
                return error_num


def ansys_call(ansys_path, work_dir, inp_path):
    """
    :param inp_path:
    :param ansys_path:
    :param work_dir:
    :return: 是否生成cdb文件True/False
    """
    input_file = inp_path
    output_file = os.path.join(work_dir,
                               'output_ansys.out')

    job_name = 'seal'
    path_string = ('"{}"  -p ane3fl -dir "{}" -j "{}" -s read -l en-us '
                   '-b -i "{}" -o "{}"').format(
        ansys_path, work_dir, job_name, input_file, output_file
    )

    subprocess.call(path_string)
    ansys_create_cdb = True
    if error_find(output_file):
        ansys_create_cdb = False
    return ansys_create_cdb


def fluent_call(fluent_path, work_dir, jou_path):
    input_file = jou_path
    output_file = os.path.join(work_dir,
                               'output_fluent.out')
    path_string = '"{}" 3ddp -t3 -g -i "{}" -o "{}"'.format(
        fluent_path, input_file, output_file
    )
    subprocess.call(path_string)
    return None


def main():
    ansys_path = r'C:\Program Files\ANSYS Inc\v160\ANSYS\bin\winx64\ansys160.exe'
    fluent_path = r'C:\Program Files\ANSYS Inc\v160\fluent\ntbin\win64\fluent.exe'
    kw = {
        'rpm': -20000,
        'inlet': 200000,
        'outlet': 100000,
        'iterate': 4000,
    }
    ansys_dir = make_work_dir('ansys')
    fluent_dir = make_work_dir('fluent')
    content = command_stream(ansys_dir, fluent_dir, **kw)
    inp_path = command_genertate(ansys_dir, content[0], 'ansys')
    jou_path = command_genertate(fluent_dir, content[1], 'fluent')
    cdb_ok = ansys_call(ansys_path, ansys_dir, inp_path)
    if cdb_ok:
        fluent_call(fluent_path, fluent_dir, jou_path)


if __name__ == '__main__':
    main()
