Nhóm 17
BÁO CÁO TÓM TẮT ĐỒ ÁN
1. MỤC TIÊU
Mục tiêu của đồ án này là nghiên cứu, phân tích, cài đặt và so sánh hiệu suất của các thuật toán tìm kiếm khác nhau (cả có thông tin và không có thông tin) khi áp dụng vào môi trường trò chơi cụ thể được xây dựng bằng PyGame, mà cụ thể ở đây là trò chơi Caro.
2. NỘI DUNG
2.1. Các thuật toán Tìm kiếm không có thông tin
2.1.1. Trình bày các thành phần chính của bài toán tìm kiếm
Bài toán tìm kiếm trong trò chơi (ví dụ: Caro) bao gồm các thành phần chính sau:

Không gian trạng thái: Tập hợp tất cả các cấu hình có thể của bàn cờ Caro (vị trí các quân X và O).
Trạng thái khởi đầu: Bàn cờ Caro trống.
Hàm kế thừa: Xác định các trạng thái bàn cờ tiếp theo có thể đạt được bằng cách một người chơi đặt quân vào một ô trống.
Kiểm tra mục tiêu: Hàm xác định trạng thái hiện tại có phải là trạng thái kết thúc trò chơi (một người chơi có 5 quân liên tiếp theo hàng ngang, dọc hoặc chéo) hay không.
Cấu trúc dữ liệu: Cách lưu trữ và truy xuất thông tin về trạng thái bàn cờ và các trạng thái đã khám phá trong quá trình tìm kiếm (ví dụ: hàng đợi cho BFS, ngăn xếp cho DFS).
Solution: Được định nghĩa là chuỗi các nước đi từ trạng thái ban đầu đến trạng thái mục tiêu (trạng thái chiến thắng), thỏa mãn các quy tắc của trò chơi Caro.
2.1.2. Hình ảnh gif của từng thuật toán khi áp dụng lên trò chơi
Dự án đã tiến hành cài đặt và ghi lại quá trình thực thi của các thuật toán tìm kiếm không có thông tin khi áp dụng vào trò chơi Caro, bao gồm:

2.1.4. Một vài nhận xét về hiệu suất của các thuật toán trong nhóm này
Qua quá trình thử nghiệm với trò chơi Caro trong môi trường PyGame, chúng tôi rút ra một số nhận xét:

Thuật toán BFS có khả năng tìm ra trạng thái chiến thắng với số nước đi ít nhất (nếu tồn tại ở độ sâu nông) nhưng tiêu tốn nhiều bộ nhớ khi không gian trạng thái lớn, đặc biệt với các trò chơi có hệ số nhánh cao như Caro.
Thuật toán DFS có thể khám phá sâu nhanh chóng và ít tốn bộ nhớ hơn BFS, nhưng có nguy cơ đi vào các nhánh vô tận (nếu không có cơ chế ngăn chặn) và không đảm bảo tìm ra trạng thái chiến thắng tối ưu về số nước đi.
Thuật toán Backtracking có thể hiệu quả trong việc tìm kiếm các cấu hình thỏa mãn một số điều kiện nhất định trong Caro, nhưng hiệu suất có thể giảm đáng kể với không gian trạng thái lớn do việc khám phá lại các nhánh không tiềm năng.
2.2. Các thuật toán Tìm kiếm có thông tin
2.2.1. Trình bày các thành phần chính của thuật toán tìm kiếm có thông tin
Các thuật toán tìm kiếm có thông tin (informed search) sử dụng kiến thức đặc thù của trò chơi Caro để định hướng quá trình tìm kiếm hiệu quả hơn. Thành phần chính bao gồm:

