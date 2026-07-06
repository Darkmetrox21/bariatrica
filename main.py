import random
from datetime import datetime, timedelta, date

from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, FadeTransition

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import (
    MDFillRoundFlatIconButton,
    MDFillRoundFlatButton,
    MDFlatButton,
)
from kivymd.uix.textfield import MDTextField
from kivymd.uix.toolbar import MDTopAppBar

from meals import MEALS
from database import (
    create_tables,
    add_pill,
    get_pills,
    delete_pill,
    save_setting,
    get_setting,
)
from notifications import show_notification


APP_BG = "#F4FAFA"
PRIMARY = "#2C7DA0"
PRIMARY_DARK = "#014F68"
GREEN = "#2D9C68"
GREEN_DARK = "#1D6F4A"
DANGER = "#C94343"
TEXT = "#17202A"
MUTED = "#607080"
CARD = "#FFFFFF"
SOFT_BLUE = "#E7F4FA"
SOFT_GREEN = "#E8F7EF"
SOFT_YELLOW = "#FFF6D8"
SOFT_PINK = "#FFECEF"


def format_time(dt):
    return dt.strftime("%H:%M")


def parse_datetime(value):
    try:
        return datetime.fromisoformat(value)
    except Exception:
        return None


def get_random_meal_by_time():
    now = datetime.now()

    if now.hour < 11:
        meal_type = "Desayuno"
    else:
        meal_type = "Almuerzo"

    options = [meal for meal in MEALS if meal["tipo"] == meal_type]

    if not options:
        options = MEALS

    return random.choice(options)


def get_random_meal_filtered(tipo, fase):
    options = [
        meal for meal in MEALS
        if meal["tipo"] == tipo and meal["fase"] == fase
    ]

    if not options:
        options = [meal for meal in MEALS if meal["tipo"] == tipo]

    if not options:
        options = MEALS

    return random.choice(options)


