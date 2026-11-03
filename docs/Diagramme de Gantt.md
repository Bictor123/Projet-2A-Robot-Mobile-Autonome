```mermaid
gantt
    title Planning du Projet Robot Mobile Autonome
    dateFormat  YYYY-MM-DD
    axisFormat  %W / %M

    section 🛠️ Mécanique & Châssis
    CAO de la base motrice et supports       :a1, 2026-11-03, 14d
    Impression 3D & Assemblage du châssis    :a2, after a1, 10d
    Intégration mécanique finale             :a3, after a2, 7d

    section ⚡ Électronique & PCB
    Schéma électrique & Bilan de puissance    :b1, 2026-11-03, 10d
    Routage du PCB (KiCad)                  :b2, after b1, 12d
    Soudure, validation & tests sous tension  :b3, after b2, 7d

    section 🔴 Firmware (STM32 & MD25)
    Liaison I2C STM32 / MD25 & Contrôle moteur:crit, active, c1, 2026-10-06, 2026-10-20
    Calibration & Machine à états (virages)  :crit, active, c2, 2026-10-20, 14d
    Lecture des encodeurs & Odométrie        :c3, after c2, 10d
    Communication Série / micro-ROS          :c4, after c3, 7d

    section 🟢 Software (Raspberry Pi 5 / ROS 2)
    Installation Ubuntu & ROS 2              :d1, 2026-11-03, 7d
    Drivers ROS 2 YDLidar X4 & Caméra        :d2, after d1, 10d
    Configuration SLAM Toolbox               :d3, after d2, 12d
    Navigation Nav2 & Évitement d'obstacles  :d4, after d3, 14d

    section 🟣 Intégration & Validation
    Tests de trajectoire & Calibration ROS 2 :e1, after c4, 10d
    Démonstration finale Point A -> Point B   :e2, after e1, 5d