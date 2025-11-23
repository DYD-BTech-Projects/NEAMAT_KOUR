import psutil
import json

def list_processes():
    """Return JSON serialized list of current system processes with essential details."""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return json.dumps(processes)

def kill_process(pid):
    """Attempt to kill a process by PID gracefully."""
    try:
        proc = psutil.Process(pid)
        proc.terminate()  # Graceful termination
        proc.wait(timeout=5)  # Wait for termination
        return True, f"Process {pid} terminated."
    except psutil.NoSuchProcess:
        return False, "Process does not exist."
    except psutil.AccessDenied:
        return False, "Permission denied to terminate process."
    except psutil.TimeoutExpired:
        try:
            proc.kill()  # Force kill if terminate times out
            proc.wait()
            return True, f"Process {pid} force killed."
        except Exception as e:
            return False, str(e)
    except Exception as e:
        return False, str(e)
