import tkinter as tk
from tkinter import ttk, scrolledtext
from ttkbootstrap.constants import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import *
import paramiko
import threading
from utils import containers, options
from utils import RVIZ_TEMPLATE, LOCAL_HOSTNAME, REMOTE_HOSTNAME
import subprocess


# establish ssh

is_start = False

def run_ssh_command(ssh_info, text_widget):
    hostname = ssh_info["hostname"]
    username = ssh_info["username"]
    password = ssh_info["password"]
    command = ssh_info["command"]

    # create ssh
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        # connect to ssh
        ssh.connect(hostname, username=username, password=password, timeout=10)
        text_widget.insert(tk.END, f"successfully connect {hostname}\n")

        # exec
        stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
        while True:
            line = stdout.readline()
            if not line:
                break
            text_widget.insert(tk.END, line)
        text_widget.insert(tk.END, "finish\n")

        # output error
        error = stderr.read().decode()
        if error:
            text_widget.insert(tk.END, f"error:\n{error}\n")

    except Exception as e:
        print(f"[ERROR]: {e}\n")
        text_widget.insert(tk.END, f"error: {e}\n")
    finally:
        ssh.close()


def on_select(text_widget):
    global is_start
    if not is_start:
        selected_option = dropbox.get()
        if selected_option in options:
            ssh_info = options[selected_option]
            threading.Thread(target=run_ssh_command, args=(ssh_info, text_widget), daemon=True).start()
            control_button.config(text = "stop",bootstyle=DANGER)
          
    else:
        stop_current_containers(options[dropbox.get()], containers[dropbox.get()],output_log_text)
        control_button.config(text = "start", bootstyle=INFO)
    
    is_start = not is_start


# Function to clear text widgets
def clear_text_widgets(text_widgets):
    for widget in text_widgets:
        widget.delete('1.0', tk.END)


# Function to stop Docker containers
def stop_current_containers(ssh_info, container_names, text_widget):
    control_button.configure(state="disabled")
    for container in container_names:
        print(f"[INFO]: start stopping container:{container}")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ssh_info["hostname"], username=ssh_info["username"], password=ssh_info["password"], timeout=10)
        for container in container_names:
            command = f"docker stop {container}"
            ssh.exec_command(command)
        for container in container_names:
            print(f"[INFO]: successfully stopped {container}")
    except Exception as e:
        print(f"[ERROR]: stop container failed: {e} ")
        text_widget.insert(tk.END, f"[ERROR]: stop container failed: {e}\n ")
    finally:
        ssh.close()
        control_button.configure(state="enabled")


# Function to stop Docker containers

def stop_running_containers(selected_option):
    
    ssh_info = options[selected_option]
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"[INFO]:stop running containers ...")
        ssh.connect(ssh_info["hostname"], username=ssh_info["username"], password=ssh_info["password"], timeout=10)
        command = f"""
        if [ "$(docker ps -q)" ];then
            docker stop $(docker ps -q) 
        fi
        """
        ssh.exec_command(command)

    except Exception as e:
        print(f"[ERROR]:stop running containers failed: {e} ")
    finally:
        ssh.close()


def quit():
    selected_option = dropbox.get()
    threading.Thread(target=stop_running_containers, args={selected_option}).start()
    root.destroy()
    print("[INFO]: Quit ")


def open_rviz():
    selected_option = dropbox.get()
    rviz_templete = RVIZ_TEMPLATE[selected_option]
    if selected_option == "fast-livo" or selected_option == "fast-lio-ros1":

        # Command to run RViz in the Docker container
        command = f"""
        docker exec ros1-visualizer bash -c "
        export ROS_IP={LOCAL_HOSTNAME}  
        export ROS_HOSTNAME={LOCAL_HOSTNAME} 
        export ROS_MASTER_URI=http://{REMOTE_HOSTNAME}:11311  
        source ros_entrypoint.sh && rviz -d {rviz_templete}" 
        echo "close rviz"
        """
        subprocess.Popen(command, shell=True)
    else:
        command = f"""
        docker exec ros2-visualizer bash -c "source ros_entrypoint.sh && rviz2 -d {rviz_templete}" 
        echo "close rviz"
        """
        subprocess.Popen(command, shell=True)

def start_visulizer():
    subprocess.Popen("docker start ros2-visualizer && docker start ros1-visualizer", shell=True)

def stop_visulizer():
    subprocess.Popen("docker stop ros2-visualizer && docker stop ros1-visualizer", shell=True)

if __name__ == "__main__":
    start_visulizer()
    root = tk.Tk()
    root.title("Orin GUI")
    root.protocol("WM_DELETE_WINDOW", quit)

    setting_frame = tk.Frame(root)

    label = ttk.Label(setting_frame, text="Select Application：")
    label.grid(row=0, column=0, pady=10, sticky="e")

    # drop box
    dropbox = ttk.Combobox(setting_frame, values=list(options.keys()), width=20, bootstyle="info-reversed")
    dropbox.current(0)
    dropbox.grid(row=0, column=1, pady=10, sticky="we")


    # start button
    control_button = ttk.Button(setting_frame, text="Start", command=lambda: on_select(output_log_text), bootstyle=INFO)
    control_button.grid(row=0, column=2, padx=10, pady=10, sticky="we")

    # # Button to stop Docker containers
    # stop_button = ttk.Button(setting_frame, text="Stop", bootstyle=DANGER,
    #                             command=lambda: stop_current_containers(options[dropbox.get()], containers[dropbox.get()],
    #                                                                     output_log_text))
    # stop_button.grid(row=0, column=3, padx=10, pady=10, sticky="we")

    # Button to clear output
    clear_button = ttk.Button(setting_frame, text="Clear Log", command=lambda: clear_text_widgets([output_log_text]))
    clear_button.grid(row=0, column=4, padx=10, pady=10, sticky="we")

    # Button to open rviz
    open_button_rviz2 = ttk.Button(setting_frame, text="Open RViz", command=open_rviz, bootstyle=SUCCESS)
    open_button_rviz2.grid(row=0, column=5, padx=10, pady=10, sticky="we")

    setting_frame.pack()
    log_frame = tk.Frame(root)

    # output log
    output_log_text = scrolledtext.ScrolledText(log_frame, width=150, height=50)
    output_log_text.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
    log_frame.pack()

    root.mainloop()

    start_visulizer()
