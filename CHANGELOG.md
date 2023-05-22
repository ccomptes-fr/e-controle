# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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


