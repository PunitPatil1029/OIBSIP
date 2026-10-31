
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timezone, timedelta
from PIL import Image
import os

from weather_api import (
    get_current_weather,
    get_forecast,
    WeatherAPIError
)

# ---------------- APP SETTINGS ----------------

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

BG = "#EAF3FA"
CARD = "#F7FBFF"
CARD2 = "#E2EFF8"
BLUE = "#69AEEB"
BLUE_HOVER = "#438FCF"
WHITE = "#FFFFFF"
TEXT = "#243B53"
MUTED = "#637D96"
CYAN = "#328CCB"
YELLOW = "#E49B25"
BORDER = "#C7DCEC"


class WeatherApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("1350x950")
        self.root.minsize(1050, 800)
        self.root.configure(fg_color=BG)

        self.unit = "C"
        self.current_data = None
        self.forecast_data = None

        self.load_background()
        self.create_widgets()

    # ---------------- BACKGROUND IMAGE ----------------

    def load_background(self):

        image_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "assets",
            "background.png"
        )

        try:
            image = Image.open(image_path).convert("RGB")

            self.bg_image = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=(1350, 950)
            )

            self.bg_label = ctk.CTkLabel(
                self.root,
                text="",
                image=self.bg_image
            )

            self.bg_label.place(
                x=0,
                y=0,
                relwidth=1,
                relheight=1
            )

            self.bg_label.lower()

        except Exception as error:
            print("Background image could not be loaded:", error)

    # ---------------- WEATHER ICON ----------------

    def get_icon(self, condition):

        condition = condition.lower()

        if "thunder" in condition:
            return "⛈️"
        elif "rain" in condition or "drizzle" in condition:
            return "🌧️"
        elif "snow" in condition:
            return "❄️"
        elif "cloud" in condition:
            return "🌤️"
        elif "clear" in condition:
            return "☀️"
        elif "mist" in condition or "fog" in condition:
            return "🌫️"

        return "🌤️"

    # ---------------- TEMPERATURE ----------------

    def convert_temp(self, temperature):

        if self.unit == "F":
            return (temperature * 9 / 5) + 32

        return temperature

    def temp_text(self, temperature):

        return f"{self.convert_temp(temperature):.1f}°{self.unit}"

    # ---------------- MAIN UI ----------------

    def create_widgets(self):

        # Header
        header = ctk.CTkFrame(
            self.root,
            fg_color="transparent"
        )
        header.pack(fill="x", padx=35, pady=(20, 12))

        title_frame = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )
        title_frame.pack(side="left")

        ctk.CTkLabel(
            title_frame,
            text="🌤️  Weather App",
            font=("Segoe UI", 30, "bold"),
            text_color=TEXT
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_frame,
            text="Check real-time weather of any city",
            font=("Segoe UI", 13),
            text_color=MUTED
        ).pack(anchor="w", pady=3)

        # Search
        search_frame = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )
        search_frame.pack(side="right", padx=5)

        self.city_entry = ctk.CTkEntry(
            search_frame,
            width=250,
            height=45,
            placeholder_text="Enter city name...",
            font=("Segoe UI", 15),
            corner_radius=15,
            fg_color=WHITE,
            text_color=TEXT,
            placeholder_text_color=MUTED,
            border_color=BORDER
        )
        self.city_entry.pack(side="left", padx=5)

        self.city_entry.bind(
            "<Return>",
            lambda event: self.show_weather()
        )

        ctk.CTkButton(
            search_frame,
            text="Search",
            width=105,
            height=45,
            corner_radius=15,
            fg_color=BLUE,
            hover_color=BLUE_HOVER,
            text_color=WHITE,
            font=("Segoe UI", 14, "bold"),
            command=self.show_weather
        ).pack(side="left", padx=5)

        self.unit_button = ctk.CTkSegmentedButton(
            search_frame,
            values=["°C", "°F"],
            width=110,
            height=40,
            corner_radius=12,
            fg_color=CARD2,
            selected_color=BLUE,
            selected_hover_color=BLUE_HOVER,
            unselected_color=WHITE,
            unselected_hover_color=CARD2,
            text_color=TEXT,

            command=self.change_unit
        )
        self.unit_button.pack(side="left", padx=10)
        self.unit_button.set("°C")

        # Main weather card
        self.main_card = ctk.CTkFrame(
            self.root,
            fg_color=CARD,
            corner_radius=25,
            border_width=1,
            border_color=BORDER
        )
        self.main_card.pack(
            fill="x",
            padx=35,
            pady=12
        )

        self.main_card.grid_columnconfigure(0, weight=1)
        self.main_card.grid_columnconfigure(1, weight=1)

        left = ctk.CTkFrame(
            self.main_card,
            fg_color="transparent"
        )
        left.grid(
            row=0,
            column=0,
            padx=30,
            pady=25,
            sticky="nsew"
        )

        self.weather_icon = ctk.CTkLabel(
            left,
            text="🌤️",
            font=("Segoe UI Emoji", 85)
        )
        self.weather_icon.pack()

        self.temperature_label = ctk.CTkLabel(
            left,
            text="--°C",
            font=("Segoe UI", 65, "bold"),
            text_color=TEXT
        )
        self.temperature_label.pack(pady=2)

        self.feels_label = ctk.CTkLabel(
            left,
            text="Feels Like: --°C",
            font=("Segoe UI", 18),
            text_color=MUTED
        )
        self.feels_label.pack()

        self.city_label = ctk.CTkLabel(
            left,
            text="Search Your City",
            font=("Segoe UI", 28, "bold"),
            text_color=TEXT
        )
        self.city_label.pack(pady=(12, 3))

        self.description_label = ctk.CTkLabel(
            left,
            text="Current Weather",
            font=("Segoe UI", 17),
            text_color=CYAN
        )
        self.description_label.pack()

        # Right side details
        right = ctk.CTkFrame(
            self.main_card,
            fg_color="transparent"
        )
        right.grid(
            row=0,
            column=1,
            padx=25,
            pady=30,
            sticky="nsew"
        )

        self.detail_labels = {}

        details = [
            ("💧", "Humidity", "humidity"),
            ("💨", "Wind Speed", "wind"),
            ("🌡️", "Pressure", "pressure"),
            ("🌅", "Sunrise", "sunrise"),
            ("🌇", "Sunset", "sunset")
        ]

        for icon, title, key in details:

            row = ctk.CTkFrame(
                right,
                fg_color=CARD2,
                corner_radius=12
            )
            row.pack(fill="x", pady=5)

            ctk.CTkLabel(
                row,
                text=f"{icon}  {title}",
                font=("Segoe UI", 15),
                text_color=TEXT
            ).pack(side="left", padx=15, pady=12)

            value = ctk.CTkLabel(
                row,
                text="--",
                font=("Segoe UI", 15, "bold"),
                text_color=CYAN
            )
            value.pack(side="right", padx=15)

            self.detail_labels[key] = value

        # Hourly forecast
        self.hourly_section = ctk.CTkFrame(
            self.root,
            fg_color=CARD,
            corner_radius=20,
            border_width=1,
            border_color=BORDER
        )
        self.hourly_section.pack(
            fill="x",
            padx=35,
            pady=12
        )

        ctk.CTkLabel(
            self.hourly_section,
            text="🕒  Next 6 Hours Forecast",
            font=("Segoe UI", 20, "bold"),
            text_color=TEXT
        ).pack(anchor="w", padx=22, pady=(15, 8))

        self.hourly_frame = ctk.CTkFrame(
            self.hourly_section,
            fg_color="transparent"
        )
        self.hourly_frame.pack(
            fill="x",
            padx=12,
            pady=(0, 15)
        )

        # Five day forecast
        self.daily_section = ctk.CTkFrame(
            self.root,
            fg_color=CARD,
            corner_radius=20,
            border_width=1,
            border_color=BORDER
        )
        self.daily_section.pack(
            fill="x",
            padx=35,
            pady=12
        )

        ctk.CTkLabel(
            self.daily_section,
            text="📅  5 Day Forecast",
            font=("Segoe UI", 20, "bold"),
            text_color=TEXT
        ).pack(anchor="w", padx=22, pady=(15, 8))

        self.daily_frame = ctk.CTkFrame(
            self.daily_section,
            fg_color="transparent"
        )
        self.daily_frame.pack(
            fill="x",
            padx=12,
            pady=(0, 15)
        )

        # Footer
        ctk.CTkLabel(
            self.root,
            text="⚡ Powered by OpenWeatherMap",
            font=("Segoe UI", 12),
            text_color=TEXT
        ).pack(pady=12)

    # ---------------- WEATHER SEARCH ----------------

    def show_weather(self):

        city = self.city_entry.get().strip()

        if not city:
            messagebox.showwarning(
                "Input Required",
                "Please enter a city name."
            )
            return

        try:
            current = get_current_weather(city)
            forecast = get_forecast(city)

            self.current_data = current
            self.forecast_data = forecast

            self.update_dashboard()

        except WeatherAPIError as error:
            messagebox.showerror(
                "Weather Error",
                str(error)
            )

    # ---------------- UPDATE DASHBOARD ----------------

    def update_dashboard(self):

        data = self.current_data
        main = data["main"]
        weather = data["weather"][0]

        self.city_label.configure(
            text=data["name"]
        )

        self.temperature_label.configure(
            text=self.temp_text(main["temp"])
        )

        self.feels_label.configure(
            text=f"Feels Like: {self.temp_text(main['feels_like'])}"
        )

        self.description_label.configure(
            text=weather["description"].title()
        )

        self.weather_icon.configure(
            text=self.get_icon(weather["main"])
        )

        self.detail_labels["humidity"].configure(
            text=f"{main['humidity']}%"
        )

        self.detail_labels["wind"].configure(
            text=f"{data['wind']['speed']} m/s"
        )

        self.detail_labels["pressure"].configure(
            text=f"{main['pressure']} hPa"
        )

        offset = data.get("timezone", 0)

        sunrise = datetime.fromtimestamp(
            data["sys"]["sunrise"],
            timezone.utc
        ) + timedelta(seconds=offset)

        sunset = datetime.fromtimestamp(
            data["sys"]["sunset"],
            timezone.utc
        ) + timedelta(seconds=offset)

        self.detail_labels["sunrise"].configure(
            text=sunrise.strftime("%I:%M %p")
        )

        self.detail_labels["sunset"].configure(
            text=sunset.strftime("%I:%M %p")
        )

        self.update_hourly_forecast()
        self.update_daily_forecast()

    # ---------------- HOURLY FORECAST ----------------

    def update_hourly_forecast(self):

        for widget in self.hourly_frame.winfo_children():
            widget.destroy()

        items = self.forecast_data["list"][:6]

        for index, item in enumerate(items):

            self.hourly_frame.grid_columnconfigure(
                index,
                weight=1
            )

            card = ctk.CTkFrame(
                self.hourly_frame,
                fg_color=CARD2,
                corner_radius=15
            )
            card.grid(
                row=0,
                column=index,
                padx=8,
                sticky="nsew"
            )

            local_time = datetime.fromtimestamp(
                item["dt"],
                timezone.utc
            ) + timedelta(
                seconds=self.forecast_data.get(
                    "city", {}
                ).get("timezone", 0)
            )

            condition = item["weather"][0]["main"]

            ctk.CTkLabel(
                card,
                text=local_time.strftime("%I:%M %p"),
                font=("Segoe UI", 14, "bold"),
                text_color=TEXT
            ).pack(pady=(12, 5))

            ctk.CTkLabel(
                card,
                text=self.get_icon(condition),
                font=("Segoe UI Emoji", 35)
            ).pack(pady=5)

            ctk.CTkLabel(
                card,
                text=self.temp_text(item["main"]["temp"]),
                font=("Segoe UI", 18, "bold"),
                text_color=CYAN
            ).pack(pady=(5, 12))

    # ---------------- FIVE DAY FORECAST ----------------

    def update_daily_forecast(self):

        for widget in self.daily_frame.winfo_children():
            widget.destroy()

        groups = {}

        offset = self.forecast_data.get(
            "city", {}
        ).get("timezone", 0)

        for item in self.forecast_data["list"]:

            local_date = (
                datetime.fromtimestamp(
                    item["dt"], timezone.utc
                ) + timedelta(seconds=offset)
            )

            date_key = local_date.strftime("%Y-%m-%d")

            if date_key not in groups:
                groups[date_key] = []

            groups[date_key].append(item)

        for index, (date_key, items) in enumerate(
            list(groups.items())[:5]
        ):

            self.daily_frame.grid_columnconfigure(
                index,
                weight=1
            )

            selected = min(
                items,
                key=lambda x: abs(
                    (
                        datetime.fromtimestamp(
                            x["dt"], timezone.utc
                        ) + timedelta(seconds=offset)
                    ).hour - 12
                )
            )

            high = max(
                x["main"]["temp_max"] for x in items
            )

            low = min(
                x["main"]["temp_min"] for x in items
            )

            condition = selected["weather"][0]["main"]

            date_obj = datetime.strptime(
                date_key, "%Y-%m-%d"
            )

            card = ctk.CTkFrame(
                self.daily_frame,
                fg_color=CARD2,
                corner_radius=15
            )

            card.grid(
                row=0,
                column=index,
                padx=5,
                sticky="nsew"
            )

            ctk.CTkLabel(
                card,
                text=date_obj.strftime("%a, %b %d"),
                font=("Segoe UI", 13, "bold"),
                text_color=TEXT
            ).pack(pady=(12, 5))

            ctk.CTkLabel(
                card,
                text=self.get_icon(condition),
                font=("Segoe UI Emoji", 32)
            ).pack(pady=5)

            ctk.CTkLabel(
                card,
                text=f"{self.convert_temp(high):.0f}° / "
                     f"{self.convert_temp(low):.0f}°",
                font=("Segoe UI", 14, "bold"),
                text_color=CYAN
            ).pack(pady=5)

            ctk.CTkLabel(
                card,
                text=selected["weather"][0]["description"].title(),
                font=("Segoe UI", 11),
                text_color=MUTED,
                wraplength=130
            ).pack(pady=(2, 12))

    # ---------------- UNIT TOGGLE ----------------

    def change_unit(self, value):

        self.unit = "F" if value == "°F" else "C"

        if self.current_data:
            self.update_dashboard()


# ---------------- RUN APP ----------------

if __name__ == "__main__":

    root = ctk.CTk()
    app = WeatherApp(root)
    root.mainloop()
