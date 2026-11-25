"""Lab 13 · Định giá agent và lập kế hoạch pilot (Gate 2a) — bài làm của nhóm (file nộp).
Chạy trong thư mục src/: python3 lab13.py   (cần pandas; Nhiệm vụ D cần thêm statsmodels)
Không cần khoá API. Dữ liệu trong hai file CSV là giả lập.
Bản gốc chưa sửa nằm ở lab13_starter.py.
"""
import math
from pathlib import Path
from statistics import NormalDist

import pandas as pd
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

# Bảng giá GIẢ ĐỊNH của lab (không phải giá thật của nhà cung cấp nào)
GIA_VAO = 26        # đồng cho 1.000 token đầu vào
GIA_RA = 130        # đồng cho 1.000 token đầu ra
GIA_TOOL = 15       # đồng cho 1 lần gọi tool
LUONG_PHUT = 2000   # đồng cho 1 phút của nhân viên (đã gồm bảo hiểm, văn phòng)
BASELINE = 12000    # đồng cho 1 yêu cầu khi nhân viên tự làm (6 phút)
FIXED_COST = 40_000_000
PILOT_TYPES = ("noi_dia", "hang_nang")


# ---------- Nhiệm vụ A1 · Kinh tế của việc chạy lại ----------
def so_lan_chay_ky_vong(p, k=None):
    """Số lần chạy trung bình cho 1 yêu cầu khi mỗi lần đúng với xác suất p.
    k = số lần chạy tối đa; k=None nghĩa là chạy lại đến khi đúng."""
    if p == 0:
        return math.inf if k is None else k
    return ti_le_thanh_cong(p, k) / p


def ti_le_thanh_cong(p, k=None):
    """Xác suất yêu cầu thành công sau tối đa k lần chạy."""
    if k is None:
        return float(p > 0)
    return 1 - (1 - p) ** k


def he_so_chi_phi_moi_viec_thanh_cong(p, k=None):
    """Chi phí mỗi việc thành công, tính bằng bội số của giá một lần chạy."""
    success_rate = ti_le_thanh_cong(p, k)
    return so_lan_chay_ky_vong(p, k) / success_rate if success_rate else math.inf


def kiem_tra_dap_an_biet_truoc():
    """Ba phép thử bắt buộc đạt 100% trước khi tính trên dữ liệu."""
    assert abs(so_lan_chay_ky_vong(0.8, 2) - 1.20) < 1e-9, 'p=0,8, tối đa 2 lần → 1,20 lần chạy'
    assert abs(so_lan_chay_ky_vong(0.8) - 1.25) < 1e-9, 'p=0,8, chạy đến khi đúng → 1,25 lần chạy'
    assert abs(he_so_chi_phi_moi_viec_thanh_cong(0.8, 3) - 1.25) < 1e-9, 'p=0,8, tối đa 3 lần → 1,25 lần giá một lần chạy'
    print('Ba phép thử đáp án biết trước: ĐẠT')


# ---------- Nhiệm vụ A2 · Mô hình chi phí từ trace ----------
def mo_hinh(runs, reqs, gia_vao=GIA_VAO, gia_ra=GIA_RA, gia_tool=GIA_TOOL, luong_phut=LUONG_PHUT,
            he_so_xem_lai=1.0, he_so_lam_lai=1.0, max_lan_chay=None):
    """Trả về dict gồm: token, tool, xem_lai, lam_lai, tong, thanh_cong, cps (chi phí mỗi việc thành công).
    - token, tool: cộng trên MỌI lần chạy trong runs, kể cả lần lỗi.
    - xem_lai, lam_lai: số phút (cột *_simulated) × LUONG_PHUT. Đây là số GIẢ LẬP, phải ghi nhãn simulated khi báo cáo.
    - thanh_cong: số yêu cầu có ket_qua == 'thanh_cong'.
    - Các tham số giá/hệ số/max_lan_chay dùng cho Nhiệm vụ B (độ nhạy, giới hạn số lần chạy); giữ mặc định ở A2.
    """
    runs = runs.loc[runs.request_id.isin(reqs.request_id)]
    reqs = reqs.copy()
    if max_lan_chay is not None:
        runs = runs.loc[runs.attempt <= max_lan_chay]
        diverted = reqs.so_lan_chay > max_lan_chay
        reqs.loc[diverted, 'ket_qua'] = 'chuyen_nhan_vien'
        reqs.loc[diverted, ['phut_xem_lai_simulated', 'phut_lam_lai_simulated']] = 0

    token = (runs.tokens_in * gia_vao + runs.tokens_out * gia_ra) / 1000
    tool = runs.tool_calls * gia_tool
    review = reqs.phut_xem_lai_simulated.sum() * luong_phut * he_so_xem_lai
    rework = reqs.phut_lam_lai_simulated.sum() * luong_phut * he_so_lam_lai
    total = float(token.sum() + tool.sum() + review + rework)
    successes = int(reqs.ket_qua.eq('thanh_cong').sum())
    return dict(
        token=float(token.sum()), tool=int(tool.sum()),
        chay_lai=float((token + tool).loc[runs.attempt > 1].sum()),
        xem_lai=float(review), lam_lai=float(rework), tong=total, thanh_cong=successes,
        cps=total / successes if successes else math.inf,
        hoa_don_moi_yc=float(token.sum() + tool.sum()) / len(reqs) if len(reqs) else math.nan,
    )


