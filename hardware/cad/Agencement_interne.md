# Agencement interne du robot

## Objectif et statut

Cette proposition organise la Raspberry Pi 5, la carte de commande STM32 et les batteries dans le châssis. C'est une implantation de référence à valider sur le prototype : les dimensions du châssis, de la batterie et des cartes définitives ne sont pas encore documentées. Il ne faut donc pas imprimer de supports définitifs avant d'avoir mesuré les composants réels.

La carte retenue pour le firmware présent dans le dépôt est une NUCLEO-F303K8. Si une autre carte STM32 ou une Arduino est finalement utilisée, conserver les zones et refaire les perçages à partir de son plan mécanique.

## Implantation proposée

Repère : vue de dessus, avant du robot en haut, axe longitudinal au centre.

```text
                         AVANT
             ┌───────────────────────────┐
             │        zone capteurs      │
             │     (câbles vers l'avant) │
             ├─────────────┬─────────────┤
             │ Raspberry   │ STM32 /     │
             │ Pi 5        │ Arduino     │
             │ ventilation │ + MD25      │
             ├─────────────┴─────────────┤
             │ batterie(s), centrée(s)   │
             │ et au plus bas possible   │
             └───────────────────────────┘
                          ARRIÈRE
```

- Placer les batteries dans un logement bas, centré entre les roues motrices et retenu par un couvercle ou une sangle mécanique. Cela abaisse le centre de gravité et empêche tout déplacement pendant les accélérations. Prévoir un accès permettant leur retrait et leur inspection.
- Installer la Pi 5 sur une entretoise isolante, au-dessus du compartiment batterie et à l'écart des drivers. Orienter ses connecteurs vers un bord accessible. Garder libres le dissipateur ou ventilateur retenu et leurs entrées/sorties d'air.
- Fixer la STM32/Arduino et le MD25 sur des supports séparés, près des moteurs et des passages de câbles moteurs. Garder les connecteurs et le bouton de programmation accessibles. Ne pas faire porter aux connecteurs des cartes les efforts mécaniques des câbles.
- Réserver une zone de distribution d'alimentation près d'un bord du châssis, accessible pour l'interrupteur général, le fusible et les connecteurs. Laisser un dégagement pour débrancher la batterie sans déposer les cartes.
- Garder libre le chemin vertical du support LiDAR et le passage des câbles capteurs vers l'avant.

## Fixations et câblage

- Prévoir des entretoises et des fixations démontables adaptées aux trous de montage des cartes réelles. Vérifier les dégagements sous les circuits imprimés afin qu'aucune vis ou entretoise ne touche leurs pistes ou composants.
- Maintenir la batterie dans un logement adapté à son format final ; ne pas la fixer uniquement avec de l'adhésif. Protéger ses fils contre l'abrasion et empêcher tout contact avec des arêtes ou des pièces mobiles.
- Acheminer les câbles moteurs et d'alimentation de puissance le long d'un côté du châssis, et les signaux de la Pi, de la STM32 et des capteurs de l'autre. Lorsqu'ils doivent se croiser, les faire se croiser brièvement et à angle droit. Fixer les faisceaux et garder du mou aux connecteurs démontables.
- Alimenter la Pi 5 via un convertisseur régulé adapté à sa tension et à son courant maximal ; alimenter séparément la logique et les moteurs selon les caractéristiques de leurs composants. Définir le retour de masse et les protections dans le schéma électrique, et non par le châssis.
- Dimensionner batterie, convertisseurs, câbles et protections à partir des tensions admissibles et des courants continus/de pointe mesurés ou spécifiés pour la Pi, les moteurs, le MD25 et les autres charges. L'estimation préliminaire de consommation du compte rendu ne suffit pas à valider le dimensionnement.
- Employer une batterie avec la protection et le chargeur adaptés à sa chimie. Protéger les bornes contre les courts-circuits et isoler la batterie des sources de chaleur. Ne pas charger la batterie dans le châssis sans une conception prévue à cet effet.

## Mesures à relever avant la CAO définitive

1. Dimensions intérieures du châssis, hauteur disponible sous le plateau et position des roues, moteurs et support LiDAR.
2. Dimensions, trous de fixation et dégagements de la Pi 5, de la carte de commande et du MD25 ; hauteur nécessaire à leur refroidissement.
3. Format, masse, tension et courant de pointe de la batterie finale, ainsi que l'encombrement de son support et de ses protections.
4. Position des connecteurs, longueur des câbles et accès aux commandes, ports et éléments à entretenir.

Après intégration, vérifier le maintien des composants, l'accès aux connecteurs, l'absence de pincement de câbles et le refroidissement de la Pi. Mesurer le centre de gravité et confirmer que le robot reste stable avant les essais de déplacement.
