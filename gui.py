# Trong class StudentDashboard
def render_view(self, key):
    if key == "history":
        self.render_history_view()
    elif key == "attend":
        self.render_attend_view()  # MỚI

def render_attend_view(self):
    title = tk.Label(self.content_frame, text="ĐIỂM DANH BUỔI HỌC", font=("Segoe UI", 16, "bold"), bg="white")
    title.pack(anchor="w", padx=20, pady=10)

    sessions = db.get_open_sessions_for_student(self.student_info["id"])
    if not sessions:
        tk.Label(self.content_frame, text="Không có buổi học nào đang mở.", bg="white").pack(pady=20)
        return

    for sess in sessions:
        frame = tk.Frame(self.content_frame, bg="#f0f0f0", relief="ridge", bd=2)
        frame.pack(fill="x", padx=20, pady=5)

        tk.Label(frame, text=f"{sess['class_code']} - {sess['subject_name']} ({sess['date']})", 
                 font=("Segoe UI", 11, "bold"), bg="#f0f0f0").pack(anchor="w", padx=10, pady=5)

        status_var = tk.StringVar(value="PRESENT")
        tk.Radiobutton(frame, text="Có mặt", variable=status_var, value="PRESENT", bg="#f0f0f0").pack(side="left", padx=20)
        tk.Radiobutton(frame, text="Vắng", variable=status_var, value="ABSENT", bg="#f0f0f0").pack(side="left")
        tk.Radiobutton(frame, text="Vắng có phép", variable=status_var, value="ABSENT_EXCUSED", bg="#f0f0f0").pack(side="left")

        note_entry = tk.Entry(frame, width=30)
        note_entry.pack(side="left", padx=10)

        def mark(status_var=status_var, sess=sess, note_entry=note_entry):
            status = status_var.get()
            note = note_entry.get().strip()
            db.student_mark_attendance(self.student_info["id"], sess["id"], status, note or None)
            messagebox.showinfo("Thành công", "Đã điểm danh!")

        tk.Button(frame, text="ĐIỂM DANH", command=mark, bg="#27ae60", fg="white").pack(side="right", padx=10)