def co_mau(p1, p2, alpha=0.05, power=0.80):
    """Cỡ mẫu mỗi nhánh cho kiểm định hai phía của hai tỉ lệ."""
    normal = NormalDist()
    za, zb = normal.inv_cdf(1 - alpha / 2), normal.inv_cdf(power)
    mean = (p1 + p2) / 2
    variance = p1 * (1 - p1) + p2 * (1 - p2)
    return math.ceil(((za * math.sqrt(2 * mean * (1 - mean))
                       + zb * math.sqrt(variance)) / (p2 - p1)) ** 2)


def print_costs(runs, reqs):
    base = mo_hinh(runs, reqs)
    print("\nA2 | Khoản | Giá trị | Nguồn")
    simulated_fields = {'xem_lai', 'lam_lai', 'tong', 'cps'}
    for key, value in base.items():
        label = 'simulated' if key in simulated_fields else 'trace'
        print(f"{key:16s} | {value:14,.2f} | {label}")
    baseline_cost = (base['tong'] + (len(reqs) - base['thanh_cong']) * BASELINE) / len(reqs)
    print(f"A2 | CPS / hoá đơn: {base['cps'] / base['hoa_don_moi_yc']:.2f}× (simulated)")
    print(f"A2 | Phần làm lại: {base['lam_lai'] / base['tong']:.2%} (simulated)")
    print(f"A2 | Chi phí cả hệ thống / yêu cầu: {baseline_cost:,.2f} đ (simulated)")

    print("\nA3 | Loại | Yêu cầu | Thành công | Lần chạy/YC | CPS (simulated) | So với baseline")
    for kind, subset in reqs.groupby('loai', sort=False):
        costs = mo_hinh(runs, subset)
        print(f"{kind:10s} | {len(subset):4d} | {costs['thanh_cong'] / len(subset):6.2%} | "
              f"{subset.so_lan_chay.mean():.2f} | {costs['cps']:,.2f} | {costs['cps'] / BASELINE:.2f}×")
    intl = runs.loc[runs.request_id.isin(reqs.loc[reqs.loai.eq('quoc_te'), 'request_id'])]
    for attempt, cohort in intl.groupby('attempt'):
        print(f"A3 | quoc_te, lần {attempt}: {cohort.status.eq('ok').sum()}/{len(cohort)} ok")

    scope = reqs.loc[reqs.loai.isin(PILOT_TYPES)]
    scoped = mo_hinh(runs, scope)
    success_share = scoped['thanh_cong'] / len(reqs)
    print("\nA4 | Tổng yêu cầu/tháng | Thành công trong phạm vi | Cố định/việc | CPS gồm cố định (simulated) | So với baseline")
    for volume in (45_000, 22_500):
        successes = volume * success_share
        fixed = FIXED_COST / successes
        cps = scoped['cps'] + fixed
        print(f"{volume:,} | {successes:,.0f} | {fixed:,.2f} | {cps:,.2f} | {cps / BASELINE:.2f}×")
    threshold = math.ceil(FIXED_COST / (BASELINE - scoped['cps']) / success_share)
    print(f"A4 | Hòa vốn theo CPS: {threshold:,} yêu cầu/tháng (simulated)")

    scenarios = (
        ('Token ×2', dict(gia_vao=GIA_VAO * 2, gia_ra=GIA_RA * 2)),
        ('Token ×0,5', dict(gia_vao=GIA_VAO / 2, gia_ra=GIA_RA / 2)),
        ('Xem lại ×2', dict(he_so_xem_lai=2)),
        ('Xem lại ×0,5', dict(he_so_xem_lai=0.5)),
        ('Làm lại ×2', dict(he_so_lam_lai=2)),
        ('Làm lại ×0,5', dict(he_so_lam_lai=0.5)),
        ('Lương +25%', dict(luong_phut=LUONG_PHUT * 1.25)),
        ('Tối đa 2 lần', dict(max_lan_chay=2)),
        ('Chỉ 1 lần', dict(max_lan_chay=1)),
    )
    for section, cases in (('B1', scenarios),
                           ('B2', (('Token ×2 và xem lại ×2', scenarios[0][1] | scenarios[2][1]),))):
        print(f"\n{section} | Kịch bản | CPS (simulated) | Thay đổi")
        for name, options in cases:
            cps = mo_hinh(runs, reqs, **options)['cps']
            print(f"{name:25s} | {cps:,.2f} | {cps / base['cps'] - 1:+.2%}")

    print("\nB3 | Lần chạy | Tổng trợ lý | Không thành công | Tổng hệ thống | CPS (chi phí simulated)")
    for cap in (1, 2, 3):
        costs = mo_hinh(runs, reqs, max_lan_chay=cap)
        remaining = len(reqs) - costs['thanh_cong']
        system = costs['tong'] + remaining * BASELINE
        print(f"{cap} | {costs['tong']:,.2f} | {remaining} | {system:,.2f} | {costs['cps']:,.2f}")

    ok_runs = runs.loc[runs.request_id.isin(scope.request_id) & runs.status.eq('ok')]
    reviewed = ok_runs.request_id.nunique()
    reworked = scope.ket_qua.eq('lam_lai').sum()
    mean_rework = reqs.loc[reqs.ket_qua.eq('lam_lai'), 'phut_lam_lai_simulated'].mean()
    bill = scoped['token'] + scoped['tool']
    print(f"\nB4 | {reviewed} lượt xem lại × 5 phút | {reworked} ca làm lại | hoá đơn {bill:,.2f} đ")
    for minutes in (9, round(mean_rework, 1)):
        rework = reworked * minutes * LUONG_PHUT
        cps = (bill + reviewed * 5 * LUONG_PHUT + rework) / scoped['thanh_cong']
        break_even = (BASELINE * scoped['thanh_cong'] - bill - rework) / (reviewed * LUONG_PHUT)
        print(f"{minutes:.1f} phút làm lại | CPS {cps:,.2f} đ ({cps / BASELINE:.3f}×) | "
              f"Hoà vốn {break_even:.2f} phút xem lại (simulated)")