class AppRoot(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.md_bg_color = APP_BG


class Page(MDScreen):
    def build_body(self):
        root = AppRoot()
        return root


class SectionTitle(MDLabel):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.font_style = "H5"
        self.bold = True
        self.theme_text_color = "Custom"
        self.text_color = TEXT
        self.size_hint_y = None
        self.height = dp(42)


class SectionSubtitle(MDLabel):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.font_style = "Body2"
        self.theme_text_color = "Custom"
        self.text_color = MUTED
        self.size_hint_y = None
        self.height = dp(44)


class AutoText(Label):
    def __init__(self, text="", font_size=15, color=TEXT, **kwargs):
        super().__init__(**kwargs)

        self.text = text
        self.markup = True
        self.font_size = dp(font_size)
        self.color = color
        self.halign = "left"
        self.valign = "top"
        self.size_hint_y = None
        self.text_size = (0, None)

        self.bind(width=self.update_text_width)
        self.bind(texture_size=self.update_height)

    def update_text_width(self, *args):
        self.text_size = (self.width, None)

    def update_height(self, *args):
        self.height = self.texture_size[1] + dp(16)


class PrettyCard(MDCard):
    def __init__(self, bg_color=CARD, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "vertical"
        self.padding = dp(18)
        self.spacing = dp(10)
        self.radius = [dp(24), dp(24), dp(24), dp(24)]
        self.elevation = 1
        self.md_bg_color = bg_color


class HeroCard(PrettyCard):
    def __init__(self, badge, title, subtitle, footer="", bg_color=SOFT_YELLOW, **kwargs):
        super().__init__(bg_color=bg_color, **kwargs)

        self.size_hint_y = None
        self.height = dp(230)

        badge_label = MDLabel(
            text=badge,
            halign="center",
            font_style="H6",
            bold=True,
            theme_text_color="Custom",
            text_color="#FFFFFF",
            size_hint_y=None,
            height=dp(46),
        )

        badge_card = MDCard(
            orientation="vertical",
            size_hint=(None, None),
            size=(dp(110), dp(46)),
            radius=[dp(20), dp(20), dp(20), dp(20)],
            md_bg_color=GREEN,
            elevation=0,
            padding=dp(4),
        )
        badge_card.add_widget(badge_label)

        title_label = MDLabel(
            text=title,
            font_style="H5",
            bold=True,
            theme_text_color="Custom",
            text_color=PRIMARY_DARK,
            size_hint_y=None,
            height=dp(42),
        )

        subtitle_label = MDLabel(
            text=subtitle,
            font_style="Body1",
            theme_text_color="Custom",
            text_color=TEXT,
            size_hint_y=None,
            height=dp(54),
        )

        footer_label = MDLabel(
            text=footer,
            font_style="Subtitle1",
            bold=True,
            theme_text_color="Custom",
            text_color=GREEN_DARK,
            size_hint_y=None,
            height=dp(36),
        )

        self.add_widget(badge_card)
        self.add_widget(title_label)
        self.add_widget(subtitle_label)
        self.add_widget(footer_label)


class InfoCard(PrettyCard):
    def __init__(self, badge, title, subtitle, bg_color=SOFT_BLUE, badge_color=PRIMARY, **kwargs):
        super().__init__(bg_color=bg_color, **kwargs)

        self.size_hint_y = None
        self.height = dp(145)

        badge_box = MDCard(
            size_hint=(None, None),
            size=(dp(95), dp(40)),
            radius=[dp(18), dp(18), dp(18), dp(18)],
            md_bg_color=badge_color,
            elevation=0,
        )

        badge_label = MDLabel(
            text=badge,
            halign="center",
            valign="middle",
            font_style="Subtitle1",
            bold=True,
            theme_text_color="Custom",
            text_color="#FFFFFF",
        )

        badge_box.add_widget(badge_label)

        title_label = MDLabel(
            text=title,
            font_style="H6",
            bold=True,
            theme_text_color="Custom",
            text_color=TEXT,
            size_hint_y=None,
            height=dp(34),
        )

        subtitle_label = MDLabel(
            text=subtitle,
            font_style="Body2",
            theme_text_color="Custom",
            text_color=MUTED,
        )

        self.add_widget(badge_box)
        self.add_widget(title_label)
        self.add_widget(subtitle_label)


class MealCard(PrettyCard):
    def __init__(self, meal, **kwargs):
        super().__init__(bg_color=CARD, **kwargs)

        self.size_hint_y = None
        self.height = dp(440)

        badge_box = MDCard(
            size_hint=(None, None),
            size=(dp(120), dp(42)),
            radius=[dp(18), dp(18), dp(18), dp(18)],
            md_bg_color=GREEN,
            elevation=0,
        )

        badge_label = MDLabel(
            text=meal["tipo"].upper(),
            halign="center",
            bold=True,
            theme_text_color="Custom",
            text_color="#FFFFFF",
        )

        badge_box.add_widget(badge_label)

        title = AutoText(
            text=f"[b]{meal['nombre']}[/b]",
            font_size=21,
            color=PRIMARY_DARK,
        )

        body = AutoText(
            text=(
                f"[b]Ingredientes:[/b]\n{meal['ingredientes']}\n\n"
                f"[b]Porción:[/b]\n{meal['porcion']}\n\n"
                f"[b]Proteína:[/b] {meal['proteina']} g\n"
                f"[b]Calorías:[/b] {meal['kcal']} kcal\n"
                f"[b]Vitaminas/Nutrientes:[/b] {meal['vitaminas']}\n\n"
                f"[b]Nota:[/b]\n{meal['nota']}"
            ),
            font_size=15,
            color=TEXT,
        )

        self.add_widget(badge_box)
        self.add_widget(title)
        self.add_widget(body)


class HomeScreen(Page):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = self.build_body()

        toolbar = MDTopAppBar(
            title="Cuidadora Bariátrica",
            md_bg_color=PRIMARY,
            specific_text_color="#FFFFFF",
            elevation=2,
        )

        content = MDBoxLayout(
            orientation="vertical",
            padding=dp(18),
            spacing=dp(14),
        )

        self.hero = HeroCard(
            badge="SALUD",
            title="Hola, Mamá",
            subtitle="Vamos a comer sano para cuidar la salud!.",
            footer="Próxima comida: calculando...",
            bg_color=SOFT_YELLOW,
        )

        btn_meals = MDFillRoundFlatIconButton(
            text="Ver comidas recomendadas",
            icon="silverware-fork-knife",
            md_bg_color=PRIMARY,
            text_color="#FFFFFF",
            icon_color="#FFFFFF",
            pos_hint={"center_x": 0.5},
        )
        btn_meals.bind(on_release=lambda x: setattr(self.manager, "current", "meals"))

        btn_schedule = MDFillRoundFlatIconButton(
            text="Configurar comidas cada 4 horas",
            icon="clock-outline",
            md_bg_color=GREEN,
            text_color="#FFFFFF",
            icon_color="#FFFFFF",
            pos_hint={"center_x": 0.5},
        )
        btn_schedule.bind(on_release=lambda x: setattr(self.manager, "current", "schedule"))

        btn_pills = MDFillRoundFlatIconButton(
            text="Pastillas y vitaminas",
            icon="pill",
            md_bg_color=PRIMARY,
            text_color="#FFFFFF",
            icon_color="#FFFFFF",
            pos_hint={"center_x": 0.5},
        )
        btn_pills.bind(on_release=lambda x: setattr(self.manager, "current", "pills"))

        btn_test = MDFillRoundFlatIconButton(
            text="Probar aviso de comida ahora",
            icon="bell-ring-outline",
            md_bg_color=PRIMARY_DARK,
            text_color="#FFFFFF",
            icon_color="#FFFFFF",
            pos_hint={"center_x": 0.5},
        )
        btn_test.bind(on_release=self.test_meal_alert)

        btn_about = MDFillRoundFlatIconButton(
            text="Consejos generales",
            icon="information-outline",
            md_bg_color=PRIMARY_DARK,
            text_color="#FFFFFF",
            icon_color="#FFFFFF",
            pos_hint={"center_x": 0.5},
        )
        btn_about.bind(on_release=lambda x: setattr(self.manager, "current", "about"))

        content.add_widget(self.hero)
        content.add_widget(btn_meals)
        content.add_widget(btn_schedule)
        content.add_widget(btn_pills)
        content.add_widget(btn_test)
        content.add_widget(btn_about)

        root.add_widget(toolbar)
        root.add_widget(content)
        self.add_widget(root)

    def on_pre_enter(self):
        self.refresh_next_meal()

    def refresh_next_meal(self):
        value = get_setting("next_meal_time", "")
        next_time = parse_datetime(value)

        if next_time:
            self.hero.children[0].text = f"Próxima comida: {format_time(next_time)}"
        else:
            self.hero.children[0].text = "Próxima comida: no programada"

    def test_meal_alert(self, instance):
        meal = get_random_meal_by_time()
        show_notification("Hora de comer", f"Recomendación: {meal['nombre']}")
        self.manager.get_screen("meal_alert").set_meal(meal)
        self.manager.current = "meal_alert"


class MealsScreen(Page):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.tipo = "Desayuno"
        self.fase = "regular"

        root = self.build_body()

        toolbar = MDTopAppBar(
            title="Comidas recomendadas",
            left_action_items=[["arrow-left", lambda x: setattr(self.manager, "current", "home")]],
            md_bg_color=PRIMARY,
            specific_text_color="#FFFFFF",
            elevation=2,
        )

        content = MDBoxLayout(
            orientation="vertical",
            padding=dp(18),
            spacing=dp(12),
        )

        content.add_widget(
            InfoCard(
                badge="COMER",
                title="Recomendador de comidas",
                subtitle="Elige desayuno o almuerzo y la app sugerirá una opción simple.",
                bg_color=SOFT_BLUE,
                badge_color=PRIMARY,
            )
        )

        controls = PrettyCard(bg_color=CARD)
        controls.size_hint_y = None
        controls.height = dp(180)

        self.tipo_spinner = Spinner(
            text="Desayuno",
            values=["Desayuno", "Almuerzo"],
            size_hint_y=None,
            height=dp(48),
            background_normal="",
            background_color=(0.90, 0.96, 0.99, 1),
            color=(0.09, 0.13, 0.17, 1),
            font_size=dp(15),
        )
        self.tipo_spinner.bind(text=self.change_tipo)

        self.fase_spinner = Spinner(
            text="regular",
            values=["blando", "regular"],
            size_hint_y=None,
            height=dp(48),
            background_normal="",
            background_color=(0.90, 0.96, 0.99, 1),
            color=(0.09, 0.13, 0.17, 1),
            font_size=dp(15),
        )
        self.fase_spinner.bind(text=self.change_fase)

        btn_recommend = MDFillRoundFlatButton(
            text="Recomendar comida aleatoria",
            md_bg_color=GREEN,
            text_color="#FFFFFF",
            pos_hint={"center_x": 0.5},
        )
        btn_recommend.bind(on_release=self.recommend_meal)

        controls.add_widget(self.tipo_spinner)
        controls.add_widget(self.fase_spinner)
        controls.add_widget(btn_recommend)

        self.result_container = MDBoxLayout(
            orientation="vertical",
            spacing=dp(12),
            adaptive_height=True,
        )

        scroll = ScrollView()
        scroll.add_widget(self.result_container)

        content.add_widget(controls)
        content.add_widget(scroll)

        root.add_widget(toolbar)
        root.add_widget(content)
        self.add_widget(root)

    def on_pre_enter(self):
        if not self.result_container.children:
            self.recommend_meal(None)

    def change_tipo(self, spinner, text):
        self.tipo = text

    def change_fase(self, spinner, text):
        self.fase = text

    def recommend_meal(self, instance):
        meal = get_random_meal_filtered(self.tipo, self.fase)

        self.result_container.clear_widgets()
        self.result_container.add_widget(MealCard(meal))


class ScheduleScreen(Page):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = self.build_body()

        toolbar = MDTopAppBar(
            title="Comidas cada 4 horas",
            left_action_items=[["arrow-left", lambda x: setattr(self.manager, "current", "home")]],
            md_bg_color=GREEN,
            specific_text_color="#FFFFFF",
            elevation=2,
        )

        content = MDBoxLayout(
            orientation="vertical",
            padding=dp(18),
            spacing=dp(12),
        )

        content.add_widget(
            InfoCard(
                badge="4H",
                title="Horario de comidas",
                subtitle="Configura la primera comida del día o empieza desde ahora.",
                bg_color=SOFT_GREEN,
                badge_color=GREEN,
            )
        )

        panel = PrettyCard(bg_color=CARD)
        panel.size_hint_y = None
        panel.height = dp(330)

        self.start_time = MDTextField(
            hint_text="Primera comida del día, ej: 08:00",
            mode="rectangle",
            size_hint_y=None,
            height=dp(58),
        )
        self.start_time.text = get_setting("first_meal_time", "08:00")

        self.status = AutoText(
            text="",
            font_size=15,
            color=TEXT,
        )

        btn_save = MDFillRoundFlatButton(
            text="Guardar desde primera comida",
            md_bg_color=GREEN,
            text_color="#FFFFFF",
            pos_hint={"center_x": 0.5},
        )
        btn_save.bind(on_release=self.save_schedule)

        btn_now = MDFillRoundFlatButton(
            text="Empezar desde ahora",
            md_bg_color=PRIMARY,
            text_color="#FFFFFF",
            pos_hint={"center_x": 0.5},
        )
        btn_now.bind(on_release=self.schedule_from_now)

        btn_test = MDFillRoundFlatButton(
            text="Probar aviso ahora",
            md_bg_color=PRIMARY_DARK,
            text_color="#FFFFFF",
            pos_hint={"center_x": 0.5},
        )
        btn_test.bind(on_release=self.test_alert)

        panel.add_widget(self.start_time)
        panel.add_widget(self.status)
        panel.add_widget(btn_save)
        panel.add_widget(btn_now)
        panel.add_widget(btn_test)

        content.add_widget(panel)

        root.add_widget(toolbar)
        root.add_widget(content)
        self.add_widget(root)

    def on_pre_enter(self):
        self.refresh_status()

    def refresh_status(self):
        next_value = get_setting("next_meal_time", "")
        next_time = parse_datetime(next_value)

        if next_time:
            self.status.text = (
                f"[b]Próxima comida programada:[/b] {format_time(next_time)}\n"
                "Cuando llegue la hora, aparecerá una comida recomendada."
            )
        else:
            self.status.text = (
                "No hay comidas programadas todavía.\n"
                "Puedes guardar una primera hora o empezar desde ahora."
            )

    def save_schedule(self, instance):
        time_text = self.start_time.text.strip()

        try:
            hour, minute = map(int, time_text.split(":"))

            now = datetime.now()
            first_time = now.replace(
                hour=hour,
                minute=minute,
                second=0,
                microsecond=0,
            )

            while first_time <= now:
                first_time += timedelta(hours=4)

            save_setting("first_meal_time", time_text)
            save_setting("next_meal_time", first_time.isoformat())

            show_notification(
                "Horario guardado",
                f"Próxima comida a las {format_time(first_time)}",
            )

            self.refresh_status()

        except Exception:
            show_notification(
                "Horario inválido",
                "Usa formato HH:MM. Ejemplo: 08:00",
            )

    def schedule_from_now(self, instance):
        next_time = datetime.now() + timedelta(hours=4)
        save_setting("next_meal_time", next_time.isoformat())

        show_notification(
            "Horario iniciado",
            f"Próxima comida a las {format_time(next_time)}",
        )

        self.refresh_status()

    def test_alert(self, instance):
        meal = get_random_meal_by_time()

        show_notification(
            "Hora de comer",
            f"Recomendación: {meal['nombre']}",
        )

        self.manager.get_screen("meal_alert").set_meal(meal)
        self.manager.current = "meal_alert"


class MealAlertScreen(Page):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = self.build_body()

        toolbar = MDTopAppBar(
            title="Hora de comer",
            left_action_items=[["arrow-left", lambda x: setattr(self.manager, "current", "home")]],
            md_bg_color=GREEN,
            specific_text_color="#FFFFFF",
            elevation=2,
        )

        content = MDBoxLayout(
            orientation="vertical",
            padding=dp(18),
            spacing=dp(12),
        )

        content.add_widget(
            InfoCard(
                badge="COMER",
                title="Es hora de comer",
                subtitle="Recuerda comer lento, poco a poco y priorizando proteína.",
                bg_color=SOFT_YELLOW,
                badge_color=GREEN,
            )
        )

        self.container = MDBoxLayout(
            orientation="vertical",
            spacing=dp(12),
            adaptive_height=True,
        )

        scroll = ScrollView()
        scroll.add_widget(self.container)

        btn_next = MDFillRoundFlatButton(
            text="Listo, avisar otra vez en 4 horas",
            md_bg_color=GREEN,
            text_color="#FFFFFF",
            pos_hint={"center_x": 0.5},
        )
        btn_next.bind(on_release=self.reschedule_next_meal)

        btn_other = MDFillRoundFlatButton(
            text="Mostrar otra recomendación",
            md_bg_color=PRIMARY,
            text_color="#FFFFFF",
            pos_hint={"center_x": 0.5},
        )
        btn_other.bind(on_release=self.show_another_meal)

        content.add_widget(scroll)
        content.add_widget(btn_next)
        content.add_widget(btn_other)

        root.add_widget(toolbar)
        root.add_widget(content)
        self.add_widget(root)

    def set_meal(self, meal):
        self.container.clear_widgets()
        self.container.add_widget(MealCard(meal))

    def show_another_meal(self, instance):
        meal = get_random_meal_by_time()
        self.set_meal(meal)

    def reschedule_next_meal(self, instance):
        next_time = datetime.now() + timedelta(hours=4)

        save_setting("next_meal_time", next_time.isoformat())

        show_notification(
            "Próxima comida",
            f"Te avisaré nuevamente a las {format_time(next_time)}",
        )

        self.manager.current = "home"


class PillsScreen(Page):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = self.build_body()

        toolbar = MDTopAppBar(
            title="Pastillas y vitaminas",
            left_action_items=[["arrow-left", lambda x: setattr(self.manager, "current", "home")]],
            md_bg_color=PRIMARY,
            specific_text_color="#FFFFFF",
            elevation=2,
        )

        content = MDBoxLayout(
            orientation="vertical",
            padding=dp(18),
            spacing=dp(12),
        )

        content.add_widget(
            InfoCard(
                badge="MED",
                title="Recordatorio de pastillas",
                subtitle="Agrega nombre, hora y una nota. La app avisará cuando toque.",
                bg_color=SOFT_PINK,
                badge_color=DANGER,
            )
        )

        form = PrettyCard(bg_color=CARD)
        form.size_hint_y = None
        form.height = dp(270)

        self.name_input = MDTextField(
            hint_text="Nombre: ej. Multivitamínico",
            mode="rectangle",
            size_hint_y=None,
            height=dp(58),
        )

        self.time_input = MDTextField(
            hint_text="Hora: ej. 09:00",
            mode="rectangle",
            size_hint_y=None,
            height=dp(58),
        )

        self.note_input = MDTextField(
            hint_text="Nota opcional",
            mode="rectangle",
            size_hint_y=None,
            height=dp(58),
        )

        btn_add = MDFillRoundFlatButton(
            text="Agregar pastilla",
            md_bg_color=GREEN,
            text_color="#FFFFFF",
            pos_hint={"center_x": 0.5},
        )
        btn_add.bind(on_release=self.add_new_pill)

        form.add_widget(self.name_input)
        form.add_widget(self.time_input)
        form.add_widget(self.note_input)
        form.add_widget(btn_add)

        self.list_container = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            adaptive_height=True,
        )

        scroll = ScrollView()
        scroll.add_widget(self.list_container)

        content.add_widget(form)
        content.add_widget(scroll)

        root.add_widget(toolbar)
        root.add_widget(content)
        self.add_widget(root)

    def on_pre_enter(self):
        self.load_pills()

    def add_new_pill(self, instance):
        name = self.name_input.text.strip()
        time = self.time_input.text.strip()
        note = self.note_input.text.strip()

        if not name or not time:
            show_notification("Faltan datos", "Debes ingresar nombre y hora.")
            return

        if ":" not in time:
            show_notification("Hora inválida", "Usa formato HH:MM. Ejemplo: 09:00")
            return

        add_pill(name, time, note)

        self.name_input.text = ""
        self.time_input.text = ""
        self.note_input.text = ""

        show_notification("Pastilla agregada", f"{name} a las {time}")
        self.load_pills()

    def remove_pill(self, pill_id):
        delete_pill(pill_id)

        show_notification(
            "Pastilla eliminada",
            "El registro fue eliminado correctamente.",
        )

        self.load_pills()

    def load_pills(self):
        self.list_container.clear_widgets()
        pills = get_pills()

        if not pills:
            empty_card = PrettyCard(bg_color=SOFT_BLUE)
            empty_card.size_hint_y = None
            empty_card.height = dp(100)
            empty_card.add_widget(
                AutoText(
                    text="No hay pastillas registradas.",
                    font_size=16,
                    color=TEXT,
                )
            )
            self.list_container.add_widget(empty_card)
            return

        for pill_id, name, time, note in pills:
            item = PrettyCard(bg_color=CARD)
            item.size_hint_y = None
            item.height = dp(150)

            label = AutoText(
                text=f"[b]MED {time} - {name}[/b]\n{note if note else 'Sin nota'}",
                font_size=15,
                color=TEXT,
            )

            delete_btn = MDFillRoundFlatButton(
                text="Borrar pastilla",
                md_bg_color=DANGER,
                text_color="#FFFFFF",
                pos_hint={"center_x": 0.5},
            )
            delete_btn.bind(
                on_release=lambda instance, pid=pill_id: self.remove_pill(pid)
            )

            item.add_widget(label)
            item.add_widget(delete_btn)

            self.list_container.add_widget(item)


class AboutScreen(Page):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = self.build_body()

        toolbar = MDTopAppBar(
            title="Consejos generales",
            left_action_items=[["arrow-left", lambda x: setattr(self.manager, "current", "home")]],
            md_bg_color=PRIMARY_DARK,
            specific_text_color="#FFFFFF",
            elevation=2,
        )

        content = MDBoxLayout(
            orientation="vertical",
            padding=dp(18),
            spacing=dp(12),
        )

        content.add_widget(
            InfoCard(
                badge="INFO",
                title="Uso responsable",
                subtitle="La app ayuda a organizar, pero no reemplaza indicaciones médicas.",
                bg_color=SOFT_BLUE,
                badge_color=PRIMARY,
            )
        )

        panel = PrettyCard(bg_color=CARD)

        text = AutoText(
            text=(
                "[b]Recordatorios importantes:[/b]\n\n"
                "- Esta app es una ayuda familiar, no reemplaza la indicación médica.\n\n"
                "- Las comidas deben ajustarse a la etapa postoperatoria de tu mamá.\n\n"
                "- Comer lento y en porciones pequeñas.\n\n"
                "- Priorizar alimentos con proteína.\n\n"
                "- Tomar vitaminas y medicamentos solo según indicación médica.\n\n"
                "- Evitar alimentos con mucha azúcar, frituras o comidas pesadas si no están autorizadas."
            ),
            font_size=16,
            color=TEXT,
        )

        panel.add_widget(text)

        scroll = ScrollView()
        scroll.add_widget(panel)

        content.add_widget(scroll)

        root.add_widget(toolbar)
        root.add_widget(content)
        self.add_widget(root)


class BariatricApp(MDApp):
    def build(self):
        create_tables()

        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Green"
        self.theme_cls.theme_style = "Light"

        self.notified_pills = set()

        sm = ScreenManager(
            transition=FadeTransition(duration=0.2)
        )

        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(MealsScreen(name="meals"))
        sm.add_widget(ScheduleScreen(name="schedule"))
        sm.add_widget(MealAlertScreen(name="meal_alert"))
        sm.add_widget(PillsScreen(name="pills"))
        sm.add_widget(AboutScreen(name="about"))

        Clock.schedule_once(self.initialize_meal_schedule, 1)
        Clock.schedule_interval(self.check_meal_reminder, 30)
        Clock.schedule_interval(self.check_pill_reminders, 30)

        return sm

    def initialize_meal_schedule(self, dt):
        next_value = get_setting("next_meal_time", "")
        next_time = parse_datetime(next_value)

        if not next_time:
            new_next = datetime.now() + timedelta(hours=4)
            save_setting("next_meal_time", new_next.isoformat())

    def check_meal_reminder(self, dt):
        value = get_setting("next_meal_time", "")
        next_time = parse_datetime(value)

        if not next_time:
            return

        now = datetime.now()

        if now >= next_time:
            meal = get_random_meal_by_time()

            show_notification(
                "Hora de comer",
                f"Recomendación: {meal['nombre']}",
            )

            new_next = now + timedelta(hours=4)
            save_setting("next_meal_time", new_next.isoformat())

            if self.root:
                self.root.get_screen("meal_alert").set_meal(meal)
                self.root.current = "meal_alert"

    def check_pill_reminders(self, dt):
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        today = date.today().isoformat()

        pills = get_pills()

        for pill_id, name, pill_time, note in pills:
            key = f"{today}-{pill_id}-{pill_time}"

            if pill_time == current_time and key not in self.notified_pills:
                message = f"Es hora de tomar: {name}"

                if note:
                    message += f"\nNota: {note}"

                show_notification(
                    "Recordatorio de pastilla",
                    message,
                )

                self.notified_pills.add(key)


if __name__ == "__main__":
    BariatricApp().run()