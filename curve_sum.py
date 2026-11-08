import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def snm(v_in, v_out):
    
    """VTC 하나로 SNM을 계산한다 (대칭 셀 가정)."""
    # 1) 45도 회전 좌표: u는 (1,-1) 방향, v는 (1,1) 방향
    u = (v_in - v_out) / np.sqrt(2)
    v = (v_in + v_out) / np.sqrt(2)

    # 2) np.interp는 x가 증가하는 순서여야 해서 u 기준으로 정렬
    order = np.argsort(u)
    u, v = u[order], v[order]

    # 3) 뒤집은 곡선은 u의 부호만 바뀐 곡선: v_B(u) = v_A(-u)
    u_grid = np.linspace(u.min(), u.max(), 4000)
    v_a = np.interp(u_grid, u, v)
    v_b = np.interp(-u_grid, u, v, left=np.nan, right=np.nan)

    ok = ~np.isnan(v_b)                               # NaN이 아닌 위치
    u_grid, v_a, v_b = u_grid[ok], v_a[ok], v_b[ok]   # 세 배열을 같은 마스크로
    d = v_a - v_b    

    # 4) 눈 두 개: d의 최댓값, -d의 최댓값 중 작은 쪽 / sqrt(2) = 정사각형 한 변
    i = d.argmax() if d.max() <= -d.min() else d.argmin()
    side = abs(d[i]) / np.sqrt(2)

    # 그 지점의 두 곡선 위 점 = 정사각형의 마주 보는 꼭짓점 (u, v -> x, y)
    x_a, y_a = (u_grid[i] + v_a[i]) / np.sqrt(2), (v_a[i] - u_grid[i]) / np.sqrt(2)
    x_b, y_b = (u_grid[i] + v_b[i]) / np.sqrt(2), (v_b[i] - u_grid[i]) / np.sqrt(2)

    return side, (min(x_a, x_b), min(y_a, y_b))