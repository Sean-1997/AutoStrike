import os
import time
from sys import exit, executable
from platform import release
from ctypes import windll
from os import system
from math import atan
from win32api import GetCurrentProcessId, OpenProcess
from win32con import PROCESS_ALL_ACCESS
from win32process import SetPriorityClass
from subprocess import ABOVE_NORMAL_PRIORITY_CLASS

# 预加载为睡眠函数做准备
import cv2

TimeBeginPeriod = windll.winmm.timeBeginPeriod
HPSleep = windll.kernel32.Sleep
TimeEndPeriod = windll.winmm.timeEndPeriod


# 简单检查gpu是否够格
def check_gpu():
    import nvidia_smi
    import pynvml
    try:
        pynvml.nvmlInit()
        gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(0)  # 默认卡1
        gpu_name = pynvml.nvmlDeviceGetName(gpu_handle)
        memory_info = pynvml.nvmlDeviceGetMemoryInfo(gpu_handle)
        pynvml.nvmlShutdown()
    except FileNotFoundError as e:
        # pynvml.nvml.NVML_ERROR_LIBRARY_NOT_FOUND
        print(str(e))
        nvidia_smi.nvmlInit()
        gpu_handle = nvidia_smi.nvmlDeviceGetHandleByIndex(0)  # 默认卡1
        gpu_name = nvidia_smi.nvmlDeviceGetName(gpu_handle)
        memory_info = nvidia_smi.nvmlDeviceGetMemoryInfo(gpu_handle)
        nvidia_smi.nvmlShutdown()
    if b'RTX' in gpu_name:
        return 2
    memory_total = memory_info.total / 1024 / 1024
    if memory_total > 3000:
        return 1
    return 0


# 高DPI感知
def set_dpi():
    if int(release()) >= 7:
        try:
            windll.shcore.SetProcessDpiAwareness(1)
        except AttributeError:
            windll.user32.SetProcessDPIAware()
    else:
        exit(0)


# 检测是否全屏
def is_full_screen(hWnd):
    try:
        full_screen_rect = (0, 0, windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))
        window_rect = win32gui.GetWindowRect(hWnd)
        return window_rect == full_screen_rect
    except Exception as e:
        print('全屏检测错误\n' + str(e))
        return False


# 检查是否为管理员权限
def is_admin():
    try:
        return windll.shell32.IsUserAnAdmin()
    except OSError as err:
        print('OS error: {0}'.format(err))
        return False


# 重启脚本
def restart(file_path):
    windll.shell32.ShellExecuteW(None, 'runas', executable, file_path, None, 1)
    exit(0)


# 清空命令指示符输出
def clear():
    _ = system('cls')


# 比起python自带sleep稍微精准的睡眠
def millisleep(num):
    TimeBeginPeriod(1)
    HPSleep(int(num))  # 减少报错
    TimeEndPeriod(1)


# 简易FOV计算
def FOV(target_move, base_len):
    actual_move = atan(target_move / base_len) * base_len  # 弧长
    return actual_move


def set_high_priority(pid=None, handle=None):
    if pid is None:
        pid = GetCurrentProcessId()
    if handle is None:
        handle = OpenProcess(PROCESS_ALL_ACCESS, True, pid)
    SetPriorityClass(handle, ABOVE_NORMAL_PRIORITY_CLASS)


if __name__ == '__main__':
    import win32gui

    import win32api

    dc = win32gui.GetDC(0)

    red = win32api.RGB(255, 0, 0)

    win32gui.SetPixel(dc, 100, 100, red)  # draw red at 0,0

    time.sleep(10)
