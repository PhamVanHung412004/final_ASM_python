import os
from datetime import datetime

# Hàm tính GPA dựa trên điểm số và tín chỉ từng môn học
def calculate_gpa(grades, credits):
    """
    Tính toán GPA dựa vào điểm số và tín chỉ

    Tham số:
    grades (list): Danh sách điểm (0.0 - 4.0)
    credits (list): Danh sách tín chỉ của từng môn

    Trả về:
    float: Giá trị GPA đã tính toán
    """
    try:
        # Kiểm tra danh sách có rỗng không
        if not grades or not credits:
            raise ValueError("Không có điểm hoặc tín chỉ được cung cấp")

        # Kiểm tra 2 danh sách có cùng độ dài không
        if len(grades) != len(credits):
            raise ValueError("Số lượng điểm và tín chỉ phải khớp nhau")

        # Tính tổng điểm trọng số và tổng tín chỉ
        weighted_sum = 0.0
        total_credits = 0

        for i in range(len(grades)):
            weighted_sum += grades[i] * credits[i]
            total_credits += credits[i]

        # Kiểm tra tổng tín chỉ có bằng 0 không để tránh chia cho 0
        if total_credits == 0:
            raise ZeroDivisionError("Tổng số tín chỉ không được bằng 0")

        # Tính và trả về GPA (làm tròn 2 chữ số thập phân)
        gpa = weighted_sum / total_credits
        return round(gpa, 2)

    except Exception as e:
        raise e

# Hàm xuất kết quả GPA ra file txt
def print_gpa(student_name, grades, credits, gpa, filename="gpa_results.txt"):
    """
    In kết quả GPA ra file văn bản

    Tham số:
    student_name (str): Tên sinh viên
    grades (list): Danh sách điểm
    credits (list): Danh sách tín chỉ
    gpa (float): GPA đã tính
    filename (str): Tên file xuất ra
    """
    try:
        # Tạo thư mục output nếu chưa tồn tại
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        filepath = os.path.join(output_dir, filename)

        # Ghi kết quả vào file
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write("=" * 50 + "\n")
            file.write("GPA CALCULATION RESULTS\n")
            file.write("=" * 50 + "\n\n")

            file.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write(f"Student Name: {student_name}\n\n")

            file.write("Course Details:\n")
            file.write("-" * 30 + "\n")
            file.write(f"{'Course #':<10} {'Grade':<10} {'Credits':<10}\n")
            file.write("-" * 30 + "\n")

            for i in range(len(grades)):
                file.write(f"{i+1:<10} {grades[i]:<10.2f} {credits[i]:<10}\n")

            file.write("-" * 30 + "\n")
            file.write(f"Total Credits: {sum(credits)}\n")
            file.write(f"Calculated GPA: {gpa:.2f}\n")
            file.write("=" * 50 + "\n")

        print(f"\nKết quả đã được lưu tại: {filepath}")
        return True

    except IOError as e:
        print(f"Lỗi khi ghi file: {e}")
        return False
    except Exception as e:
        print(f"Lỗi không xác định: {e}")
        return False

# Hàm kiểm tra tính hợp lệ của đầu vào điểm
def validate_grade(grade_str):
    """
    Kiểm tra đầu vào điểm số

    Tham số:
    grade_str (str): Điểm dạng chuỗi

    Trả về:
    float: Điểm đã kiểm tra hợp lệ
    """
    try:
        grade = float(grade_str)
        if grade < 0.0 or grade > 4.0:
            raise ValueError("Điểm phải nằm trong khoảng từ 0.0 đến 4.0")
        return grade
    except ValueError as e:
        if "could not convert" in str(e):
            raise ValueError("Định dạng điểm không hợp lệ. Hãy nhập số.")
        else:
            raise e

# Hàm kiểm tra tính hợp lệ của đầu vào tín chỉ
def validate_credit(credit_str):
    """
    Kiểm tra đầu vào tín chỉ

    Tham số:
    credit_str (str): Tín chỉ dạng chuỗi

    Trả về:
    int: Tín chỉ đã kiểm tra hợp lệ
    """
    try:
        credit = int(credit_str)
        if credit <= 0:
            raise ValueError("Tín chỉ phải là số nguyên dương")
        return credit
    except ValueError as e:
        if "invalid literal" in str(e):
            raise ValueError("Định dạng tín chỉ không hợp lệ. Hãy nhập số nguyên.")
        else:
            raise e

# Hàm nhập và kiểm tra tên sinh viên
def get_student_name():
    """
    Nhập và kiểm tra tên sinh viên

    Trả về:
    str: Tên sinh viên hợp lệ
    """
    while True:
        try:
            name = input("Nhập tên sinh viên: ").strip()

            # Kiểm tra tên rỗng
            if not name:
                raise ValueError("Tên không được để trống")

            # Kiểm tra tên toàn khoảng trắng
            if name.isspace():
                raise ValueError("Tên không được chỉ toàn khoảng trắng")

            # Cảnh báo nếu tên chứa số
            if any(char.isdigit() for char in name):
                print("Cảnh báo: Tên có chứa số. Tiếp tục? (y/n): ", end="")
                if input().lower() != 'y':
                    continue

            return name

        except ValueError as e:
            print(f"Lỗi: {e}")
        except Exception as e:
            print(f"Lỗi không xác định: {e}")

