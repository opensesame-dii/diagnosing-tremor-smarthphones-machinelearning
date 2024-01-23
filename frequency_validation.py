import math
import numpy.fft as fft
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

def postprocess(x:np.complex128):
    return np.abs(x)

if __name__ == "__main__":
    #sample_rate = 50.711552
    file_path = "var\\accelerometerRecording\july 22 2015\AYG\leg\VibrationData 2015-07-22 at 16 04 02-email.csv"
    f = open(file_path)

    for i in range(10):
        line = f.readline()
    
    sample_rate = 50
    
    line = f.readline()
    print("line:",line)

    t = []
    x = []
    y = []
    z = []
    u = []
    all_axes = []
    
    zero = [] #list of when peak (slope_cur < 0 & slope-prev > 0) occurs for given direction (axe_ind)
        
    while line != "":
        line = f.readline()
        line = line.strip()
        line_list = line.strip().split(",")
        line_len = len(line_list)
        if line == "" or line_len < 4:
            break
        
        #Obtains the current time and position and stores them in the corresponding arrays
        t_cur = float(line_list[0])
        x_cur = float(line_list[1])
        y_cur = float(line_list[2])
        z_cur = float(line_list[3])
        u_cur = math.sqrt(x_cur**2 + y_cur**2 + z_cur**2) #u = sqrt(x^2 + y^2 + z^2), and hence is a composite of x, y, z and u
        t.append(t_cur)
        x.append(x_cur)
        y.append(y_cur)
        z.append(z_cur)
        u.append(u_cur)
        #all_axes.append([x_cur,y_cur,z_cur,u_cur])
    for i in range(3):
        f.readline()
    x_original = []
    y_original = []
    z_original = []

    line_len = 4
    while line_len>=4:
        line = f.readline()
        line = line.strip()
        line_list = line.strip().split(",")
        line_len = len(line_list)
        if line_len <4:
            break
       
        x_original.append(float(line_list[1]))
        y_original.append(float(line_list[2]))
        z_original.append(float(line_list[3]))
    x_original = np.array(x_original)
    y_original = np.array(y_original)
    z_original = np.array(z_original)

    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    x_trend_removed = x - np.mean(x)
    y_trend_removed = y - np.mean(y)
    z_trend_removed = z - np.mean(z)


    x_fft = fft.fft(x_trend_removed * np.hamming(len(x)))
    y_fft = fft.fft(y_trend_removed * np.hamming(len(x)))
    z_fft = fft.fft(z_trend_removed * np.hamming(len(x)))
    x_fft = postprocess(x_fft)
    y_fft = postprocess(y_fft)
    z_fft = postprocess(z_fft)
    freq_fft = fft.fftfreq(len(x_fft), 0.5/25.355479)
    # freq_fft = abs(fft.fftfreq(len(x_fft)))*sample_rate
    with open(f"{file_path}_fft.csv","w") as f:
        f.write("frequency, x_fft, y_fft, z_fft \n")
        for i in range(len(x_fft)//2):
            f.write(f"{freq_fft[i]}, {x_fft[i]}, {y_fft[i]}, {z_fft[i]}\n")
    
    fig = plt.figure()
    ax1 = fig.add_subplot(2,2,1)
    ax2 = fig.add_subplot(2,2,2)
    ax3 = fig.add_subplot(2,2,3)
   
    length = len(x_fft)//2

    ax1.plot(freq_fft[:length], x_fft[:length] / np.max(x_fft[:length]), label = "ours" )
    ax2.plot(freq_fft[:length], y_fft[:length] / np.max(y_fft[:length]), label = "ours" )
    ax3.plot(freq_fft[:length], z_fft[:length] / np.max(z_fft[:length]), label = "ours" )
    ax1.plot(freq_fft[:length], x_original[:length] / np.max(x_original[:length]), label = "original" )
    ax2.plot(freq_fft[:length], y_original[:length] / np.max(y_original[:length]), label = "original" )
    ax3.plot(freq_fft[:length], z_original[:length] / np.max(z_original[:length]), label = "original" )
    ax1.legend()
    ax2.legend()
    ax3.legend()

    print(np.max(x_fft[:length]) / np.max(x_original[:length]))
    print(np.max(y_fft[:length]) / np.max(y_original[:length]))
    print(np.max(z_fft[:length]) / np.max(z_original[:length]))

    fig.tight_layout()
    plt.show()


    



