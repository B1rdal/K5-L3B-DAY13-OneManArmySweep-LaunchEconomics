# Chỉ số, event và rủi ro kinh tế · Nhiệm vụ E1 và E2

## E1 · Đặc tả chỉ số

Tính trên 1.200 yêu cầu LogiX-VN giả lập bằng `src/lab13.py`. Đợt chạy thử chưa có đối chứng đồng thời. Baseline 70% trong thiết kế D là giả định về luồng nhân viên.

| Loại | Chỉ số và công thức | Kết quả đợt chạy thử |
|---|---|---:|
| Chính | Số yêu cầu đóng trong 24 giờ và không mở lại trong 7 ngày sau khi đóng ÷ toàn bộ yêu cầu | 994/1.200 = 82,83% |
| Sử dụng | Yêu cầu có quyết định `sua` hoặc `bo` ÷ yêu cầu được xem lại | 48/177 = 27,12% |
| An toàn | Yêu cầu mở lại trong 7 ngày ÷ toàn bộ yêu cầu | 51/1.200 = 4,25% |
| Sử dụng, bổ sung | Yêu cầu đủ điều kiện trong nhánh can thiệp được hiển thị gợi ý ít nhất một lần ÷ tổng yêu cầu đủ điều kiện trong nhánh | Đo trong pilot |
| An toàn, bổ sung | Khoản hoàn sai số tiền ÷ khoản hoàn được chọn kiểm tra trong mẫu ngẫu nhiên tuần | Đo trong pilot |

## Event và cách tính

Mọi event có `trace_id` và `request_id`. Giữ một mã tương quan cấp yêu cầu, liên kết mọi `run_trace_id` với mã đó. Mỗi chỉ số cấp yêu cầu đếm theo `request_id` duy nhất.

| Event | Nguồn | Thuộc tính ngoài hai mã chung | Khi ghi |
|---|---|---|---|
| `refund_request_created` | Hệ thống yêu cầu | `created_at, eligible, arm, staff_id, depot, loai` | Tạo yêu cầu |
| `agent_run_completed` | Agent | `run_trace_id, attempt, tokens_in, tokens_out, tool_calls, status` | Sau mỗi lượt, gồm cả lỗi |
| `agent_suggestion_shown` | Giao diện CSKH | `shown_at, staff_id, arm` | Gợi ý xuất hiện |
| `staff_review_decision` | Giao diện CSKH | `decision, review_minutes` | Nhân viên giữ, sửa hoặc bỏ |
| `staff_rework_completed` | Giao diện CSKH | `rework_minutes, reason` | Hoàn tất làm lại |
| `manual_resolution_completed` | Giao diện CSKH | `manual_minutes, reason` | Hoàn tất xử lý thủ công |
| `refund_ledger_write` | Sổ cái | `refund_obligation_id, idempotency_key, amount_vnd, status` | Ghi kết quả lệnh hoàn |
| `handoff_to_staff` | Agent | `reason, summary_present` | Chuyển nhân viên |
| `ticket_closed` | Hệ thống yêu cầu | `closed_at` | Mỗi lần đóng |
| `ticket_reopened` | Hệ thống yêu cầu | `reopened_at, reason` | Mỗi lần mở lại |
| `audit_sample_checked` | Kế toán | `sample_week, audited_amount, expected_amount` | Đối soát mẫu |
| `refund_input_rejected` | Bộ kiểm tra đầu vào | `reason, bank_code` | Từ chối đầu vào không hợp lệ |
| `refund_notice_sent` | Dịch vụ thông báo | `sent_at, customer_timezone, after_hours_opt_in` | Gửi thông báo hoàn phí |

- **Chính và mở lại:** Nối `refund_request_created`, `ticket_closed` và `ticket_reopened`. Dùng lần đóng đầu tiên, giữ cả yêu cầu không đóng trong mẫu số của chỉ số chính, và đợi hết cửa sổ theo dõi trước khi chốt cohort.
- **Sửa hoặc bỏ:** Dùng `staff_review_decision`, lấy quyết định cuối trên mỗi yêu cầu đã xem lại. **Hiển thị gợi ý:** Nối `agent_suggestion_shown` với cohort có `eligible=true` và thuộc nhánh can thiệp.
- **Sai tiền:** So `audited_amount` với `expected_amount` trong `audit_sample_checked`. **Chi phí cả hệ thống:** Kết hợp lượt chạy, phút xem lại, phút làm lại, phút xử lý thủ công và chi phí cố định phân bổ. Đối soát thời gian để tránh tính trùng phần nhân viên.

## E2 · Rủi ro kinh tế

| Rủi ro | Tác động đã tính | Dấu hiệu theo dõi | Hành động | Vai trò |
|---|---|---|---|---|
| Chi phí làm lại tăng gấp đôi | CPS lên 6.786,90 đ (+51,77%, simulated) | Tỉ lệ làm lại vượt 7%/tuần, so với 48/982 = 4,89% trong mẫu thuộc phạm vi | Rà 20 trace làm lại và giữ phạm vi nếu chưa xác định được nguyên nhân | PM trợ lý hoàn phí |
| Duy trì xem lại mọi ca có lượt ok | 11.742,79 đ ở 9 phút làm lại và 12.414,79 đ ở 15,3 phút (simulated) | Review vẫn trên 50% cuối nấc 25%, hoặc thời gian trung bình vượt 4,80 phút | Đo phút thật và thử giảm review theo bậc sau khi đạt ngưỡng an toàn | Trưởng nhóm CSKH |
| Lượng yêu cầu chỉ bằng nửa dự kiến | Cố định tăng từ 1.185,19 lên 2.370,37 đ/việc theo dự phóng (simulated) | Lượng ca thành công dưới 50% kế hoạch tuần | Giữ nấc hiện tại và tính lại chi phí trên số ca trưởng thành | Giám đốc vận hành |

Chi tiết các kịch bản trong [bảng chi phí](bang_chi_phi.md).
