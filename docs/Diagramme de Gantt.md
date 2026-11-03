gantt
    title Planning Global - Projet Robot Mobile Autonome
    dateFormat  YYYY-MM-DD
    axisFormat  %W / %M

    section 🛠️ 1. Conception Mécanique
    Modélisation CAO base roulante & moteurs    :a1, 2026-11-03, 10d
    Modélisation supports capteurs (Lidar/Cam)  :a2, after a1, 7d
    Conception agencement interne & fixations   :a3, after a2, 7d
    Impression 3D & assemblage mécanique       :a4, after a3, 10d

    section ⚡ 2. Électronique & PCB
    Bilan de puissance & schéma d'alimentation   :b1, 2026-11-03, 7d
    Schéma de câblage global (Schematic)         :b2, after b1, 7d
    Listage composants & Routage du PCB         :b3, after b2, 10d
    Validation PCB (par le professeur)           :crit, b4, after b3, 3d
    Soudure composants (CMS & Traversants)       :b5, after b4, 7d
    Tests électriques & validation PCB           :b6, after b5, 5d

    section 🔴 3. Firmware STM32
    Config matérielle (STM32CubeIDE / I2C MD25) :c1, 2026-11-03, 7d
    Asservissement PID & Odométrie               :c2, after c1, 12d
    Lecture de l'IMU                             :c3, after c2, 7d
    Communication Série / micro-ROS Pi 5 <=> STM32:c4, after c3, 7d

    section 🟢 4. Software ROS 2 & Navigation
    Installation OS Ubuntu & ROS 2 (Pi 5)        :d1, 2026-11-03, 5d
    Drivers YDLidar X4, Caméra & RViz            :d2, after d1, 10d
    Configuration Arbre de Transformation (TF)   :d3, after d2, 5d
    Cartographie SLAM & Stack Navigation (Nav2)  :d4, after d3, 14d

    section 📱 5. Application Mobile
    Développement UI & Chronomètre intégré      :e1, 2026-11-24, 10d
    Flux télémétrie (LiDAR, Caméra, IMU/Vitesse) :e2, after e1, 12d

    section 📦 6. Logistique & Essais
    Inventaire & commande des composants        :f1, 2026-11-03, 7d
    Calibrage du robot réel & Essais finaux     :crit, f2, after d4, 7d