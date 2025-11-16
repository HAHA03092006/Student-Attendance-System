markdown# 
Hệ Thống Điểm Danh Sinh Viên (Attendance System)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![SQLite](https://img.shields.io/badge/SQLite-3.36-lightgrey?logo=sqlite)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)
![Status](https://img.shields.io/badge/Status-Completed-success)

> **Đồ án môn học - Nhóm 03**  
> **Hoàn thành:** 17/11/2025  
> **Môi trường:** Python 3.11 + SQLite + Tkinter + Docker


## Tính năng chính

| Vai trò | Chức năng |
|--------|----------|
| **Admin** | Quản lý lớp, người dùng, xuất báo cáo tổng hợp toàn trường |
| **Giáo viên** | Mở buổi, điểm danh, đóng buổi |
| **Sinh viên** | Tự điểm danh, xem lịch sử |

**Báo cáo tổng hợp:** Sĩ số, số buổi, có mặt/vắng/muộn, **tỉ lệ điểm danh (%)**


## Cấu trúc dự án
├── Dockerfile
├── docker-compose.yml
├── schema.sql
├── database.py
├── gui.py
├── attendance.db     ← tạo tự động
├── data/            ← backup, log
└── README.md
text
## Yêu cầu hệ thống

- **Docker Desktop** (khuyên dùng)
- Hoặc: Python 3.11 + Tkinter
## Hướng dẫn chạy (Docker – ưu tiên)

1. **Clone / copy project**  
   ```bash
   git clone <your-repo-url>
   cd attendance-system

2.Chạy

bash

&nbsp;&nbsp;&nbsp;docker-compose up --build &nbsp;&nbsp;&nbsp;
   → Thành công khi thấy:
   text
    &nbsp;&nbsp;&nbsp;DB initialized with seed data. &nbsp;&nbsp;&nbsp;

3.Mở GUI

   * Windows: VcXsrv hoặc Docker Desktop WSL2
   
   * Mac: Tự động
   
   * Linux:
   
     bash
     
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;xhost +local:docker
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;docker-compose up --build 
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
Hướng dẫn chạy (Local)

bash

textpython -c "import database; database.init_db()"
python gui.py

Đăng nhập mẫu

UserPassRoleadminadmin123ADMINt_giangteacher123TEACHERsv001student123STUDENT

Test Coverage

18 test cases – 100% functional

Xem: docs/Testing_Document.xlsx

Công nghệ

Python 3.11
SQLite
Tkinter
Docker
























UserPassRoleadminadmin123ADMINt_giangteacher123TEACHERsv001student123STUDENT

Test Coverage

18 test cases – 100% functional
Xem: docs/Testing_Document.xlsx


Công nghệ

Python 3.11
SQLite
Tkinter
Docker
