# gui.py – Chỉ phần AdminDashboard.render_report_view và StudentDashboard.render_attend_view

# === ADMIN: BÁO CÁO TỔNG HỢP ===
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

    tk.Button(filter_frame, text="Xem", command=load, bg="#E64A19", fg="white").pack(side="left", padx=10)

    cols = ("Lớp", "Tên lớp", "Sĩ số", "Buổi", "Có mặt", "Vắng", "Muộn", "Tỉ lệ")
    tree = ttk.Treeview(self.content_frame, columns=cols, show="headings", height=15)
    for col in cols: 
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")
    tree.pack(padx=20, pady=10, fill="both", expand=True)
    load()

# === STUDENT: TỰ ĐIỂM DANH ===
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
        for text, val in [("Có mặt", "PRESENT"), ("Vắng", "ABSENT"), ("Vắng có phép", "ABSENT_EXCUSED")]:
            tk.Radiobutton(status_frame, text=text, variable=status_var, value=val, bg="#f8f9fa").pack(side="left", padx=10)

        note_entry = tk.Entry(frame, width=40)
        note_entry.pack(pady=5, padx=10)
        note_entry.insert(0, "Lý do (nếu vắng)")

        def mark():
            status = status_var.get()
            note = note_entry.get().strip() if note_entry.get().strip() != "Lý do (nếu vắng)" else ""
            db.student_mark_attendance(self.student_info["id"], sess["id"], status, note or None)
            messagebox.showinfo("Thành công", f"Đã điểm danh: {status}")

        tk.Button(frame, text="ĐIỂM DANH", command=mark, bg="#28a745", fg="white", font=("Segoe UI", 10, "bold")).pack(pady=5)
