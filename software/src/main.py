import time
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Line, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import Screen, ScreenManager

import cv2
from kivy.graphics.texture import Texture

# Fixer la fenêtre en orientation paysage sur PC pour les tests
Window.size = (900, 450)


# ---------------------------------------------------
# ÉCRAN 1 : Accueil
# ---------------------------------------------------
class HomeScreen(Screen):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    layout = FloatLayout()

    # Image de fond
    self.bg = Image(
        source='assets/bg_home.jpg', fit_mode='fill', size_hint=(1, 1)
    )
    layout.add_widget(self.bg)

    # Bouton Start
    btn_start = Button(
        text='START',
        size_hint=(0.25, 0.15),
        pos_hint={'x': 0.25, 'y': 0.4},
        background_color=(0, 0.8, 0, 1),
    )
    btn_start.bind(on_release=self.go_to_speed)
    layout.add_widget(btn_start)

    # Bouton Exit
    btn_exit = Button(
        text='EXIT',
        size_hint=(0.25, 0.15),
        pos_hint={'x': 0.55, 'y': 0.4},
        background_color=(0.8, 0, 0, 1),
    )
    btn_exit.bind(on_release=self.exit_app)
    layout.add_widget(btn_exit)

    self.add_widget(layout)

  def go_to_speed(self, instance):
    self.manager.current = 'speed'

  def exit_app(self, instance):
    App.get_running_app().stop()


# ---------------------------------------------------
# ÉCRAN 2 : Choix de la vitesse
# ---------------------------------------------------
class SpeedScreen(Screen):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    layout = FloatLayout()

    # Menu déroulant de vitesse (0 à 20 km/h)
    self.dropdown = DropDown()
    for speed in range(0, 21):
      btn = Button(text=f'{speed} km/h', size_hint_y=None, height=44)
      btn.bind(
          on_release=lambda btn: self.dropdown.select(btn.text)
      )  # type: ignore
      self.dropdown.add_widget(btn)

    self.main_btn = Button(
        text='Sélectionner la vitesse (km/h)',
        size_hint=(0.4, 0.15),
        pos_hint={'center_x': 0.5, 'center_y': 0.6},
    )
    self.main_btn.bind(on_release=self.dropdown.open)
    self.dropdown.bind(on_select=self.on_speed_selected)  # type: ignore

    layout.add_widget(self.main_btn)

    # Bouton de validation
    self.btn_validate = Button(
        text='Valider et démarrer',
        size_hint=(0.3, 0.12),
        pos_hint={'center_x': 0.5, 'center_y': 0.3},
        disabled=True,
    )
    self.btn_validate.bind(on_release=self.start_camera_screen)
    layout.add_widget(self.btn_validate)

    self.add_widget(layout)

  def on_speed_selected(self, instance, x):
    self.main_btn.text = f'Vitesse choisie : {x}'
    self.selected_speed = x
    self.btn_validate.disabled = False

  def start_camera_screen(self, instance):
    cam_screen = self.manager.get_screen('camera')
    cam_screen.selected_speed = getattr(self, 'selected_speed', '0 km/h')
    self.manager.current = 'camera'


