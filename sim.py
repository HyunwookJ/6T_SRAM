import os
import subprocess


def run_ngspice(template_path, subs, out_files=(), tmp="tmp.cir"):
    """템플릿의 키워드를 치환해 ngspice를 batch 실행하고 stdout을 돌려준다.

    - 실행 전에 out_files를 지워서, 시뮬레이션이 실패했을 때 이전 결과를 읽는 일을 막는다.
    - ngspice가 실패하거나 출력 파일이 생기지 않으면 예외를 던진다.
    """
    with open(template_path) as f:
        netlist = f.read()
        
    for key, value in subs.items():
        netlist = netlist.replace(key, str(value))

    for path in out_files:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        if os.path.exists(path):
            os.remove(path)

    with open(tmp, "w") as f:
        f.write(netlist)

    result = subprocess.run(["ngspice", "-b", tmp], capture_output=True, text=True)
    missing = [p for p in out_files if not os.path.exists(p)]

    if result.returncode != 0 or missing:
        raise RuntimeError(
            f"ngspice 실패 ({template_path}, returncode={result.returncode}, "
            f"missing={missing})\n{result.stdout[-800:]}\n{result.stderr[-800:]}"
        )
    
    return result.stdout
