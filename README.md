# Projet-2A-Robot-Mobile-Autonome
Autonomous mobile robot base for indoor navigation. Features custom 3D-printed mechanics, electronics, ROS 2 SLAM with LiDAR, and Raspberry Pi 5 / STM32 control.

# Autonomous Mobile Robot 🤖

This repository contains the hardware design and software stack for an autonomous mobile robot capable of indoor navigation, localization, and obstacle avoidance. The robot is designed to move precisely from point A to B, making it suitable for applications in warehouses and production lines.

## 🛠️ Technical Stack & Features
This project covers the full robotics pipeline, from mechanical and electronic design to autonomous perception and navigation.

* **Computing & Control:** Raspberry Pi 5 (High-level navigation) + STM32/Arduino (Low-level motor control)
* **Sensors:** YDLidar X4, IMU, Encoders, Camera
* **Software:** ROS 2, SLAM (Simultaneous Localization and Mapping), Autonomous Path Planning
* **Hardware:** Custom 3D-designed mechanical structure, custom power distribution, and motor drivers

# Projet Robot Mobile Autonome 🤖

Base roulante autonome pour la navigation en intérieur. Intègre une conception mécanique 3D, ROS 2 SLAM avec LiDAR, et un contrôle via Raspberry Pi 5 / STM32.

## 👥 L'équipe
* **[Ton Prénom/Nom]** - Rôle (ex: Développeur ROS 2 / SLAM)
* **[Prénom Associé 1]** - Rôle (ex: Électronique & STM32)
* **[Prénom Associé 2]** - Rôle (ex: Conception Mécanique 3D)

## 🛠️ Architecture du système
* **Haut niveau :** Raspberry Pi 5 sous Ubuntu + ROS 2 (Traitement LiDAR YDLidar X4, Caméra, SLAM, Planification).
* **Bas niveau :** STM32 / Arduino (Lecture IMU, Roues codeuses, asservissement des moteurs via drivers).
* **Châssis :** Modélisé en 3D et imprimé sur mesure.

## 🚀 Installation (Exemple pour la partie ROS 2)

```bash
# 1. Cloner le dépôt
git clone [https://github.com/VOTRE_NOM/VOTRE_PROJET.git](https://github.com/VOTRE_NOM/VOTRE_PROJET.git)

# 2. Se rendre dans le workspace ROS 2
cd VOTRE_PROJET/software

# 3. Compiler les paquets
colcon build
source install/setup.bash
