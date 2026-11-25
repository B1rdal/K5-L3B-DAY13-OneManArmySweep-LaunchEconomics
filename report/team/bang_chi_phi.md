# Bảng chi phí · Nhiệm vụ A và B

Kết quả từ `src/lab13.py`. CPS là chi phí trợ lý trên mỗi yêu cầu thành công. So sánh theo yêu cầu dùng thêm chi phí nhân viên xử lý các ca còn lại.

## A1 · Ba phép thử với p = 0,8

| Phép thử | Kết quả |
|---|---:|
| Số lần chạy kỳ vọng, tối đa 2 lần | 1,20 |
| Số lần chạy kỳ vọng, chạy đến khi đúng | 1,25 |
| Hệ số CPS, tối đa 3 lần | 1,25 |

## A2 · Chi phí từ trace

| Khoản | Giá trị | Nguồn |
|---|---:|---|
| Token | 245.585,13 đ | Trace |
| Tool | 84.000,00 đ | Trace |
| Phần token và tool của lần chạy thứ 2 và 3 | 93.804,49 đ | Trace, đã nằm trong hai dòng trên |
| Xem lại | 1.780.000,00 đ | simulated |
| Làm lại | 2.264.000,00 đ | simulated |
| Tổng chi phí trợ lý | 4.373.585,13 đ | simulated |
| Số việc thành công | 978/1.200 | Kết quả cấp yêu cầu |
| CPS | 4.471,97 đ | simulated |
| Hóa đơn token + tool trên mỗi yêu cầu | 274,65 đ | Trace |

- CPS gấp **16,28×** hóa đơn token + tool trên mỗi yêu cầu (simulated). Tử số gồm chi phí của mọi lượt chạy. Mẫu số chỉ gồm 978 yêu cầu có `ket_qua = thanh_cong`.
- Làm lại chiếm **51,77%** tổng chi phí (simulated), lớn nhất trong bốn khoản.
- So sánh cùng đơn vị với nhân viên tự làm: (4.373.585,13 + 222 × 12.000) ÷ 1.200 = **5.864,65 đ/yêu cầu** (simulated), bằng 48,87% baseline, trước chi phí cố định.

## A3 · Theo loại yêu cầu

| Loại | Yêu cầu | Thành công | Lượt chạy/yêu cầu | CPS (simulated) | So với 12.000 đ (simulated) |
|---|---:|---:|---:|---:|---:|
| noi_dia | 824 | 95,02% | 1,11 | 2.695,64 đ | 0,22× |
| hang_nang | 158 | 74,05% | 1,47 | 8.220,73 đ | 0,69× |
| quoc_te | 150 | 27,33% | 2,32 | 22.515,17 đ | 1,88× |
| doi_tac | 68 | 54,41% | 1,88 | 10.214,87 đ | 0,85× |

- Loại `quoc_te` khỏi pilot vì CPS là 1,88× baseline (simulated). Tỉ lệ lượt chạy ok giảm từ 45/150 (30,0%) xuống 12/105 (11,4%) rồi 2/93 (2,2%). Lần 3 chỉ thêm 2 lượt ok.
- Giữ `doi_tac` ngoài pilot vì có điều khoản riêng và chỉ thành công 54,41%. Thử hai loại còn lại với ngưỡng theo dõi riêng cho hàng nặng.

## A4 · Cộng 40 triệu đ/tháng cho phạm vi nội địa và hàng nặng

| Tổng yêu cầu/tháng | Thành công trong phạm vi | Chi phí cố định/việc | CPS gồm cố định (simulated) | So với 12.000 đ (simulated) |
|---|---:|---:|---:|---:|
| 45.000 | 33.750 | 1.185,19 đ | 4.599,09 đ | 0,38× |
| 22.500 | 16.875 | 2.370,37 đ | 5.784,27 đ | 0,48× |

- Dự phóng số việc thành công theo 900/1.200 của mẫu trên tổng lượng yêu cầu toàn công ty. CPS còn dưới 12.000 đ ở cả hai quy mô và hòa vốn gần 6.212 yêu cầu/tháng (simulated). Đây là ngưỡng CPS, cần cộng chuyển người khi quyết định về chi phí cả hệ thống.

## B1 · Độ nhạy so với CPS gốc 4.471,97 đ (simulated)

| Kịch bản | CPS (simulated) | Thay đổi (simulated) |
|---|---:|---:|
| Giá token gấp đôi | 4.723,08 đ | +5,62% |
| Giá token giảm một nửa | 4.346,41 đ | −2,81% |
| Tiền xem lại gấp đôi | 6.292,01 đ | +40,70% |
| Tiền xem lại giảm một nửa | 3.561,95 đ | −20,35% |
| Tiền làm lại gấp đôi | 6.786,90 đ | +51,77% |
| Tiền làm lại giảm một nửa | 3.314,50 đ | −25,88% |
| Lương tăng 25% | 5.505,71 đ | +23,12% |
| Tối đa 2 lượt | 4.237,29 đ | −5,25% |
| Tối đa 1 lượt | 4.110,99 đ | −8,07% |

Ba kịch bản giảm một nửa có mức giảm bằng nửa mức tăng tương ứng trước khi làm tròn. Mô hình đổi hệ số thời gian review/rework để biểu diễn độ nhạy của chi phí.

## B2 · Đổi một cặp

- Gấp đôi giá token và tiền xem lại đưa CPS lên **6.543,12 đ (+46,31%)** (simulated). Hai tác động cộng được vì mẫu số cố định và hai khoản chi phí độc lập trong phép tính.
- Ba yếu tố nhạy nhất (simulated) là làm lại **+51,77%**, xem lại **+40,70%**, lương **+23,12%**.

## B3 · So sánh giới hạn lượt chạy

| Giới hạn | Tổng trợ lý (simulated) | Không thành công | Tổng hệ thống (simulated) | CPS (simulated) |
|---|---:|---:|---:|---:|
| 1 | 3.621.780,64 đ | 319 | 7.449.780,64 đ | 4.110,99 đ |
| 2 | 4.093.220,23 đ | 234 | 6.901.220,23 đ | 4.237,29 đ |
| 3 | 4.373.585,13 đ | 222 | 7.037.585,13 đ | 4.471,97 đ |

- **2 lượt** rẻ nhất cho công ty (6.901.220,23 đ simulated). **1 lượt** giảm CPS xuống 4.110,99 đ (simulated) nhưng có thêm 85 yêu cầu cần nhân viên. Tổng hệ thống cộng 12.000 đ cho mỗi ca không thành công.

## B4 · Xem lại 100% trong phạm vi pilot

- Với 948 yêu cầu có lượt ok được xem lại 5 phút/yêu cầu, 48 ca làm lại và 900 thành công, CPS là **11.742,79 đ** ở 9 phút làm lại và **12.414,79 đ** ở 15,3 phút làm lại (simulated). Mốc 15,3 là trung bình của các ca làm lại toàn mẫu, làm tròn một chữ số.
- So với 12.000 đ, hai kịch bản lần lượt là 0,979× và 1,035× (simulated). Điểm hòa vốn của thời gian xem lại giảm từ **5,12 xuống 4,80 phút** (simulated). Pilot cần đo thời gian thật và xác định mức xem lại có thể giảm mà vẫn an toàn.
