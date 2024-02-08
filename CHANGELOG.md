# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.3.0] - 2024-02-08

### Added

- Les contrôles supprimés sont affichés en rouge

### Fixed

- Supprimer un espace de dépôt depuis la page admin
- Résoudre les problèmes de connexion aléatoires de la DB en utilisant la version 5.3.0 de Whitenoise

### Security

- Interdire l'accès à des internes depuis des postes non sécurisés

## [2.2.0] - 2024-01-23

### Added

- Une alerte est envoyée N jours avant la date d'échéance d'un questionnaire publié
- Il est désormais possible d'afficher une alerte globale aux utilisateurs sur la page d'accueil
- Lorsqu'un demandeur est supprimé d'un espace de dépôt, il reçoit une notification
- Il est désormais possible d'ajouter un fichier annexe au questionnaire
- Il n'est plus possible d'accéder à un Espace de dépôt et/ou un Questionnaire supprimer
- Un utilisateur peut être à la fois Demandeur et Répondant
- Ajout d'une page de non conformité au RGAA

### Changed

- Application des retours sur les règles RGAA : balises
- Application des retours sur les règles RGAA : tags alt des logos d'en-tête et de pied de page
- Adaptation des couleurs pour le respect du RGAA
- Utilisation de la langue française au lieu de la langue anglaise pour le respect du RGAA
- L'adresse de support est désormais paramétrable
- Les boutons d'export et de duplication ne sont visibles que si des questionnaires sont présents

### Fixed

- Date limite de réponse : modifier le format de date à la norme française
- Le bouton de repli du panneau latéral est correctement positionné
- Les questions trop longues sont coupées sur plusieurs lignes pour un meilleur affichage
- L'animation d'attente du téléchargement est disponible pour tous les téléchargements
- Dépôt de fichier: interdire le dépôt de fichier au nom trop long

### Security

- Remplacement de la librairie obsolète soft-delete par django-soft-delete
- Mettre à jour le serveur RabbitMQ

## [2.1.0] - 2023-05-22

### Added

- Envoi par mails de rapports mensuels pour lister les contrôles :
  - orphelins (destinataire : les admins)
  - "anciens" (destinataire : les contrôleurs)
- Quand on clique sur un espace de dépôt dans le menu de gauche, le focus est sur le haut de la page de l’espace de dépôt sélectionné
- Ajout du statut "Non terminé" (accepté ou non accepté par le contrôleur) au questionnaire
- Sur la liste des questionnaires d'un espace de dépôt, ajout de l'affichage de la colonne "statut" pour un contrôlé
- Fichier CHANGELOG.md
- Bloquer l'upload des fichiers avec l’extension « .msg ».

### Fixed

- Export zip d'un espace de dépôt ne contient plus les fichiers supprimés
- Gestion des statuts lors de la duplication d'un espace de dépôt
- Appels trop nombreux au LDAP sur la partie webdav (mise en place d'un cache de 30 min)

### Changed

- La suppression d'un espace dépôts supprimer physiquement le dossier sur le serveur
- Le point "." n'est plus un caractère accepté pour un nom abrégé dans un espace de dépôt
- Mise à jour de sécurité de Django et WsgiDAV
- Optimisations image Docker sur la partie js en embarquant que les lib nécessaires
- Renommage des conteneurs Docker
- Utilisation de black pour formatter le code Python


