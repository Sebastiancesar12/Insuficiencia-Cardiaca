"""
Práctica 3: Sistema Muscuesqueletico


Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Luis Abdiel Fernandez Lira
Número de control: 21212154
Correo institucional: l21212154@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control
#!pip install slycot

# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import math as m
import matplotlib.pyplot as plt
import control as ctrl

# Datos de la simulación
x0, t0, tF, dt, w, h=0, 0, 10, 1E-3, 8, 5
N = round((tF-t0)/dt)+1
t = np.linspace(t0,tF,N) 
u = 2.5* np.sin(m.pi/2*t) 


#Función de transferencia: Individuo Saludable (Control)
R1=1000
R2=100
C=5E-6
L=10E-3
num = [L, R1]
den = [C*L*(R1+R2),L+C*R1*R2,R1]
sys = ctrl.tf(num,den)
print('Individuo sano (control):')
print(sys)

#Función de transferencia: Individuo Enfermo (Caso)
R1=1000
R2=100
C=30E-3
L=10E-3
num = [L, R1]
den = [C*L*(R1+R2),L+C*R1*R2,R1]
sysE = ctrl.tf(num,den)
print('Individuo enfermo (caso):')
print(sysE)

#Controlador
Rr = 4899.9314
Re = 130.9291
Ce = 1.0927E-4
Cr = 1E-6
numPID = [Rr*Re*Cr*Ce, Re*Ce+Rr*Cr,1]
denPID = [Re*Cr,0]
PID = ctrl.tf(numPID,denPID)
print(PID)

#Sistema de control de tratamiento
X = ctrl.series(PID,sysE)
sysPID = ctrl.feedback(X,1,sign=-1)
print('Sistema con tratamiento')
print(sysPID)

fig = plt.figure()
ts,Vs = ctrl.forced_response(sys,t,u,x0)
plt.plot(t, Vs, '-', color = [0,0,1], label = 'Fs(t):Control')
ts,Ve = ctrl.forced_response(sysE,t,u,x0)
plt.plot(t,Ve, "-" ,color = [0.8500,0.3250,0.0980],label = "Fs(t):Caso")
ts,pi = ctrl.forced_response(sysPID,t,Vs,x0)
plt.plot(t,pi,':', linewidth = 3, color = [1,0,1], label = 'Fs(t):Tratamiento')
plt.grid(False)

#Configuracion de limites
plt.xlim(0, 10)
plt.xticks(np.arange(0, 11, 1))
plt.ylim(-3, 3)
plt.yticks(np.arange(-3, 3.5, 0.5))
 
#Personalizacion de la grafica   
plt.title("Insuficiencia cardiaca", fontsize = 13) #Titulo de la grafica        
plt.xlabel('$t$[segundos]', fontsize = 11) #Etiqueta EjeX
plt.ylabel('$V(t)$ [Flujo]', fontsize = 11) #Etiqueta EjeY
plt.legend(bbox_to_anchor = (0.5,-0.23),loc = 'center',ncol = 4) #Caja de leyendas

fig.set_size_inches(w, h) #Configuracion de tamaño de imagen
fig.tight_layout() 
namepng = 'insuficiencia_cardiaca' + '.png'
namepdf = 'insuficiencia_cardiaca' + '.pdf'
fig.savefig(namepng, dpi = 600,bbox_inches = 'tight')
fig.savefig(namepdf, bbox_inches = 'tight')