# -----------------------------------------------------
# WIDGET MAP : Zone de sélection du point (LiDAR)
# -----------------------------------------------------
class LidarMapWidget(FloatLayout):

  def __init__(self, camera_screen=None, **kwargs):
    super().__init__(**kwargs)
    self.camera_screen = camera_screen  # Référence directe à CameraScreen
    self.pin_point = None
    self.target_coords = None

    with self.canvas.before:
      Color(0.2, 0.2, 0.2, 1)
      self.rect = Rectangle(pos=self.pos, size=self.size)
      Color(0.8, 0.8, 0.8, 1)
      self.border = Line(
          rectangle=(self.x, self.y, self.width, self.height), width=1.5
      )

    self.bind(pos=self.update_graphics, size=self.update_graphics)

  def update_graphics(self, *args):
    self.rect.pos = self.pos
    self.rect.size = self.size
    self.border.rectangle = (self.x, self.y, self.width, self.height)

  def on_touch_down(self, touch):
    if self.collide_point(*touch.pos):
      if self.pin_point:
        self.remove_widget(self.pin_point)

      self.pin_point = Label(
          text='[color=ff0000]X[/color]',
          markup=True,
          font_size='24sp',
          pos=(touch.x - 12, touch.y - 12),
          size_hint=(None, None),
          size=(24, 24),
      )
      self.add_widget(self.pin_point)

      # Calcul des coordonnées relatives
      rel_x = (touch.x - self.x) / self.width
      rel_y = (touch.y - self.y) / self.height
      self.target_coords = (rel_x, rel_y)

      # Activation directe du bouton via la référence reçue
      if self.camera_screen:
        self.camera_screen.enable_confirm_button()

      return True

    return super().on_touch_down(touch)
# ---------------------------------------------------
# ÉCRAN 3 : Caméra Live & Pilotage
# ---------------------------------------------------

class CameraScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_speed = '0 km/h'
        self.start_time = 0
        self.tracking_active = False
        
        # Attributs pour la capture vidéo
        self.capture = None
        self.event_update_cam = None

        self.layout = FloatLayout()

        # Widget Image qui affichera le flux de la vraie caméra
        self.camera_feed = Image(size_hint=(1, 1), allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(self.camera_feed)

        # Bouton Pause (2 barres verticales)
        self.btn_pause = Button(
            text='||',
            size_hint=(0.08, 0.12),
            pos_hint={'center_x': 0.5, 'top': 0.98},
            opacity=0,
            disabled=True,
        )
        self.btn_pause.bind(on_release=self.open_pause_popup)
        self.layout.add_widget(self.btn_pause)

        # Overlay / HUD d'informations
        self.hud_label = Label(
            text='',
            markup=True,
            size_hint=(None, None),
            size=(300, 100),
            pos_hint={'x': 0.02, 'top': 0.98},
            halign='left',
            valign='top',
            opacity=0,
        )
        self.hud_label.bind(size=self.hud_label.setter('text_size'))
        self.layout.add_widget(self.hud_label)

        # Mini-carte LiDAR
        self.mini_map = Image(
            source='assets/lidar_map.png',
            size_hint=(0.25, 0.35),
            pos_hint={'right': 0.98, 'top': 0.98},
            opacity=0,
        )
        self.layout.add_widget(self.mini_map)

        self.add_widget(self.layout)

    def on_enter(self):
        """Méthode appelée automatiquement lorsque l'écran devient actif."""
        # 1. Démarrer la capture de la webcam (0 désigne la caméra par défaut)
        self.capture = cv2.VideoCapture(0)
        
        # 2. Planifier la mise à jour de l'image (30 images par seconde)
        self.event_update_cam = Clock.schedule_interval(self.update_camera_feed, 1.0 / 30.0)

        # Réinitialisation de l'état
        self.btn_pause.opacity = 0
        self.btn_pause.disabled = True
        self.hud_label.opacity = 0
        self.mini_map.opacity = 0
        self.tracking_active = False

        Clock.schedule_once(self.show_pause_button, 5)

    def on_leave(self):
        """Méthode appelée automatiquement lorsqu'on quitte cet écran."""
        # Arrêt de la boucle de rafraîchissement et libération de la caméra
        if self.event_update_cam:
            self.event_update_cam.cancel()
        if self.capture and self.capture.isOpened():
            self.capture.release()

    def update_camera_feed(self, dt):
        """Capture une image de la webcam et l'affiche sur le widget Kivy."""
        if self.capture and self.capture.isOpened():
            ret, frame = self.capture.read()
            if ret:
                # 1. Inverser l'image verticalement (Kivy place l'origine en bas à gauche)
                buf = cv2.flip(frame, 0).tobytes()
                
                # 2. Créer une texture Kivy à partir de la matrice d'image (BGR)
                texture = Texture.create(
                    size=(frame.shape[1], frame.shape[0]), colorfmt='bgr'
                )
                texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                
                # 3. Assigner la texture au widget Image
                self.camera_feed.texture = texture

    # --- Reste des méthodes inchangées ---
    def show_pause_button(self, dt):
        self.btn_pause.opacity = 1
        self.btn_pause.disabled = False

    def open_pause_popup(self, instance):
        self.popup_pause = ModalView(
            size_hint=(0.5, 0.5), background_color=(0, 0, 0, 0.6)
        )
        box = BoxLayout(
            orientation='vertical', padding=20, spacing=15, size_hint=(0.8, 0.8)
        )

        btn_continue = Button(text='Continue')
        btn_continue.bind(on_release=lambda x: self.popup_pause.dismiss())

        btn_select_point = Button(text="Choisir un point d'arrivée")
        btn_select_point.bind(on_release=self.open_map_popup)

        box.add_widget(btn_continue)
        box.add_widget(btn_select_point)
        self.popup_pause.add_widget(box)
        self.popup_pause.open()

    def open_map_popup(self, instance):
        self.popup_pause.dismiss()

        self.popup_map = ModalView(
            size_hint=(0.95, 0.9), background_color=(0, 0, 0, 0.5)
        )
        map_layout = FloatLayout()

        self.lidar_widget = LidarMapWidget(
            size_hint=(0.63, 0.9), pos_hint={'x': 0.02, 'center_y': 0.5}
        )
        map_layout.add_widget(self.lidar_widget)

        side_panel = BoxLayout(
            orientation='vertical',
            spacing=20,
            size_hint=(0.3, 0.9),
            pos_hint={'x': 0.67, 'center_y': 0.5},
        )

        self.btn_confirm_pos = Button(
            text='Choisir cette position',
            disabled=True,
            background_color=(0.5, 0.5, 0.5, 1),
        )
        self.btn_confirm_pos.bind(on_release=self.start_robot_navigation)

        btn_back = Button(text='<- Retour')
        btn_back.bind(on_release=self.back_to_pause)

        side_panel.add_widget(self.btn_confirm_pos)
        side_panel.add_widget(btn_back)
        map_layout.add_widget(side_panel)

        self.popup_map.add_widget(map_layout)
        self.popup_map.open()

    def enable_confirm_button(self):
        self.btn_confirm_pos.disabled = False
        self.btn_confirm_pos.background_color = (0, 0.8, 0, 1)

    def back_to_pause(self, instance):
        self.popup_map.dismiss()
        self.open_pause_popup(None)

    def start_robot_navigation(self, instance):
        self.popup_map.dismiss()

        self.hud_label.opacity = 1
        self.mini_map.opacity = 1

        self.start_time = time.time()
        self.tracking_active = True
        Clock.schedule_interval(self.update_hud, 0.5)

    def update_hud(self, dt):
        if not self.tracking_active:
            return False

        elapsed = int(time.time() - self.start_time)
        hrs, rem = divmod(elapsed, 3600)
        mins, secs = divmod(rem, 60)
        timer_str = f'{hrs:02d}:{mins:02d}:{secs:02d}'

        x, y, z = 1.25, 3.40, 0.00

        self.hud_label.text = (
            f'[b]X:[/b] {x:.2f}  [b]Y:[/b] {y:.2f}  [b]Z:[/b] {z:.2f}\n'
            f'[b]Vitesse:[/b] {self.selected_speed}\n'
            f'[b]Temps:[/b] {timer_str}'
        )

# ---------------------------------------------------
# APPLICATION PRINCIPALE
# ---------------------------------------------------
class RobotControlApp(App):

  def build(self):
    sm = ScreenManager()
    sm.add_widget(HomeScreen(name='home'))
    sm.add_widget(SpeedScreen(name='speed'))
    sm.add_widget(CameraScreen(name='camera'))
    return sm


if __name__ == '__main__':
  RobotControlApp().run()
