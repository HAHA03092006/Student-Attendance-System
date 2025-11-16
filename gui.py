# gui.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import database as db
from auth import hash_password, verify_password, validate_email, validate_required, validate_username
from datetime import datetime

# === BASE DASHBOARD ===
class BaseDashboard:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.content_frame = None
        self.create_sidebar()
    
    def create_sidebar(self):
        sidebar = tk.Frame(self.root, bg="#1976D2", width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        tk.Label(sidebar, text="ĐIỂM DANH", font=("Segoe UI", 14, "bold"), bg="#1976D2", fg="white").pack(pady=20)
        tk.Label(sidebar, text=f"Xin chào,\n{self.user['full_name']}", font=("Segoe UI", 10), bg="#1976D2", fg="white").pack(pady=10)
        
        menu_frame = tk.Frame(sidebar, bg="#1976D2")
        menu_frame.pack(pady=20, fill="both", expand=True)
        
        self.menu_items = self.get_menu_items()
        for key, text, color in self.menu_items:
            btn = tk.Button(menu_frame, text=text, bg=color, fg="white", font=("Segoe UI", 10, "bold"),
                          command=lambda k=key: self.switch_view(k), height=2, relief="flat")
            btn.pack(fill="x", pady=2, padx=10)
        
        tk.Button(sidebar, text="Đăng xuất", bg="#D32F2F", fg="white", font=("Segoe UI", 10),
                command=self.logout).pack(side="bottom", fill="x", pady=20, padx=10)
    
    def get_menu_items(self):
        return []
    
    def switch_view(self, view_key):
        if self.content_frame:
            self.content_frame.destroy()
        self.content_frame = tk.Frame(self.root, bg="white")
        self.content_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        view_method = getattr(self, f"render_{view_key}_view", None)
        if view_method:
            view_method()
        else:
            tk.Label(self.content_frame, text="Chức năng đang phát triển...", font=("Segoe UI", 14), bg="white").pack(pady=50)
    
    def logout(self):
        if messagebox.askyesno("Đăng xuất", "Bạn có chắc muốn đăng xuất?"):
            self.root.destroy()
            import main
            main.main()

# === ADMIN DASHBOARD ===
class AdminDashboard(BaseDashboard):
    def get_menu_items(self):
        return [
            ("classes", "Quản lý lớp", "#7B1FA2"),
            ("users", "Quản lý người dùng", "#7B1FA2"),
            ("report", "Báo cáo tổng hợp", "#E64A19"),
        ]
    
    def render_report_view(self):
        title = tk.Label(self.content_frame, text="BÁO CÁO TỔNG HỢP TOÀN TRƯỜNG", font=("Segoe UI", 16, "bold"), bg="white")
        title.pack(pady=10)

        filter_frame = tk.Frame(self.content_frame, bg="white")
        filter_frame.pack(pady=5)
        tk.Label(filter_frame, text="Từ:", bg="white").pack(side="left")
        from_entry = tk.Entry(filter_frame, width=12)
        from_entry.insert(0, "2025-11-01")
        from_entry.pack(side="left", padx=5)
        tk.Label(filter_frame, text="Đến:", bg="white").pack(side="left")
        to_entry = tk.Entry(filter_frame, width=12)
        to_entry.insert(0, "2025-11-16")
        to_entry.pack(side="left", padx=5)

        def load():
            try:
                data = db.get_school_attendance_report(from_entry.get() or None, to_entry.get() or None)
                for i in tree.get_children(): tree.delete(i)
                for row in data:
                    total = (row['total_sessions'] or 0) * (row['total_students'] or 1)
                    rate = f"{(row['present_count'] or 0) / total * 100:.1f}%" if total > 0 else "0.0%"
                    tree.insert("", "end", values=(
                        row['class_code'], row['class_name'], row['total_students'],
                        row['total_sessions'], row['present_count'], row['absent_count'],
                        row['late_count'], rate
                    ))
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể tải báo cáo: {e}")

        tk.Button(filter_frame, text="Xem", command=load, bg="#E64A19", fg="white").pack(side="left", padx=10)

        cols = ("Lớp", "Tên lớp", "Sĩ số", "Buổi", "Có mặt", "Vắng", "Muộn", "Tỉ lệ")
        tree = ttk.Treeview(self.content_frame, columns=cols, show="headings", height=15)
        for col in cols: 
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")
        tree.pack(padx=20, pady=10, fill="both", expand=True)
        load()

# === TEACHER DASHBOARD ===
class TeacherDashboard(BaseDashboard):
    def get_menu_items(self):
        return [
            ("attendance", "Điểm danh", "#388E3C"),
            ("history", "Lịch sử", "#F57C00"),
        ]

# === STUDENT DASHBOARD ===
class StudentDashboard(BaseDashboard):
    def get_menu_items(self):
        return [
            ("attend", "Tự điểm danh", "#28a745"),
            ("history", "Lịch sử", "#F57C00"),
        ]
    
    def render_attend_view(self):
        title = tk.Label(self.content_frame, text="TỰ ĐIỂM DANH BUỔI HỌC", font=("Segoe UI", 16, "bold"), bg="white")
        title.pack(anchor="w", padx=20, pady=10)

        try:
            sessions = db.get_open_sessions_for_student(self.user["id"])
            if not sessions:
                tk.Label(self.content_frame, text="Không có buổi học nào đang mở.", bg="white", fg="gray").pack(pady=20)
                return

            for sess in sessions:
                frame = tk.Frame(self.content_frame, bg="#f8f9fa", relief="ridge", bd=1)
                frame.pack(fill="x", padx=20, pady=8)

                info = f"{sess['class_code']} - {sess['subject_name']} | {sess['date']} | Mã: {sess['session_code']}"
                tk.Label(frame, text=info, font=("Segoe UI", 10, "bold"), bg="#f8f9fa", anchor="w").pack(fill="x", padx=10, pady=5)

                status_frame = tk.Frame(frame, bg="#f8f9fa")
                status_frame.pack(pady=5)
                status_var = tk.StringVar(value="PRESENT")
                for text, val in [("Có mặt", "PRESENT"), ("Vắng", "ABSENT"), ("Vắng có phép", "ABSENT_EXCUSED")]:
                    tk.Radiobutton(status_frame, text=text, variable=status_var, value=val, bg="#f8f9fa").pack(side="left", padx=10)

                note_entry = tk.Entry(frame, width=40)
                note_entry.pack(pady=5, padx=10)
                note_entry.insert(0, "Lý do (nếu vắng)")

                def mark():
                    status = status_var.get()
                    note = note_entry.get().strip() if note_entry.get().strip() != "Lý do (nếu vắng)" else ""
                    try:
                        db.student_mark_attendance(self.user["id"], sess["id"], status, note or None)
                        messagebox.showinfo("Thành công", f"Đã điểm danh: {status}")
                    except Exception as e:
                        messagebox.showerror("Lỗi", f"Không thể điểm danh: {e}")

                tk.Button(frame, text="ĐIỂM DANH", command=mark, bg="#28a745", fg="white", font=("Segoe UI", 10, "bold")).pack(pady=5)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải buổi học: {e}")

# === LOGIN SCREEN ===
class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root, bg="white")
        self.frame.pack(expand=True, fill="both", padx=60, pady=60)
        
        tk.Label(self.frame, text="ĐĂNG NHẬP HỆ THỐNG", font=("Segoe UI", 20, "bold"), bg="white", fg="#1976D2").pack(pady=30)
        
        # Username
        tk.Label(self.frame, text="Tên đăng nhập:", bg="white", font=("Segoe UI", 10)).pack(anchor="w", padx=100)
        self.username_entry = tk.Entry(self.frame, width=35, font=("Segoe UI", 11))
        self.username_entry.pack(pady=8, padx=100)
        self.username_entry.focus()
        
        # Password
        tk.Label(self.frame, text="Mật khẩu:", bg="white", font=("Segoe UI", 10)).pack(anchor="w", padx=100)
        self.password_entry = tk.Entry(self.frame, width=35, font=("Segoe UI", 11), show="*")
        self.password_entry.pack(pady=8, padx=100)
        self.password_entry.bind("<Return>", lambda e: self.login())
        
        # Buttons
        btn_frame = tk.Frame(self.frame, bg="white")
        btn_frame.pack(pady=25)
        tk.Button(btn_frame, text="Đăng nhập", command=self.login, bg="#1976D2", fg="white", font=("Segoe UI", 11, "bold"), width=15).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Quên mật khẩu?", command=self.forgot_password, bg="#757575", fg="white", font=("Segoe UI", 9)).pack(side="left", padx=10)
    
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        # Validation
        if err := validate_required(username, "Tên đăng nhập"): messagebox.showerror("Lỗi", err); return
        if err := validate_username(username): messagebox.showerror("Lỗi", err); return
        if err := validate_required(password, "Mật khẩu"): messagebox.showerror("Lỗi", err); return
        
        try:
            user = db.get_user_by_username(username)
            if not user or not verify_password(password, user["password_hash"]):
                messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng.")
                return
            
            self.frame.destroy()
            if user["role"] == "ADMIN":
                AdminDashboard(self.root, user)
            elif user["role"] == "TEACHER":
                TeacherDashboard(self.root, user)
            else:
                StudentDashboard(self.root, user)
        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", f"Không thể kết nối cơ sở dữ liệu:\n{e}")
    
    def forgot_password(self):
        email = simpledialog.askstring("Quên mật khẩu", "Nhập email của bạn:", parent=self.root)
        if not email: return
        if not validate_email(email):
            messagebox.showerror("Lỗi", "Email không hợp lệ.")
            return
        try:
            token = db.request_password_reset(email)
            if token:
                messagebox.showinfo("Thành công", "Link đặt lại mật khẩu đã được gửi đến email!")
            else:
                messagebox.showerror("Lỗi", "Email không tồn tại trong hệ thống.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể gửi yêu cầu: {e}")
