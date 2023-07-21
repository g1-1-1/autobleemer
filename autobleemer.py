import subprocess
import ctypes
import os

tools = os.path.join(os.getcwd(), "tools")


def is_admin():
    """are we running as administrator?"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_cdrecord(scsi_id, speed):
    """this is just a full port of the bash commands using subprocess."""
    cdrecord = os.path.join(tools, "cdrecord")
    mkisofs = os.path.join(tools, "mkisofs")
    ippatch = os.path.join(tools, "ippatch")
    data_iso = os.path.join(tools, "data.iso")
    data_path = os.path.join(tools, "data/")
    ip_bin = os.path.join(tools, "IP.BIN")

    with open("msinfo.txt", "w") as f:
        subprocess.run([cdrecord, f"-dev={scsi_id}", "-msinfo"], stdout=f)

    print("Creating data.iso with mkisofs...")
    mkisofs_process = subprocess.run(
        [mkisofs, "-C", "@msinfo.txt", "-V", "BLEEM!", "-l", "-o", data_iso, data_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if any(
        error_phrase in mkisofs_process.stderr
        for error_phrase in ["No such file or directory", "Invalid node", "Malformed"]
    ):
        raise RuntimeError("mkisofs error: " + mkisofs_process.stderr)
    else:
        print("mkisofs completed.")

    os.remove("msinfo.txt")
    print("msinfo deleted.")

    print("patching data.iso with ippatch...")
    ippatch_process = subprocess.run(
        [ippatch, data_iso, ip_bin],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if any(
        error_phrase in ippatch_process.stderr
        for error_phrase in ["No such file or directory", "can't open"]
    ):
        raise RuntimeError("ippatch error: " + ippatch_process.stderr)
    else:
        print("ippatch completed.")

    subprocess.run([cdrecord, f"-dev={scsi_id}", "-xa1", f"speed={speed}", data_iso])
    print("data.iso burn completed.")

    subprocess.run([cdrecord, f"-dev={scsi_id}", "-eject"])
    print("ejected disc from drive.")
    os.remove(data_iso)
    print("data.iso deleted.")


def get_first_cd_drive():
    """acquire the first drive in sequence by parsing the output of cdrecord"""
    try:
        cdrecord_path = os.path.join(tools, "cdrecord")
        output = subprocess.check_output(
            [cdrecord_path, "-scanbus"], universal_newlines=True
        )
        lines = output.split("\n")
        for line in lines:
            if "CD-ROM" in line:
                scsi_id = line.split()[0]
                return scsi_id
    except subprocess.CalledProcessError:
        return None


def main():
    if not is_admin():
        # the user should be running this as admin
        print(
            "insufficient privileges! this script needs to be ran as an administrator.",
        )
        return

    # get the first CD drive available
    scsi_id = get_first_cd_drive()
    if scsi_id is None:
        print("error!\n", "no CD drive found.")
        return

    speed = "10"  # refactor out of existence

    # run the CD recording process
    run_cdrecord(scsi_id, speed)

    # print completion
    print("successfully bleemed!\nyou're all done! happy bleem!castin'..")


if __name__ == "__main__":
    main()
