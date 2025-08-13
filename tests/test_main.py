from ..maino import sm

def test_sm():
    assert sm(2,4)==6
    assert sm(2, 7) == 9


def exe_cmd_to_file(cmd, output_file, check_status=True):
    try:
        with open(output_file, "wb") as f:
            p = sp.Popen(cmd, stdout=f, stderr=sp.PIPE, shell=True)
            _, errors = p.communicate()

        if p.returncode != 0 and check_status:
            raise Exception(f"cmd: {cmd} failed to execute: {errors.decode('utf-8')}")
        
        return output_file  # Path to saved file
    except Exception as e:
        raise Exception(f"Error executing cmd: {repr(e)}")
