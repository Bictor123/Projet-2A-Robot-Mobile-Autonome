# Châssis imprimé et assemblage

Le modèle `chassis.scad` fournit une plaque de base pour le prototype à trois
roues documenté dans les comptes rendus : deux roues motrices et un support
à bille. Il comporte des lumières de fixation pour les moteurs, un motif de
fixation pour le support à bille, les trous de montage d'une Raspberry Pi 5
et des passages pour des sangles de batterie.

## Préparation et impression

1. Ouvrir `chassis.scad` dans OpenSCAD et ajuster les paramètres en tête de
   fichier aux composants réellement utilisés.
2. Mesurer l'entraxe et le diamètre des fixations des moteurs et du support à
   bille. Les valeurs par défaut des trous moteurs et du support à bille sont
   des dégagements de départ, pas des mesures des pièces du prototype.
3. Vérifier que les composants, les roues et les câbles ne se gênent pas et que
   les perçages restent dans le contour de la plaque.
4. Faire le rendu (F6), exporter en STL, puis imprimer la plaque à plat. Une
   épaisseur de couche et un remplissage adaptés à l'imprimante et aux efforts
   attendus sont à choisir avec le slicer.
5. Imprimer d'abord un petit gabarit de perçage si les entraxes n'ont pas été
   confirmés. Ébavurer les lumières et vérifier les ajustements avant le montage.

## Ordre d'assemblage

1. Fixer les deux moteurs sous la plaque au moyen des lumières latérales, en
   laissant les roues libres de tourner sans toucher le châssis.
2. Fixer le support à bille sous l'extrémité avant, puis contrôler que les deux
   roues motrices et la bille portent simultanément sur le sol.
3. Fixer la Raspberry Pi 5 sur ses quatre trous. Ajouter des entretoises pour
   éviter tout contact électrique avec la plaque ou les têtes de vis.
4. Immobiliser la batterie avec des sangles passant dans les lumières prévues.
   La placer bas et près du centre du châssis; ne pas la percer ni la comprimer.
5. Installer le LiDAR sur son support dédié (non fourni par ce modèle) et vérifier
   qu'il est horizontal, dégagé et solidement retenu.
6. Faire un contrôle final des fixations, du débattement des roues, du passage des
   câbles et de la stabilité avant toute mise sous tension.

Les positions du moteur, du support à bille et de la batterie doivent être
validées avec le prototype physique avant de produire la pièce finale. Le
modèle ne remplace pas le support de LiDAR existant ni les essais mécaniques.
