# Robot Mobile Autonome 🤖

> Projet 2A – ENSEA · Base roulante autonome pour la navigation en intérieur

Ce dépôt regroupe la conception matérielle (mécanique et électronique) et la pile logicielle d'une **base roulante autonome** capable de se déplacer avec précision d'un point A à un point B, de se localiser et d'éviter les obstacles dans un environnement intérieur.

Ce type de robot trouve des applications dans les entrepôts, les ateliers et les chaînes de production, notamment pour le transport autonome de pièces ou de matériel.

<!-- TODO : ajouter une photo ou un GIF du robot en action -->
<!-- ![Photo du robot](docs/images/robot.jpg) -->

---

## 📑 Sommaire

1. [Objectifs](#-objectifs)
2. [Architecture générale](#-architecture-générale)
3. [Matériel](#-matériel)
4. [Structure du dépôt](#-structure-du-dépôt)
5. [Installation](#-installation)
6. [Utilisation](#-utilisation)
7. [Détail des sous-systèmes](#-détail-des-sous-systèmes)
8. [État d'avancement](#-état-davancement)
9. [Résultats](#-résultats)
10. [Équipe](#-équipe)
11. [Licence](#-licence)

---

## 🎯 Objectifs

Le projet couvre la chaîne robotique complète, de la conception à la navigation autonome :

- **Concevoir la structure mécanique** avec des outils de CAO 3D, puis l'imprimer en 3D.
- **Concevoir l'architecture électronique** : alimentation, distribution de puissance, commande des moteurs, connectique.
- **Percevoir l'environnement** avec un LiDAR YDLidar X4 complété par des capteurs de distance.
- **Se localiser et cartographier** grâce à ROS 2 et à un algorithme SLAM, avec l'aide d'une IMU et d'encodeurs.
- **Naviguer** : planifier un trajet, éviter les obstacles et atteindre une destination imposée de manière autonome.

**Démonstration finale visée :** le robot se localise sur une carte, planifie son déplacement, évite les obstacles et rejoint de façon autonome un point d'arrivée imposé.

---

## 🧩 Architecture générale

Le robot repose sur deux niveaux de contrôle :

| Niveau | Calculateur | Rôle |
|---|---|---|
| **Haut niveau** | Raspberry Pi 5 (ROS 2) | Acquisition LiDAR, SLAM, localisation, planification, évitement d'obstacles |
| **Bas niveau** | STM32 | Asservissement des moteurs, lecture des encodeurs, exécution des consignes de déplacement |

```
┌──────────────────────── Raspberry Pi 5 (ROS 2) ────────────────────────┐
│                                                                        │
│  ydlidar_driver ──► /scan ──► slam_toolbox ──► /map                    │
│                                   ▲                                    │
│  robot_localization (odométrie + IMU) ──► /odom, TF                    │
│                                   │                                    │
│  Nav2 (planification + évitement) ──► /cmd_vel                         │
│                                                                        │
└──────────────┬─────────────────────────────────────▲───────────────────┘
               │ /cmd_vel (liaison série / USB)      │ odométrie, état
               ▼                                     │
┌─────────────────────────────── STM32 ──────────────┴───────────────────┐
│  Asservissement vitesse (PID) · Lecture encodeurs · Génération PWM     │
└──────────────┬─────────────────────────────────────────────────────────┘
               ▼
        Drivers moteur ──► Moteurs + roues codeuses
```

<!-- TODO : remplacer ce schéma ASCII par un schéma propre dans docs/ (architecture matérielle + graphe de nœuds ROS 2 via rqt_graph) -->

> **Liaison Raspberry Pi ↔ STM32 :** _à compléter (ex. UART/USB avec protocole maison, ou micro-ROS)._

---

## 🔧 Matériel

| Élément | Référence / Modèle | Rôle |
|---|---|---|
| Calculateur principal | Raspberry Pi 5 | Navigation haut niveau (ROS 2) |
| Microcontrôleur | STM32 _(préciser la carte, ex. Nucleo-F4xx)_ | Contrôle moteur bas niveau |
| LiDAR | YDLidar X4 | Perception 2D, SLAM |
| IMU | _à préciser_ | Amélioration de la localisation |
| Encodeurs | Roues codeuses _(préciser)_ | Odométrie |
| Capteurs de distance | _à préciser_ | Détection d'obstacles complémentaire |
| Caméra | _à préciser_ | Perception complémentaire |
| Drivers moteur | _à préciser_ | Commande de puissance des moteurs |
| Moteurs | _à préciser_ | Propulsion |
| Alimentation | _batterie + régulation, à préciser_ | Distribution de puissance |
| Châssis | Conception 3D personnalisée, imprimée en 3D | Structure mécanique |

<!-- TODO : ajouter une BOM détaillée (quantités, prix, liens) dans hardware/bom.md -->

---

## 📁 Structure du dépôt

> _Adapter cette arborescence à la réalité du dépôt._

```
Projet-2A-Robot-Mobile-Autonome/
├── hardware/
│   ├── mechanical/        # Fichiers CAO et STL du châssis
│   ├── electronics/       # Schémas, PCB, distribution de puissance
│   └── bom.md             # Liste du matériel
├── firmware/
│   └── stm32/             # Code embarqué STM32 (asservissement, encodeurs, comm.)
├── ros2_ws/
│   └── src/               # Packages ROS 2 (description, bringup, navigation…)
├── docs/                  # Schémas, photos, rapport, présentations
└── README.md
```

---

## ⚙️ Installation

### Prérequis

- Raspberry Pi 5 sous Ubuntu _(version à préciser, ex. 24.04)_
- ROS 2 _(distribution à préciser, ex. Jazzy)_
- Outils de build : `colcon`, `rosdep`
- Chaîne de développement STM32 : _STM32CubeIDE / PlatformIO (à préciser)_

### Côté Raspberry Pi (ROS 2)

```bash
# Cloner le dépôt
git clone https://github.com/Bictor123/Projet-2A-Robot-Mobile-Autonome.git
cd Projet-2A-Robot-Mobile-Autonome/ros2_ws

# Installer les dépendances
rosdep install --from-paths src --ignore-src -r -y

# Compiler
colcon build --symlink-install
source install/setup.bash
```

### Côté STM32

1. Ouvrir le projet dans `firmware/stm32/` avec _(IDE à préciser)_.
2. Compiler et flasher la carte via ST-Link.
3. Vérifier la liaison série avec la Raspberry Pi.

---

## 🚀 Utilisation

> _Remplacer les noms de packages et de fichiers de lancement par les vôtres._

```bash
# 1. Lancer les drivers et la communication avec la STM32
ros2 launch <package_bringup> bringup.launch.py

# 2. Cartographier l'environnement (SLAM)
ros2 launch <package_slam> slam.launch.py

# 3. Sauvegarder la carte
ros2 run nav2_map_server map_saver_cli -f maps/ma_carte

# 4. Naviguer de façon autonome sur la carte
ros2 launch <package_navigation> navigation.launch.py map:=maps/ma_carte.yaml
```

---

## 🔍 Détail des sous-systèmes

### Mécanique
Châssis conçu sur mesure et imprimé en 3D, avec supports pour le LiDAR, les capteurs, l'électronique et les batteries.
_À compléter : logiciel de CAO, matériaux d'impression, choix des roues et de la motorisation._

### Électronique
Alimentation, distribution de puissance, commande des moteurs et connectique.
_À compléter : tensions utilisées, protection, schéma de câblage._

### Firmware STM32
Asservissement en vitesse des moteurs à partir des encodeurs, exécution des consignes de déplacement reçues de la Raspberry Pi, renvoi de l'odométrie.
_À compléter : fréquence de la boucle de contrôle, gains du PID, format des messages._

### Localisation et SLAM
Le LiDAR YDLidar X4 fournit les scans 2D. L'odométrie des roues codeuses et l'IMU améliorent la précision de la localisation.
_À compléter : packages utilisés (ex. `slam_toolbox`, `robot_localization`), paramètres clés._

### Navigation et évitement d'obstacles
Planification du trajet et évitement d'obstacles à partir de la carte et des capteurs.
_À compléter : stack utilisée (ex. Nav2), planificateurs et paramètres retenus._

---

## ✅ État d'avancement

- [ ] Conception CAO du châssis
- [ ] Impression 3D et assemblage mécanique
- [ ] Schéma électronique et distribution de puissance
- [ ] Câblage et tests des drivers moteur
- [ ] Firmware STM32 : lecture des encodeurs
- [ ] Firmware STM32 : asservissement de vitesse
- [ ] Communication Raspberry Pi ↔ STM32
- [ ] Odométrie
- [ ] Intégration de l'IMU
- [ ] Driver LiDAR dans ROS 2
- [ ] Cartographie SLAM
- [ ] Localisation sur carte
- [ ] Navigation autonome A → B
- [ ] Évitement d'obstacles
- [ ] Démonstration finale

_Cocher les cases au fil de l'avancement du projet._

---

## 📊 Résultats