def print_pilot(reqs):
    at_five, at_six = co_mau(0.70, 0.75), co_mau(0.70, 0.76)
    icc, staff, depot, per_staff = 0.02, 20, 6, 75
    design_effect = 1 + (per_staff - 1) * icc
    min_per_staff = math.ceil(at_six * (1 - icc) / (staff - at_six * icc))
    power_five = NormalIndPower().power(proportion_effectsize(0.75, 0.70), at_six, 0.05)
    print(f"\nD1a | {at_five:,} yêu cầu/nhánh")
    print(f"D1b | DE {design_effect:.2f} | {math.ceil(at_five * design_effect):,} yêu cầu/nhánh | "
          f"{math.ceil(at_five * design_effect / per_staff)} nhân viên/nhánh")
    print(f"D1c | Trần n hiệu dụng với {staff} nhân viên/nhánh: {staff / icc:,.0f}")
    print(f"D1d | Trần n hiệu dụng với {depot} depot/nhánh: {depot / icc:,.0f}")
    print(f"D1e | {at_six} yêu cầu hiệu dụng/nhánh ở +6 điểm | {min_per_staff} yêu cầu/nhân viên | "
          f"DE {1 + (min_per_staff - 1) * icc:.2f} | power ở +5 điểm {power_five:.1%}")
    scope = reqs.loc[reqs.loai.isin(PILOT_TYPES)]
    reviewed = reqs.loc[reqs.duoc_xem_lai.eq(1)]
    print("\nE1 | Chỉ số | Tử số / Mẫu số | Tỉ lệ")
    metrics = (
        ('Đóng 24h, không mở lại 7 ngày', reqs.dong_trong_24h.eq(1) & reqs.mo_lai_trong_7_ngay.eq(0)),
        ('Sửa hoặc bỏ gợi ý', reviewed.quyet_dinh_xem_lai.isin(['sua', 'bo'])),
        ('Mở lại 7 ngày', reqs.mo_lai_trong_7_ngay.eq(1)),
        ('Mở lại 7 ngày trong phạm vi pilot', scope.mo_lai_trong_7_ngay.eq(1)),
        ('Làm lại trong phạm vi pilot', scope.ket_qua.eq('lam_lai')),
    )
    for name, mask in metrics:
        print(f"{name} | {mask.sum()}/{len(mask)} | {mask.mean():.2%}")


if __name__ == '__main__':
    kiem_tra_dap_an_biet_truoc()
    source = Path(__file__).resolve().parent
    runs = pd.read_csv(source / 'logix_runs.csv')
    reqs = pd.read_csv(source / 'logix_requests.csv', keep_default_na=False)
    print_costs(runs, reqs)
    print_pilot(reqs)