Không gian trạng thái: Tương tự như tìm kiếm không có thông tin, nhưng thứ tự khám phá các trạng thái được ưu tiên dựa trên hàm heuristic.
Hàm heuristic h(n): Ước lượng "chi phí" hoặc "khoảng cách" từ trạng thái bàn cờ hiện tại đến trạng thái kết thúc (ví dụ: trạng thái chiến thắng). Trong Caro, hàm heuristic có thể dựa trên số lượng các dãy quân liên tiếp của một người chơi (ví dụ: 2, 3, 4 quân) và khoảng trống có thể mở rộng chúng, đồng thời xem xét khả năng chặn đối phương.
Hàm chi phí g(n): Chi phí thực tế (thường là số lượng nước đi) từ trạng thái ban đầu đến trạng thái hiện tại.
Hàm đánh giá f(n): Thường là tổng của g(n) và h(n) (trong trường hợp A*), được sử dụng để đánh giá và lựa chọn trạng thái tiếp theo cần khám phá. Đối với Minimax, hàm đánh giá tập trung vào giá trị của trạng thái đối với người chơi hiện tại.
Các thuật toán tìm kiếm có thông tin được cài đặt và phân tích trong dự án bao gồm:

Thuật toán A (A-Star):* Kết hợp chi phí thực tế của các nước đi đã thực hiện (g(n)) và ước lượng chi phí đến trạng thái mục tiêu (h(n)) để tìm đường đi tối ưu. Việc định nghĩa hàm heuristic hiệu quả cho Caro là một thách thức thú vị, có thể dựa trên việc đánh giá các dãy quân liên tiếp có tiềm năng chiến thắng.
Thuật toán Minimax: Đặc biệt phù hợp cho trò chơi đối kháng như Caro, thuật toán này tìm cách tối đa hóa lợi ích của người chơi hiện tại và giảm thiểu lợi ích của đối thủ, giả định rằng cả hai đều chơi tối ưu. Thuật toán này thường sử dụng độ sâu tìm kiếm để khám phá các nước đi tiềm năng trong tương lai.
Thuật toán Deep Hill Climbing: Một biến thể của thuật toán leo đồi, có thể được áp dụng để tìm kiếm các trạng thái bàn cờ có giá trị heuristic cao hơn bằng cách thực hiện các bước đi theo hướng cải thiện giá trị heuristic, mặc dù không đảm bảo tìm thấy trạng thái chiến thắng toàn cục và có thể mắc kẹt ở cực tiểu cục bộ.
2.2.2. Hình ảnh gif của từng thuật toán khi áp dụng lên trò chơi
Dự án đã tiến hành ghi lại quá trình thực thi của các thuật toán tìm kiếm có thông tin khi áp dụng vào trò chơi Caro, thể hiện qua:

Quá trình khám phá không gian trạng thái của A* (nếu được áp dụng để tìm kiếm trạng thái chiến thắng hoặc một trạng thái có giá trị heuristic cao), cho thấy cách thuật toán ưu tiên các trạng thái có giá trị f(n) thấp nhất.
Cây trò chơi và quá trình đánh giá các nước đi của thuật toán Minimax, minh họa cách thuật toán đệ quy tìm kiếm các nước đi và gán giá trị cho từng trạng thái dựa trên kết quả giả định của các nước đi tiếp theo.
Các bước "leo đồi" và khả năng (hoặc thiếu sót) vượt qua các "cực tiểu cục bộ" của thuật toán Deep Hill Climbing trong không gian trạng thái của Caro, cho thấy cách thuật toán di chuyển từ trạng thái này sang trạng thái khác dựa trên giá trị heuristic.
(Các hình ảnh gif minh họa quá trình thực thi của các thuật toán này trên môi trường PyGame-Caro đã được ghi lại.)

2.2.3. Một vài nhận xét về hiệu suất của các thuật toán trong nhóm này
Qua quá trình thử nghiệm trên trò chơi Caro trong môi trường PyGame, chúng tôi rút ra nhận xét:

Thuật toán A* (nếu có hàm heuristic tốt) có tiềm năng tìm ra các nước đi hiệu quả hoặc trạng thái chiến thắng một cách tối ưu hơn so với các thuật toán không có thông tin, đặc biệt trong các tình huống phức tạp của trò chơi Caro.
Thuật toán Minimax (có thể kết hợp với cắt tỉa Alpha-Beta để giảm bớt không gian tìm kiếm) cho phép xây dựng một đối thủ AI thông minh cho trò chơi Caro, với khả năng dự đoán các nước đi và tối ưu hóa chiến lược chơi dựa trên độ sâu tìm kiếm.
Thuật toán Deep Hill Climbing có thể đưa ra các nước đi tốt trong thời gian ngắn với chi phí tính toán thấp, nhưng dễ bị mắc kẹt trong các tình huống không tối ưu và không đảm bảo tìm được nước đi tốt nhất trong dài hạn cho trò chơi Caro.
2.2.4 Hình ảnh so sánh hiệu suất của tất cả các thuật toán
Dự án đã tiến hành đo lường và so sánh hiệu suất của tất cả các thuật toán tìm kiếm (cả không có thông tin và có thông tin) khi áp dụng vào trò chơi Caro dựa trên các tiêu chí:

Thời gian thực thi: Thời gian cần thiết để thuật toán tìm ra giải pháp (hoặc kết thúc nếu không tìm thấy) hoặc thời gian trung bình để đưa ra một nước đi (đối với các thuật toán AI).
Bộ nhớ sử dụng: Lượng bộ nhớ cần thiết để lưu trữ các trạng thái đã khám phá và các cấu trúc dữ liệu liên quan trong quá trình tìm kiếm.
Số lượng trạng thái đã khám phá: Tổng số trạng thái mà thuật toán đã duyệt qua trong quá trình tìm kiếm để đạt được mục tiêu hoặc đưa ra quyết định.
Độ dài của đường đi tìm được: Số lượng nước đi trong chuỗi dẫn đến trạng thái chiến thắng (trong ngữ cảnh tìm kiếm trạng thái chiến thắng).
Chất lượng của giải pháp/nước đi: Đánh giá hiệu quả của giải pháp tìm được (ví dụ: đường đi ngắn nhất) hoặc chất lượng nước đi của AI (ví dụ: khả năng dẫn đến chiến thắng).
Khả năng mở rộng: Hiệu suất của thuật toán khi kích thước bàn cờ Caro tăng lên.
(Hình ảnh so sánh hiệu suất của tất cả các thuật toán này, có thể dưới dạng biểu đồ (ví dụ: biểu đồ cột đa nhóm so sánh thời gian, bộ nhớ, số lượng trạng thái) hoặc bảng số liệu chi tiết, đã được tạo ra từ kết quả thử nghiệm trên PyGame-Caro.)

2.3. Tích hợp thuật toán vào môi trường trò chơi
Dự án đã xây dựng một môi trường trò chơi Caro hoàn chỉnh bằng PyGame để thử nghiệm các thuật toán, bao gồm:

Giao diện người dùng trực quan cho phép người chơi tương tác với bàn cờ, thực hiện nước đi và quan sát quá trình chơi.
Khả năng tích hợp và tùy chỉnh các tham số của các thuật toán tìm kiếm (ví dụ: lựa chọn thuật toán AI, điều chỉnh độ sâu tìm kiếm của Minimax, thiết lập hàm heuristic cho A*).
Chức năng ghi lại và xuất kết quả thử nghiệm hiệu suất của các thuật toán (ví dụ: thời gian chạy, số lượng trạng thái đã khám phá) để phân tích và so sánh.
Khả năng chuyển đổi lượt chơi giữa người chơi và AI (sử dụng các thuật toán đã cài đặt).
(Hình ảnh 1 và 2 bạn cung cấp có thể là một phần của cấu trúc thư mục dự án PyGame-Caro này, cho thấy các module và file liên quan đến việc triển khai các thuật toán và giao diện trò chơi.)

3. KẾT LUẬN
3.1. Trình bày một số kết quả đạt được khi thực hiện project này
Thông qua dự án này, chúng tôi đã đạt được những kết quả sau:

Xây dựng thành công hệ thống mô phỏng và trực quan hóa quá trình tìm kiếm của tất cả các thuật toán khác nhau (DFS, BFS, Backtracking, A*, Minimax, Deep Hill Climbing) trong ngữ cảnh trò chơi Caro bằng PyGame.
Cài đặt và thử nghiệm tất cả các thuật toán tìm kiếm cả có và không có thông tin để điều khiển hành vi của đối thủ AI trong trò chơi Caro.
Thiết lập các phương pháp đánh giá hiệu suất cụ thể cho từng thuật toán khi áp dụng vào trò chơi Caro, dựa trên thời gian thực thi, bộ nhớ sử dụng, số lượng trạng thái đã khám phá và chất lượng nước đi.
Tiến hành so sánh hiệu suất toàn diện giữa tất cả các thuật toán đã cài đặt trong các tình huống chơi Caro khác nhau, thu thập dữ liệu về các tiêu chí đã xác định.
Xác định được những ưu điểm và hạn chế của từng thuật toán khi áp dụng vào trò chơi Caro, cũng như sự phù hợp của chúng cho các mục tiêu tìm kiếm khác nhau (ví dụ: tìm nước đi tối ưu cho AI, tìm trạng thái chiến thắng).
3.2. Đánh giá tổng quan
Qua quá trình nghiên cứu và thực nghiệm với trò chơi Caro trong môi trường PyGame, chúng tôi nhận thấy:

Nhìn chung, các thuật toán tìm kiếm có thông tin (A*, Minimax, Deep Hill Climbing) có xu hướng đạt được hiệu suất tốt hơn các thuật toán tìm kiếm không có thông tin (DFS, BFS, Backtracking) trong việc tìm kiếm các nước đi hiệu quả hoặc trạng thái chiến thắng trong trò chơi Caro, đặc biệt khi không gian trạng thái mở rộng. Kết quả so sánh cho thấy sự khác biệt rõ rệt về thời gian tìm kiếm và số lượng trạng thái cần khám phá.
Thuật toán Minimax nổi bật như một phương pháp hiệu quả để xây dựng đối thủ AI thông minh cho Caro, có khả năng đưa ra các quyết định chiến lược dựa trên việc dự đoán các nước đi tiềm năng của đối thủ.
Hiệu suất của thuật toán A* chịu ảnh hưởng lớn bởi chất lượng của hàm heuristic được thiết kế. Một hàm heuristic tốt có thể giúp A* tìm ra giải pháp tối ưu một cách hiệu quả hơn.
Các thuật toán tìm kiếm không có thông tin, mặc dù có những hạn chế về hiệu suất trong không gian trạng thái lớn của Caro, vẫn cung cấp những hiểu biết cơ bản về cấu trúc của bài toán tìm kiếm và là cơ sở để so sánh hiệu suất với các thuật toán phức tạp hơn, làm nổi bật tầm quan trọng của việc sử dụng thông tin đặc thù của bài toán.
3.3. Hướng phát triển
Dự án có thể được phát triển thêm theo các hướng:

Tiếp tục tối ưu hóa việc cài đặt và hiệu suất của tất cả các thuật toán đã nghiên cứu, đặc biệt là việc tinh chỉnh hàm heuristic cho A* và các kỹ thuật cắt tỉa cho Minimax.
Mở rộng phạm vi so sánh hiệu suất trên nhiều kích thước bàn cờ và độ phức tạp khác nhau của trò chơi Caro, bao gồm cả việc đánh giá khả năng thích ứng của các thuật toán với các điều kiện khác nhau.
Tích hợp và so sánh hiệu suất với các phương pháp học máy (ví dụ: Q-Learning) để phát triển các chiến lược chơi linh hoạt và thích ứng hơn cho AI.
Nghiên cứu và triển khai các thuật toán tìm kiếm kết hợp để tận dụng ưu điểm của cả tìm kiếm có thông tin và không có thông tin, sau đó tiến hành so sánh hiệu suất với các thuật toán đơn lẻ để xác định phương pháp tiếp cận tốt nhất cho các tình huống khác nhau trong trò chơi Caro.
# PyGame-Caro-Demo
 Đây là Phú tự làm demo theo youtube:
https://youtu.be/LbTu0rwikwg?si=tExi3GXhQVnyhIBp
