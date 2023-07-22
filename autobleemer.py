import subprocess
import ctypes
import os
import tkinter as tk
from tkinter import messagebox

# globals
tools: str = os.path.join(os.getcwd(), "tools")
root: tk.Tk = tk.Tk()
root.iconbitmap("assets/icon.ico")
debug: bool = False
status_label: tk.Label  # type hint for the status_label


def is_admin() -> bool:
    """are we running as administrator?"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def update_status(status_text: str) -> None:
    """update top-left status box."""
    global status_label  # use the global status_label
    status_label.config(text=status_text)
    root.update_idletasks()
    if debug:
        print(status_text)


def run_cdrecord(scsi_id: str, speed: str) -> None:
    """this is just a full port of the bash commands using subprocess."""
    cdrecord: str = os.path.join(tools, "cdrecord")
    mkisofs: str = os.path.join(tools, "mkisofs")
    ippatch: str = os.path.join(tools, "ippatch")
    data_iso: str = os.path.join(tools, "data.iso")
    data_path: str = os.path.join(tools, "data/")
    ip_bin: str = os.path.join(tools, "IP.BIN")
    msinfo: str = os.path.join(tools, "msinfo.txt")

    with open(msinfo, "w") as f:
        subprocess.run([cdrecord, f"-dev={scsi_id}", "-msinfo"], stdout=f)

    update_status("creating data.iso with mkisofs...")
    if debug:
        print(
            "mkisofs command:",
            [
                mkisofs,
                "-C",
                f"@{msinfo}",
                "-V",
                "BLEEM!",
                "-l",
                "-o",
                data_iso,
                data_path,
            ],
        )
    mkisofs_process = subprocess.run(
        [mkisofs, "-C", f"@{msinfo}", "-V", "BLEEM!", "-l", "-o", data_iso, data_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # display stdout and stderr from mkisofs_process
    if debug:
        print("mkisofs stdout:", mkisofs_process.stdout)
        print("mkisofs stderr:", mkisofs_process.stderr)

    if any(
        error_phrase in mkisofs_process.stderr
        for error_phrase in ["No such file or directory", "Invalid node", "Malformed"]
    ):
        update_status("mkisofs error: " + mkisofs_process.stderr)
        raise RuntimeError("mkisofs error: " + mkisofs_process.stderr)
    else:
        update_status("mkisofs completed.")

    os.remove(msinfo)
    update_status("msinfo deleted.")

    update_status("\npatching data.iso with ippatch...")
    if debug:
        print(
            "ippatch command:",
            [
                ippatch,
                data_iso,
                ip_bin,
            ],
        )
    ippatch_process = subprocess.run(
        [ippatch, data_iso, ip_bin],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # display stdout and stderr from ippatch_process
    if debug:
        print("ippatch stdout:", ippatch_process.stdout)
        print("ippatch stderr:", ippatch_process.stderr)

    if any(
        error_phrase in ippatch_process.stderr
        for error_phrase in ["No such file or directory", "can't open"]
    ):
        update_status("ippatch error: " + ippatch_process.stderr)
        raise RuntimeError("ippatch error: " + ippatch_process.stderr)
    else:
        update_status("ippatch completed.")

    update_status("\nstarting data.iso burn...")
    if debug:
        print(
            "cdrecord command:",
            [
                cdrecord,
                f"-dev={scsi_id}",
                "-xa1",
                f"speed={speed}",
                data_iso,
            ],
        )
    cdrecord_process = subprocess.run(
        [cdrecord, f"-dev={scsi_id}", "-xa1", f"speed={speed}", data_iso],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # display stdout and stderr from cdrecord_process
    if debug:
        print("cdrecord stdout:", cdrecord_process.stdout)
        print("cdrecord stderr:", cdrecord_process.stderr)

    if (
        "No such file or directory" in cdrecord_process.stdout
        or "can't open" in cdrecord_process.stdout
        or "No such file or directory" in cdrecord_process.stderr
        or "can't open" in cdrecord_process.stderr
    ):
        update_status("cdrecord error: " + cdrecord_process.stderr)
        raise RuntimeError("cdrecord error: " + cdrecord_process.stderr)
    else:
        update_status("data.iso burn completed.")

    os.remove(data_iso)
    update_status("data.iso deleted.")


def get_first_cd_drive() -> str:
    """acquire the first drive in sequence by parsing the output of cdrecord"""
    try:
        cdrecord_path: str = os.path.join(tools, "cdrecord")
        output: str = subprocess.check_output(
            [cdrecord_path, "-scanbus"], universal_newlines=True
        )
        lines: List[str] = output.split("\n")
        for line in lines:
            if "CD-ROM" in line:
                scsi_id: str = line.split()[0]
                return scsi_id
    except subprocess.CalledProcessError:
        return None


def main() -> None:
    global status_label

    if not is_admin():
        # the user should be running this as admin
        messagebox.showerror(
            "insufficient privileges",
            "this program needs to be run as an administrator.",
        )
        return

    # create the main window
    root.title("autobleemer")

    # define the GUI elements
    status_label = tk.Label(root, text="initialising", padx=10, pady=10)
    status_label.pack()

    # tell the user to wait for everything to finish
    messagebox.showinfo(
        "starting to autobleem...",
        "please wait for everything to finish! do not close any windows without a prompt.",
    )

    # get the first CD drive available
    scsi_id: str = get_first_cd_drive()
    if scsi_id is None:
        messagebox.showerror("error!", "no CD drive found.")
        root.destroy()
        return

    speed: str = "10"  # refactor out of existence

    try:
        # run the CD recording process
        run_cdrecord(scsi_id, speed)

        # display completion message
        messagebox.showinfo(
            "successfully bleemed!", "you're all done! happy bleem!castin'.."
        )
    except Exception as e:
        if debug:
            print(e)
        messagebox.showerror(
            "error!",
            f"something happened...\n\n{str(e)}\nif you believe this is in error, report it on github.",
        )

    # close the main window
    root.destroy()
    root.mainloop()


if __name__ == "__main__":
    main()
