# Bảng lỗi và cách khắc phục · Nhiệm vụ C

20 ca lỗi nằm trong `docs/Ngay13_Lab13_De_bai_hoc_vien.docx`. Năm loại theo Google PAIR: **Do người dùng · Hệ thống · Ngữ cảnh · Giới hạn hệ thống · Ngầm**. Gắn nhãn theo nguyên nhân gốc, không theo chỗ cần sửa.

## Phân loại 20 ca

Nhãn theo [hướng dẫn của lab](../../docs/Lab13_Huong_dan_chi_tiet_buoi_chieu.md#nhãn-tham-khảo-cho-20-ca).

| Ca | Nhãn tham chiếu | Căn cứ từ mô tả ca |
| --: | --- | --- |
| 1 | Do người dùng | Số tài khoản khách nhập thiếu hai chữ số. |
| 2 | Hệ thống | Trợ lý chọn tham số hàng thường cho kiện 28 kg, dẫn đến hoàn thiếu. |
| 3 | Ngữ cảnh | Luồng hoàn vào ví chạy đúng thiết kế, còn khách chờ tiền về ngân hàng. |
| 4 | Giới hạn hệ thống | LogiX thiếu dữ liệu chặng giao do hãng nước ngoài phụ trách. |
| 5 | Ngầm | Hoàn dư theo giá trước giảm, chỉ phát hiện khi kiểm tra mẫu. |
| 6 | Do người dùng | Khách chọn luồng giao trễ dù yêu cầu liên quan hàng bị vỡ. |
| 7 | Hệ thống | Trợ lý thông báo hoàn thành dù sổ cái trả lỗi 503. |
| 8 | Hệ thống | Câu trả lời viện dẫn một điều khoản không tồn tại trong chính sách. |
| 9 | Do người dùng | Khách nhập mã đơn sàn thương mại điện tử vào ô mã vận đơn. |
| 10 | Ngữ cảnh | Từ chối hoàn đúng điều khoản bất khả kháng, còn ứng dụng hiển thị cam kết 24 giờ. |
| 11 | Giới hạn hệ thống | Trợ lý thiếu khả năng xử lý tin nhắn thoại. |
| 12 | Ngầm | Kết quả vẫn đúng, nhưng chi phí token tăng gấp ba trong ba tuần trước khi bị phát hiện. |
| 13 | Giới hạn hệ thống | Hoàn phí bảo hiểm của đối tác nằm ngoài phạm vi trợ lý. |
| 14 | Do người dùng | Khách bấm xác nhận đã nhận tiền trước khi tiền về. |
| 15 | Hệ thống | Công thức hoàn 100% trái với mức 50% quy định. Nhân viên phát hiện trước khi gửi. |
| 16 | Ngữ cảnh | Gửi ngay đúng thiết kế, nhưng thời điểm 2:14 sáng gây phiền cho khách. |
| 17 | Ngầm | Bảng giá cũ làm lệch 212 đơn trong 9 ngày mà không có yêu cầu mở lại. |
| 18 | Ngữ cảnh | Số tiền hoàn đúng. Thông báo thiếu phép tính khiến khách tưởng hoàn thiếu. |
| 19 | Giới hạn hệ thống | Yêu cầu nằm ngoài cửa sổ truy cập dữ liệu 12 tháng. |
| 20 | Hệ thống | Thiếu khóa chống trùng cho lệnh thứ hai, gây hoàn hai lần. |

**Kiểm tra bảng:** 20 ca, gồm 4 ca do người dùng, 5 ca hệ thống, 4 ca ngữ cảnh, 4 ca giới hạn hệ thống và 3 ca ngầm. Đồng thuận giữa người gắn nhãn: chưa đo.

## Quy tắc phân biệt

- Ca 6 và 9 bắt đầu từ dữ liệu hoặc lựa chọn sai của khách. Hướng dẫn sửa đầu vào là biện pháp khắc phục.
- Ca 7, 8 và 15 có đầu ra mâu thuẫn với trạng thái hoặc chính sách. Ca 12 và 17 cần giám sát chi phí hoặc đối soát mẫu để phát hiện.
- Ca 3, 10, 16 và 18 có chênh lệch giữa hành vi đúng thiết kế và kỳ vọng của khách. Ca 4, 11, 13 và 19 có giới hạn về dữ liệu, năng lực hoặc phạm vi.

## Bảng khắc phục cho 5 ca, mỗi loại một ca

Cách phát hiện phải đo được (event, ngưỡng, tần suất). Người phụ trách là một vai trò, không ghi "cả đội".

| Ca | Loại lỗi | Phát hiện bằng gì | Khắc phục thế nào | Ai phụ trách |
| --: | --- | --- | --- | --- |
| 1 | Do người dùng | Theo dõi `refund_input_rejected` theo ngày. Cảnh báo khi trên 2% yêu cầu bị từ chối vì thiếu chữ số tài khoản. | Kiểm tra định dạng theo ngân hàng trước khi gửi lệnh và cho khách sửa số tài khoản. | PM trợ lý hoàn phí |
| 20 | Hệ thống | Đối soát `refund_ledger_write` theo mã đơn và nghĩa vụ hoàn. Cảnh báo ngay khi thấy 2 lần ghi thành công cho cùng một nghĩa vụ. | Dùng khóa idempotency theo nghĩa vụ hoàn. Yêu cầu lặp lại trả trạng thái hiện có. | Kỹ sư trưởng agent |
| 16 | Ngữ cảnh | Đếm `refund_notice_sent` ngoài 08:00–21:00 theo giờ địa phương, với ngưỡng 0 tin ngoài giờ khi khách chưa đồng ý. | Gửi thông báo giờ phù hợp theo kênh khách chọn, đồng thời hiển thị trạng thái trong ứng dụng. | Trưởng nhóm CSKH |
| 19 | Giới hạn hệ thống | Rà hằng tuần `handoff_to_staff` có lý do ngoài thời hạn lưu dữ liệu. Cảnh báo nếu có bất kỳ ca nào thiếu tóm tắt. | Kiểm hạn 12 tháng trước khi tra, giải thích giới hạn và chuyển nhân viên kèm mã đơn và khoảng thời gian. | Quản lý nghiệp vụ hoàn phí |
| 5 | Ngầm | Đối soát mẫu 100 đơn có mã giảm giá mỗi tuần qua `audit_sample_checked`. Điều tra ngay nếu có ít nhất 1 ca lệch tiền. | Tính trên số tiền đã trả sau giảm giá và giữ phiên bản quy tắc trong trace. | Kế toán trưởng |
