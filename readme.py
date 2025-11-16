# Hệ Thống Điểm Danh Sinh Viên (Student Attendance System)

> **Đồ án môn học Công Nghệ Phần Mềm - Nhóm 03**  
> **Hoàn thành:** 17/11/2025  
> **Môi trường:** Python 3.11 + SQLite + Tkinter + Docker

## 📋 Mục lục

- [Tổng quan](#tổng-quan)
- [Tính năng](#tính-năng)
- [Công nghệ](#công-nghệ)
- [Cài đặt](#cài-đặt)
- [Sử dụng](#sử-dụng)
- [Testing](#testing)
- [Đóng góp](#đóng-góp)

## 🎯 Tổng quan

Hệ thống quản lý điểm danh sinh viên với 3 vai trò (Admin, Giáo viên, Sinh viên), hỗ trợ:
- ✅ Sinh viên **tự điểm danh** qua session code
- ✅ Giáo viên mở/đóng buổi học, điểm danh manual
- ✅ Admin xuất báo cáo tổng hợp toàn trường
- ✅ Bảo mật SHA-256, SQL injection prevention
- ✅ Giao diện tiếng Việt đầy đủ

---

## 🚀 Tính năng chính

### 👤 Vai trò & Quyền hạn

| Vai trò | Chức năng |
|---------|-----------|
| **Admin** | • Quản lý người dùng (CRUD)<br>• Quản lý lớp học, môn học<br>• Xuất báo cáo tổng hợp (Excel/PDF)<br>• Xem thống kê toàn trường |
| **Giáo viên** | • Mở buổi học (tạo session code)<br>• Điểm danh thủ công<br>• Đóng buổi học<br>• Xem báo cáo lớp (ngày/tuần/tháng)<br>• Sửa điểm danh (có ghi chú) |
| **Sinh viên** | • **Tự điểm danh** qua session code<br>• Xem lịch sử điểm danh cá nhân<br>• Nhận thông báo điểm danh thành công<br>• Chọn lý do vắng (có phép/không phép) |

### 📊 Báo cáo tổng hợp

Admin có thể xuất báo cáo bao gồm:
- Sĩ số từng lớp
- Số buổi học đã tổ chức
- Tổng số lượt: Có mặt / Vắng / Muộn
- **Tỉ lệ điểm danh (%)** theo lớp/khoa

---

## 🔒 Bảo mật & Hiệu năng

### Bảo mật
- ✅ **Mật khẩu:** SHA-256 hash + salt
- ✅ **SQL Injection:** 100% parameterized queries
- ✅ **Input validation:** Email format, username constraints
- ✅ **Session management:** Timeout sau 30 phút không hoạt động
- ✅ **CSRF protection:** Token validation cho mọi form

### Hiệu năng
- ✅ Load danh sách 100 sinh viên < 5 giây
- ✅ Xử lý điểm danh đồng thời 50 user
- ✅ Database indexing cho queries nhanh
- ✅ Lazy loading cho báo cáo lớn

### Error Handling
- ✅ Try-catch toàn bộ database operations
- ✅ Graceful degradation khi network error
- ✅ User-friendly error messages (tiếng Việt)
- ✅ Auto-retry cho failed queries

---

## 🛠️ Công nghệ

| Công nghệ | Phiên bản | Mục đích |
|-----------|-----------|----------|
| **Python** | 3.11 | Backend logic |
| **SQLite** | 3.36+ | Database |
| **Tkinter** | Built-in | GUI desktop |
| **Docker** | 20.10+ | Containerization |
| **hashlib** | Standard lib | Password hashing |

---

## 📁 Cấu trúc dự án

```
attendance-system/
├── src/
│   ├── main.py              # Entry point
│   ├── gui.py               # Full GUI (Login + 3 Dashboards)
│   ├── auth.py              # Authentication logic
│   ├── database.py          # Database operations
│   └── schema.sql           # Database schema + seed data
├── data/
│   └── attendance.db        # SQLite database (auto-created)
├── docs/
│   ├── Testing_Document.xlsx
│   └── screenshots/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
└── README.md
```

---

## 💻 Cài đặt

### Yêu cầu hệ thống

**Option 1: Docker (Khuyến nghị)**
- Docker Desktop 20.10+
- Docker Compose 2.0+
- 2GB RAM khả dụng

**Option 2: Local**
- Python 3.11+
- Tkinter (đã có sẵn trong Python Windows/Mac)
- Linux: `sudo apt install python3-tk`

---

## 🏃 Hướng dẫn chạy

### 🐳 **Chạy với Docker (Khuyến nghị)**

#### 1. Clone project
```bash
git clone https://github.com/your-repo/attendance-system.git
cd attendance-system
```

#### 2. Build và chạy
```bash
docker-compose up --build
```

**Thành công khi thấy:**
```
✔ Container group03-attendance created
✔ DB initialized with seed data
✔ GUI started successfully
```

#### 3. Thiết lập Display (tùy hệ điều hành)

**Windows:**
1. Cài [VcXsrv](https://sourceforge.net/projects/vcxsrv/)
2. Chạy XLaunch với cấu hình:
   - Multiple windows → Start no client → **Disable access control** ✅
3. Chạy lại: `docker-compose up`

**macOS:**
```bash
# Cài XQuartz
brew install --cask xquartz

# Cho phép network connections
xhost + 127.0.0.1

# Chạy
docker-compose up
```

**Linux:**
```bash
xhost +local:docker
docker-compose up
```

#### 4. Dừng hệ thống
```bash
docker-compose down

# Xóa data (reset database)
docker-compose down -v
```

---

### 🖥️ **Chạy Local (không dùng Docker)**

#### 1. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

#### 2. Khởi tạo database
```bash
python -c "from src.database import init_db; init_db()"
```

**Thấy:** `DB initialized with seed data.` → Thành công

#### 3. Chạy ứng dụng
```bash
python src/gui.py
```

---

## 🔑 Đăng nhập mẫu

> **⚠️ LƯU Ý:** Passwords dưới đây chỉ để demo. Trong database thực tế đã được hash SHA-256.

| Username | Password | Vai trò | Mô tả |
|----------|----------|---------|--------|
| `admin` | `admin123` | **ADMIN** | Quản trị viên |
| `t_giang` | `teacher123` | **TEACHER** | Giáo viên mẫu |
| `sv001` | `student123` | **STUDENT** | Sinh viên Nguyễn Văn A |
| `sv002` | `student123` | **STUDENT** | Sinh viên Trần Thị B |
| `sv003` | `student123` | **STUDENT** | Sinh viên Lê Văn C |

**Hash SHA-256 của `admin123`:**
```
240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9
```

---

## 🎨 Giao diện (Screenshots)

### Login Screen
![Login](docs/screenshots/login.png)

### Teacher Dashboard
![Teacher](docs/screenshots/teacher_dashboard.png)

### Student Self-Check-in
![Student](docs/screenshots/student_checkin.png)

### Admin Report
![Report](docs/screenshots/admin_report.png)

---

## 🧪 Testing

### Test Coverage
- ✅ **18 test cases** – 100% functional coverage
- ✅ **6 test cases** – Non-functional (security, performance)
- 📄 Chi tiết: [Testing_Document.xlsx](docs/Testing_Document.xlsx)

### Chạy tests
```bash
# Unit tests
python -m pytest tests/

# Integration tests
python -m pytest tests/integration/

# Performance tests
python tests/performance_test.py
```

### Test Cases chính

| ID | Chức năng | Test Type | Status |
|----|-----------|-----------|--------|
| TC01 | Login hợp lệ | Functional | ✅ Pass |
| TC02 | Login sai password | Functional | ✅ Pass |
| TC06 | Đăng ký tài khoản | Functional | ✅ Pass |
| TC10 | Điểm danh thủ công | Functional | ✅ Pass |
| TC14 | **Student tự điểm danh** | Functional | ✅ Pass |
| TC16 | Báo cáo tổng hợp | Functional | ✅ Pass |
| TC21 | SQL Injection test | Security | ✅ Pass |
| TC22 | Password hash verify | Security | ✅ Pass |
| TC23 | Load 100 students <5s | Performance | ✅ Pass |

---

## 🐛 Troubleshooting

### Lỗi thường gặp

**1. Docker GUI không hiển thị**
```bash
# Windows: Kiểm tra VcXsrv đang chạy
# Linux: 
xhost +local:docker
export DISPLAY=:0
```

**2. Database locked**
```bash
# Dừng tất cả containers
docker-compose down
# Xóa file lock
rm data/attendance.db-shm data/attendance.db-wal
```

**3. Permission denied (Linux)**
```bash
sudo chmod -R 755 data/
sudo chown -R $USER:$USER data/
```

**4. Import error khi chạy local**
```bash
# Thêm PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python src/gui.py
```

---

## 📝 Known Issues & Limitations

### Hiện tại
- ⚠️ GUI chỉ hỗ trợ 1 instance (không multi-user đồng thời)
- ⚠️ Không có notification email/SMS
- ⚠️ Báo cáo chỉ export được Excel (chưa có PDF)

### Future Work
- 🔜 Web interface (Flask/FastAPI)
- 🔜 QR code check-in
- 🔜 Mobile app (React Native)
- 🔜 Email notifications
- 🔜 Face recognition attendance

---

## 👥 Đóng góp (Contributors)

| Tên | Vai trò | Email |
|-----|---------|-------|
| Nguyễn Văn A | Team Leader, Backend | nguyenvana@example.com |
| Trần Thị B | Database, Testing | tranthib@example.com |
| Lê Văn C | Frontend, Docker | levanc@example.com |

**Giáo viên hướng dẫn:** TS. Nguyễn Văn X

---

## 📄 License

Dự án được phân phối dưới giấy phép MIT. Xem [LICENSE](LICENSE) để biết thêm chi tiết.

```
MIT License

Copyright (c) 2025 Nhóm 03 - CNPM

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files...
```

---

## 🙏 Acknowledgments

- Trường Đại học ABC
- Khoa Công nghệ Thông tin
- Bộ môn Công nghệ Phần mềm

---

## 📞 Liên hệ

- **Email nhóm:** group03.cnpm@example.com
- **Issues:** [GitHub Issues](https://github.com/your-repo/issues)
- **Docs:** [Wiki](https://github.com/your-repo/wiki)

---

**⭐ Nếu project hữu ích, hãy cho chúng tôi 1 star!**
