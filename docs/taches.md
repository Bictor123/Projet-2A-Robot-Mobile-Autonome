## Pôle Matériel (Hardware)
###Ingénieur Mécanique (1 personne) : Modélisation CAO 3D du châssis, conception des supports pour les capteurs (LiDAR, caméra), impression 3D et assemblage physique.

###Ingénieur Électronique (1 personne) : Conception du PCB sur mesure, routage, gestion rigoureuse de l'alimentation (batterie, convertisseurs pour sécuriser la Pi 5 et la STM32) et soudure.

## Pôle Bas Niveau (Firmware STM32)
###Développeur Contrôle Moteur (1 personne) : Programmation de la STM32 pour générer les signaux de commande des drivers moteurs, lecture des roues codeuses et réglage de l'asservissement PID.

###Développeur Capteurs (1 personne) : Intégration du code bas niveau pour lire l'IMU de manière fiable, calcul mathématique de l'odométrie brute, et structuration des messages à envoyer à la Raspberry Pi.

## Pôle Haut Niveau (Software ROS 2 sur Pi 5)
###Ingénieur SLAM & Perception (1 personne) : Intégration du LiDAR YDLidar X4 et de la caméra sous ROS 2, mise en place de l'algorithme pour cartographier l'environnement et localiser le robot.

###Ingénieur Navigation (1 personne) : Configuration de la stack de navigation (ex: Nav2), gestion de la planification de trajectoire globale (aller au point B) et de l'évitement dynamique des obstacles.

## Intégration (Rôle Transversal)
###Intégrateur Système : L'un de vous (souvent le développeur Navigation ou Capteurs) doit prendre cette double casquette. Cette personne configure l'OS de la Raspberry Pi 5 et s'assure que le pont de communication (via liaison série ou micro-ROS) entre la STM32 et ROS 2 fonctionne parfaitement.
