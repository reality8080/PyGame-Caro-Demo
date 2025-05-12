# Nhóm 17 - BÁO CÁO TÓM TẮT ĐỒ ÁN

## 1. MỤC TIÊU

Mục tiêu của đồ án này là nghiên cứu, phân tích, cài đặt và so sánh hiệu suất của các thuật toán tìm kiếm khác nhau (cả có thông tin và không có thông tin) khi áp dụng vào môi trường trò chơi cụ thể được xây dựng bằng PyGame, mà cụ thể ở đây là trò chơi Caro.

## 2. NỘI DUNG

### 2.1. Trình bày các thành phần chính của bài toán tìm kiếm

Bài toán tìm kiếm trong trò chơi (ví dụ: Caro) bao gồm các thành phần chính sau:

* **Không gian trạng thái:** Tập hợp tất cả các cấu hình có thể của bàn cờ Caro (vị trí các quân X và O).
* **Trạng thái khởi đầu:** Bàn cờ Caro trống.
* **Hàm kế thừa:** Xác định các trạng thái bàn cờ tiếp theo có thể đạt được bằng cách một người chơi đặt quân vào một ô trống.
* **Kiểm tra mục tiêu:** Hàm xác định trạng thái hiện tại có phải là trạng thái kết thúc trò chơi (một người chơi có 5 quân liên tiếp theo hàng ngang, dọc hoặc chéo) hay không.
* **Cấu trúc dữ liệu:** Cách lưu trữ và truy xuất thông tin về trạng thái bàn cờ và các trạng thái đã khám phá trong quá trình tìm kiếm (ví dụ: hàng đợi cho BFS, ngăn xếp cho DFS).
* **Solution:** Được định nghĩa là chuỗi các nước đi từ trạng thái ban đầu đến trạng thái mục tiêu (trạng thái chiến thắng), thỏa mãn các quy tắc của trò chơi Caro.
* **Giao diện thiết kế theo thuật của youtuber:** [https://youtu.be/LbTu0rwikwg?si=tExi3GXhQVnyhIBp](https://youtu.be/LbTu0rwikwg?si=tExi3GXhQVnyhIBp)

### 2.2. Uniform Cost Search (UCS)

![UCS](/DEMO/UCS.gif)

### 2.3. A Search (A-Star Search)

![A* Search](/DEMO/A.gif)

### 2.4. Depth-First Hill Climbing

![Depth-First Hill Climbing](/DEMO/DeepHillClimbing.gif)

### 2.5. AND-OR Search

![AND-OR Search](/DEMO/and_or.gif)

### 2.6. Constraint Satisfaction Problem (CSP) Backtracking

![(CSP) Backtracking](/DEMO/Backtracking.gif)

### 2.7. Q-learning

![QLearning](/DEMO/QLearning.gif)

### 2.8. Minimax Algorithm

![MiniMax](/DEMO/miniMax.gif)

### 2.9. Nhận xét

![Figure](/DEMO/FigureTimes.png)

## 3. KẾT LUẬN

### 3.1. Trình bày một số kết quả đạt được khi thực hiện project này

Thông qua dự án này, chúng tôi đã đạt được những kết quả sau:

* Xây dựng thành công hệ thống mô phỏng và trực quan hóa quá trình tìm kiếm của tất cả các thuật toán khác nhau (DFS, BFS, Backtracking, A\*, Minimax, Deep Hill Climbing) trong ngữ cảnh trò chơi Caro bằng PyGame.
* Cài đặt và thử nghiệm tất cả các thuật toán tìm kiếm cả có và không có thông tin để điều khiển hành vi của đối thủ AI trong trò chơi Caro.
* Thiết lập các phương pháp đánh giá hiệu suất cụ thể cho từng thuật toán khi áp dụng vào trò chơi Caro, dựa trên thời gian thực thi, bộ nhớ sử dụng, số lượng trạng thái đã khám phá và chất lượng nước đi.
* Tiến hành so sánh hiệu suất toàn diện giữa tất cả các thuật toán đã cài đặt trong các tình huống chơi Caro khác nhau, thu thập dữ liệu về các tiêu chí đã xác định.
* Xác định được những ưu điểm và hạn chế của từng thuật toán khi áp dụng vào trò chơi Caro, cũng như sự phù hợp của chúng cho các mục tiêu tìm kiếm khác nhau (ví dụ: tìm nước đi tối ưu cho AI, tìm trạng thái chiến thắng).

### 3.2. Đánh giá tổng quan

Qua quá trình nghiên cứu và thực nghiệm với trò chơi Caro trong môi trường PyGame, chúng tôi nhận thấy:

* Nhìn chung, các thuật toán tìm kiếm có thông tin (A\*, Minimax, Deep Hill Climbing) có xu hướng đạt được hiệu suất tốt hơn các thuật toán tìm kiếm không có thông tin (DFS, BFS, Backtracking) trong việc tìm kiếm các nước đi hiệu quả hoặc trạng thái chiến thắng trong trò chơi Caro, đặc biệt khi không gian trạng thái mở rộng. Kết quả so sánh cho thấy sự khác biệt rõ rệt về thời gian tìm kiếm và số lượng trạng thái cần khám phá.
* Thuật toán Minimax nổi bật như một phương pháp hiệu quả để xây dựng đối thủ AI thông minh cho Caro, có khả năng đưa ra các quyết định chiến lược dựa trên việc dự đoán các nước đi tiềm năng của đối thủ.
* Hiệu suất của thuật toán A\* chịu ảnh hưởng lớn bởi chất lượng của hàm heuristic được thiết kế. Một hàm heuristic tốt có thể giúp A\* tìm ra giải pháp tối ưu một cách hiệu quả hơn.
* Các thuật toán tìm kiếm không có thông tin, mặc dù có những hạn chế về hiệu suất trong không gian trạng thái lớn của Caro, vẫn cung cấp những hiểu biết cơ bản về cấu trúc của bài toán tìm kiếm và là cơ sở để so sánh hiệu suất với các thuật toán phức tạp hơn, làm nổi bật tầm quan trọng của việc sử dụng thông tin đặc thù của bài toán.

### 3.3. Hướng phát triển

Dự án có thể được phát triển thêm theo các hướng:

* Tiếp tục tối ưu hóa việc cài đặt và hiệu suất của tất cả các thuật toán đã nghiên cứu, đặc biệt là việc tinh chỉnh hàm heuristic cho A\* và các kỹ thuật cắt tỉa cho Minimax.
* Mở rộng phạm vi so sánh hiệu suất trên nhiều kích thước bàn cờ và độ phức tạp khác nhau của trò chơi Caro, bao gồm cả việc đánh giá khả năng thích ứng của các thuật toán với các điều kiện khác nhau.
* Tích hợp và so sánh hiệu suất với các phương pháp học máy (ví dụ: Q-Learning) để phát triển các chiến lược chơi linh hoạt và thích ứng hơn cho AI.
* Nghiên cứu và triển khai các thuật toán tìm kiếm kết hợp để tận dụng ưu điểm của cả tìm kiếm có thông tin và không có thông tin, sau đó tiến hành so sánh hiệu suất với các thuật toán đơn lẻ để xác định phương pháp tiếp cận tốt nhất cho các tình huống khác nhau trong trò chơi Caro.