# Hàm nhập điểm và tín chỉ từng môn học từ người dùng
def get_course_data():
    """
    Nhập điểm và tín chỉ các môn học từ người dùng

    Trả về:
    tuple: (danh sách điểm, danh sách tín chỉ)
    """
    grades = []
    credits = []
    course_count = 0

    print("\nNhập thông tin môn học (gõ 'done' để kết thúc):")
    print("Định dạng: Nhập điểm (0.0-4.0) và tín chỉ cho từng môn\n")

    while True:
        try:
            # Nhập điểm
            grade_input = input(f"Môn học {course_count + 1} - Nhập điểm (hoặc 'done' để kết thúc): ").strip()

            if grade_input.lower() == 'done':
                if course_count == 0:
                    raise ValueError("Phải nhập ít nhất 1 môn học")
                break

            # Kiểm tra điểm hợp lệ
            grade = validate_grade(grade_input)

            # Nhập tín chỉ
            credit_input = input(f"Môn học {course_count + 1} - Nhập tín chỉ: ").strip()

            # Kiểm tra tín chỉ hợp lệ
            credit = validate_credit(credit_input)

            # Thêm vào danh sách
            grades.append(grade)
            credits.append(credit)
            course_count += 1

            print(f"Đã thêm môn học {course_count} thành công!\n")

        except ValueError as e:
            print(f"Lỗi: {e}")
            print("Vui lòng thử lại.\n")
        except KeyboardInterrupt:
            print("\n\nĐã hủy thao tác bởi người dùng.")
            return None, None
        except Exception as e:
            print(f"Lỗi không xác định: {e}")
            print("Vui lòng thử lại.\n")

    return grades, credits

# Hàm chính của chương trình
def main():
    """
    Hàm chính của chương trình
    """
    print("=" * 50)
    print("CHƯƠNG TRÌNH TÍNH GPA")
    print("=" * 50)
    print()

    try:
        # Bước 1: Nhập tên sinh viên
        student_name = get_student_name()

        # Bước 2: Nhập dữ liệu môn học
        grades, credits = get_course_data()

        if grades is None or credits is None:
            print("Chương trình đã kết thúc.")
            return

        # Bước 3: Tính GPA
        print("\nĐang tính GPA...")
        gpa = calculate_gpa(grades, credits)

        # Bước 4: Hiển thị kết quả
        print("\n" + "=" * 30)
        print("KẾT QUẢ TÍNH TOÁN")
        print("=" * 30)
        print(f"Tên sinh viên: {student_name}")
        print(f"Số lượng môn học: {len(grades)}")
        print(f"Tổng tín chỉ: {sum(credits)}")
        print(f"GPA: {gpa:.2f}")
        print("=" * 30)

        # Bước 5: Lưu kết quả ra file
        print("\nĐang lưu kết quả ra file...")
        filename = f"gpa_{student_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        if print_gpa(student_name, grades, credits, gpa, filename):
            print("Đã lưu kết quả thành công!")
        else:
            print("Lưu kết quả ra file thất bại.")

        # Hỏi người dùng có muốn tính GPA khác không
        print("\nTính GPA khác? (y/n): ", end="")
        if input().lower() == 'y':
            print()
            main()
        else:
            print("\nCảm ơn bạn đã sử dụng chương trình tính GPA!")

    except KeyboardInterrupt:
        print("\n\nChương trình bị gián đoạn bởi người dùng.")
    except Exception as e:
        print(f"\nLỗi nghiêm trọng: {e}")
        print("Chương trình sẽ kết thúc.")

# Hàm demo chức năng, dùng thử nghiệm nhanh
def demonstrate_functions():
    """
    Demo cách sử dụng các hàm tính và xuất GPA
    """
    print("\n" + "=" * 50)
    print("DEMO CHỨC NĂNG")
    print("=" * 50)

    # Dữ liệu ví dụ
    demo_name = "John Doe"
    demo_grades = [3.7, 3.3, 4.0, 3.0, 3.5]
    demo_credits = [3, 4, 3, 3, 2]

    print(f"\nSinh viên demo: {demo_name}")
    print("Danh sách môn học:")
    for i in range(len(demo_grades)):
        print(f"  Môn học {i+1}: Điểm={demo_grades[i]}, Tín chỉ={demo_credits[i]}")

    try:
        # Tính GPA
        demo_gpa = calculate_gpa(demo_grades, demo_credits)
        print(f"\nGPA đã tính: {demo_gpa}")

        # Lưu ra file
        print_gpa(demo_name, demo_grades, demo_credits, demo_gpa, "demo_results.txt")

    except Exception as e:
        print(f"Lỗi khi demo: {e}")

# Chạy chương trình chính
if __name__ == "__main__":
    # Cho phép demo trước (tùy chọn)
    print("Bạn có muốn chạy demo chức năng không? (y/n): ", end="")
    if input().lower() == 'y':
        demonstrate_functions()
        print("\nNhấn Enter để tiếp tục vào chương trình chính...")
        input()
        print()

    # Chạy chương trình chính
    main()
