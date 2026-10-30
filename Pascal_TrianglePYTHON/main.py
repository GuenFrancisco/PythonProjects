
import math
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG_COLOR = "#0B1120"
SIDEBAR_COLOR = "#101A2E"
PANEL_COLOR = "#151F33"
INPUT_COLOR = "#202C43"
BORDER_COLOR = "#2B3A54"
TEXT_COLOR = "#F1F5F9"
MUTED_COLOR = "#94A3B8"
ACCENT_COLOR = "#2DD4BF"
PURPLE_COLOR = "#A78BFA"


class PascalTriangleApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Pascal's Triangle")
        self.geometry("1100x720")
        self.minsize(850, 600)
        self.configure(fg_color=BG_COLOR)

        self.current_page = None
        self.nav_buttons = {}

        self.create_sidebar()
        self.create_content_area()

        self.show_page("Triangle")


    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0,
            fg_color=SIDEBAR_COLOR
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        logo = ctk.CTkLabel(
            self.sidebar,
            text="PASCAL'S\nTRIANGLE",
            font=("Segoe UI", 23, "bold"),
            text_color=ACCENT_COLOR,
            justify="left"
        )
        logo.pack(anchor="w", padx=24, pady=(35, 5))

        subtitle = ctk.CTkLabel(
            self.sidebar,
            text="BINOMIAL COEFFICIENTS",
            font=("Segoe UI", 10, "bold"),
            text_color=MUTED_COLOR
        )
        subtitle.pack(anchor="w", padx=25, pady=(0, 35))

        nav_label = ctk.CTkLabel(
            self.sidebar,
            text="NAVIGATION",
            font=("Segoe UI", 11, "bold"),
            text_color=MUTED_COLOR
        )
        nav_label.pack(anchor="w", padx=24, pady=(0, 10))

        pages = [
            ("Triangle", "△"),
            ("nCk Calculator", "∑"),
            ("Patterns", "◇")
        ]

        for page_name, symbol in pages:

            button = ctk.CTkButton(
                self.sidebar,
                text=f"  {symbol}   {page_name}",
                height=45,
                anchor="w",
                corner_radius=10,
                font=("Segoe UI", 13),
                fg_color="transparent",
                hover_color="#263650",
                text_color=TEXT_COLOR,
                command=lambda name=page_name: self.show_page(name)
            )

            button.pack(fill="x", padx=14, pady=4)
            self.nav_buttons[page_name] = button

        footer = ctk.CTkLabel(
            self.sidebar,
            text="PYTHON PROJECT",
            font=("Segoe UI", 10),
            text_color=MUTED_COLOR
        )
        footer.pack(side="bottom", anchor="w", padx=24, pady=25)


    def create_content_area(self):

        self.content = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=BG_COLOR
        )
        self.content.pack(
            side="left",
            fill="both",
            expand=True
        )

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    def show_page(self, page_name):

        self.current_page = page_name
        self.clear_content()

        for name, button in self.nav_buttons.items():

            if name == page_name:
                button.configure(
                    fg_color="#263650",
                    text_color=ACCENT_COLOR
                )
            else:
                button.configure(
                    fg_color="transparent",
                    text_color=TEXT_COLOR
                )

        if page_name == "Triangle":
            self.create_triangle_page()

        elif page_name == "nCk Calculator":
            self.create_calculator_page()

        elif page_name == "Patterns":
            self.create_patterns_page()



    def create_page_header(self, title, description):

        header = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )
        header.pack(
            fill="x",
            padx=35,
            pady=(30, 20)
        )

        # Centered page title
        ctk.CTkLabel(
            header,
            text=title,
            font=("Segoe UI", 27, "bold"),
            text_color=TEXT_COLOR,
            anchor="center"
        ).pack(fill="x")

        # Centered page description
        ctk.CTkLabel(
            header,
            text=description,
            font=("Segoe UI", 12),
            text_color=MUTED_COLOR,
            anchor="center",
            justify="center",
            wraplength=650
        ).pack(fill="x", pady=(5, 0))

    def create_panel(self, parent, **kwargs):

        return ctk.CTkFrame(
            parent,
            fg_color=PANEL_COLOR,
            corner_radius=15,
            border_width=1,
            border_color=BORDER_COLOR,
            **kwargs
        )

    def create_input(self, parent, placeholder, width=180):

        return ctk.CTkEntry(
            parent,
            width=width,
            height=42,
            placeholder_text=placeholder,
            fg_color=INPUT_COLOR,
            border_color=BORDER_COLOR,
            text_color=TEXT_COLOR,
            placeholder_text_color=MUTED_COLOR,
            corner_radius=9,
            font=("Segoe UI", 13)
        )

    def create_action_button(self, parent, text, command):

        return ctk.CTkButton(
            parent,
            text=text,
            height=42,
            corner_radius=9,
            fg_color=ACCENT_COLOR,
            hover_color="#20B8A7",
            text_color="#071521",
            font=("Segoe UI", 13, "bold"),
            command=command
        )


    def create_octagon(self, parent, value, row_index):

      
        number_width = max(48, len(value) * 10 + 16)
        number_height = 44

        canvas = tk.Canvas(
            parent,
            width=number_width,
            height=number_height,
            bg=PANEL_COLOR,
            highlightthickness=0,
            bd=0
        )


        corner = 9
        padding = 2

        points = [
            padding + corner, padding,
            number_width - padding - corner, padding,
            number_width - padding, padding + corner,
            number_width - padding, number_height - padding - corner,
            number_width - padding - corner, number_height - padding,
            padding + corner, number_height - padding,
            padding, number_height - padding - corner,
            padding, padding + corner
        ]

    
        outline_color = (
            ACCENT_COLOR if row_index == 0
            else BORDER_COLOR
        )

        text_color = (
            ACCENT_COLOR if row_index == 0
            else TEXT_COLOR
        )

        canvas.create_polygon(
            points,
            fill=PANEL_COLOR,
            outline=outline_color,
            width=1.5
        )

        canvas.create_text(
            number_width / 2,
            number_height / 2,
            text=value,
            fill=text_color,
            font=("Consolas", 11, "bold")
        )

        canvas.pack(side="left", padx=3, pady=3)

        return canvas



    def create_triangle_page(self):

        # Shortened title as requested.
        self.create_page_header(
            "Triangle",
            "Generate rows and explore binomial coefficients."
        )

        controls = self.create_panel(self.content)
        controls.pack(fill="x", padx=35, pady=(0, 18))

        ctk.CTkLabel(
            controls,
            text="NUMBER OF ROWS",
            font=("Segoe UI", 11, "bold"),
            text_color=MUTED_COLOR
        ).pack(anchor="w", padx=20, pady=(18, 8))

        input_row = ctk.CTkFrame(
            controls,
            fg_color="transparent"
        )
        input_row.pack(fill="x", padx=20, pady=(0, 18))

        self.rows_entry = self.create_input(
            input_row,
            "Enter number of rows",
            width=220
        )
        self.rows_entry.pack(side="left", padx=(0, 12))

        self.create_action_button(
            input_row,
            "Generate Triangle",
            self.generate_triangle
        ).pack(side="left")

        self.rows_entry.bind(
            "<Return>",
            lambda event: self.generate_triangle()
        )

        self.triangle_panel = self.create_panel(self.content)
        self.triangle_panel.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(0, 30)
        )

        self.triangle_output = ctk.CTkScrollableFrame(
            self.triangle_panel,
            fg_color="transparent",
            corner_radius=10
        )
        self.triangle_output.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=12
        )

        self.triangle_placeholder = ctk.CTkLabel(
            self.triangle_output,
            text="Your triangle will appear here",
            font=("Segoe UI", 14),
            text_color=MUTED_COLOR
        )
        self.triangle_placeholder.pack(pady=80)

    def generate_triangle(self):

        value = self.rows_entry.get().strip()

        if not value:
            messagebox.showwarning(
                "Missing Input",
                "Please enter the number of rows."
            )
            return

        try:
            rows = int(value)

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter a whole number."
            )
            return

        if rows < 1 or rows > 30:
            messagebox.showwarning(
                "Invalid Number",
                "Please enter a number from 1 to 30."
            )
            return

        for widget in self.triangle_output.winfo_children():
            widget.destroy()

        for row_index in range(rows):

            values = [
                str(math.comb(row_index, column))
                for column in range(row_index + 1)
            ]

            
            row_frame = ctk.CTkFrame(
                self.triangle_output,
                fg_color="transparent"
            )
            row_frame.pack(
                fill="x",
                pady=2
            )

            number_container = ctk.CTkFrame(
                row_frame,
                fg_color="transparent"
            )
            number_container.pack(anchor="center")

            # Put each coefficient inside its own octagon.
            for number in values:
                self.create_octagon(
                    number_container,
                    number,
                    row_index
                )



    def create_calculator_page(self):

        self.create_page_header(
            "nCk Calculator",
            "Calculate a binomial coefficient using row n and column k."
        )

        calculator = self.create_panel(self.content)
        calculator.pack(
            fill="x",
            padx=35,
            pady=(0, 20)
        )

        ctk.CTkLabel(
            calculator,
            text="BINOMIAL COEFFICIENT",
            font=("Segoe UI", 11, "bold"),
            text_color=MUTED_COLOR
        ).pack(anchor="w", padx=22, pady=(22, 16))

        fields = ctk.CTkFrame(
            calculator,
            fg_color="transparent"
        )
        fields.pack(fill="x", padx=22, pady=(0, 18))

        n_frame = ctk.CTkFrame(
            fields,
            fg_color="transparent"
        )
        n_frame.pack(side="left", padx=(0, 15))

        ctk.CTkLabel(
            n_frame,
            text="Row (n)",
            text_color=TEXT_COLOR,
            font=("Segoe UI", 12)
        ).pack(anchor="w", pady=(0, 7))

        self.n_entry = self.create_input(
            n_frame,
            "Enter n",
            width=150
        )
        self.n_entry.pack()

        k_frame = ctk.CTkFrame(
            fields,
            fg_color="transparent"
        )
        k_frame.pack(side="left", padx=(0, 15))

        ctk.CTkLabel(
            k_frame,
            text="Column (k)",
            text_color=TEXT_COLOR,
            font=("Segoe UI", 12)
        ).pack(anchor="w", pady=(0, 7))

        self.k_entry = self.create_input(
            k_frame,
            "Enter k",
            width=150
        )
        self.k_entry.pack()

        self.create_action_button(
            fields,
            "Calculate",
            self.calculate_combination
        ).pack(side="left", anchor="center", pady=(22, 0))

        self.n_entry.bind(
            "<Return>",
            lambda event: self.calculate_combination()
        )

        self.k_entry.bind(
            "<Return>",
            lambda event: self.calculate_combination()
        )

        self.result_panel = self.create_panel(self.content)
        self.result_panel.pack(
            fill="x",
            padx=35,
            pady=(0, 20)
        )

        ctk.CTkLabel(
            self.result_panel,
            text="RESULT",
            font=("Segoe UI", 11, "bold"),
            text_color=MUTED_COLOR
        ).pack(anchor="w", padx=22, pady=(20, 8))

        self.result_label = ctk.CTkLabel(
            self.result_panel,
            text="—",
            font=("Segoe UI", 36, "bold"),
            text_color=ACCENT_COLOR
        )
        self.result_label.pack(anchor="w", padx=22)

        self.formula_label = ctk.CTkLabel(
            self.result_panel,
            text="Enter n and k to calculate the coefficient.",
            font=("Segoe UI", 13),
            text_color=MUTED_COLOR,
            wraplength=650,
            justify="left"
        )
        self.formula_label.pack(
            anchor="w",
            padx=22,
            pady=(8, 22)
        )

    def calculate_combination(self):

        n_value = self.n_entry.get().strip()
        k_value = self.k_entry.get().strip()

        if not n_value or not k_value:
            messagebox.showwarning(
                "Missing Input",
                "Please enter both n and k."
            )
            return

        try:
            n = int(n_value)
            k = int(k_value)

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Both n and k must be whole numbers."
            )
            return

        if n < 0 or k < 0:
            messagebox.showwarning(
                "Invalid Values",
                "n and k cannot be negative."
            )
            return

        if n > 1000:
            messagebox.showwarning(
                "Number Too Large",
                "Please enter n up to 1000."
            )
            return

        if k > n:
            messagebox.showwarning(
                "Invalid Values",
                "k must be less than or equal to n."
            )
            return

        result = math.comb(n, k)

        self.result_label.configure(
            text=f"C({n}, {k}) = {result}"
        )

        self.formula_label.configure(
            text=(
                f"C(n, k) = n! / (k! × (n-k)!)\n\n"
                f"C({n}, {k}) = {n}! / "
                f"({k}! × ({n}-{k})!)\n"
                f"Result = {result}"
            )
        )



    def create_patterns_page(self):

        self.create_page_header(
            "Patterns",
            "Discover mathematical patterns inside Pascal's Triangle."
        )

        scroll = ctk.CTkScrollableFrame(
            self.content,
            fg_color="transparent"
        )
        scroll.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(0, 25)
        )

        patterns = [
            (
                "01",
                "Symmetry",
                "Each row reads the same from left to right "
                "and right to left.",
                "1   4   6   4   1"
            ),
            (
                "02",
                "Row Sums",
                "The sum of the numbers in row n equals 2ⁿ.",
                "1 + 3 + 3 + 1 = 8 = 2³"
            ),
            (
                "03",
                "Fibonacci Diagonals",
                "Adding the numbers along selected shallow "
                "diagonals produces Fibonacci numbers.",
                "1, 1, 2, 3, 5, 8, ..."
            ),
            (
                "04",
                "Binomial Theorem",
                "Each row gives the coefficients for expanding "
                "(a + b)ⁿ.",
                "(a + b)³ = a³ + 3a²b + 3ab² + b³"
            )
        ]

        for number, title, description, example in patterns:

            card = self.create_panel(scroll)
            card.pack(fill="x", pady=7)

            ctk.CTkLabel(
                card,
                text=number,
                font=("Segoe UI", 12, "bold"),
                text_color=ACCENT_COLOR
            ).pack(anchor="w", padx=20, pady=(16, 3))

            ctk.CTkLabel(
                card,
                text=title,
                font=("Segoe UI", 18, "bold"),
                text_color=TEXT_COLOR
            ).pack(anchor="w", padx=20, pady=(0, 6))

            ctk.CTkLabel(
                card,
                text=description,
                font=("Segoe UI", 12),
                text_color=MUTED_COLOR,
                wraplength=680,
                justify="left"
            ).pack(anchor="w", padx=20, pady=(0, 10))

            ctk.CTkLabel(
                card,
                text=example,
                font=("Consolas", 13),
                text_color=PURPLE_COLOR,
                wraplength=680,
                justify="left"
            ).pack(anchor="w", padx=20, pady=(0, 16))


if __name__ == "__main__":
    app = PascalTriangleApp()
    app.mainloop()
