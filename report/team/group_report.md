# Báo cáo nhóm · Lab 13

## 1. Thông tin nhóm

- Tên bài nộp: Đào Đức Sơn-2A202604105
- Lớp: L3B
- Thành viên và phần việc: xem [TEAM.md](../../TEAM.md).

## 2. Mục tiêu và cách tiếp cận

Đánh giá chi phí của trợ lý hoàn phí LogiX-VN trên 1.200 yêu cầu và 1.624 lượt chạy giả lập, sau đó đề xuất pilot có đối chứng. Mô hình tách chi phí trợ lý, nhân viên xử lý phần còn lại và chi phí cố định.

## 3. Giải pháp

- A–B: chạy [chương trình phân tích](../../src/lab13.py), so các kịch bản và đối chiếu số trong [bảng chi phí](bang_chi_phi.md).
- C: lập [bảng đối chiếu nhãn tham chiếu cho 20 ca và biện pháp khắc phục](bang_loi.md) cho năm loại lỗi. Chưa có tỉ lệ đồng thuận giữa hai người gắn nhãn.
- D–E: tính cỡ mẫu, viết [kế hoạch pilot](pilot_plan.yaml), đặc tả [chỉ số và event](chi_so.md) và tổng hợp [hồ sơ Gate 2a](ho_so_launch_v0.md).

## 4. Kết quả

CPS trước cố định là 4.471,97 đ và chi phí hệ thống trước cố định là 5.864,65 đ/yêu cầu (simulated). Trong ba giới hạn lượt chạy, 2 lượt cho tổng hệ thống thấp nhất (6.901.220,23 đ simulated trên mẫu). Đề xuất Go có điều kiện cho `noi_dia` và `hang_nang`. Nhóm Economics đánh giá bài nộp này tại Gate 2a. [Phiếu chấm](phieu_cham.md) chưa có kết quả.

## 5. Khó khăn và cách xử lý

Python mặc định ban đầu thiếu thư viện. Đã cài các gói theo `src/requirements.txt` vào môi trường ảo và chạy lại chương trình. Ba phép thử A1 đạt 1,20 · 1,25 · 1,25. Đối chiếu A2: (245.585,13 + 84.000 + 1.780.000 + 2.264.000) ÷ 978 ≈ 4.471,97 đ (simulated).

## 6. Tổng hợp đóng góp

Đào Đức Sơn phụ trách phân tích chi phí, phân tích ca lỗi và hồ sơ pilot. Xem [TEAM.md](../../TEAM.md) và [báo cáo cá nhân](2A202604105_DaoDucSon.md).

## 7. Hạn chế và hướng cải thiện

Đợt chạy thử thiếu đối chứng đồng thời, nên 82,83% chỉ mô tả mẫu. Pilot phân nhóm 20 nhân viên mỗi nhánh, hướng tới 299 yêu cầu/người để phát hiện mức chênh +6 điểm, và dùng phút thao tác thực đo để thay số phút giả lập.

## 8. Tài liệu tham khảo

- [Dữ liệu và công thức của lab](../../docs/du_lieu_va_cong_thuc.md)
- [Hướng dẫn chi tiết các nhiệm vụ A–E](../../docs/Lab13_Huong_dan_chi_tiet_buoi_chieu.md)
