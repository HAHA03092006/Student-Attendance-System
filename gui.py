# Trong class StudentDashboard (thêm vào menu + render)
def __init__(self, master, user_info: dict, student_info: dict):
    self.student_info = student_info
    menu_items = [
        ("history", "Lịch sử điểm danh", "#2E7D32"),
        ("attend", "Tự điểm danh", "#9E9E9E"),
    ]
    super().__init__(master, user_info, "Sinh viên", menu_items)
    self.switch_view("attend")

def render_view(self, key):
    if key == "history":
        self.render_history_view()
    elif key == "attend":
        self.render_attend_view()

def render_attend_view(self):
    title = tk.Label(self.content_frame, text="TỰ ĐIỂM DANH BUỔI HỌC", font=("Segoe UI", 16, "bold"), bg="white")
    title.pack(anchor="w", padx=20, pady=10)

    sessions = db.get_open_sessions_for_student(self.student_info["id"])
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
        options = [("Có mặt", "PRESENT"), ("Vắng", "ABSENT"), ("Vắng có phép", "ABSENT_EXCUSED")]
        for text, val in options:
            tk.Radiobutton(status_frame, text=text, variable=status_var, value=val, bg="#f8f9fa").pack(side="left", padx=10)

        note_entry = tk.Entry(frame, width=40)
        note_entry.pack(pady=5, padx=10)
        note_entry.insert(0, "Lý do (nếu vắng)")

        def mark():
            status = status_var.get()
            note = note_entry.get().strip()
            if note == "Lý do (nếu vắng)": note = ""
            db.student_mark_attendance(self.student_info["id"], sess["id"], status, note or None)
            messagebox.showinfo("Thành công", f"Đã điểm danh: {status}")

        tk.Button(frame, text="ĐIỂM DANH", command=mark, bg="#28a745", fg="white", font=("Segoe UI", 10, "bold")).pack(pady=5)
