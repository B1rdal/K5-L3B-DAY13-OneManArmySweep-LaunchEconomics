# Hồ sơ launch v0 · Trợ lý hoàn phí LogiX-VN · Gate 2a

Đào Đức Sơn-2A202604105 · L3B

Phạm vi đề xuất gồm `noi_dia` và `hang_nang`. Nhân viên tiếp tục xử lý `quoc_te` và `doi_tac`.

| Mục | Bằng chứng chính | Trạng thái | Vai trò phụ trách |
|---|---|---|---|
| 1 · Chi phí mỗi việc thành công | Toàn mẫu: 4.471,97 đ mỗi ca trên 978 ca thành công, trước cố định (simulated). [A2](bang_chi_phi.md#a2--chi-phí-từ-trace) | Giả lập | Chuyên viên phân tích chi phí |
| 2 · Ba yếu tố nhạy nhất | Làm lại +51,77%, xem lại +40,70%, lương +23,12% trong các kịch bản B1 (simulated). [B1–B2](bang_chi_phi.md) | Giả lập | PM trợ lý hoàn phí |
| 3 · So với nhân viên tự làm | Cả hệ thống 5.864,65 đ/yêu cầu trước cố định so với 12.000 đ. CPS trong phạm vi ở 45.000 yêu cầu/tháng là 4.599,09 đ gồm cố định (simulated). [A2–A4](bang_chi_phi.md) | Giả lập | Giám đốc vận hành |
| 4 · Kết quả, sử dụng, an toàn | Đóng 24 giờ và không mở lại 82,83%, sửa/bỏ 27,12%, mở lại 4,25% trong mẫu chạy thử. [E1](chi_so.md) | Xong, có bằng chứng | Chuyên viên phân tích sản phẩm |
| 5 · Lỗi và khắc phục | Có 20 nhãn tham chiếu và 5 biện pháp. Chưa đo đồng thuận giữa người gắn nhãn. [C](bang_loi.md) | Chưa | Trưởng nhóm QA |
| 6 · Thiết kế pilot | 20 nhân viên/nhánh, 299 yêu cầu/người cho mức chênh +6 điểm. Power chỉ 64,2% nếu tác động là +5 điểm. Có 4 luật dừng. [D](pilot_plan.yaml) | Xong, có bằng chứng | Giám đốc vận hành |
| 7 · Rủi ro kinh tế | Review 100% và làm lại 15,3 phút đưa CPS lên 12.414,79 đ, trên baseline 12.000 đ (simulated). [E2](chi_so.md) | Giả lập | Trưởng nhóm CSKH |

Các điều kiện kiểm tra trước khi mở pilot vào ngày dự kiến 07/12/2026:

- Kỹ sư trưởng agent kiểm tra khóa chống hoàn trùng và đối soát sổ cái trước ngày 04/12/2026. Trưởng nhóm QA hoàn tất hai lượt gắn nhãn và rà biện pháp xử lý vào cùng ngày.
- Giám đốc vận hành xác nhận đủ 40 nhân viên, lượng yêu cầu mỗi nhánh và chấp nhận độ nhạy +6 điểm trước ngày 04/12/2026.
- Trưởng nhóm CSKH kiểm tra event và phép đo phút thật trước ngày 04/12/2026. Ngày 14/12/2026, rà chi phí tuần đầu và giữ nấc hiện tại nếu dữ liệu hoặc an toàn chưa đạt.

**Đề xuất: Go có điều kiện.**
